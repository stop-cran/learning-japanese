"""Synthetic future M/host transport controls; actual old evidence is read-only.

Only the absent merged snapshot/gates and synthetic host/home/output are mocked.
The real CLI handlers, complete source builder, audit, capacity, structure and
substantive acceptance execute. Synthetic producers/candidate cannot be actual
M evidence. No reviewer is contacted and no repository/index writes occur.
"""
import copy
import contextlib
import datetime as dt
import json
import sys
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import freeze_json, frozen, json_bytes, load_module, sha, start_guard, write_frozen

HERE = Path(__file__).resolve().parent
RUNTIME = Path(sys.argv.pop(1))
m = load_module("b134_integration_followup_subject", RUNTIME)
t = m.t
old = load_module("b134_integration_prior_synthetic_transport",
                  HERE.parent / "authorization-continuation-prep-001" / "test-authorized.py")
M = "f" * 40
NEW = "11111111-2222-4333-8444-555555555555"


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard, _ = start_guard("B134 replacement integration synthetic controls")
        cls.area = HERE.parent / ("integration-followup-fixtures-" + uuid.uuid4().hex)
        cls.area.mkdir()
        cls.home = cls.area / "synthetic-home"
        cls.producer = cls.area / "SYNTHETIC_NOT_AN_ACTUAL_LIFECYCLE.py"
        write_frozen(cls.producer, b"# Synthetic future M and host events; NOT ACTUAL REVIEW EVIDENCE.\n")
        freeze_json(cls.area / "NOT_ACTUAL_EVIDENCE.json", {"synthetic": True, "candidate": M})
        cls.accepted_claude = None
        cls.prepared_gpt = None
        cls.actual_roots = {}
        for family in ("claude", "gpt"):
            refs, final, accepted, root = m.prior_evidence({"family": family})
            cls.actual_roots[family] = (refs, final, accepted, root)
        cls.bootstrap_raw = cls.bootstrap()

    class FixtureGuard:
        def check(self):
            return None

        def finish(self):
            return {"breach": None, "syntheticInnerGuard": "outer pinned runner guards complete test process"}

    class FixtureResource:
        @staticmethod
        def available_ram():
            return 6 * 1024**3

    @contextlib.contextmanager
    def inner_guard(self):
        value = (self.FixtureGuard(), self.FixtureResource())
        with patch.object(m, "start_guard", return_value=value), patch.object(t, "start_guard", return_value=value):
            yield

    @classmethod
    def tearDownClass(cls):
        freeze_json(cls.area / "memory.json", cls.guard.finish())

    @staticmethod
    def bootstrap():
        _, _, _, root = m.prior_evidence({"family": "claude"})
        system = [row for row in t.parse_events(t.read(root))
                  if row["type"] == "system.message"]
        return old.Controls.encode_events([
            {"type": "session.start", "data": {"sessionId": NEW, "selectedModel": "claude-opus-5.5",
                "contextTier": "long_context", "context": {"cwd": str(t.WS.parent)}}},
            *system,
            {"type": "user.message", "data": {"content": m.BOOTSTRAP, "source": "agent-" + t.COORDINATOR}},
            {"type": "assistant.turn_start", "data": {"agentMode": "interactive"}},
            {"type": "session.usage_record", "data": {"usage": {"model": "claude-opus-5.5",
                "responseModel": "claude-opus-5.5", "inputTokens": 10000, "maxPromptTokens": 952000}}},
            {"type": "assistant.message", "data": {"content": "READY"}},
            {"type": "assistant.turn_end", "data": {}},
        ])

    def spec(self, family, unbound=False):
        gates = self.area / ("gates-" + uuid.uuid4().hex)
        gate = t.ref(freeze_json(gates / "summary.json", {"syntheticFixtureOnly": True})["path"])
        spec = {
            "schemaVersion": 1, "mode": "integration", "scope": m.SCOPE, "family": family,
            "run": f"N1-B134-{family.upper()}-INTEGRATION-001", "candidate": M,
            "session": None if unbound else NEW if family == "claude" else t.OWN["gpt"],
            "basisSnapshot": m.REVIEWED, "signedClosure": m.CLOSURE,
            "basisAcceptance": m.PRIOR[family], "authorization": m.AUTH, "obligations": [],
            "originalGates": {"closure": gate, "committed": gate},
            "mergeGates": {"merge": gate, "committed-merge": gate},
            "preservationProof": gate, "templateOnly": unbound,
            "bootstrap": None, "syntheticFixtureOnly": True,
            "reviewerOrigin": {"kind": "replacement-Claude-family-integration-impact-confirmation"
                if family == "claude" else "same-reviewer-integration-impact",
                "priorSession": t.OWN[family], "priorRun": f"N1-B134-{family.upper()}-REVISION-002"},
        }
        if family == "claude" and not unbound:
            path = self.area / ("bootstrap-" + uuid.uuid4().hex) / "events.jsonl"
            write_frozen(path, self.bootstrap_raw)
            spec["bootstrap"] = t.ref(path)
        return spec

    def live(self, session, raw):
        path = self.home / ".copilot" / "session-state" / session / "events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return path

    def fixtures(self):
        original = {"manifest.json": ("100644", "blob", "a" * 40)}
        original.update({name: ("100644", "blob", "b" * 40) for name in m.contract.CONTENT})
        closed = {**original, m.contract.PROGRESS: ("100644", "blob", "c" * 40),
                  m.contract.CLOSURE + "provenance.json": ("100644", "blob", "d" * 40)}
        merged = {**closed, **{name: ("100644", "blob", "e" * 40) for name in m.contract.CHANGED}}
        def tree(git, commit):
            return {m.REVIEWED: original, m.CLOSURE: closed, M: merged}[commit]
        def blob(git, commit, name):
            return ("PRIVATE_OPPOSITE_FAMILY_RESULT\n" if name.endswith("provenance.json") else
                    '{"syntheticFixtureOnly":true}\n' if name == "manifest.json" else
                    "SYNTHETIC complete incoming unit " + name + "\n").encode()
        def git(*args):
            if "--" in args:
                return b"diff --git a/manifest.json b/manifest.json\n+SYNTHETIC runtime delta\n"
            if args[-2:] == (m.REVIEWED, M):
                return b"SYNTHETIC full delta PRIVATE_OPPOSITE_FAMILY_RESULT\n"
            return b"diff --git a/articles/numbers-and-counters.md b/articles/numbers-and-counters.md\n+SYNTHETIC incoming\n"
        return git, tree, blob

    def prepare(self, family, unbound=False):
        spec = self.spec(family, unbound)
        prefix = (self.bootstrap_raw if family == "claude" else
                  t.read(self.actual_roots[family][3]))
        if spec["session"]:
            self.live(spec["session"], prefix)
        request = self.area / ("request-" + uuid.uuid4().hex + ".json")
        freeze_json(request, spec)
        output = self.area / ("prepared-" + uuid.uuid4().hex)
        git, tree, blob = self.fixtures()
        with patch.object(t, "ROOT", self.area), patch.object(m, "ROOT", self.area), patch.object(
            Path, "home", return_value=self.home), patch.object(m, "actual_merge", return_value=(git, {
                "syntheticFixtureOnly": True})), patch.object(m.contract, "tree", side_effect=tree), patch.object(
            m.contract, "blob", side_effect=blob), self.inner_guard():
            self.assertEqual(m.main(["prepare", str(request), str(output)]), 0)
        record = json.loads(frozen(output / "preflight.json"))
        config, chain = t.value(record["config"]), t.value(record["chain"])
        joined = b"".join(t.reconstruct(chain).values())
        self.assertNotIn(b"PRIVATE_OPPOSITE_FAMILY_RESULT", joined)
        self.assertEqual(len(chain["sources"]), 14)
        self.assertEqual(t.reconstruct(chain)["own-basis/report.md"], t.read(self.actual_roots[family][0]["report"]))
        return output, record, config, spec, chain, prefix

    def test_01_authorization_and_bootstrap_exactness(self):
        creation = json.loads((HERE / "parent-create-session-parameters.json").read_bytes())
        self.assertEqual(creation["kickoff"]["prompt"], m.BOOTSTRAP)
        self.assertEqual(m.verify_bootstrap(self.bootstrap_raw, NEW)["status"], "PASS")
        for mutate in ("model", "cwd", "read", "user", "reply", "identity", "compaction", "system", "unfinished"):
            rows = t.parse_events(self.bootstrap_raw)
            if mutate == "model":
                rows[0]["data"]["selectedModel"] = "claude-unknown"
            elif mutate == "cwd":
                rows[0]["data"]["context"]["cwd"] += "-other"
            elif mutate == "read":
                rows.insert(-1, {"type": "tool.execution_start", "data": {"toolName": "view"}})
            elif mutate == "user":
                rows.insert(-1, {"type": "user.message", "data": {"content": "Read now"}})
            elif mutate == "reply":
                rows[-2]["data"]["content"] = "READY but reviewed already"
            elif mutate == "identity":
                rows[0]["data"]["sessionId"] = t.OWN["claude"]
            elif mutate == "compaction":
                rows.append({"type": "session.compaction_complete", "data": {}})
            elif mutate == "system":
                next(row for row in rows if row["type"] == "system.message")["data"]["content"] += " modified"
            else:
                rows.pop()
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                m.verify_bootstrap(old.Controls.encode_events(rows), NEW)
        data = old.Controls.forward("fixture")
        data.pop("agentMode")
        self.assertTrue(m.selected.forwarded(data, "fixture"))
        for mutate in ("source", "id", "missing", "content"):
            bad = copy.deepcopy(data)
            if mutate == "source":
                bad["source"] = "agent-wrong"
            elif mutate == "id":
                bad["transformedContent"] = bad["transformedContent"].replace(m.SOURCE["id"], "wrong")
            elif mutate == "missing":
                bad.pop("transformedContent")
            else:
                bad["content"] += "\nunauthorized"
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                m.selected.forwarded(bad, "fixture")

    def test_02_fresh_and_retained_exact_boundaries(self):
        events = t.parse_events(self.bootstrap_raw)
        events[-3]["data"]["usage"]["inputTokens"] = 700000 - 49000 - 1
        self.assertEqual(m.context(events, "claude", NEW, 0)["forecast"], 699999)
        with self.assertRaises(ValueError):
            m.context(events, "claude", NEW, 1)
        for family, cap in (("claude", 740000), ("gpt", 710000)):
            raw = t.read(self.actual_roots[family][3])
            rows = t.parse_events(raw)
            model, maximum = ("claude-opus-5.5", 952000) if family == "claude" else ("gpt-6.1-sol", 922000)
            usage = {"type": "session.usage_record", "data": {"usage": {"model": model, "responseModel": model,
                "inputTokens": cap - 49000, "maxPromptTokens": maximum}}}
            result = m.context(rows + [usage], family, t.OWN[family], 0)
            self.assertEqual((result["forecast"], result["limit"]), (cap, cap))
            self.assertEqual(sum(result["reserves"].values()), 49000)
            with self.assertRaises(ValueError):
                m.context(rows + [usage], family, t.OWN[family], 1)
            wrong = copy.deepcopy(usage)
            wrong["data"]["usage"]["responseModel"] = "unknown"
            with self.assertRaises(ValueError):
                m.context(rows + [wrong], family, t.OWN[family], 0)
        with self.assertRaises((ValueError, KeyError)):
            m.context(events, "unknown", NEW, 0)

    def test_03_prepare_unbound_and_bind_actual_bootstrap(self):
        prepared, _, _, _, _, _ = self.prepare("claude", unbound=True)
        self.assertEqual(json.loads(frozen(prepared / "readiness.json"))["status"],
                         "UNBOUND_TEMPLATE_NOT_ADMISSION_READY")
        with self.assertRaises(ValueError):
            m.preflight(prepared / "preflight.json")
        self.live(NEW, self.bootstrap_raw)
        git, tree, blob = self.fixtures()
        bound = self.area / "bound-claude"
        with patch.object(t, "ROOT", self.area), patch.object(m, "ROOT", self.area), patch.object(
            Path, "home", return_value=self.home), patch.object(m, "actual_merge", return_value=(git, {
                "syntheticFixtureOnly": True})), patch.object(m.contract, "tree", side_effect=tree), patch.object(
            m.contract, "blob", side_effect=blob), self.inner_guard():
            self.assertEqual(m.main(["bind", str(prepared / "preflight.json"), NEW, str(bound)]), 0)
        m.preflight(bound / "preflight.json")
        type(self).prepared_claude = bound

    def test_04_replacement_and_gpt_full_cli_pipelines(self):
        self.pipeline("claude", type(self).prepared_claude, native=True)
        prepared, _, _, _, _, _ = self.prepare("gpt")
        self.pipeline("gpt", prepared, native=False)
        result = m.contract.accepted({"merge": M, "confirmations": {
            "claude": type(self).accepted_claude, "gpt": type(self).accepted_gpt}})
        self.assertTrue(result)

    def pipeline(self, family, prepared, native, verdict="CONFIRMED"):
        git, tree, blob = self.fixtures()
        self.synthetic_verified_merge = (git, {"syntheticFixtureOnly": True})
        with patch.object(m.contract, "tree", side_effect=tree), patch.object(
            m.contract, "blob", side_effect=blob):
            self.pipeline_body(family, prepared, native, verdict)

    def pipeline_body(self, family, prepared, native, verdict):
        record, config, spec, chain = m.preflight(prepared / "preflight.json")
        prefix = self.bootstrap_raw if family == "claude" else t.read(self.actual_roots[family][3])
        live = self.live(record["session"], prefix)
        rows = [{"id": sid, "activity": {"status": "idle"}, "mode": "interactive"}
                for sid in (t.COORDINATOR, record["session"])]
        status = freeze_json(self.area / (family + "-status.json"), {"sessions": rows, "summary": {"total": len(rows)}})
        roster = freeze_json(self.area / (family + "-roster.json"), [{"id": row["id"]} for row in rows])
        observation = {"observedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
                       "status": old.Controls.small(status), "roster": old.Controls.small(roster)}
        if family == "gpt":
            observation["priorClaudeAcceptance"] = type(self).accepted_claude
        obs = self.area / (family + "-observation.json")
        freeze_json(obs, observation)
        admitted, final, accepted = (self.area / (family + "-" + stage) for stage in ("admit", "final", "accept"))
        with patch.object(t, "ROOT", self.area), patch.object(t, "actual_merge",
            return_value=self.synthetic_verified_merge), patch.object(
            Path, "home", return_value=self.home), self.inner_guard(), patch.object(t, "__file__", str(self.producer)), patch.object(
            m, "__file__", str(self.producer)):
            self.assertEqual(m.main(["admit", str(prepared / "preflight.json"), str(obs), str(admitted)]), 0)
        admission = json.loads(frozen(admitted / "admission.json"))
        text = old.Controls.report(record, chain, {})
        if family == "claude":
            text = text.replace("## Scope\n", "## Scope\nReviewer: replacement Claude-family integration-impact "
                                "confirmation; NEW session, not original reviewer\n")
        if verdict == "NEEDS FIX":
            source = chain["sources"][0]["source"]
            text = text.replace("Verdict: CONFIRMED", "Verdict: NEEDS FIX").replace(
                "Correctness: CLEAN", "Correctness: NEEDS FIX").replace(
                "## Findings\nNone.", "## Findings\n### F1: SYNTHETIC impact finding\n"
                "- Facet: Correctness\n- Severity: major\n- Confidence: high\n"
                f"- Citations: {source}:1\n- Evidence: SYNTHETIC fixture only\n"
                "- Required change: SYNTHETIC remedy, not a real teaching request")
        self.assertEqual(t.check_structure(text, record, chain, verdict)["status"], "PASS")
        report = Path(config["report"])
        stored = text.replace("\n", "\r\n")
        report.write_bytes(stored.encode())
        events = old.Controls.suffix(record, config, chain, text, stored, admission, native)
        events[0]["data"].pop("agentMode")
        events[0]["data"].update(turnId="synthetic-delivery", interactionId="synthetic-interaction")
        for row in events:
            if row["type"] == "assistant.turn_start":
                row["data"].update(turnId="synthetic-delivery", interactionId="synthetic-interaction")
            for call in row["data"].get("toolRequests", []):
                if call["name"] == "functions.send_session_message":
                    call["arguments"]["message"] = verdict
        raw = prefix + old.Controls.encode_events(events)
        for mutation in ("wrong-authorization", "no-authorization", "wrong-turn", "read-bytes", "external-session",
                         "new-user", "old-prefix", "partial-source", "wrong-read-path"):
            changed, bad_prefix = copy.deepcopy(events), prefix
            if mutation == "wrong-authorization":
                changed[0]["data"]["transformedContent"] = changed[0]["data"]["transformedContent"].replace(
                    m.SOURCE["id"], "wrong")
            elif mutation == "no-authorization":
                changed[0]["data"].pop("transformedContent")
            elif mutation == "wrong-turn":
                changed[1]["data"]["turnId"] = "wrong"
            elif mutation == "read-bytes":
                next(r for r in changed if r["type"] == "tool.execution_complete")["data"]["result"]["content"] += "cut"
            elif mutation == "external-session":
                next(r for r in changed if r["type"] == "external_tool.requested")["data"]["sessionId"] = "wrong"
            elif mutation == "new-user":
                changed.append(copy.deepcopy(changed[0]))
            elif mutation == "old-prefix":
                bad_prefix = prefix[1:]
            elif mutation == "partial-source":
                call = next(r for r in changed if r["type"] == "tool.execution_start")
                call["data"]["arguments"]["view_range"] = [1, 2]
            else:
                call = next(r for r in changed if r["type"] == "tool.execution_start")
                call["data"]["arguments"]["path"] += "-wrong"
            with self.subTest(family=family, mutation=mutation), self.assertRaises((ValueError, KeyError)):
                t.audit_snapshot(bad_prefix + old.Controls.encode_events(changed), record, config, chain, admission)
        live.write_bytes(raw)
        with patch.object(t, "ROOT", self.area), patch.object(t, "actual_merge",
            return_value=self.synthetic_verified_merge), patch.object(
            Path, "home", return_value=self.home), self.inner_guard(), patch.object(t, "__file__", str(self.producer)), patch.object(
            m, "__file__", str(self.producer)):
            self.assertEqual(m.main(["final", str(prepared / "preflight.json"), str(admitted / "admission.json"),
                                     str(final)]), 0)
        decision = {
            "final": t.ref(final / "final.json"), "report": t.ref(report), "candidate": M,
            "run": spec["run"], "session": spec["session"], "family": family, "scope": m.SCOPE,
            "verdict": verdict, "reportReadCompletely": True,
            "claimChecks": [{"claim": "SYNTHETIC integration impact", "evidence": "SYNTHETIC complete sources",
                             "disposition": "SYNTHETIC no invalidation"}],
            "limitsPreserved": ["SYNTHETIC ONLY; not independent counter correctness or prior verdict transfer"],
            "acceptedNewFindings": [] if verdict == "CONFIRMED" else ["F1"],
            "openClaimIds": [] if verdict == "CONFIRMED" else ["F1"],
            "dispositions": {}, "authorization": m.AUTH,
            "basisAcceptance": m.PRIOR[family], "reviewerOrigin": spec["reviewerOrigin"],
            "integrationImpactOnly": True, "priorLimitsAndHeldEvidencePreserved": True,
        }
        for mutation in ("authorization", "basisAcceptance", "integrationImpactOnly", "claimChecks"):
            bad = copy.deepcopy(decision)
            if mutation in ("authorization", "basisAcceptance"):
                bad.pop(mutation)
            elif mutation == "integrationImpactOnly":
                bad[mutation] = False
            else:
                bad[mutation] = []
            path = self.area / (family + "-bad-" + mutation + ".json")
            freeze_json(path, bad)
            with patch.object(t, "ROOT", self.area), patch.object(t, "__file__", str(self.producer)), patch.object(
                m, "__file__", str(self.producer)), self.assertRaises((ValueError, KeyError)):
                m.main(["accept", str(final / "final.json"), str(path), str(accepted)])
        path = self.area / (family + "-decision.json")
        freeze_json(path, decision)
        with patch.object(t, "ROOT", self.area), patch.object(t, "actual_merge",
            return_value=self.synthetic_verified_merge), patch.object(
            self.inner_guard(), patch.object(t, "__file__", str(self.producer)), patch.object(m, "__file__", str(self.producer)):
            self.assertEqual(m.main(["accept", str(final / "final.json"), str(path), str(accepted)]), 0)
        result = json.loads(frozen(accepted / "acceptance.json"))
        self.assertTrue(result["integrationImpactOnly"] and result["authorizationProspective"])
        self.assertEqual(result["mode"], "integration")
        self.assertEqual(result["confirmationAccepted"], verdict == "CONFIRMED")
        self.assertTrue(result["reviewEvidenceAccepted"])
        self.assertEqual(result["priorRawVerdict"], "NEEDS FIX")
        self.assertNotEqual(result["producer"]["sha256"], sha(frozen(RUNTIME)))
        setattr(type(self), "accepted_" + family if verdict == "CONFIRMED" else "actual_shaped_needs_fix",
                t.ref(accepted / "acceptance.json"))

    def test_05_identity_old_hold_and_semantic_tail_rejections(self):
        for family in ("claude", "gpt"):
            spec = self.spec(family)
            for name in ("authorization", "basisAcceptance", "session", "obligations", "reviewerOrigin"):
                bad = copy.deepcopy(spec)
                if name in ("authorization", "basisAcceptance"):
                    bad[name] = dict(bad[name], sha256="0" * 64)
                elif name == "session":
                    bad[name] = t.OWN["claude"]
                elif name == "obligations":
                    bad[name] = [{"id": "F1"}]
                else:
                    bad[name]["kind"] = "original-session-reuse"
                with self.subTest(family=family, field=name), self.assertRaises((ValueError, KeyError)):
                    m.identity(bad)
        with self.assertRaises(ValueError):
            m.previous_claude(m.PRIOR["claude"], M, m.SCOPE)
        spec = self.spec("gpt")
        spec_ref = freeze_json(self.area / "tail-spec.json", spec)
        record = {"spec": old.Controls.small(spec_ref)}
        prior = t.read(self.actual_roots["gpt"][3])
        for raw in (prior[1:], prior + json_bytes({"type": "user.message", "data": {"content": "extra"}})):
            with self.assertRaises(ValueError):
                m.verify_retained_prefix(record, raw)

    def test_06_needs_fix_remains_unaccepted(self):
        accepted = t.value(type(self).accepted_gpt)
        changed = dict(accepted, verdict="NEEDS FIX", confirmationAccepted=False,
                       acceptedNewFindings=["F1"], openClaimIds=["F1"])
        path = self.area / "synthetic-needs-fix.json"
        freeze_json(path, changed)
        with self.assertRaises(ValueError):
            m.contract.accepted({"merge": M, "confirmations": {
                "claude": type(self).accepted_claude, "gpt": t.ref(path)}})

    def test_07_complete_source_rederivation_rejects_reduced_packet(self):
        prepared = type(self).prepared_claude
        record, config, spec, chain = m.preflight(prepared / "preflight.json")
        git, tree, blob = self.fixtures()
        with patch.object(m.contract, "tree", side_effect=tree), patch.object(
            m.contract, "blob", side_effect=blob):
            m.verify_complete_dossier(record, config, spec, chain, git, {"syntheticFixtureOnly": True})
            changed = t.reconstruct(chain)
            changed["own-basis/report.md"] = changed["own-basis/report.md"][:20]
            with patch.object(t, "reconstruct", return_value=changed), self.assertRaises(ValueError):
                m.verify_complete_dossier(record, config, spec, chain, git, {"syntheticFixtureOnly": True})

    def test_08_needs_fix_full_controller_path_is_valid_but_not_accepted(self):
        prepared, _, _, _, _, _ = self.prepare("claude")
        # Separate synthetic case paths; do not overwrite the preceding pipeline.
        original_area = self.area
        self.area = self.area / "needs-fix-case"
        self.area.mkdir()
        try:
            self.pipeline("claude", prepared, native=False, verdict="NEEDS FIX")
            with self.assertRaises(ValueError):
                m.contract.accepted({"merge": M, "confirmations": {
                    "claude": type(self).actual_shaped_needs_fix, "gpt": type(self).accepted_gpt}})
        finally:
            self.area = original_area

    def test_09_full_fresh_status_and_serial_idle_are_mandatory(self):
        for mutation in ("busy", "unknown", "mode", "stale", "incomplete"):
            directory = self.area / ("status-" + mutation)
            rows = [{"id": sid, "activity": {"status": "idle"}, "mode": "interactive"}
                    for sid in (t.COORDINATOR, NEW, "synthetic-other-session")]
            if mutation in ("busy", "unknown"):
                rows[-1]["activity"]["status"] = mutation
            elif mutation == "mode":
                rows[1]["mode"] = "autopilot"
            roster = [{"id": row["id"]} for row in rows]
            if mutation == "incomplete":
                roster.pop()
            status_ref = freeze_json(directory / "status.json", {"sessions": rows, "summary": {"total": len(rows)}})
            roster_ref = freeze_json(directory / "roster.json", roster)
            observation = {"observedAt": "2000-01-01T00:00:00+00:00" if mutation == "stale"
                           else dt.datetime.now(dt.timezone.utc).isoformat(),
                           "status": old.Controls.small(status_ref), "roster": old.Controls.small(roster_ref)}
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                t.roster_check(observation, NEW, dt.datetime.now(dt.timezone.utc))

    def test_10_one_command_finalizer_builds_both_families_without_contact(self):
        helper = load_module("b134_integration_finalizer_controls", HERE / "finalize-integration.py")
        spec = self.spec("gpt")
        plan = {key: spec[key] for key in ("candidate", "originalGates", "mergeGates", "preservationProof")}
        path = self.area / "synthetic-actual-plan.json"
        freeze_json(path, plan)
        self.live(t.OWN["gpt"], t.read(self.actual_roots["gpt"][3]))
        git, tree, blob = self.fixtures()
        with patch.object(helper, "load_module", return_value=m), patch.object(helper, "start_guard",
                return_value=(self.FixtureGuard(), self.FixtureResource())), patch.object(
            t, "ROOT", self.area), patch.object(m, "ROOT", self.area), patch.object(
            Path, "home", return_value=self.home), patch.object(m, "actual_merge", return_value=(git, {
                "syntheticFixtureOnly": True})), patch.object(m.contract, "tree", side_effect=tree), patch.object(
            m.contract, "blob", side_effect=blob):
            helper.main([str(RUNTIME), str(path), "integration-followup-packet-001"])
        target = self.area / "integration-followup-packet-001"
        index = json.loads(frozen(target / "index.json"))
        self.assertTrue(index["noReviewerContact"] and index["requiresActualClaudeBootstrapAndBind"])
        self.assertEqual(index["serialOrder"], ["claude", "gpt"])
        self.assertEqual(json.loads(t.read(index["outputs"]["claude"]["readiness"]))["status"],
                         "UNBOUND_TEMPLATE_NOT_ADMISSION_READY")
        self.assertEqual(json.loads(t.read(index["outputs"]["gpt"]["readiness"]))["status"],
                         "PREPARED_NOT_ADMITTED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
