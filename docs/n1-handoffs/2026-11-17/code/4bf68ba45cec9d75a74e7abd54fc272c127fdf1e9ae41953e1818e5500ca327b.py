"""Synthetic prospective CLI controls; never admits/messages an actual reviewer.

The actual immutable prior streams are read-only inputs. Future events, reports,
status/roster and acceptance files live exclusively below a synthetic test root.
Only Path.home and the output-root seam are substituted for the CLI pipeline.
"""
import copy
import datetime as dt
import json
import os
import subprocess
import sys
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import freeze_json, frozen, json_bytes, load_module, sha, start_guard, write_frozen

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
RUNTIME = REVIEW / "authorization-runtime-002" / "b134_authorized_confirmation_v1.py"
m = load_module("b134_authorized_test_subject", RUNTIME)
t = m.legacy


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard, _ = start_guard("B134 prospective authorization synthetic CLI controls")
        cls.area = HERE / ("synthetic-" + uuid.uuid4().hex)
        cls.area.mkdir()
        cls.home = cls.area / "synthetic-home"
        cls.synthetic_producer = cls.area / "SYNTHETIC_NOT_AN_ACTUAL_LIFECYCLE.py"
        write_frozen(cls.synthetic_producer, b"# Synthetic test provenance; never an authorized runtime.\n")
        cls.accepted_claude = None

    @classmethod
    def tearDownClass(cls):
        freeze_json(cls.area / "memory.json", cls.guard.finish())

    def test_01_actual_received_authorization_and_transport_rejections(self):
        row = m.authority()
        kickoff = "SYNTHETIC bounded prospective instructions"
        data = self.forward(kickoff)
        self.assertTrue(m.forwarded(data, kickoff))
        self.assertEqual(m.block(row["data"]["transformedContent"], "forwarded_user_message_source_json"), m.SOURCE)
        for mutation in ("source", "id", "revision", "quote", "content", "instructions", "missing", "duplicate"):
            bad = copy.deepcopy(data)
            if mutation == "source":
                bad["source"] = "agent-not-this-coordinator"
            elif mutation == "id":
                bad["transformedContent"] = bad["transformedContent"].replace(m.SOURCE["id"], str(uuid.uuid4()))
            elif mutation == "revision":
                bad["transformedContent"] = bad["transformedContent"].replace('"revision":3', '"revision":2')
            elif mutation == "quote":
                bad["transformedContent"] = bad["transformedContent"].replace(m.AUTH_TEXT, "Blanket authorization")
            elif mutation == "content":
                bad["content"] += "\nextra instruction"
            elif mutation == "instructions":
                bad["transformedContent"] = bad["transformedContent"].replace(kickoff, "different")
            elif mutation == "missing":
                bad.pop("transformedContent")
            else:
                bad["transformedContent"] += '<forwarded_user_message_json>"extra"</forwarded_user_message_json>'
            with self.subTest(mutation=mutation), self.assertRaises((ValueError, KeyError)):
                m.forwarded(bad, kickoff)

    def test_02_old_tail_and_held_evidence_are_bound_not_erased(self):
        for family in ("claude", "gpt"):
            prepared = REVIEW / f"authorized-{family}-confirmation-002" / "preflight.json"
            record, _, _, _ = t.preflight(prepared)
            _, raw, _ = m.retained(family)
            m.verify_retained_prefix(record, raw)
            for bad in (raw[1:], raw[:-2] + b" \n", raw + json_bytes({
                "type": "user.message", "data": {"content": "unadmitted"}})):
                with self.subTest(family=family), self.assertRaises(ValueError):
                    m.verify_retained_prefix(record, bad)
        with self.assertRaises((ValueError, KeyError)):
            m.previous_claude(t.value(m.HOLD)["retainedClaudeAcceptance"],
                              t.value(m.HOLD)["candidate"], t.REVISION_SCOPE)

    def test_03_exact_capacity_boundaries_and_original_profile(self):
        for family, cap in (("claude", 740000), ("gpt", 710000)):
            _, raw, _ = m.retained(family)
            events = t.parse_events(raw)
            model, max_tokens = ("claude-opus-5.5", 952000) if family == "claude" else ("gpt-6.1-sol", 922000)
            usage = {"type": "session.usage_record", "data": {"usage": {
                "model": model, "responseModel": model, "inputTokens": cap - 49000,
                "maxPromptTokens": max_tokens}}}
            result = t.context(events + [usage], family, t.OWN[family], 0)
            self.assertEqual((result["forecast"], result["limit"], result["originalStartupGateUnchanged"]),
                             (cap, cap, 700000))
            self.assertEqual(sum(result["reserves"].values()), 49000)
            with self.assertRaises(ValueError):
                t.context(events + [usage], family, t.OWN[family], 1)
            wrong = copy.deepcopy(usage)
            wrong["data"]["usage"]["responseModel"] = "unknown-model"
            with self.assertRaises(ValueError):
                t.context(events + [wrong], family, t.OWN[family], 0)
            with self.assertRaises(ValueError):
                t.context(events + [{"type": "session.compaction_complete", "data": {}}],
                          family, t.OWN[family], 0)
        with self.assertRaises(ValueError):
            t.context(events, "unknown", t.OWN["gpt"], 0)

    def test_04_cli_entry_smoke_and_all_action_fail_closed(self):
        for argv, expected in ((["--help"], 0), (["prepare", "--help"], 0),
                               (["admit", "--help"], 0), (["final", "--help"], 0), (["accept", "--help"], 0),
                               (["prepare", str(HERE / "absent-request.json"), str(self.area / "bad")], 1),
                               (["prepare", str(HERE / "request-claude.json"),
                                 str(HERE / "FORBIDDEN_NOT_A_DIRECT_REVIEW_OUTPUT")], 1),
                               (["admit", str(HERE / "absent-preflight.json"), "absent", "absent"], 1),
                               (["final", str(HERE / "absent-preflight.json"), "absent", "absent"], 1),
                               (["accept", str(HERE / "absent-final.json"), "absent", "absent"], 1)):
            process = subprocess.Popen([sys.executable, "-B", str(RUNTIME), *argv],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
            try:
                while True:
                    try:
                        out, err = process.communicate(timeout=.1)
                        break
                    except subprocess.TimeoutExpired:
                        self.guard.check()
            finally:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=10)
            self.assertEqual(process.returncode, expected, (argv, err.decode()))
            write_frozen(self.area / ("cli-" + uuid.uuid4().hex + ".log"), out + err)

    def test_05_claude_admit_final_accept_cli_pipeline_native_crlf_desktop(self):
        self.pipeline("claude", native=True)

    def test_06_gpt_complete_dossier_admit_final_accept_cli_pipeline(self):
        self.assertIsNotNone(type(self).accepted_claude)
        self.pipeline("gpt", native=False)

    def test_07_missing_authorization_old_identity_and_source_reduction_rejected(self):
        for mutation in ("missing-auth", "wrong-auth", "old-run", "claude-source", "gpt-source"):
            family = "gpt" if mutation == "gpt-source" else "claude"
            def spec_change(spec):
                if mutation == "missing-auth":
                    spec.pop("authorization")
                elif mutation == "wrong-auth":
                    spec["authorization"] = dict(m.AUTH, sha256="0" * 64)
                elif mutation == "old-run":
                    spec["run"] = "N1-B134-CLAUDE-REVISION-001"
            def source_change(sources):
                if mutation in ("claude-source", "gpt-source"):
                    sources.pop()
            prepared, _, _, _, _ = self.clone(family, spec_change, source_change)
            with self.subTest(mutation=mutation), self.assertRaises((ValueError, KeyError)):
                t.preflight(prepared / "preflight.json")

    def test_08_serial_fresh_complete_status_and_idle_mode_required(self):
        for mutation in ("busy", "mode", "stale", "roster"):
            rows = [{"id": sid, "activity": {"status": "idle"}, "mode": "interactive"}
                    for sid in (t.COORDINATOR, t.OWN["claude"], "synthetic-other-session")]
            if mutation == "busy":
                rows[-1]["activity"]["status"] = "busy"
            if mutation == "mode":
                rows[1]["mode"] = "autopilot"
            roster = [{"id": row["id"]} for row in rows]
            if mutation == "roster":
                roster.pop()
            folder = self.area / ("status-rejection-" + mutation)
            obs = {"observedAt": ("2000-01-01T00:00:00+00:00" if mutation == "stale"
                                  else dt.datetime.now(dt.timezone.utc).isoformat()),
                   "status": self.small(freeze_json(folder / "status.json", {"sessions": rows, "summary": {"total": 3}})),
                   "roster": self.small(freeze_json(folder / "roster.json", roster))}
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                t.roster_check(obs, t.OWN["claude"], dt.datetime.now(dt.timezone.utc))

    @staticmethod
    def forward(kickoff):
        data = copy.deepcopy(m.authority()["data"])
        old = m.block(data["transformedContent"], "coordinator_instructions_json")
        data["transformedContent"] = data["transformedContent"].replace(json.dumps(old), json.dumps(kickoff))
        data["content"] = "Forwarded user message:\n\n> " + m.AUTH_TEXT + "\n\nCoordinator instructions:\n\n" + kickoff
        data["agentMode"] = "interactive"
        return data

    def clone(self, family, spec_change=None, source_change=None):
        prepared = REVIEW / f"authorized-{family}-confirmation-002" / "preflight.json"
        old_record, old_config, old_spec, old_chain = t.preflight(prepared)
        target = self.area / ("synthetic-prepared-" + family + "-" + uuid.uuid4().hex)
        target.mkdir()
        spec = copy.deepcopy(old_spec)
        if spec_change:
            spec_change(spec)
        spec_ref = freeze_json(target / "request.json", spec)
        _, _, _, builder = t.modules()
        sources = [(name, raw, None) for name, raw in t.reconstruct(old_chain).items()]
        if source_change:
            source_change(sources)
        chain = builder.build_chain(sources, target / "segments", target / "chain.json", self.guard, spec["run"])
        report = target / "report" / "review.md"
        report.parent.mkdir()
        prompt = t.render_prompt(spec, chain, report, "NEEDS FIX")
        write_frozen(target / "prompt.txt", prompt.encode())
        write_frozen(target / "kickoff.txt", b"Read SYNTHETIC fixture prompt; not an actual admission.")
        config = copy.deepcopy(old_config)
        config.update(run=spec["run"], prompt=str(target / "prompt.txt"), kickoff=str(target / "kickoff.txt"),
                      report=str(report), chainManifest=str(target / "chain.json"))
        config["files"] += [t.ref(target / "prompt.txt"), t.ref(target / "kickoff.txt"), t.ref(target / "chain.json")]
        config_ref = freeze_json(target / "config.json", config)
        record = copy.deepcopy(old_record)
        record.update(run=spec["run"], spec=self.small(spec_ref), config=self.small(config_ref),
                      chain=t.ref(target / "chain.json"),
                      dossierBound=len(prompt.encode()) + sum(r["bytes"] for r in chain["segments"]))
        freeze_json(target / "preflight.json", record)
        freeze_json(target / "preparation-memory.json", {"breach": None, "syntheticFixtureOnly": True})
        return target, record, config, spec, chain

    @staticmethod
    def small(ref):
        return {key: ref[key] for key in ("path", "sha256")}

    def pipeline(self, family, native):
        prepared, record, config, spec, chain = self.clone(family)
        _, prefix, _ = m.retained(family)
        live = self.home / ".copilot" / "session-state" / record["session"] / "events.jsonl"
        live.parent.mkdir(parents=True)
        live.write_bytes(prefix)
        rows = [{"id": sid, "activity": {"status": "idle"}, "mode": "interactive"}
                for sid in (t.COORDINATOR, record["session"])]
        status = freeze_json(self.area / f"{family}-status.json",
                             {"sessions": rows, "summary": {"total": len(rows)}})
        roster = freeze_json(self.area / f"{family}-roster.json", [{"id": row["id"]} for row in rows])
        obs = {"observedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
               "status": self.small(status), "roster": self.small(roster)}
        if family == "gpt":
            obs["priorClaudeAcceptance"] = type(self).accepted_claude
        observation = self.area / f"{family}-observation.json"
        freeze_json(observation, obs)
        admitted, final_dir, accepted_dir = (self.area / (family + "-" + step)
                                            for step in ("admit", "final", "accept"))
        with patch.object(Path, "home", return_value=self.home), patch.object(t, "ROOT", self.area), patch.object(
                t, "__file__", str(self.synthetic_producer)):
            self.assertEqual(m.main(["admit", str(prepared / "preflight.json"),
                                     str(observation), str(admitted)]), 0)
        admission = json.loads(frozen(admitted / "admission.json"))
        dispositions = {row["id"]: ("DECLINE ACCEPTED" if family == "claude" else
                                    "RESOLVED" if row["id"] in ("F1", "F2") else "DISPUTE ACCEPTED")
                        for row in spec["obligations"]}
        text = self.report(record, chain, dispositions)
        source = chain["sources"][0]["source"]
        for citation in ("not-a-source.md:1", source + ":999999", source + ":1,3"):
            result = t.check_structure(text.replace(source + ":1", citation), record, chain, "CONFIRMED")
            self.assertEqual(result["status"], "FAIL", citation)
        report = Path(config["report"])
        stored = text.replace("\n", "\r\n") if native else text
        report.write_bytes(stored.encode())
        events = self.suffix(record, config, chain, text, stored, admission, native)
        raw = prefix + self.encode_events(events)
        for mutation in ("missing-auth", "wrong-auth", "extra-user", "early-auth", "late-auth", "wrong-mode", "bad-read", "bad-path", "bad-native",
                         "bad-external", "bad-completion", "bare-cr", "wrong-prefix"):
            changed = copy.deepcopy(events)
            bad = prefix
            if mutation == "missing-auth":
                changed[0]["data"].pop("transformedContent")
            elif mutation == "wrong-auth":
                changed[0]["data"]["transformedContent"] = changed[0]["data"]["transformedContent"].replace(
                    m.SOURCE["id"], str(uuid.uuid4()))
            elif mutation == "extra-user":
                changed.append(copy.deepcopy(changed[0]))
            elif mutation == "early-auth":
                changed[0]["timestamp"] = "2026-01-01T00:00:00Z"
            elif mutation == "late-auth":
                changed[0]["timestamp"] = "2099-01-01T00:00:00Z"
            elif mutation == "wrong-mode":
                changed[0]["data"]["agentMode"] = "autopilot"
            elif mutation == "bad-read":
                next(r for r in changed if r["type"] == "tool.execution_complete")["data"]["result"]["content"] += "TRUNCATED"
            elif mutation == "bad-path":
                next(r for r in changed if r["type"] == "tool.execution_start")["data"]["arguments"]["path"] += "-wrong"
            elif mutation == "bad-native" and native:
                next(r for r in changed if r["type"] == "tool.execution_complete" and r["data"].get("fileEdits"))["data"]["fileEdits"][0]["kind"] = "update"
            elif mutation == "bad-external":
                next(r for r in changed if r["type"] == "external_tool.requested")["data"]["sessionId"] = "wrong"
            elif mutation == "bad-completion":
                next(r for r in changed if r["type"] == "external_tool.requested")["data"]["arguments"]["message"] = "CONFIRMED but"
            elif mutation == "wrong-prefix":
                bad = prefix[1:]
            elif mutation == "bare-cr":
                report.chmod(0o644)
                report.write_bytes(stored.encode() + b"\r")
            else:
                continue
            with self.subTest(family=family, mutation=mutation), self.assertRaises((ValueError, KeyError)):
                t.audit_snapshot(bad + self.encode_events(changed), record, config, chain, admission)
            report.chmod(0o644)
            report.write_bytes(stored.encode())
        live.write_bytes(raw)
        with patch.object(Path, "home", return_value=self.home), patch.object(t, "ROOT", self.area), patch.object(
                t, "__file__", str(self.synthetic_producer)):
            self.assertEqual(m.main(["final", str(prepared / "preflight.json"),
                                     str(admitted / "admission.json"), str(final_dir)]), 0)
        final_ref = t.ref(final_dir / "final.json")
        decision = {
            "final": final_ref, "report": t.ref(report), "candidate": record["candidate"],
            "run": record["run"], "session": record["session"], "family": family,
            "scope": record["scope"], "verdict": "CONFIRMED", "reportReadCompletely": True,
            "claimChecks": [{"claim": row["id"], "evidence": "SYNTHETIC fixture only",
                             "disposition": dispositions[row["id"]]} for row in spec["obligations"]],
            "limitsPreserved": ["SYNTHETIC only; all original/held evidence preserved."],
            "acceptedNewFindings": [], "openClaimIds": [], "dispositions": dispositions,
            "authorization": m.AUTH, "heldEvidenceTreatment": "retained-not-retroactively-authorized",
        }
        missing = dict(decision)
        missing.pop("authorization")
        missing_path = self.area / (family + "-bad-decision.json")
        freeze_json(missing_path, missing)
        with patch.object(t, "ROOT", self.area), patch.object(
                t, "__file__", str(self.synthetic_producer)), self.assertRaises(ValueError):
            m.main(["accept", str(final_dir / "final.json"), str(missing_path), str(accepted_dir)])
        decision_path = self.area / (family + "-decision.json")
        freeze_json(decision_path, decision)
        with patch.object(t, "ROOT", self.area), patch.object(t, "__file__", str(self.synthetic_producer)):
            self.assertEqual(m.main(["accept", str(final_dir / "final.json"), str(decision_path), str(accepted_dir)]), 0)
        accepted = json.loads(frozen(accepted_dir / "acceptance.json"))
        self.assertTrue(accepted["authorizationProspective"])
        self.assertEqual(accepted["mode"], "revision")
        self.assertEqual(accepted["priorRawVerdict"], "NEEDS FIX")
        self.assertEqual(accepted["authorization"], m.AUTH)
        self.assertEqual(accepted["deliveryCredit"], 0)
        self.assertNotEqual(accepted["producer"]["sha256"], sha(frozen(RUNTIME)))
        if family == "claude":
            type(self).accepted_claude = t.ref(accepted_dir / "acceptance.json")
            audit = json.loads(frozen(final_dir / "audit.json"))
            self.assertEqual(audit["transportBinding"]["originalAuditorBinding"], "line-endings-normalized")

    @staticmethod
    def encode_events(events):
        return b"".join(json.dumps(row, ensure_ascii=False).encode("utf-8") + b"\n" for row in events)

    @staticmethod
    def report(record, chain, dispositions):
        source = chain["sources"][0]["source"]
        rows = "\n".join(f"- {key} - {value} - SYNTHETIC retained-evidence fixture"
                         for key, value in dispositions.items())
        return f"""# B134 confirmation - {record['run']}
## Snapshot
Commit: {record['candidate']}
Model: {'claude-opus-5.5' if record['family'] == 'claude' else 'gpt-6.1-sol'} long_context
## Scope
Chain: All {len(chain['segments'])} complete segments
Fetches: 0
## Dispositions
{rows}
## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN
## Confirmation
Verdict: CONFIRMED
Basis: SYNTHETIC prospective fixture ({source}:1).
## Findings
None.
## Optional
None.
## Limits
- L1: {record['scope']}
- L2: SYNTHETIC ONLY. Original NEEDS FIX and held evidence are not upgraded retroactively.
"""

    @staticmethod
    def suffix(record, config, chain, text, stored, admission, native):
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        events = [{"type": "user.message", "timestamp": now, "data": Controls.forward(admission["kickoff"])}]
        calls = [("view", {"path": config["prompt"], "forceReadLargeFiles": True}, frozen(config["prompt"]).decode())]
        calls += [("view", {"path": row["path"], "forceReadLargeFiles": True}, t.read(row).decode())
                  for row in chain["segments"]]
        patch_text = "*** Begin Patch\n*** Add File: " + config["report"] + "\n" + "".join(
            "+" + line + "\n" for line in text.splitlines()) + "*** End Patch\n"
        calls += [(("create" if native else "apply_patch"),
                   ({"path": config["report"], "file_text": text} if native else patch_text), ""),
                  ("view", {"path": config["report"], "forceReadLargeFiles": True}, stored),
                  ("send_session_message", {"session_id": t.COORDINATOR, "message": "CONFIRMED"}, "delivered")]
        family = record["family"]
        model, maximum = ("claude-opus-5.5", 952000) if family == "claude" else ("gpt-6.1-sol", 922000)
        for index, (name, args, returned) in enumerate(calls):
            call_id = "synthetic-" + str(index)
            events += [
                {"type": "assistant.turn_start", "data": {"agentMode": "interactive"}},
                {"type": "session.usage_record", "data": {"usage": {"model": model, "responseModel": model,
                    "inputTokens": 600000 if family == "claude" else 400000, "maxPromptTokens": maximum}}},
                {"type": "assistant.message", "data": {"model": model, "apiCallId": "api-" + call_id,
                    "toolRequests": [{"name": "functions." + name, "arguments": args, "toolCallId": call_id}]}},
                {"type": "tool.execution_start", "data": {"toolCallId": call_id, "toolName": name, "arguments": args}},
            ]
            if name == "send_session_message":
                request_id = str(uuid.uuid4())
                events += [
                    {"type": "external_tool.requested", "data": {"requestId": request_id, "sessionId": record["session"],
                        "toolCallId": call_id, "toolName": name, "arguments": args, "workingDirectory": str(t.WS.parent)}},
                    {"type": "external_tool.completed", "data": {"requestId": request_id}},
                ]
            completion = {"toolCallId": call_id, "success": True, "result": {"content": returned}}
            if name == "create":
                completion["fileEdits"] = [{"path": config["report"], "kind": "create"}]
            events += [{"type": "tool.execution_complete", "data": completion},
                       {"type": "assistant.turn_end", "data": {}}]
        return events


if __name__ == "__main__":
    unittest.main(verbosity=2)
