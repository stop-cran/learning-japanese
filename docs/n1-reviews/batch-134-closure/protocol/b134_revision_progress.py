"""Extend the closure ledger with separate authorized descendant confirmations."""
import json
from pathlib import Path

from common import frozen, load_module, require

HERE = Path(__file__).parent
SOURCE = HERE / "b134_closure_progress.py"
SOURCE_SHA = "1cfd64ab8ab56c4752bac5b8d9747951483e75f2167dcd247c18ce68ce591428"
HISTORY = HERE / "b134_revision_history.py"
HISTORY_SHA = "3fb4c7f222d055794303223a0abb1d43afea6af84ab5b6d95bb836aa7e728eac"
frozen(SOURCE, SOURCE_SHA)
frozen(HISTORY, HISTORY_SHA)
prior = load_module("b134_revision_progress_pinned_base", SOURCE)
history = load_module("b134_revision_progress_pinned_history", HISTORY)
prior.validate_history = history.validate_history
prior.validate_resolution = history.validate_resolution
validate_archived_resolution = prior.validate_archived_resolution


def validate_progress(ledger, reviewed, manifest, closure_raw):
    accounting = prior.validate_progress(ledger, reviewed, manifest, closure_raw)
    closure = json.loads(closure_raw)
    require(ledger["priorReviewedSnapshot"] == closure["priorReviewedSnapshot"] == history.PRIOR
            and ledger["review"]["confirmationRuns"] == closure["confirmationRuns"]
            and ledger["review"]["authorizedDescendantConfirmations"] is True,
            "Ledger lost its separately attributed authorized descendant confirmations")
    return accounting


def closed_progress(original, closure_raw, manifest, resolution, original_claims):
    ledger = prior.closed_progress(original, closure_raw, manifest, resolution, original_claims)
    closure = json.loads(closure_raw)
    ledger["priorReviewedSnapshot"] = closure["priorReviewedSnapshot"]
    ledger["review"]["confirmationRuns"] = list(closure["confirmationRuns"])
    ledger["review"]["authorizedDescendantConfirmations"] = True
    validate_progress(ledger, closure["reviewedSnapshot"], manifest, closure_raw)
    return ledger
