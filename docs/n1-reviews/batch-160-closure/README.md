# Batch 160: textual-review closure

**Status:** Textual review is closed. Publication is recorded only by the generated
[`batch-160-publication/provenance.json`](../batch-160-publication/provenance.json); until that
receipt exists, no publication is asserted here. This batch adds ten kanji cards, eleven support
articles and changes 21 reused articles. It is not completion of the full N1 expansion.

## Reviewed candidate

- Base: `e946e840fcf6fc5f530758d861390af77936cd1e`.
- Candidate HEAD: `fdf0df122332d39b18c4d36c04e9cde98f591baf` plus the uncommitted content and ledger
  changes; the final reviewed binary diff SHA-256 is
  `5d5130a948aa6ec3fc1b51e70b60cea10e77d7afeac4be8a59c2085030f1a999`.
- Final manifest content version: `25556a8e69ecf82d`.
- Initial blind-review diff: `38156b04dc98e127eaecacbd0439ee99795f786a48b285263c7e72638f89094b`.
- Reconciliation diff: `82f153095ad3b18f9b6761ad011af72d149dfdb86d552f3e42a7d703a44212fa`.
- The final delta was a direct 嘆–悔 quiz exclusion, its ledger entry and the corrected 嗣子 Daijisen
  fragment. GPT-6.2 Sol confirmed both fixes and Claude Sonnet 5.5 confirmed the fragment. These
  final confirmations are in `reports/f2-gpt.md` and `reports/f2-claude.md`.

  The progress ledger's delivery-accounting fields were added after textual review to carry forward
  the verified B159 totals and mark B160 review closure. They are contributor metadata, not part of
  the reviewed app-facing diff; the final manifest content version is unchanged.

The full source and baseline records are in
[`docs/n1-sources`](../../n1-sources/), especially
[`batch-160-progress.json`](../../n1-sources/batch-160-progress.json),
[`batch-160-jmdict.xml`](../../n1-sources/batch-160-jmdict.xml) and
[`batch-160-jmdict-selection.json`](../../n1-sources/batch-160-jmdict-selection.json).
The authoring contract is [`docs/content-format.md`](../../content-format.md).

## Reviewers and reports

The initial reports reviewed the same candidate snapshot with independent facets:

| Report | Runtime model | Facet |
|---|---|---|
| [`r1-claude.md`](reports/r1-claude.md) | Claude Sonnet 5.5 | Correctness and scoped coverage |
| [`r1-claude-supplement.md`](reports/r1-claude-supplement.md) | Claude Sonnet 5.5 | Focused 示唆 / 唆 quiz-safety supplement |
| [`r2-gpt.md`](reports/r2-gpt.md) | GPT-6.2 Sol | Consistency and quiz safety |
| [`r3-grok.md`](reports/r3-grok.md) | Grok 4.7 | Comprehensibility and scoped coverage |

The same reviewers then checked the revised candidate:

| Report | Runtime model | Scope |
|---|---|---|
| [`f1-claude.md`](reports/f1-claude.md) | Claude Sonnet 5.5 | Correctness, coverage and revised claims |
| [`f1-gpt.md`](reports/f1-gpt.md) | GPT-6.2 Sol | Quiz safety, consistency and source-ledger records |
| [`f1-grok.md`](reports/f1-grok.md) | Grok 4.7 | Seven prior comprehensibility/coverage findings and regressions |
| [`f2-gpt.md`](reports/f2-gpt.md) | GPT-6.2 Sol | Final 嘆–悔 and 嗣子-link fixes |
| [`f2-claude.md`](reports/f2-claude.md) | Claude Sonnet 5.5 | Final 嗣子-link fix |

Runtime model names are from the agent execution records; the original Claude-family report's own
model disclosure remains unchanged in its full report. Reports preserve their individual scopes and
limits; an out-of-scope facet is not treated as independently reviewed by that reviewer.

## Reconciliation

- **Meaning and source claims — resolved.** The unsupported admiration sense was removed from
  嘆く; admiration remains attached to compounds such as 感嘆. 嗣子 is narrowed to the family-heir
  sense and cites Daijisen. 画伯 now demonstrates the name-plus-honorific use and distinguishes it
  from 画家. 画's はかりごと/はか.る senses are separated. The final Daijisen fragment in 嗣子 was
  repaired and independently confirmed.
- **Reading and learner explanations — resolved.** The reviews' actionable notes for 子守唄, 啓,
  唱, 喝, 嘱, 伯 and 画 were reconciled in the current files. The 子守唄 ledger attributes `spec2`
  to the relevant spelling/reading rather than to the selected 子守唄 spelling; the 喚く note
  distinguishes the 叫く spelling flag from kana-usual usage.
- **Quiz ambiguity — resolved.** Direct kanji and word exclusions are recorded in the cards and
  batch ledger. The final review added 悔 to 嘆's direct exclusions; the card and ledger now match.
  Exclusions remain direct pairs, not transitive groups.
- **Navigation and citations — resolved.** The 伯仲 secondary link is retained, the 升 citation
  points to the ます entry, malformed Daijisen fragments in the reviewed links were corrected, and
  the nonexistent 恐喝 article link was changed to plain text rather than adding an unapproved word
  article.
- **Comprehensibility — resolved within the assigned scope.** Grok's seven actionable findings were
  confirmed resolved in the revised snapshot; no regression was reported.
- **Optional suggestions** such as further glosses for “shamisen” and the KANJIDIC2 “Brazil” note
  were not promoted to defects. No evidence-backed consequential claim remained unresolved in the
  reviewed scope.

## Mechanical checks and limits

On the final content candidate:

- `python -X utf8 -B tools/audit_n1_batch.py --batch 160` passed; the exact baseline runtime was
  preserved outside recorded changes and the manifest is fresh.
- `python -X utf8 -B tools/validate.py` passed with 0 errors.
- `python -X utf8 -B -m unittest discover -s tools -p "test_*.py"` passed: 448 tests.
- `python -X utf8 -B tools/check_content_budget.py` passed: 9,880 files / 9,896 entries;
  56,949,081 retained bytes; 57,385,153 inflated bytes; 36,573,057 local ZIP bytes.
- `python -X utf8 -B tools/grammar_vocabulary.py check` passed: 3,201/3,539 reviewed prompts,
  `stage=pilot`; this pre-existing pilot coverage is not a full vocabulary-completeness claim.
- `git diff --check` passed; Git emitted only the existing manifest LF-to-CRLF warning.

The reports identify evidence not re-fetched or independently pinned, including the absence of a
B160 KANJIDIC2 record packet. No native-speaker review, Android runtime/RealContentTest, rare-glyph
test, phone acceptance or general-release certification was performed for this batch. The review
closure is textual and source-bounded, not runtime or device acceptance.

Publication verification must use the exact pushed commit, its successful content CI run and the
exact GitHub ZIP/runtime-hash verifier. The repository's publication recorder will then advance
the batch ledger and preserve the delivery receipt; a later contributor-only receipt commit also
requires its own CI/exported-tree check.
