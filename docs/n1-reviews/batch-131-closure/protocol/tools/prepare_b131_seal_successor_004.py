"""Use ordinary direct guarded Python commands; do not change/bypass the host's script execution policy."""
from b131_review_v3_common import TOOLS, freeze_json, frozen, require, sha, start_guard, write_frozen


def main():
    guard, _ = start_guard("B131003 direct-command handoff successor")
    try:
        source = TOOLS / "seal_b131_preparation_003.py"
        raw = frozen(source)
        text = raw.decode("utf-8")
        start = text.index('        wrapper = HERE / "Invoke-B131Review003.ps1"')
        end = text.index('        command_binding = ', start)
        replacement = '''
        environment = "$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'; "
        common = (environment + "$receipt='" + str(RECORDS / "preparation-v3-command-")
                  + "'+[guid]::NewGuid().ToString('N'); python -B '"
                  + str(RECORDS / "guarded-test-v3.py") + "' $receipt python -B '"
                  + str(TOOLS / "run_b127_tool.py") + "' ")
        commands = {"verify": common + "'" + str(TOOLS / "verify_b131_preparation_003.py") + "'"}
        for action, argument in (("admit", "admissionRequest"), ("launch", "sessionId"),
                                 ("phase1", "sessionId"), ("final", "sessionId"),
                                 ("accept", "adjudication")):
            commands[action] = (common + "'" + str(TOOLS / "step_b131_neutral_005.py")
                                + "' 131 claude " + action + " $" + argument + " '"
                                + str(DEFAULT_PREFLIGHT) + "'")
'''
        text = text[:start] + replacement + text[end:]
        text = text.replace("guarded-commands-003.json", "guarded-commands-004.json")
        text = text.replace("preparation-handoff-003.json", "preparation-handoff-004.json")
        text = text.replace("Replace -Family claude with -Family gpt", "Replace 131 claude with 131 gpt")
        anchor = '"verify_b131_preparation_003.py", "seal_b131_preparation_003.py"'
        require(text.count(anchor) == 1, "Tool-list anchor differs")
        text = text.replace(anchor, anchor +
                            ', "prepare_b131_seal_successor_004.py", "seal_b131_preparation_004.py"')
        anchor = '"guard": "Wrapper sets UTF8/no-bytecode and invokes pinned guarded-test-v3.py with a fresh UUID receipt. "'
        require(text.count(anchor) == 1, "Command metadata anchor differs")
        text = text.replace(anchor,
            '"guard": "Direct commands set UTF8/no-bytecode and invoke pinned guarded-test-v3.py with a fresh UUID receipt. "')
        anchor = '            "preparation-v3-inventory-001"):'
        require(text.count(anchor) == 1, "Receipt-list anchor differs")
        text = text.replace(anchor,
            '            "preparation-v3-inventory-001", "preparation-v3-wrapper-001",\n'
            '            "preparation-v3-seal-successor-001"):')
        anchor = '            "limits": qualification["limits"], "notPerformed": qualification["notPerformed"]}'
        require(text.count(anchor) == 1, "Limitation anchor differs")
        text = text.replace(anchor,
            '            "commandDeliveryLimitation": "The optional frozen .ps1 wrapper was refused by the host\'s "\n'
            '                "script execution policy and is INACTIVE. No policy was changed or bypassed. "\n'
            '                "Use the ordinary direct guarded Python commands in guarded-commands-004.json; "\n'
            '                "these are the same supported invocation path used throughout preparation.",\n'
            + anchor)
        compile(text, "seal_b131_preparation_004.py", "exec")
        output = write_frozen(TOOLS / "seal_b131_preparation_004.py", text.encode("utf-8"))
        print(freeze_json(TOOLS / "b131-seal-successor-004.json", {
            "source": str(source), "sourceSha256": sha(raw), "output": output,
            "scope": "Command delivery only. Inactive .ps1 wrapper/failure preserved. No execution-policy "
                     "change/bypass, runtime/preflight/prompt/evidence/gate change or reviewer action."}))
    finally:
        require(not guard.finish()["breach"], "Seal successor RAM breach")


if __name__ == "__main__":
    main()
