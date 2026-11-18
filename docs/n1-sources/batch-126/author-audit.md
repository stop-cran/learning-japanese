# B126 author audit: 傘

## Scope and accounting

Base: `ea9e1e364da4f3421a05d2a9706e5dcf44f0d797`, freshly fetched signed
receipt/main. The verified standalone assignment SHA-256 is
`dded326d4af9789df0cd918a21e32ed8666ce01284440cd69fcbbc08accc6c3c`.
This is authoring only: one new kanji, its generated stroke file and one
link-only change to the existing N5 word. No review, publication, native,
phone, emulator or complete-set acceptance is claimed.

Frozen pending row **70**, 傘, is absent at base. Both raw community membership
and source-index hashes match the freeze; `statusAtFreeze` remains unchanged.
Published accounting remains **255/1228 delivered, 973 undelivered**. This one
unreviewed local draft is not delivery; 972 other members remain outside it.
The six earlier N2 placements are included in 255 and are not relabelled.

The initial simple-reading survey found 伯, 憶 and 撲. 伯母さん and 相撲 do
not establish their respective metadata on readings; neither candidate is
admitted. B120's preliminary 憶 row 395 remains deferred, not safe or delivered.
The broader survey established existing support for 傘, but did not admit its
other candidates. The one-card bound is intentional, not a fifteen-card quota.

## Complete sources and reading decisions

`source-receipt.json` binds the compressed and fully decompressed dictionary
inputs, raw membership bytes, original SVG identity, and output hashes.
The XML files preserve **all 56 complete JMdict families containing 傘 in
any written form**, the complete KANJIDIC2 character record, and complete
comparison records. They are parsed/reserialized XML, not raw slices of the
compressed inputs. No field, spelling, reading, sense restriction or priority
tag was removed to simplify the lesson. Absent priority flags prove no rarity.

The full KANJIDIC2 record gives 人/9, 12 strokes, grade 8, on `[サン]`,
kun `[かさ]`, no nanori, and English meaning "umbrella." Source order is
preserved. The source's historical JLPT field is not substituted for the
frozen community membership policy.

| Source reading or word | Evidence and disposition |
| --- | --- |
| サン | Complete JMdict 1301960 傘下/さんか and 1548660 落下傘/らっかさん support the compound reading. Both are given in the table; neither has an existing dedicated word article. `quizOnyomi: []` keeps this reading in metadata without inventing a linked example or calling it rare. |
| かさ | Complete JMdict 1301940 傘/かさ, sense 1 umbrella/parasol, agrees with the existing article's identity, N5 level, reading and usage. The only selected kun prompt has that exact relative word link. |
| がさ | 1464080 日傘/ひがさ and 1586610 雨傘/あまがさ support contextual voicing. This is not a new independent metadata reading. |
| からかさ | Complete 1774770 permits the single spelling 傘 alongside から傘 and 唐傘. It is not marked search-only, name-only or rare there. The card explicitly acknowledges it as a valid separate whole-word reading and supplies it positively to the bounded exposure check. It is not inserted into or used to reorder frozen KANJIDIC2 metadata. |
| 1301940 sense 2 | Lampshade, mushroom cap and umbrella/conical-hat-shaped objects are positive secondary senses, retained and discussed. They are not dismissed by a standard-list or frequency argument. |
| 傘下 affiliation/jurisdiction | These are meanings of the whole compound, not independent character glosses for "govern" or "control." |

All 56 families were inspected, including their later senses and restrictions.
The packet retains, rather than silently promoting, 1774770's alternate spelling,
1572100's script-dependent reading restrictions, 1400940 and 2714020's search-only
spellings, 1604120's rare 松傘 spelling, and the no-kanji kana readings in
2263470, 2536360, 2595710, 2595750 and 2792660. Specialized shelterwood,
biological, broadcast, political, festival and legendary compound senses stay
with their complete words; they are not character-level practice prompts.
2863745 explicitly marks its sunshade term rare and its attendant use archaic;
those flags do not transfer to unrelated families. No new example sentence,
historical formation, verified phonetic claim or unsupported rarity assertion
is introduced.

## Actual baseline comparison scan

`baseline-gloss-scan.json` is the first actual 1,245-card scan, including every
baseline title, full KANJIDIC2 English meanings, per-card raw hash and matched
tokens. It is preserved unchanged. `baseline-gloss-scan-002.json` extends it to
**all content words in every single-spelling 傘 JMdict sense**, including
shade/cap/hat and paper/bamboo, plus declared semantic expansions. Only the
explicitly listed function words are ignored. Both actual outputs, not merely
this disposition table, are retained. The second scan has nine matches.
Whole-compound affiliation and parachute senses are not promoted to the glyph.
The complete baseline cards of all nine matches and all three distractors are
retained and were read, including secondary readings and body comparisons.

