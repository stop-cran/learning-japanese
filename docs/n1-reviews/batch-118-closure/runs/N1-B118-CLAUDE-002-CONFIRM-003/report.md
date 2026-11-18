# B118 confirmation — N1-B118-CLAUDE-002-CONFIRM-003

## Snapshot
Commit: a7b4edfb3d3c3bfcc061cfbdd0ee04de1e53204e
Model: identity unverified; the host labels this session Claude Opus 5.5, which I cannot independently verify

## Scope
Chain: segments 1-44 of n1-b118-claude-002-confirm-003, each read once in order; no re-views
Fetches: none

## Dispositions


## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The only runtime change since fa2f64f is in 析.md, which adds 11 exclusions and two Notes bullets (diffs/fix.patch:1-22; snapshot/kanji/析.md:14; snapshot/kanji/析.md:46-47). The eleven earlier exclusions keep their order, no added target overlaps distractors 新/本/休, and metadata, readings, selection, link, strokes and other Notes are unchanged. Each Notes claim matches a positive Digital Daijisen sense in the opened sections: 断 たち切る／切り分ける (source-display-003/断.html.txt:38), 絶 途中でたち切る (source-display-003/絶.html.txt:36), 折 二つに分け離す (source-display-003/折.html.txt:62), 研 物事の本質をきわめる (source-display-003/研.html.txt:40), 究 真理や本質をつかむため推し進める (source-display-003/究.html.txt:49), 査 しらべる (source-display-003/査.html.txt:37), 調 とりしらべる (source-display-003/調.html.txt:46), 察 調べて明らかにする (source-display-003/察.html.txt:38), 考 調べる (source-display-003/考.html.txt:40), 討 問題点をくまなく探り調べる (source-display-003/討.html.txt:39) and 批 つきあわせて良否をきめる (source-display-003/批.html.txt:39). Set against 析's こまかく分かつ／こみ入ったものを解きほぐす (source-display-003/析-daijisen.html.txt:38) and KANJIDIC2 chop/divide (snapshot/docs/n1-sources/batch-118/reconciliation-001/kanjidic2-records.xml:1153-1156), each of these direct symmetric pairs has a defensible overlap. In my previous passes I called several of these pairs harmless; guarding them anyway is conservative but source-backed, and over-exclusion only narrows fallback pools rather than creating a wrong or ambiguous option. The Notes qualify every overlap and claim no interchangeability. I accept the 論 decline: its senses 筋道を立てて述べる, opinion and theory (source-display-003/論.html.txt:38-39) concern stating a reasoned position, not dividing or disentangling material. Modeled runtime is unchanged, with curated options still filling all slots (gates-reconciliation-002/quiz-safety.log:1-2), and all ten gates pass with reproducible manifest 4c1ac444c3672e64. I found no new defect, and no consequential claim remains unresolved.

## Findings
None.

## Optional
### O1: Broadened examination rationale leaves some earlier no-guard pairs without fresh disposition
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/析.md:47; scratch-118/review/reconciliation-002/comparison-cards/批.md:3; snapshot/docs/n1-sources/batch-118/reconciliation-001/kanjidic2-records.xml:1809-1885
- Evidence: The new Notes justify the 批 exclusion as "comparing to judge" and the 考 exclusion as general thinking and examining. The 判 "judge; seal" pair (KANJIDIC2 judgment) and other examination titles judged no-guard in the reconciliation-001 record, such as 診 and 試, were not re-dispositioned under this broader standard. I still judge them harmless, but the boundary is now less self-evident.
- Suggestion: Optionally record a one-line disposition for 判 (and 診/試) against the broadened examination rationale, or narrow the 批 note so that judging alone is not the stated basis.

## Limits
- L1: All limits from my previous confirmation still apply. The raw HTTP responses, raw KanjiVG SVG, Joyo PDF and manifest.json bytes were not supplied, and no geometry claim is made.
- L2: changed-file-inventory.json again lists a 析.md worktree hash that differs from the staged hash. Its own stagedWorktreeNormalization note attributes this to CRLF/LF normalization, which I could not independently verify. I reviewed the staged-hash content supplied as snapshot/kanji/析.md.
- L3: The quiz-safety and reading-exposure logs are bounded host models. They do not establish caller-built or multi-borrow pools, Kotlin execution, native or phone acceptance, publication, or compatibility with the installed APK 5c000bd, which predates quiz_exclusions.
- L4: The exclusion judgments are editorial semantic assessments based on KANJIDIC2, Digital Daijisen sections and supplied cards. They are not native-speaker certification or an exhaustive corpus boundary, and pairs never opened in any pass (for example 観 and 理) remain unassessed.
- L5: The .txt section derivatives are author markup-stripped. I relied on the exact HTML display slices, whose derivation records say they add only one LF; I did not re-verify their hashes against the raw responses.
