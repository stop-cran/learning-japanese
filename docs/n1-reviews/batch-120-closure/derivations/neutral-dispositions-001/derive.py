"""Coordinator derivation of reviewer-neutral and per-reviewer views of the author's pair-dispositions.md."""
import hashlib, json, re
from pathlib import Path
OUT = Path(__file__).resolve().parent
SRC = Path(r"C:\Users\stop-\n1-kanji-workspace\b120-worktree\docs\n1-sources\batch-120\reconciliation-001\pair-dispositions.md")
SHA = "879407225815967d6a482046d042eb6b765f2dbf3c4122f56c93814b61edcd88"
raw = SRC.read_bytes(); assert hashlib.sha256(raw).hexdigest() == SHA
text = raw.decode("utf-8").replace("\r\n", "\n")
lines = text.split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("The comparison card snapshots"))
end = next(i for i, l in enumerate(lines) if l.startswith("## Other consequential"))
table = "\n".join(lines[start:end]).rstrip() + "\n"
assert "GPT" not in table and "Claude" not in table and "initials" not in table
sup = next(i for i, l in enumerate(lines) if l.startswith("This document supersedes"))
supersede = " ".join(l.strip() for l in lines[sup:sup + 2]).strip()
assert supersede.endswith("`../preauthoring-notes-002.md`.")
flat = re.sub(r"\s+", " ", text)
def q(s):
    assert s in flat, s
    return f"> {s}"
header = ("# B120 author pair dispositions — coordinator reviewer-neutral view\n\n"
          f"Coordinator derivation from the author's committed `docs/n1-sources/batch-120/reconciliation-001/pair-dispositions.md` "
          f"(SHA-256 `{SHA}`). Source lines {start + 1}-{end} are reproduced verbatim below. The author's opening paragraph and final "
          "section are omitted here because they mention more than one review; your own claim routing follows separately. "
          "The original candidate is `8637cccb25507a1123559041ebba5401203de2db`; original batch base "
          "`aab6e2782f093ace1deb4f567c5e4dee8890cbf6`. Verbatim author sentence from the omitted opening: \n\n"
          + q(supersede) + "\n\n"
          "Coordinator source note: the cited English source is supplied as a coordinator text display of the Noun/Verb sections "
          "(`wiktionary-arrest-english-senses.txt`), bound to the raw capture SHA-256 quoted below. `comparison-cards/` snapshots "
          "are byte-identical to the candidate blobs; the actual revised `kanji/` cards are supplied instead. "
          "These are author claims to verify, not evidence of their own correctness.\n\n---\n\n")
neutral = (header + table).encode("utf-8")
common_tail = [q("Existing 捕/追/届/至/達/着 guards remain. Their prior complete source families and comparison cards are in the initial evidence; 着 is justified by arrival/reach, not unverified secondary attachment or skill claims. The new table supplies independent 到/取/握/止/停/接/触 evidence."),
               q("Font cmap evidence establishes that all three pinned fonts contain 逮, not that separate 辶/隶 or native fallback render correctly. Arbitrary pools, multi-borrow, Kotlin/native/device, old APK, served ZIP and publication acceptance remain unverified.")]
maps = {
 "claude": ["# Claim routing for your initial report (coordinator-prepared)", "",
   "Coordinator routing from the omitted final section of the author's pair-dispositions.md. Quoted lines are verbatim author text; unquoted routing lines are the coordinator's pointers to rows of the neutral table and are not evidence. References to any other review are omitted.", "",
   "- D1/L1 → the 留 row (guard added). The complete 留 evidence was extracted after your initial review and is supplied as `retention-*` records with their receipt.",
   "- O4 → the 循 row (guard added).",
   "- D8 → the 得 row. Author text:", q("Claude D8 is superseded by the 得 precaution above."),
   "- D2/D3, D5–D7, D12. Author text:", q("Claude D2/D3: searching and pursuit have different goals; the initial's categorical claim that the chased target must be in view is not adopted. D5/D6/D7/D12 remain bounded observations from that initial, not independent certification of every secondary sense. No inference from mere lack of a source or present pool exposure is used as a proof."),
   "- D9–D11. Author text (portion naming only your IDs):", q("Claude D9-D11"), q("distinguish reaching from the supplied crossing/exceeding senses"), q("This is not a whole-corpus non-collision claim."),
   "- L3. Author text:", q("Claude L3's unread 禁/束/防/制 remain screening limits, not safety approvals. Neither this packet nor the title index certifies all old cards."),
   "- L2, L4–L7. Author text (portion naming only your IDs):", q("Claude L2/L4-L7"), q("retain their bounded source, stroke geometry, host-model and execution limits as applicable."),
   "- O1–O3 are answered in your author response. Its O1 cites `bindings.json`, which is not supplied because it names files of another review; the same CRLF/wrapper proof is the supplied `coordinator-candidate-verification.json`.",
   "- Existing guards and general limits. Author text:", *common_tail, ""],
 "gpt": ["# Claim routing for your initial report (coordinator-prepared)", "",
   "Coordinator routing from the omitted final section of the author's pair-dispositions.md. Quoted lines are verbatim author text; unquoted routing lines are the coordinator's pointers to rows of the neutral table and are not evidence. References to any other review are omitted.", "",
   "- D5/L3 → the 留 row (guard added). The complete 留 evidence was extracted after your initial review and is supplied as `retention-*` records with their receipt.",
   "- D6/L3 → the 循 row (guard added).",
   "- D7–D9/D13 → the 得, 持, 収 and 凌 rows. Author text:", q("GPT D7-D9/D13 receive separate two-direction dispositions above."),
   "- L4/L5 → the 到, 取, 握, 止, 停, 接 and 触 rows. Author text:", q("GPT L4/L5 receive complete 到/取/握/止/停/接/触 cards and applicable independent sources above; their original guards remain."),
   "- D10–D12, L6. Author text (portion naming only your IDs):", q("GPT D10-D12 distinguish reaching from the supplied crossing/exceeding senses; GPT L6 notes not every other family, including moving-house 越す, was independently verified. This is not a whole-corpus non-collision claim."),
   "- D1–D4. Author text:", q("GPT D1-D4 及/拘/捉/掴 have no current cards and are not added. No unsupported 逮ぶ spelling is asserted."), q("Neither this packet nor the title index certifies all old cards."),
   "- L2/L6. Author text (portion naming only your IDs):", q("GPT L2/L6 retain their bounded source, stroke geometry, host-model and execution limits as applicable."),
   "- Existing guards and general limits. Author text:", *common_tail, ""],
}
rec = {"source": {"path": str(SRC), "sha256": SHA}, "verbatimTableLines": [start + 1, end], "outputs": {}}
def write(name, data):
    p = OUT / name
    with p.open("xb") as f: f.write(data)
    rec["outputs"][name] = {"path": str(p), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
write("pair-dispositions-neutral.md", neutral)
for fam, body in maps.items():
    data = "\n".join(body).encode("utf-8")
    other = "gpt" if fam == "claude" else "claude"
    assert other.upper() not in data.decode().upper().replace("GPT D", "X D") if fam == "gpt" else "GPT" not in data.decode()
    write(f"claim-routing-{fam}.md", data)
rec["script"] = {"path": str(Path(__file__).resolve()), "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (OUT / "derivation.json").open("x", encoding="utf-8") as f: f.write(json.dumps(rec, indent=2) + "\n")
print(json.dumps(rec, indent=1))
