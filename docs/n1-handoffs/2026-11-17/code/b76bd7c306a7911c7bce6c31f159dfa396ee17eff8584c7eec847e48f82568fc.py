"""Actual-event repair of the selected authorized B134 runtime (runtime-002, SHA-pinned).

Actual App-forwarded user.message events carry no agentMode field; the reviewer's actual
mode is recorded on the assistant.turn_start that opens the delivered turn. The selected
runtime required the field only because its synthetic fixtures invented it, so it rejected
the first actual delivery (authorized-claude-final-001, preserved). This successor changes
only that predicate: a present non-interactive value is still rejected, and the delivered
message's own turn (same turnId and interactionId) must actually start in interactive mode.
Every other V5/V1 transport, authorization, retained-prefix, audit, capacity and decision
gate is unchanged; the pinned event_envelope still requires every turn_start to be interactive.
"""
import sys
from pathlib import Path

from common import frozen, load_module, require

SELECTED = Path(__file__).resolve().parent.parent / "authorization-runtime-002" / "b134_authorized_confirmation_v1.py"
SELECTED_SHA = "65956a69b4f0c0cf4849228f8a554cd9c6d13afefdcf4a1427682cfea24964a1"
frozen(SELECTED, SELECTED_SHA)
selected = load_module("b134_authorized_selected_runtime002", SELECTED)
legacy = selected.legacy
legacy.PINS["authorizedSelectedV1"] = (SELECTED, SELECTED_SHA)
selected_audit = selected.audit_snapshot
selected_forwarded = selected.forwarded


def authorization_message(row, kickoff):
    authority = selected.authority()
    require(row["data"].get("agentMode", "interactive") == "interactive",
            "Authorization delivered in wrong actual mode")
    require(selected.dt.datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
            > selected.dt.datetime.fromisoformat(authority["timestamp"].replace("Z", "+00:00")),
            "Authorization cannot be applied retroactively")
    return selected_forwarded(row["data"], kickoff)


def delivered_turn_mode(suffix):
    users = [index for index, row in enumerate(suffix) if row["type"] == "user.message"]
    require(len(users) == 1, "Exactly one delivered authorization turn is required")
    data = suffix[users[0]]["data"]
    turn, interaction = data.get("turnId"), data.get("interactionId")
    require(isinstance(turn, str) and turn and isinstance(interaction, str) and interaction,
            "Delivered authorization turn identity is missing")
    opened = [row for row in suffix[users[0] + 1:] if row["type"] == "assistant.turn_start"]
    require(opened and opened[0]["data"].get("turnId") == turn
            and opened[0]["data"].get("interactionId") == interaction
            and opened[0]["data"].get("agentMode") == "interactive",
            "The delivered authorization turn did not actually start in interactive mode")
    return True


def audit_snapshot(raw, record, config, chain, admission):
    result = selected_audit(raw, record, config, chain, admission)
    delivered_turn_mode(legacy.parse_events(raw[admission["offset"]:]))
    return result


selected.authorization_message = authorization_message
legacy.authorization_message = authorization_message
selected.audit_snapshot = audit_snapshot
legacy.audit_snapshot = audit_snapshot
legacy.__file__ = __file__


def main(argv=None):
    return legacy.main(argv)


if __name__ == "__main__":
    sys.exit(main())
