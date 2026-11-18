"""Report-transport repair of the active authorized B134 runtime (runtime-003, SHA-pinned).

The actual GPT confirmation wrote its report with exactly one host apply_patch Add File
whose patch text is LF-only; the Windows host stored that exact content with CRLF line
endings. The pinned V4 audit accepts the inherited auditor's CRLF-normalization note only
after exactly one native create, so it rejected the actual GPT final
(authorized-gpt-final-001, preserved). This successor re-derives the selected runtime-002
audit byte-for-byte (its compiled code must equal the pinned runtime's) and widens only
that one predicate: the note is also accepted when, with no native create, the reviewer
made exactly one successful apply_patch that adds only the configured report, every
added line is a "+" line, the requested content has no CR, and the stored bytes are
neither the LF content nor anything except its exact LF-to-CRLF expansion. Every
reviewer tool call must be a read, that one patch, or the reply. The auditor's binding
and note are retained, never relabelled; every other authorization, transport,
retained-prefix, delivered-turn, read/write/readback, capacity and decision gate is
unchanged.
"""
import inspect
import sys
from pathlib import Path

from common import frozen, load_module, require, sha

HERE = Path(__file__).resolve().parent
ACTIVE = HERE.parent / "authorization-runtime-003" / "b134_authorized_confirmation_v2.py"
ACTIVE_SHA = "b76bd7c306a7911c7bce6c31f159dfa396ee17eff8584c7eec847e48f82568fc"
frozen(ACTIVE, ACTIVE_SHA)
active = load_module("b134_authorized_active_runtime003", ACTIVE)
selected = active.selected
legacy = active.legacy
legacy.PINS["authorizedActualEventV2"] = (ACTIVE, ACTIVE_SHA)

READ_TOOLS = frozenset({"view", "grep", "glob"})
RULE = "single-apply-patch-add-file-lf-to-crlf-v1"


def single_add_file_crlf(suffix, report, native):
    """Return the transport binding only for the exact narrow case; otherwise None."""
    calls = [call for row in suffix if row["type"] == "assistant.message"
             for call in (row.get("data") or {}).get("toolRequests", [])]
    names = [str(call.get("name", "")).removeprefix("functions.") for call in calls]
    if native or names.count("apply_patch") != 1 or names.count("send_session_message") > 1:
        return None
    if not set(names) <= READ_TOOLS | {"apply_patch", "send_session_message"}:
        return None
    call = calls[names.index("apply_patch")]
    patch, identity = call.get("arguments"), call.get("toolCallId")
    if not isinstance(patch, str) or not isinstance(identity, str) or not identity:
        return None
    lines = patch.split("\n")
    if (len(lines) < 5 or lines[0] != "*** Begin Patch" or lines[1] != "*** Add File: " + str(report)
            or lines[-2:] != ["*** End Patch", ""]):
        return None
    body = lines[2:-2]
    if not all(line.startswith("+") for line in body):
        return None
    requested = "".join(line[1:] + "\n" for line in body).encode("utf-8")
    completed = [row["data"] for row in suffix if row["type"] == "tool.execution_complete"
                 and (row.get("data") or {}).get("toolCallId") == identity]
    if b"\r" in requested or len(completed) != 1 or completed[0].get("success") is not True:
        return None
    stored = Path(report).read_bytes()
    if stored == requested or stored != requested.replace(b"\n", b"\r\n"):
        return None
    return {"rule": RULE, "requestedSha256": sha(requested), "hostEditKind": "apply_patch-add-file",
            "toolCallId": identity}


# Re-derive the selected runtime-002 audit exactly as it did, and prove equality.
source = inspect.getsource(selected.parent.parent.audit_snapshot)
anchor = "    prefix_raw = legacy.read(admission[\"prefix\"])\n"
require(source.count(anchor) == 1, "Pinned V4 prefix predicate changed")
source = source.replace(anchor, '    verify_retained_prefix(record, legacy.read(admission["prefix"]))\n' + anchor, 1)
before = ('len(users) == 1 and users[0]["data"].get("source") == "agent-" + legacy.COORDINATOR\n'
          '            and users[0]["data"].get("content") == admission["kickoff"]')
require(source.count(before) == 1, "Pinned V4 kickoff predicate changed")
source = source.replace(before, 'len(users) == 1 and authorization_message(users[0], admission["kickoff"])', 1)
probe = {}
exec(compile(source, str(__file__), "exec"), dict(selected.__dict__), probe)
require(probe["audit_snapshot"].__code__ == active.selected_audit.__code__,
        "Re-derived audit differs from the pinned selected runtime-002 audit")

# The one widened predicate and its recorded transport binding.
edits = (
    ("    binding_ok = (\n",
     '    add_file = single_add_file_crlf(suffix, config["report"], native)\n    binding_ok = (\n'),
    ('"line-endings-normalized" and len(native) == 1\n',
     '"line-endings-normalized" and (len(native) == 1 or add_file is not None)\n'),
    ("    report.chmod(0o444)\n",
     '    if add_file is not None and audit["reportBinding"] == "line-endings-normalized":\n'
     '        audit["transportBinding"].update(add_file)\n    report.chmod(0o444)\n'),
    ("def audit_snapshot(", "def add_file_audit_snapshot("),
)
for old, new in edits:
    require(source.count(old) == 1, "Pinned V4 transport anchor changed: " + old.strip())
    source = source.replace(old, new, 1)
selected.single_add_file_crlf = single_add_file_crlf
exec(compile(source, str(__file__), "exec"), selected.__dict__)
widened_audit = selected.add_file_audit_snapshot
active.selected_audit = widened_audit
require(legacy.audit_snapshot is active.audit_snapshot, "Active runtime-003 audit entry changed")
legacy.__file__ = __file__


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    require(argv and argv[0] in ("final", "accept"),
            "This repair only audits/accepts an existing frozen authorized admission")
    return legacy.main(argv)


if __name__ == "__main__":
    sys.exit(main())
