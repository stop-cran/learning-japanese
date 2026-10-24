"""Private run locking and conservative, prepaid request accounting."""
from __future__ import annotations

from contextlib import contextmanager
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import tempfile

from validate_listening import canonical_hash


def read_json(path: Path) -> dict:
    if path.is_symlink():
        raise ValueError(f"Symlink is not a run record: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextmanager
def run_lock(root: Path):
    lock = root / "operation.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError("Run is locked. After a crash, verify its recorded PID has stopped before removing operation.lock.") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="ascii") as stream:
            stream.write(str(os.getpid()))
            stream.flush()
            os.fsync(stream.fileno())
        yield
    finally:
        lock.unlink()


def positive_decimal(value: str) -> Decimal:
    number = Decimal(value)
    if not number.is_finite() or number <= 0:
        raise ValueError("Price and monetary ceiling must be finite positive decimals")
    return number


def authorize(root: Path, plan_hash: str, scope: str, max_units: int,
              max_usd: str, usd_per_million: str, note: str) -> None:
    if scope not in ("preview", "complete") or type(max_units) is not int or max_units <= 0 or not note.strip():
        raise ValueError("Explicit scope, positive request-unit ceiling and authorization note are required")
    positive_decimal(max_usd)
    positive_decimal(usd_per_million)
    with run_lock(root):
        if any((root / name).exists() for name in ("authorization.json", "spend.json")):
            raise ValueError("Authorization/accounting already exists; do not reset a spent run")
        record = {"planSha256": plan_hash, "scope": scope, "maxRequestUnits": max_units,
                  "maxUsd": max_usd, "usdPerMillion": usd_per_million, "note": note}
        write_json(root / "authorization.json", record)
        write_json(root / "spend.json", {"authorizationSha256": canonical_hash(record), "attempts": []})


class BudgetSession:
    """Wrap every shared-engine POST, including retries and recursive split retries.

    The caller holds run_lock for the entire render. A crash after reservation
    still consumes that allowance; unsuccessful requests are not refunded.
    """

    def __init__(self, session, root: Path, endpoint: str, plan_hash: str, phase: str, verify_plan):
        self.session, self.root, self.endpoint = session, root, endpoint
        self.verify_plan = verify_plan
        self.authorization = read_json(root / "authorization.json")
        auth = self.authorization
        if auth["planSha256"] != plan_hash or phase not in ("preview", "complete"):
            raise ValueError("Authorization does not match the frozen plan/phase")
        if auth["scope"] not in ("preview", "complete") or (phase == "complete" and auth["scope"] != "complete"):
            raise ValueError("Only previews have been authorized")
        if type(auth["maxRequestUnits"]) is not int or auth["maxRequestUnits"] <= 0:
            raise ValueError("Invalid request-unit ceiling")
        self.price, self.ceiling = positive_decimal(auth["usdPerMillion"]), positive_decimal(auth["maxUsd"])
        self._ledger()

    def _ledger(self) -> dict:
        state = read_json(self.root / "spend.json")
        if state["authorizationSha256"] != canonical_hash(self.authorization):
            raise ValueError("Authorization changed; the previous spend ledger cannot be reset or reused")
        attempts = state["attempts"]
        if not isinstance(attempts, list) or any(
            not isinstance(item, dict) or type(item.get("units")) is not int or item["units"] <= 0
            or item.get("sequence") != index
            for index, item in enumerate(attempts, 1)
        ):
            raise ValueError("Invalid spend ledger; do not reset it")
        return state

    def post(self, url, **kwargs):
        self.verify_plan()
        if read_json(self.root / "authorization.json") != self.authorization:
            raise ValueError("Authorization changed during rendering")
        data = kwargs.get("data")
        if url != self.endpoint or not isinstance(data, (str, bytes)):
            raise ValueError("Only the planned TTS endpoint and an explicit SSML body are permitted")
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        # Count all markup too, even exempt tags; Japanese kanji can cost two units.
        units = 2 * len(text)
        if not units:
            raise ValueError("Empty synthesis request")
        state = self._ledger()
        total = sum(item["units"] for item in state["attempts"]) + units
        if total > self.authorization["maxRequestUnits"] or Decimal(total) * self.price > self.ceiling * 1_000_000:
            raise ValueError("Paid request blocked: explicit cumulative authorization ceiling would be exceeded")
        state["attempts"].append({"sequence": len(state["attempts"]) + 1, "units": units,
                                  "requestSha256": hashlib.sha256(text.encode("utf-8")).hexdigest()})
        write_json(self.root / "spend.json", state)
        kwargs["allow_redirects"] = False
        response = self.session.post(url, **kwargs)
        if 300 <= response.status_code < 400:
            raise ValueError("Synthesis redirect blocked; only the explicitly planned endpoint is permitted")
        return response
