# B127 author audit

Base: `dd45f6fb7cd3ce579422e2333860aa6d245af898`.
Scope: one missing frozen member, **倉**, row 57, U+5009.
This is an authoring candidate, not independent review closure or publication.

## Membership, lexical support and preservation

The frozen index and community response hashes match the implementation
snapshot; the row was pending at freeze and neither runtime file existed at
the supplied base. The current published ledger is B126: 256 delivered,
972 undelivered. This local draft does not change those published counts.

Every active word metadata declaration was checked. The only required pair
is 倉 / 倉庫. The existing N2 word's JMdict family 1399120 has spelling
倉庫, reading そうこ and sense 1, storehouse/warehouse/godown, with no
spelling or reading restriction separating that pair. The existing article
also explicitly allocates ソウ + コ; the new card and wrapper agree.
Only the first substantive 倉 component introduction receives a link.
Word IDs, metadata, easier level, exclusions and all non-link prose are
unchanged. Five incidental occurrences are enumerated, not silently counted
as required reciprocal relationships.

## Complete source retention and reading distinctions

`source-receipt.json` binds the original compressed and decompressed
dictionary hashes, all 78 complete applicable JMdict families, the complete
KANJIDIC2 character record and full comparison records. These are parsed and
reserialized XML, not raw compressed-file slices. No field, spelling,
reading, sense restriction or priority flag was removed. Membership is
every family with 倉 in any `k_ele/keb`, not only the selected teaching words.
The second complete-source verification rechecks field completeness and
selection against the original frozen input streams.

ソウ / くら remain in their exact original metadata order. ソウ is selected
via the existing linked 倉庫 article. くら is a valid native noun (JMdict
1592380, alternate spellings 蔵 / 倉 / 庫); it is not selected because this
slice has no standalone linked word article, not because of a rarity claim.
穀倉 こくそう is JMdict 1287270, which also retains こくぐら; the chosen
example does not erase the other reading.

The actual Kanjipedia entry positively supplies にわか and a sudden/hurried
character sense. Daijisen independently confirms the hurried branch.
倉皇 そうこう (1399160) and 倉卒 そうそつ (1399200) support the examples;
only the latter family has the formal/literary flag. Neither absent priority
flags nor the outside-Joyo mark licenses dismissing the positive sense.
Jitsu's storing/prison glosses and its explicitly labelled old-dictionary
ホロブ / モロシ quotation are retained separately. The host exposure check
explicitly supplies にわか, ほろぶ, もろし, plus conservatively supplied
おさめる / ひとや kun-gloss keys. It does not merely run the ordinary
metadata-only check or promote all glosses into surface readings.

Full external-page captures stay in `scratch-127\external-pages`;
published bindings contain hashes and short attributable excerpts only.
The search summary's inconsistent Kanjipedia URL is not used as evidence.

## Meaning labels and actual corpus scans

Both `baseline-gloss-scan.json` and `baseline-gloss-scan-002.json` retain
all 1,246 baseline rows, their actual titles, complete KANJIDIC2 English
meanings and source-byte bindings. The first includes every token of every
new metadata meaning; the second expands to inspected secondary source
senses and English polysemy, including store, magazine, elevator, storing,
prison and old-dictionary lookup implications. The actual output is
retained, not replaced by a retrospective assertion that a scan occurred.

All 38 second-scan matches have finite dispositions after inspection of the
actual comparison articles and complete character records. Eleven direct
pairs are guarded: 庫, 蔵, 府, 室, 収, 貯, 急, 突, 亡, 置, 入.
Some are conservative broad-label guards in just one prompt/label direction,
not universal synonym claims. 府's storehouse sense and the sudden senses
are not ignored merely because their displayed primary labels differ.
Store-as-shop, magazine-as-periodical, putting-on-clothes and putting-up-
notices are disambiguated rather than treated as storage synonyms.
Compound senses such as 胸倉 "collar" and お倉入り "shelving" do not
automatically become direct character glosses. The shared dictionary head
くら's contextual historical money-broker, source-of-income, shelving,
abbreviation and trade-numeral senses are recorded without converting 倉
into a generic money, clothing, cancellation or number character.

The three curated choices 金 / 全 / 合 are broad-top shape comparisons
with different money, completeness and joining labels. The finite packet
checks both prompt/label directions and the mutual choice labels. A
treasury's contents do not make a granary a synonym of gold/money.
No guard is inferred transitively from an older card.

## Geometry, code points, fonts and preserved attempts

Ten strokes are generated by the exact pinned converter and canonical
KanjiVG `05009.svg`; the SVG's Git blob and SHA-256 are checked. Geometry
was never hand-edited. The second producer regenerates in memory and checks
byte equality with the first output without overwriting it.

The mnemonic is expressly non-etymological; historical classification and
phonetic analysis are not claimed. 人 (U+4EBA) is the indexed radical;
口 (U+53E3) is only a modern shape cue. 倉 (U+5009), 人 and 口 are present
in all three actual bundled font cmaps. Contrast-only 宀 (U+5B80), explicitly
not this character's radical/component, is absent from all three subsets.
System fallback is not rendered/device acceptance.

The original generation attempt wrongly asserted coverage for all four
queried glyphs and failed at its final assertion after generating the valid
stroke file. Its unchanged producer, memory receipt and diagnostic are
retained. Attempt 002 reports the actual missing contrast glyph instead of
claiming coverage. It does not change app fonts or remove the distinction.

`author-gates-001` passed all exit-code gates but retained seven quiz-safety
warnings about exclusions not named in Notes. The Notes now explain all
eleven pairs. `author-gates-002` had zero scoped lint or quiz-safety warnings.
The coordinator then identified an inherited exceptional-cleanup risk:
individual waits were at most 0.1 seconds, but the post-kill retry loop
lacked an aggregate deadline. Executed helper sources remain preserved in
`pre-cleanup-fix-001`. B127 helpers now use bounded 10-second deadlines per
terminate/kill stage and retain cleanup errors in receipts. Focused
synthetic-child checks cover that correction; `author-gates-003` reruns all
ten gates with the corrected helpers and is the final author-gate set.
No earlier log or report was overwritten.
Unittest retry/429 lines are fixture output; 431 tests passed. Vocabulary
coverage remains the existing 2,122/2,431 reviewed prompts at pilot stage;
the successful vocabulary command is not full vocabulary closure.

The first finalization attempt passed all complete-source comparisons but
failed when a default Windows cp1252 read tried to decode the UTF-8
quiz-safety log. Its original producer, exact exception/context record and
memory receipt are retained. The corrected attempt uses explicit UTF-8
and rechecks the existing identical source-verification report without
overwriting it; no runtime content changed because of that read failure.

## Boundaries

All commands are serial and admitted above 2 GiB free with the pinned
0.25-second monitor, 1 GiB abort threshold and at-most-0.1-second child waits.
Receipts report the verifier's own working set, not subprocess memory peaks.
The reading model checks N1, All and Starter plus this one borrowed target,
with 100 seeds per pool; all three have zero positive-reading hits. It does
not prove arbitrary/custom-pool, multiple-borrow, Kotlin/native/device,
independent linguistic, whole-set or publication acceptance.

伯, 憶 and 撲 remain deferred, with their known reading/evidence obstacles;
唇 was considered but not admitted. No new word, app/media change, reviewer
launch, push, publication or next-batch work belongs to this slice.
