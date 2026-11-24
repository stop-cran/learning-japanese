# B161 finding reconciliation

The original reports all reviewed the same committed candidate,
`bac3477e5323fad11c54e2f2bd424cd5c3693096`. The revised candidate is identified by the final
baseline-to-candidate diff hash and manifest version in [`provenance.json`](provenance.json).
Statuses below are the author's direct checks of the revised files and ledgers, not independent
post-fix reviewer confirmations.

## Claude Sonnet 5.5 — correctness and scoped coverage

| Finding | Status | Evidence |
|---|---|---|
| Add hardship-endurance and “worthy of” examples to たえる | Resolved | `words/たえる.md` now shows `厳しい訓練に耐える` and `この作品は鑑賞に堪える`; the cited Digital Daijisen entries support the patterns. |
| Show 坪 with a quantity | Resolved | `words/坪.md` now uses `30坪` in a land-area example and gives its approximate metric equivalent. |
| Optional claim that 耐える is the more frequent spelling | Optional; not asserted | The available evidence supports the chosen example spellings, not a frequency comparison, so the article does not make that claim. |

## GPT-6.2 Sol — consistency and quiz safety

| Finding | Status | Evidence |
|---|---|---|
| 圏内/内 direct quiz ambiguity | Resolved | `words/圏内.md` declares `内`; `wordQuizAudit.directExclusions` records the full list `[以内, 内]`. |
| たえる/我慢 direct quiz ambiguity | Resolved | `words/たえる.md` declares `我慢`; the audit records `[こらえる, 我慢, 凌ぐ]`. |
| 培/修 and 培養/育てる direct ambiguities | Resolved | The new cards declare `修` and `育てる`; the kanji and word audit lists match the cards. One declaration per pair is sufficient under `docs/content-format.md`'s documented symmetry. |
| Stale mechanical check values | Resolved | `batch-161-progress.json` records manifest `09243c4be32646a3` and the latest budget counts and byte totals. The validation, manifest, batch-audit and budget commands were rerun after the ledger edit. |

## Grok 4.7 — comprehensibility and scoped coverage

| Finding | Status | Evidence |
|---|---|---|
| 威嚇 needed a concrete display and warning contrast | Resolved | `words/威嚇.md` shows a dog baring its teeth and contrasts that with a warning sign; the kanji explanation gives supported character associations while saying to learn the compound as a whole. |
| 囚人 gloss conflicted with the legal-status explanation | Resolved | Both `kanji/囚.md` gloss rows and `words/囚人.md` use “prisoner; captive.” |
| Historical 囚人 readings were not labeled | Resolved | The word and kanji articles label めしゅうど and めしうど as historical and identify しゅうじん as the reading taught. |
| たえる/堪 worthy sense needed an example | Resolved | The article and kanji card explain `鑑賞に堪える`; the word article includes a complete example and translation. |
| 凌ぐ comparison lacked a usable distinction | Resolved | `words/たえる.md` illustrates `風雨を凌ぐ` and distinguishes “getting through” from withstanding a condition. |
| 耐える/堪える reading and こらえる contrast needed clarification | Resolved | `words/たえる.md` states both spellings are read たえる here and distinguishes the separate こらえる reading; `words/こらえる.md` now annotates 耐える as さむさにたえる. |
| 培養's figurative sense was not illustrated | Resolved | `words/培養.md` now focuses on biological culture and explicitly leaves broader dictionary senses outside its scope. |
| 堕落 was broadened beyond the taught moral/social sense | Resolved | `words/堕落.md` focuses on moral/social deterioration and contrasts it with neutral measured 低下. |
| Optional 坪 quantity example and 圏内 quiz-engine wording | Resolved | The quantity example was added; the 圏内 comparison now describes 内 and 以内 without quiz-engine language. |
| Other optional examples and gloss suggestions | Optional; not promoted to defects | The existing articles already explain the relevant definitions and contrasts; no unsupported claim was established by these suggestions. |

## Additional checks

- Validation initially identified a broken `圏外.md` link in `words/圏内.md`; it was corrected to
  plain text because no such article exists.
- The final content validator, manifest build, B161 audit, content-budget check and
  `git diff --check` all passed on the revised candidate.
- No actionable finding from the three original reports remains open in the reviewed scope.
- Independent post-fix confirmations were unavailable: the original review agents were
  synchronous one-shot tasks, and the runtime rejected follow-up messages. This reconciliation is
  author-performed; it is not represented as a fresh independent review.
