Snapshot: `3158b2b97cc9ba61368b722d0c45c37536a909c5`, compared with `acf7297ef66a82f620a6c5551d95a2e3fa356bc7`. Reviewer: OpenAI GPT-family model; the exact serving model/version identifier is not exposed to me.

Scope:

Independent, blind, read-only second confirmation. I read 契 completely, checked the sole changed hunk against all four facets, and examined the corrected meaning/reading evidence for every batch card.

**Current packet: `confirm2-138-gpt`**

- **Full text:** `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`; `diffs\fix.patch`, `diffs\changed-files.txt`, `diffs\changed-lines.txt`; `snapshot\kanji\契.md`.
- **Full text, bounded reads:** `checks\reading-exposure.txt`, `checks\reading-options.txt`.
- **Full text:** `checks\quiz-safety.txt`, `checks\link-targets.tsv`; `evidence\README.md`, `evidence\extras-merge-fix.txt`, `evidence\QuizBuilder.kt`, `evidence\kanjipedia-契.txt`, `evidence\jmdict-cited-entries.xml`.
- **Selective substantive inspection and full byte comparison:** `evidence\KanjiReadings.kt`, lines 1–160; `evidence\Words.kt`, lines 160–260. The latter was also read programmatically to extract the mutation rules.
- **Full programmatic comparison:** `evidence\reading-exposure-b6020f9e.txt`, `evidence\reading-options-b6020f9e.txt`.
- **Full programmatic reads for exact comparisons and selected metadata inspection:** `snapshot\kanji\噴.md`, `垂.md`, `垣.md`, `執.md`, `堅.md`, `塊.md`, `墨.md`, `壁.md`, `壊.md`, `奏.md`, `契.md`, `奨.md`, `奪.md`, `妨.md`, `威.md`. This was not a fresh full editorial rereading of the fourteen unchanged cards.

**Earlier authorized material reopened**

- `reports-138\confirm-gpt.md`: full text.
- Under `confirm-138-gpt`: the complete text of `snapshot\kanji\垣.md`, `執.md`, `堅.md`, `塊.md`, `壊.md`, `奏.md`, `契.md`, `奪.md`, `妨.md`, `威.md`, read programmatically for exact comparisons; `checks\reading-exposure.txt` and `checks\reading-options.txt`, compared in full, with headers and changed output inspected.
- Under `batch-138-b6020f9e`: `snapshot\kanji\噴.md`, `垂.md`, `墨.md`, `壁.md`, `奨.md`, compared programmatically in full; `evidence\app-code\QuizBuilder.kt`, `KanjiReadings.kt`, `Words.kt`, full byte comparisons; `evidence\audits\quiz-safety.txt`, full byte comparison.
- Also under the original packet: `evidence\kanjipedia-outside-readings.json`, parsed in full with 垂/執/壊/奏/奪 records inspected; `evidence\daijisen-heads.txt`, read programmatically with selected 垂/壊/奏 records inspected; `repo\kanji\出.md`, `話.md`, `足.md`, `敗.md`, `破.md`, lines 1–18 inspected and metadata extracted programmatically.

