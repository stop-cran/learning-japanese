## Snapshot: b6c33ca7cf8c3e445256be7ae84744275ca8f216; committed files only

**GPT-01 is resolved. No actionable regression was established in the revised teaching passages.** Snapshot identity and clean-worktree status are author-supplied, not independently Git-verified.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Read the supplied teaching diff first, then all eight teaching files completely for changed-passage context. Checked the direct exclusion, qualified 流す comparison, added comparison links and their targets, revised 測 mnemonic, 温もり note, and updated source citations against relevant pinned records and fetched dictionary entries.

This was read-only: no edits, commands, delegation, or agents. No assigned revised passage was omitted. Unchanged material was used as context, not comprehensively re-reviewed; other reviewers’ reports and prohibited materials were not consulted. Git, structural validation, aggregate reading counts, and manifest builds were not independently checked.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\浅.md` | CLEAN | CLEAN | CLEAN |
| `kanji\浴.md` | CLEAN | CLEAN | CLEAN |
| `kanji\混.md` | CLEAN | CLEAN | CLEAN |
| `kanji\減.md` | CLEAN | CLEAN | CLEAN |
| `kanji\温.md` | CLEAN | CLEAN | CLEAN |
| `kanji\測.md` | CLEAN | CLEAN | CLEAN |
| `kanji\湾.md` | CLEAN | CLEAN | CLEAN |
| `words\浴びせる.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within this changed-passage scope, not exhaustive truth or native-fluency certification.

## Findings:

**GPT-01 — RESOLVED; originally Minor, scoped coverage. Confidence: high.**

`words\浴びせる.md:8` now directly includes `流す` in `quiz_exclusions`, preserving all previous exclusions. Under the symmetric, pairwise behavior documented in `docs\content-format.md:85-99`, this protects the pair without relying on transitivity through 注ぐ. The original minimal remedy is fully implemented.

The accompanying comparison at `words\浴びせる.md:36-37` accurately limits the overlap to a physical washing use and explicitly rejects unrestricted synonymy. Its citations at lines 46-48 support that distinction:

- Pinned `docs\n2-batch-sources\batch-13.json`, entry **1552120**, 流す／ながす, sense 1, includes “to pour”; the complete retained reading record has no spelling restriction or kana-only limitation.
- The fetched [精選版 日本国語大辞典, 流す／ながす](https://kotobank.jp/word/%E6%B5%81%E3%81%99-587809), 一④, explicitly describes washing by applying water over the body.
- The fetched [Digital Daijisen, 浴びせる／あびせる](https://kotobank.jp/word/%E6%B5%B4%E3%81%B3%E3%81%9B%E3%82%8B-426412), senses 1 and 3, supports the physical and question-bombarding uses without requiring the same range for 流す.

**Adopted revisions — no new actionable issue.** The links at `kanji\浅.md:20`, `kanji\減.md:20`, `kanji\混.md:46`, `kanji\温.md:46`, `kanji\測.md:41-42`, and `kanji\湾.md:43` resolve to the intended existing comparisons. The revised mnemonic at `kanji\測.md:22` distinguishes 則’s “rule to follow” from a measuring scale and remains explicitly non-etymological.

At `kanji\温.md:48`, 温もり／ぬくもり is correctly presented as a distinct noun, not the archaic standalone 温／ぬく. Pinned entry **1183330** explicitly supports “warmth,” noun status, the spelling/reading pair, and “usually written using kana alone.” The unchanged archaic qualification remains intact.

## Optional:

None.

## Limits:

No consequential linguistic claim remains unresolved in the revised passages. Runtime quiz behavior was assessed against the documented exclusion contract, not executed. The author’s exact correction-file count, structural results, aggregate counts, and byte-identical manifest builds remain independently unverified. Generated stroke drawings and unchanged pages outside the contextual reads were not re-reviewed.
