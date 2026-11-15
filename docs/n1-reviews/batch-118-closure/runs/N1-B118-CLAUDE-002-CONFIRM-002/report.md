# B118 confirmation — N1-B118-CLAUDE-002-CONFIRM-002

## Snapshot
Commit: fa2f64f2472cf9ef10b8ac5f48db14dcaa248cd2
Model: identity unverified; the host labels this session Claude Opus 5.5, which I cannot independently verify

## Scope
Chain: segments 1-35 of n1-b118-claude-002-confirm-002, each read once in order; no re-views
Fetches: none

## Dispositions
- F1 - RESOLVED - snapshot/kanji/析.md:14 now declares 別 and 離 directly on 析 (diffs/fix.patch:11), so both symmetric direct pairs are handled independently of the existing 分/離 and 別/離 exclusions. The overlap is supported by the opened records: 析 divide (snapshot/docs/n1-sources/batch-118/reconciliation-001/kanjidic2-records.xml:1153-1156), 別 separate/branch off (same file 2209-2290), 離 detach/separation (same file 2476-2477), plus the 別 and 離 card titles and meaning text (scratch-118/review/reconciliation-001/comparison-cards/別.md:3; scratch-118/review/reconciliation-001/comparison-cards/離.md:3). The new Notes line (snapshot/kanji/析.md:44) states the separation overlap without claiming interchangeability. The original seven exclusions are kept in order, and no target overlaps distractors 新/本/休. validate.log reports 0 errors. Modeled runtime is unchanged: curated options still fill all three slots (gates/quiz-safety.log:1-2).
- O1 - RESOLVED - 盤 is added (snapshot/kanji/析.md:14), and Notes now explicitly call both 板 and 盤 precautionary guards for the single historical へぎ thin-board entry (snapshot/kanji/析.md:46). This matches the folk-terminology extract (source-display/folk-terminology.html.txt:29-31) and the KANJIDIC2 board gloss for 盤 (same xml, 1959-2033). The rationale is now consistent and qualified, and makes no claim of a modern 析 board sense.
- O2 - RESOLVED - The suggestion offered two alternatives, and the author took the second. The 切 rationale is narrowed to the explicit KANJIDIC2 chop gloss (snapshot/kanji/析.md:45) and no longer implies that every cutting-family title is unsafe. Declining a 断 guard is consistent with the evidence. 断 records severance/cutting/refusal/judgment (same xml, 1452-1547) and its card defines sever as cut off (scratch-118/review/reconciliation-001/comparison-cards/断.md:41-46), but no opened 析 source glosses sever or cut off. The author also correctly identifies that my initial D3/O2 citation evidence/kanjidic2-records.xml:57-60 pointed at French glosses; the English glosses are original-packet/evidence/kanjidic2-records.xml:51-54. That was a citation error in my report, not a content change.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The only runtime change is to 析.md: lines 14 and 44-46 (diffs/fix.patch:1-25; changed-file-inventory runtimeDelta). The diff adds the direct exclusions 別, 離, 刻 and 盤 and rewrites three Notes bullets. Each new guard rests on an opened ordinary or explicitly qualified sense. 刻, an unrequested addition, is supported by the KANJIDIC2 chop/cut fine gloss (same xml, 577-657) and by its card's 刻む "chop finely" (comparison-cards/刻.md:20-21, 33-37). That makes the 刻 guard conservative but defensible, and it is not a defect. The Notes wording is accurate: KANJIDIC2 析 chop and tear (xml 1153-1155), the 破 tear title, and the qualified へぎ source. Metadata, readings, the reading selection, the linked word, strokes and the original exclusions are unchanged. The ten gates pass with the reproducible manifest 1ea7bbc1cc57bd24. I reviewed the author's no-new-guard decisions for 断, 絶, 査, 究, 調, 研, 察, 診, 判, 削, 区, 片, 折, 細, 論, 批, 考, 刈, 討 and 試 against the supplied cards and records, using displayed titles plus secondary senses. None establishes 析 itself as having that displayed sense, so I accept them. All three dispositions are accepting, there is no new established defect, and no consequential claim remains unresolved.

## Findings
None.

## Optional
None.

## Limits
- L1: The added docs/n1-sources/batch-118/reconciliation-001/README.md, the manifest.json bytes, the raw Weblio response, raw KanjiVG SVG and the Joyo PDF were not supplied and remain unread. The pair-dispositions and source-extraction copies I read carry the same hashes as the staged docs files listed in changed-file-inventory.json.
- L2: changed-file-inventory.json lists a 析.md worktree hash (4d86df31…) that differs from its staged hash (9d33c5df…) while the worktree status is clean. This is probably line-ending conversion, but I could not verify it. I reviewed the staged-hash content supplied as snapshot/kanji/析.md.
- L3: The quiz-safety and reading-exposure logs are bounded host models. They do not establish caller-built or multi-borrow pools, Kotlin execution, native or phone acceptance, publication, or compatibility with the installed APK 5c000bd, which predates quiz_exclusions.
- L4: The judgments on exclusion pairs are editorial semantic assessments based on KANJIDIC2 glosses, the supplied cards and the Weblio sections. They are not native-speaker certification, and the automated checks do not test semantic ambiguity.
- L5: I did not compute exact meaning-line offsets inside every comparison KANJIDIC2 record. Several citations use the author-identified whole-record ranges, which I confirmed lie within the chain segments I read.
- L6: content-format.md lines 140-1419 were supplied as context. Only the quiz-authoring and exclusion sections (lines 97-133) bore on this confirmation.