Actual public entries inspected: [Kanjipedia 契](https://www.kanjipedia.jp/kanji/0001765100), [Kanjipedia 壊](https://www.kanjipedia.jp/kanji/0000825600), and the opening 12,000 characters of [Weblio 壊れる](https://www.weblio.jp/content/%E5%A3%8A%E3%82%8C%E3%82%8B), including Daijisen's こわれる entry. The outside-table やぶれる verification comes from Kanjipedia, not an inference from the Weblio extract.

Dispositions:

- **A1 — RESOLVED** — Both corrected command headers contain exactly the deduplicated union of the earlier arguments: nineteen arguments become fourteen unique-kanji arguments. Independent normalization reproduces the twelve discarded readings; 壊 エ/やぶる were already metadata-protected, 奪 タツ was mutation-protected, and the exposure audit already obtained 垂 しで from JMdict. All eight previously unchecked readings now appear in the outputs. The newly recorded 壊 やぶれる case is genuinely attested and remains blocked in the shipped pools; see the independent check below. This resolves the supplied audit correction, not certification of the unavailable audit programs.
- **OR — RESOLVED, for case retention** — The complete corrected exposure audit records all nine latent cases, including 壊 やぶれる offered by 敗/破. Both corrected original-snapshot audit bodies match the revised-snapshot bodies exactly after their first lines. Retention is verified; future execution schedules are not.
- **L1 — RESOLVED** — The documentation corrects the earlier literal “line for line” claim. The current meaning audit is byte-identical to the original packet's complete audit, independently verified by comparison and SHA-256.

Verdicts:

- **Correctness: CLEAN** — 契's changed reading is correct, the paragraph remains consistent, and no new factual defect was established.
- **Scoped coverage: CLEAN** — No reading, example, qualification or citation was removed; the corrected audits restore previously omitted checks.
- **Consistency and quiz safety: CLEAN** — All fifteen cards' supplied meaning options and corrected reading evidence were checked; no new actionable collision was established in the audited shipped pools.
- **Comprehensibility: CLEAN** — Hiragana for the word reading matches the surrounding examples and does not change the separate katakana notation for on-readings.

No card differs within this confirmation's scope.

**Changed-hunk check**

Exact comparison establishes that `契.md:43` changes only `契闊 ケッカツ` to `契闊 けっかつ`. The other fourteen supplied cards are byte-identical to their previously supplied versions; all fifteen front matters are unchanged. The patch and changed-line list agree.

The actual Kanjipedia entry prints 契闊(ケッカツ), associates it with ケツ and 久しく会わない, and marks ケツ outside the official reading table. Thus けっかつ preserves the pronunciation and the stated sense. The same entry supports the paragraph's キツ/契丹 account; supplied JMdict entry 2714430 confirms きったん and けいたん. No local link or quoted title changed. The external Kanjipedia link resolves. No contradiction with the rest of 契's card was established.

**All fifteen cards: quiz recheck**

The actual English meaning labels in the complete audit were assessed, including reverse-direction and ordinary-secondary-sense considerations. All forty-five authored alternatives remain defensibly wrong; none changed.

| Card | Meaning wrong-option cards | Reading prompt checked |
|---|---|---|
| 噴 | 口・古・買 | フン |
| 垂 | 郵・乗・重 | スイ |
| 垣 | 坂・城・埋 | かき |
| 執 | 報・幸・熱 | シツ |
| 堅 | 臣・監・基 | かたい |
| 塊 | 魅・城・場 | かたまり |
| 墨 | 墓・型・堂 | すみ |
| 壁 | 辛・基・坂 | かべ |
| 壊 | 均・埋・塔 | こわす; shared-stem handling of こわれる |
| 奏 | 春・天・実 | ソウ |
| 契 | 大・天・分 | ケイ |
| 奨 | 美・奥・奇 | ショウ |
| 奪 | 集・隼・雑 | うばう |
| 妨 | 姉・始・旅 | さまたげる |
| 威 | 成・歳・減 | イ |

All three supplied app sources are byte-identical to the original copies. The meaning builder still applies direct exclusions symmetrically, including between wrong options; it does not infer transitive cliques. Unchanged front matter preserves the previously confirmed exclusions.

The reading builder protects full metadata readings and their mutations, selects one usable reading per curated holder first, then uses closeness-ranked fallback readings. It stops after three wrong options. Consequently the options audit's two HIT labels, 噴 ほん and 契 けつ, still do not establish drawable shipped-pool collisions: their curated holders fill all three slots. These are normalized keys; actual on-reading labels use katakana.

The corrected exposure audit reports **0 production hits, 0 Starter padded-session hits, 0 one-holder padded hits and 9 latent collisions**. The nine normalized cases are 噴 ほん/はく, 塊 ほど, 壁 がけ, 壊 やぶれる, 契 きつ/けつ/せつ and 奪 とる. 執 し remains explicitly name-only, not an ordinary on/kun collision.

For the newly recorded case, live Kanjipedia explicitly lists 壊 やぶれる outside the official table. Its closeness to the scheduled こわす is **2**. Independently inspected Starter cards 出, 話 and 足 supply distinct, unexcluded best readings だす, はなす and たす, each scoring **3**. Those three higher-tier alternatives block やぶれる in Starter and the larger shipped pools, also after borrowing either holder 敗 or 破. A small in-memory reproduction verified every holder-order permutation of those three-card subsets, with and without each holder. Conversely, `{壊, 敗}` and `{壊, 破}` reproduce the stated restricted-pool exposure. This supports a latent case, not a new shipped-pool defect.

Confirmation: **CONFIRMED** — A1, OR and L1 are resolved as qualified above; the single-line card revision introduces no established actionable defect.

Findings:

None new.

Optional:

None new.

Limits:

- The audit programs and gate runner are absent. I verified the merged arguments, complete output changes, cross-snapshot equality, relevant app mechanics and the new case independently; I did not inspect the actual parser fix or rerun whole-pool enumeration. The claimed packet-builder cause of the earlier blank-line loss and claims about other batches were not independently verified.
- The corrected outputs supersede my earlier count of eight latent cases. Their generic “card text” labels are provenance shortcuts, not proof that a reading appears in a card. In particular, しで was already covered by the exposure audit's JMdict evidence but is newly present in the options audit.
- Seed sampling is not exhaustive; some reachable options are not observed and some printed candidate lists are abbreviated. Conclusions are bounded to the supplied frozen inputs, restored extra-reading list, stated shipped/one-holder pools and default four-choice behavior—not every dictionary reading, hypothetical smaller pool, future quiz size or changed client. 壊's two selected forms share a stem and produce one normally scheduled prompt.
- Unchanged material retains the earlier review's scope and limitations; it was not all freshly dictionary-checked. No external checkout, Git ancestry, generated manifest, Kotlin/JVM execution, phone rendering, future audit schedule or closure process was certified.
- All tool calls were serial. No parallel calls, agents, other sessions, background jobs, recursive listings, corpus scans or other reviewer's report were used. Only authorized packet/report paths were opened. The only intentional persistent change is this report.
