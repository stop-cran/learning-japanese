# B129 confirmation — N1-B129-CLAUDE-REPLACEMENT-CONFIRM-004

## Snapshot
Commit: 1b27107972311bdb9f485d0dc4879670a76cdc43
Model: Claude Opus 5.5 (runtime-reported; identity not independently verifiable)

## Scope
Chain: segments 1-65 of n1-b129-claude-replacement-confirm-004, each read once in order through END OF CHAIN; no re-views
Fetches: None

## Dispositions
- O1 - DECLINE ACCEPTED - The author defers the optional 絹/繭 guard (author-response/current.json:11). The supplied complete 絹 articles give fibre taken from cocoons, woven silk fabric, the broader 布帛 cloth sense, きぎぬ and the 羂 snare use, but no cocoon sense of 絹 (original-packet/evidence/external-snapshots/02-extract.txt:11-12; original-packet/evidence/external-snapshots/02-extract.txt:24-46). The original report rated the pair semantically harmless (initial-report/initial-claude-001.md:47). The 繭 card itself was not resupplied, so I rely on that attributed reading for 繭's side.
- O2 - RESOLVED - O2 named 撃, 劾, 批, 騒, 抗 and 盆 as unguarded despite overlapping guarded labels (initial-report/initial-claude-001.md:88-94). All six are now direct 虹 exclusions (snapshot/kanji/虹.md:14; diffs/fix.patch:30-31). Each pair has its own positive complete-source sense: Daijisen 攻める for 撃 (external-reconciliation/14-complete-lexical.txt:1-46); Jitsu せめる for 劾 (external-reconciliation/03-complete-lexical.txt:1-51); Jitsu 責問 for 批 (external-reconciliation/10-complete-lexical.txt:1-43); Jitsu さわぎみだれる for 騒 (external-reconciliation/28-complete-lexical.txt:1-88); Daijisen さからう for 抗 (external-reconciliation/11-complete-lexical.txt:1-45); Daijisen 浅い器 for 盆 (external-reconciliation/16-complete-lexical.txt:1-90). The card now frames them as conservative, non-transitive guards, not as synonymy (snapshot/kanji/虹.md:59-61). The remaining 競 (D19) item is optional below.
- O3 - DECLINE ACCEPTED - The 未 note is unchanged (snapshot/kanji/茉.md:61; author-response/current.json:13). It is internal wording, but it is accurate: KANJIDIC2 records み as nanori (evidence/english-readings/kanjidic2-target-records.xml:2). The み holders 未 and 味 are not drawable in the shipped pools (committed-checks/reading-exposure.log:19-21). No learner-facing error is established.
- O4 - DECLINE ACCEPTED - structure-unclassified remains in place (snapshot/kanji/茉.md:5; snapshot/kanji/絹.md:5; snapshot/kanji/虹.md:5) and is allowed. 字通 gives 虹 as 形声 with 工 (original-packet/evidence/external-snapshots/04-extract.txt:66-127). The 絹 sound element is only an unlabelled image (original-packet/evidence/external-snapshots/02-extract.txt:40-41), which supports the author's caution (author-response/current.json:14). The mnemonics stay explicitly non-etymological (snapshot/kanji/絹.md:29-32; snapshot/kanji/虹.md:29-32).
- O5 - DECLINE ACCEPTED - The card says only that コウ is unpractised because it lacks a support article. It makes no Joyo claim (snapshot/kanji/虹.md:38; author-response/current.json:15). Wiktionary marks コウ 表外 (original-source-sections/rainbow-wiktionary-japanese.txt:8-10), while the Daijisen header shows ［常用漢字］ with ［音］コウ and no 表外 label (original-packet/evidence/external-snapshots/04-extract.txt:19-20). Leaving the inventory unqualified is therefore safe.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: All five original optional points have accepting dispositions verified against the chain. All 26 new direct guards are supported by actual secondary senses in the complete counterpart articles: on 絹, 絡 Jitsu きぎぬ, 緒 and 線 thread, 索 Buddhist 羂索 cord, and 括 Nikkoku くくり snare; on 虹, 輪 円 光 via Nipponica's coloured ring of light, plus the 字通 dispute/reproach/attack/disorder/vessel ranges and 曲's curve noun. The new card prose matches those sources and keeps restrictions and the JMdict/monolingual discrepancies. The two non-guards, 絹/結 and 虹/容, are reasoned. Curated options 紙約級 and 紅功石 and the practice readings are unchanged and none is newly excluded. Committed host checks report 0 lint, validate and quiz-safety errors, 0 production or padded reading hits and 6 disclosed latent collisions. No new established defect was found; the residual items are disclosed limits and one optional consistency point.

## Findings
None.

## Optional
### O1: 競 remains outside the あらそう guard range
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: medium
- Citations: initial-report/initial-claude-001.md:55; evidence/reconciliation/jmdict-complete-records.xml:95; snapshot/kanji/虹.md:59-60
- Evidence: The original D19 row sent 競 (compete) to O2 because sense 1 of 争う あらそう is to compete/contest/contend. The revision now guards weaker overlaps such as 談 and 動 under the same unresolved あらそう/せめる range, but leaves 競 unguarded. The pair is not semantically required, and 競 is not a curated 虹 option, so modelled exposure is nil.
- Suggestion: For even-handed conservatism, either add 競 to 虹's quiz_exclusions with a one-line note on the compete sense, or record why it is left open.

## Limits
- L1: Execution-model identity is only runtime-reported (Claude Opus 5.5) and cannot be independently verified.
- L2: I am a replacement, not the historical initial reviewer. Coverage of the initial review stays attributed to that reviewer. I did not reread inputs that were not in this chain: the 繭 and 競 cards, the title index, joyo-rows.json, other external extracts beyond the supplied sections, raw HTML or images, or the non-English KANJIDIC2 fields.
- L3: Runtime evidence comes only from bounded host/static models: N1/All/Starter plus one borrowed target. Arbitrary, custom or multi-borrow pools, Kotlin execution, native or device acceptance, and compatibility with the older installed APK are not verified. The one-additional-holder Starter risks for 橋, 攻 and 責 and the six latent reading collisions remain (committed-checks/reading-exposure.log:56-73).
- L4: The 字通 せめる/あらそう allocation between the attack and reproach branches remains philologically unresolved. The guards are conservative, not disambiguating. Two source disagreements also persist: 羂索 is a noose in Nikkoku/Daijisen but a swing in Jitsu, and JMdict 2763660 lacks the Nikkoku くくり snare sense.
- L5: The supplied jmdict-noose-complete-records.xml has SHA-256 c5805d7b… in the chain, while the receipt records 862be4b7… for its output. Both describe an empty exact-zero 羂索 query result. I could not reconcile the serialization difference, and it has no effect on card content.
- L6: Rendering of 茉 (absent from the bundled fonts), stroke geometry and image-only source elements were not assessed. I did not rerun the committed check logs; I read them as supplied.