| Direct pair | Disposition against the actual labels and source senses |
| --- | --- |
| 傘 / 被 (`cover; incur`) | **Guard.** The broad cover/shelter label can be accepted for an umbrella or lampshade considered as a protective covering. Conservative direct broad-label protection, not universal synonymy, verb interchangeability or transitive propagation. |
| 傘 / 包 (`wrap; enclose`) | No guard. Wrapping/enclosing and the source cover/conceal verbs do not name an umbrella, parasol or lampshade. Conversely "umbrella; parasol" does not label 包. Functional association alone is insufficient. |
| 傘 / 帽 (`hat; headgear`) | No guard. JMdict's "something shaped like ... a conical hat" is a shape comparison, not a claim that the character names ordinary wearable headgear. Mushroom cap is an English cap polysemy, not the displayed headgear label. 帽's source-only おお.う does not make it an umbrella. |
| 傘 / 暗 (`dark`) | No guard. KANJIDIC2's "shade" concerns darkness; the secondary native noun is a physical lampshade, not darkness or becoming dark. Neither displayed label answers the other. |
| 傘 / 灯 (`lamp; lamplight`) | No guard. A lampshade is a part/cover, not the lamp or illumination itself. Do not equate part and whole. |
| 傘 / 札 (`tag; banknote`) | No guard. "Paper money" shares the material token with paper umbrella, not the referent or either answer label. |
| 傘 / 紙 (`paper`) | No guard. A paper umbrella is a manufactured object, not the material in general; parasols need not be paper. Neither label is the other's meaning. |
| 傘 / 竹 (`bamboo`) | No guard. Bamboo can be a frame material; a whole paper/bamboo umbrella is not bamboo as a plant or material. |
| 傘 / 笹 (`bamboo grass`) | No guard. The smaller-bamboo plant label is neither umbrella nor parasol. A material/shape association is not a direct synonymous sense. |

No baseline card shares the literal KANJIDIC2 gloss token "umbrella."
The expansion intentionally catches English polysemy and part/material
relationships instead of treating them as automatic exclusions. This bounded
corpus scan does not establish exhaustive semantic discovery.

## Three curated wrong choices, both directions

| Choice | Full card / source inspection and direction checks |
| --- | --- |
| 金 (`gold, money`) | Similar broad top and center. KANJIDIC2 English gold and the existing card's metal/money uses do not mean umbrella; an umbrella is not gold, money or metal as a character meaning. Its material could contain metal, but that is not synonymy. |
| 全 (`whole; complete`) | Broad top over a compact lower stack, versus 傘's four inner person-like shapes and central stem. Whole/entire/all/complete/fulfill do not mean umbrella; umbrella/parasol does not answer 全. |
| 合 (`fit together`) | Broad top over 一/口, not four inner shapes and 十. Fit/suit/join and the source measurement gloss 0.1 do not name an umbrella; an umbrella's parts fitting together is not the meaning of 傘. Conversely umbrella/parasol does not answer 合. |

None of the curated cards is excluded against the target or one another.
These ordinary semantic exclusions, not title inequality alone, support the
default four-choice group. Reading pools still require their separate host
check; a meaning comparison is not a reading guarantee.

## Support and preservation

The full active word metadata scan finds exactly **one declaring article**,
`words/傘.md`, with primary reading かさ and independently sourced N5 level.
The frozen candidate record and current metadata agree. The required reciprocal
pair is 傘 word -> 傘 kanji and 傘 kanji -> 傘 word; both are explicit links.
The one word edit wraps the character at its substantive meaning introduction.
The single-component section has no literal character to wrap, so its prose is
left intact rather than inserting one. Removing precisely that link reproduces the baseline bytes after
the documented runtime LF normalization. IDs, all metadata, title, example
sentences, original exclusions and other prose remain unchanged.

A separate bounded literal search found incidental umbrella examples in 16
other existing files (including 雨傘 in 雨 and 傘の骨 in 骨). They do not declare
傘 as a constituent of their own word identity and contain no stale claim
that a 傘 card is absent. They require no reciprocal wrappers. The support
relationship audit is not restricted to the convenient linked example.

## Strokes, components, fonts and limits

The pinned KanjiVG canonical SVG is verified by its frozen Git blob and byte
count. The pinned converter generates all 12 strokes; no geometry is hand-edited.
KanjiVG groups the broad top as a variant 人, four inner 人-like shapes and a
十-shaped crossing. The learner-facing description is explicitly a modern-shape
mnemonic, not etymology; no phonetic component is asserted.

`stroke-font-evidence.json` binds the converter, SVG, output and the three actual
Android bundled font files. New display code points are 傘 U+5098, 人 U+4EBA
and 十 U+5341. The cmap check is bounded font availability evidence only,
not actual native or physical-device rendering, drawing recognition or visual
acceptance. No app, media, fonts, old deck or source-freeze file is changed.

All ten serial author and committed host gates, exact logs and resource receipts
are kept in new scratch-126 directories and bound in the bounded handoff.
Manifest reproduction and full baseline runtime preservation must bind to the
final signed direct child, not merely the authoring tree. Host reading checks
include the positively supplied からかさ reading; metadata-only scanning is
not substituted for that check. These gates do not establish arbitrary/custom
pools, multiple borrowed cards, Kotlin execution, native/device, independent
linguistic review, whole-set acceptance, CI or exact served-ZIP publication.
