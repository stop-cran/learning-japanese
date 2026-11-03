I'm withdrawing one sentence of my confirmation: the claim that I made one tool call per response and saw no overlapping calls. It was wrong. The text verdicts are unchanged.

**Snapshot:** The teaching snapshot stays 8534b8989d7a0aeaff80f5ed55eeb6c2683cc642 (the original was 09e480adadc433f54cdbe20e3691ab38126bb711). This supplement only corrects a statement about how my confirmation was run; no teaching content changed.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), the same session as the original review.
- **Read fresh:** this supplement's prompt, then one view of my own `docs\n1-reviews\batch-009-confirmation-claude.md`.
- **Not done:** no linguistic re-review, source fetch, packet reread or other report.

**Verdicts:** All are carried over from the confirmation, not re-reviewed:
- `kanji\杏.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\杏.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `kanji\李.md` and `words\李.md`: CLEAN on all three facets, carried over from the initial review.

**Findings:**
1. **Process claim withdrawn (confidence: high).**
   - **Withdrawn:** the Scope line in my confirmation that says "I made one tool call per response and saw no overlapping calls."
   - **Coordinator's observation:** the view of `batch-009-origin-evidence.json` and the web_fetch of the Kotobank 杏子 entry overlapped by about 7 ms. I accept this; I did not inspect the logs myself.
   - **My own transcript agrees:** I put both calls in a single response, which broke the "one call per response" instruction.
   - **Effect on the review:** both calls succeeded and returned their full content, so the linguistic findings and verdicts are unaffected.
   - The confirmation's text and its receipt stay as they were; this supplement does not replace them.
   - My initial-review statement that it made no overlapping calls is untouched; I had no reason to question it.

**Optional:** None new. The earlier optional notes stand unchanged.

**Limits:**
- **Timings:** I have not checked the JSONL timestamps myself; they are as the coordinator reported them.
- **Seriality between processes:** reviewer processes exiting before the next launch is a separate matter that I did not check.
- **Not run:** `validate.py` and the manifest check.
- **Text-only:** no phone or native-speaker evidence.
