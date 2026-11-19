# Blind review — batch 143 (initial, reviewer 1)

Reviewer model: Claude (Anthropic model family), working alone and read-only.

## Snapshot

- Commit: `6b5934e71945ed215cf57a8291117762e67b1d9e` (batch 143)
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-143-6b5934e7` (packet-manifest.json sha256 `0958b56bb788c25212c320adad22f17d9155108c276d84728e933a9df16a331b`, as stated by the owner; I did not recompute it)
- Cards under review: 施 旋 旗 既 旦 旨 暑 暦 朗 条 架 柄 染 株 桜

## Scope

Unit reviewed: the 15 new cards in `snapshot\kanji\`, the 15 files in `snapshot\strokes\`, and the 17 modified word articles (via `diffs\`, plus full text where needed).

Packet files I opened:

| File | Read |
| --- | --- |
| INSTRUCTIONS.md | full |
| mechanical-checks.md | full |
| evidence\source-metadata.json | full |
| evidence\joyo-pages.md | full (front matter pp. 2-3 and every cited page) |
| evidence\daijisen-heads.txt | full |
| evidence\kanjipedia-outside-readings.json | full |
| evidence\public-source\ (listing) and weblio-施, 旋, 旗, 既, 旦, 旨, 暑, 暦, 朗, 条, 架, 柄, 染, 株, 桜 .txt | full (all 15) |
| evidence\jmdict-digest.tsv | part (header and first rows only, to learn the format) |
| evidence\jmdict-families.xml | parsed in full with a script; I printed only targeted entries (about 150 entries: every example word on every card, plus all family entries for 旦, the 旋 めぐ- readings, the 朗 あき- readings, the 暦 りゃく readings, the 株 くい/しゅ readings, 架 たな, and 施 し-く) |
| evidence\audits\reading-exposure.txt | part (every "unlisted readings attested" and "attested reading … offered by" line, the summary lines and the last 12 lines) |
| snapshot\kanji\*.md (15 cards) | full, each read at least twice |
| snapshot\strokes\*.json (15 files) | full (parsed: the `kanji`, `source`, `strokeCount` and `strokes` fields) |
| snapshot\words\柄.md | full |
| snapshot\words\株.md | part (lines 1-22) |
| snapshot\words\西暦.md | full |
| diffs\ (all 17) | full |
| titles\kanji-titles.tsv | part (header, line count, and lookups of about 60 kanji) |
| titles\word-titles.tsv | part (header and lookups of 一旦, 旗, 柄, 株, 桜, 西暦) |
| repo\docs\content-format.md | part (headings and lines 86-154: card format, distractors, exclusions) |

Not opened: evidence\kanjidic2-records.xml (I relied on source-metadata.json and the reading-exposure audit for KANJIDIC2 data), evidence\audits\quiz-safety.txt, evidence\audits\reading-options.txt, evidence\okurigana-scan.txt, evidence\app-code\, rubric files, and any other repo\ file.

Public web: I used one web search that returned the Agency for Cultural Affairs pages for the Joyo kanji table's "how to read the table" section (bunka.go.jp). Everything else came from the packet's frozen Weblio/Daijisen extracts and JMdict data.

## Verdicts

| Facet | Overall | Per card where it differs |
| --- | --- | --- |
| 1 Correctness | NEEDS FIX | NEEDS FIX: 既, 朗 (C1); 桜 (C2, C3); 染 (C4); 旨 (C5); 株 (C6). CLEAN: 施, 旋, 旗, 旦, 暑, 暦, 条, 架, 柄 |
| 2 Scoped coverage | CLEAN | All 15 cards account for every metadata reading. No important common family word is wrongly omitted. |
| 3 Consistency and quiz safety | CLEAN with one minor fix | NEEDS FIX (minor): 旗 (C7). All other cards CLEAN. Links, grades, tags, strokes and section order are correct. Exclusions are direct pairs, not cliques. The reading audit's accounting is correct. |
| 4 Comprehensibility | NEEDS FIX (minor) | 旦 (C8), 柄 (C9). Others CLEAN. Some cards have only optional polish. |
| Word diffs (17) | CLEAN | 16 diffs are pure one-line link wraps to the right card. 西暦 is the declared remark edit, and the passage reads correctly. |

What I verified mechanically:
- Front matter matches source-metadata.json for strokes, radical, radical number, grade, on and kun lists, and quiz subsets on all 15 cards.
- Grade tags: 旗 4; 暑 3; 条 and 桜 5; 朗, 染 and 株 6; the rest grade-8.
- All 15 stroke files have `strokes` and `strokeCount` matching the card's stroke count: 9, 11, 14, 10, 5, 6, 12, 14, 10, 7, 9, 9, 9, 10, 10. All come from KanjiVG at the same revision.
- Every quizzed reading has a linked word article: 施 実施; 旋 凱旋; 旗 旗; 既 既に; 旦 一旦; 旨 要旨; 暑 暑い and 蒸し暑い; 暦 西暦; 朗 朗らか; 条 条件; 架 架空; 柄 柄 (がら and え); 染 伝染 and 汚染; 株 株; 桜 桜.

## Findings

### C1 — minor — facet 1 — 既.md:38 and 朗.md:43
**Claim:** 既.md:38 says the Joyo table "prints 既 in parentheses as a compatibility ideograph, not as a historical form". 朗.md:43 says it "prints 朗 in parentheses; it is a compatibility ideograph, not an older form".

**Why it is wrong:** The table's own instructions (表の見方 item 6) say: 「丸括弧に入れて添えたものは，いわゆる康熙字典体である。これは，明治以来行われてきた活字の字体とのつながりを示すために参考として添えた」. The bracketed forms are the traditional Kangxi-dictionary forms. In the PDF text layer they happen to be encoded with CJK Compatibility Ideographs (U+FA42 既, U+F929 朗), but that is an encoding artifact, not what the table prints or means.

**Impact:** The two cards tell learners the opposite of what the table says. They also conflict with 暦.md:39 ("曆 … genuine older form"), 条.md:49 ("條 … older form") and 桜.md:39 ("櫻 as the older form").

**Remedy:** Say that the table adds the traditional (Kangxi-dictionary) form in parentheses. Or drop the sentence.

**Evidence:** The Agency for Cultural Affairs pages for the Joyo kanji table (bunka.go.jp; the 2010 PDF's "how to read the table" section, item 6). That item sits on a front-matter page outside the packet's pp. 2-3 extract.

**Confidence:** high.

### C2 — minor — facet 1 — 桜.md:37
**Claim:** After naming 桜桃 and 桜ん坊 さくらんぼ, the card says "the reading belongs to the whole word, not to one kanji. Do not infer the reading オウ or さくら for 桜 from this unrelated whole-word reading."

**Why it is wrong:** That is true for the jukujikun spelling 桜桃 = さくらんぼ. It is false for 桜ん坊, where 桜 is plainly さくら + ん + 坊 (ぼう/ぼ). The word is not "unrelated" either: it is literally "cherry's boy", the cherry fruit.

**Impact:** The card tells learners not to see the card's own quizzed reading さくら in a transparent everyday word.

**Remedy:** Limit the whole-word caveat to 桜桃 read さくらんぼ. Say that in 桜ん坊, 桜 is さくら.

**Evidence:** JMdict 1298460 (桜ん坊, 桜桃 | さくらんぼ, さくらんぼう; usually written in kana); Daijisen 難読 桜桃(さくらんぼ).

**Confidence:** high.

### C3 — minor — facet 1 — 桜.md:25
**Claim:** Daijisen's second オウ sense is "the mizaru cherry".

**Why it is wrong:** Daijisen says ミザクラ (実桜, mizakura, the fruit-bearing cherry). "Mizaru" is not a cherry name; it reads like 見ざる.

**Remedy:** Write "the fruit cherry (ミザクラ, mizakura)".

**Evidence:** evidence\public-source\weblio-桜.txt: 「２ 木の名。ミザクラ。「桜桃(おうとう)」」.

**Confidence:** high.

### C4 — minor — facet 1 — 染.md:34 and 染.md:40, against 染.md:42
**Claim:** The ゼン row and the paragraph call 愛染 あいぜん "a whole-word reading, not split here". They say its reading "does not establish an independent reading for 染". Line 42 then says ゼン "is recorded by Digital Daijisen".

**Why it is wrong:** Daijisen gives 染 the on readings セン（慣） and ゼン（漢）. ゼン is the kan'on, and Kanjipedia also lists ゼン outside the table. 愛染 is ordinary アイ + ゼン. The card contradicts itself and the sources. ゼン is not in this card's KANJIDIC2 metadata, so presenting it as a sourced, non-quizzed reading is fine. Calling 愛染 a non-splittable whole-word reading is not.

**Remedy:** For 愛染 あいぜん, say that 染 is read ゼン (an on reading recorded by Daijisen and Kanjipedia, outside the Joyo table and not quizzed). Delete the "does not establish an independent reading" sentence.

**Evidence:** weblio-染.txt 「［音］セン（慣） ゼン（漢）」; kanjipedia-outside-readings.json (染: ゼン); JMdict 2583650 愛染 あいぜん.

**Confidence:** high.

### C5 — minor — facet 1 — 旨.md:37 and 旨.md:25
**Claim:** Line 37 says JMdict's うまい entry ("Its entry") "also lists 旨味 うまみ as an ateji (phonetic) reading of the whole word, not a reading to split between its kanji."

**Why it is wrong:** 旨味 is not in the うまい entry (1310460). It is a separate entry (1310520: 旨み, 旨味 {ateji}, うま味). The ateji tag marks 味 used phonetically for the suffix み. 旨 itself still writes うま in 旨味, exactly as in 旨み.

**Related problem:** Line 25 presents うま.い as "'delicious; tasty' as well as 'skillful; skilful; skilled'". JMdict marks the skillful sense "esp. 上手い, 巧い" and the delicious and good-deal senses "esp. 旨い". As written, the card implies 旨い is the spelling for "skillful".

**Remedy:** Cite 1310520 as its own entry and drop "not a reading to split". Say that the skillful sense is normally spelled 上手い or 巧い.

**Evidence:** jmdict-families.xml entries 1310460 and 1310520.

**Confidence:** high.

### C6 — minor — facet 1 — 株.md:25 (and the echo at 株.md:36)
**Claim:** "守株 しゅしゅ is a word-level reading … do not split that whole-word reading among the characters."

**Why it is wrong:** 守株 is transparently シュ (守) + シュ (株). It is the stump-guarding fable, the same story JMdict cites for 株を守る くいぜをまもる. It is actually the best example of the シュ "stump" sense the card is explaining, so telling learners not to split it is wrong.

**Remedy:** Present 守株 as 守 シュ + 株 シュ, the "guarding the stump" idiom. Optionally mention 株を守る くいぜをまもる.

**Evidence:** JMdict 1882040 守株 しゅしゅ; 2834654 株を守る (from a fable in the Han Feizi; "to guard the tree stub"); weblio-株.txt 〈シュ〉１ 木の切りかぶ。くいぜ。「守株」.

**Confidence:** high.

### C7 — minor — facet 3 — 旗.md:3 (title "flag; banner; standard")
**Claim:** The title shares the word "standard" with three existing titles that are not excluded: 準 "standard, conform", 範 "model; standard" and 規 "standard; rule".

**Impact:** For a learner at about N5-N4 English, "standard" reads as "norm", not "banner". If 旗 is drawn as a fallback wrong option on a 準, 範 or 規 prompt, two options contain "standard", and the 旗 option can be defended from the title text alone. The card's other title words (flag, banner) already carry the meaning. JMdict glosses 旗 only as "flag"; KANJIDIC2's "standard" is the banner sense.

**Remedy:** Drop "standard" from the title (for example "flag; banner"), or exclude 準, 範 and 規.

**Note:** I did not open quiz-safety.txt, so I cannot say whether the current pools ever draw this pair. Severity is minor because the curated distractors (施, 旋, 旅) fill all slots on the 旗 prompt itself.

**Evidence:** titles\kanji-titles.tsv; 旗.md:14 (exclusions are only 標 and 印).

**Confidence:** medium.

### C8 — minor — facet 4 — 旦.md:25 and 旦.md:52
**Claim:** "it does not support a new reading in 一旦 or another ordinary JMdict word" (line 25) and "do not treat it as support for splitting the reading into 一旦" (line 52).

**Why it is a problem:** Both sentences are garbled. The intended point is that Kanjipedia's outside-table あした has no ordinary JMdict word written with 旦 and has nothing to do with 一旦 (which is いっ + タン). As written, a learner may think 一旦 hides an あした reading.

**Remedy:** State plainly: "Kanjipedia also lists あした (morning) outside the official table; no ordinary word in JMdict uses it, and 一旦 is read いっ + タン."

**Related:** 旦.md:41 writes "the reading is ダンナ" in katakana while everything else uses だんな (ダンナ is only a search-only form in JMdict).

**Confidence:** high.

### C9 — minor — facet 4 — 柄.md:48 (Common words)
**Claim:** "[柄](../words/柄.md) え — handle; pattern".

**Why it is a problem:** It pairs the reading え with "pattern". The card itself insists (lines 23 and 42) that え is the handle and がら is the pattern. The line copies the existing word article's title "handle; pattern", but pinning it to え contradicts the card on the one point it stresses.

**Remedy:** Write "柄 え / がら — handle (え); pattern (がら)", or list the two readings separately.

**Confidence:** high.

## Optional

- **O1 条.md:45.** The すじ row opens with "muscle; tendon; sinew". JMdict does not restrict those senses away from 条, but Daijisen marks 条 for すじ as outside the table (すじ【筋/▽条】), and 条 is in practice the spelling for lines and stripes (条播き すじまき). Leading with "line; stripe; streak" would mislead less.
- **O2 条.md:58.** 未 and 末 are 木 plus an added horizontal stroke, not "a changed upper stroke". 条.md:61 is a dense jargon paragraph (gikun, jukujikun, hard-to-read form) that an N5-N4 reader will not need; consider cutting it to one sentence about 発条 ばね.
- **O3 架.md:25.** "a supported platform or shelf, as in 架 か" is presented as Daijisen's example, but the Daijisen extract gives 架蔵, 画架, 開架, 銃架, 書架, 担架 and 十字架. The standalone noun 架 か "rack; mount; stand" comes from JMdict 1919060. Attribute it to JMdict, or use 書架 or 担架 as the Daijisen example.
- **O4 朗.md:51.** "These three cards supply the distractors" follows a sentence that names 良, 月, 有 and 朝. A reader could take 良 for a distractor; the actual distractors are 月, 有 and 朝. Name them explicitly.
- **O5 株.md:42 and 柄.md:48.** Both copy existing word-article titles ("stock share; stump"; "handle; pattern"). The word articles are out of scope, but "stock share" is odd English for a card's Common words line.
- **O6 施 title "carry out; give; alms".** It shares "carry" with 運 "carry; luck" and 提 "carry in hand", and "give" with 返 "give back; repay" and 産 "give birth". The phrasal meanings differ clearly enough that I do not consider any of these defensible as correct answers. Other shared words I judged harmless: 暑 with 候, 寒 and 曇 ("weather") and with 旬, 春 and 節 ("season"); 条 with 弧 ("line"); 株 with 挿, 植, 稲 and 苗 ("plant"); 桜 with the specific tree names 幹, 松, 桂, 梓, 梨, 椋 and 楠 ("tree"). No change needed. The same goes for the weak-overlap exclusions listed in lead (l): each is a direct one-to-one overlap with one sense of the title (for example 株 with 桜 through "rooted plant" and "tree"). None is a transitive clique, and over-exclusion only narrows the pools.
- **O7 株 シュ coverage.** 菌株 きんしゅ/きんかぶ ("(bacterial) strain") is a modern シュ word that may be more recognisable than 雌雄異株. JMdict reads the plain 変異株 as へんいかぶ, so do not use that one.
- **O8 朗 name readings あき and お.** The card need not mention them. They are KANJIDIC2 name-only readings, and the audit shows they are not drawable in any pool.

**Leads I checked and found no defect:**
- (a) 施/旋/旗 curation in both directions.
- (b) 既's accounts of 既成, 皆既 and すんでに. JMdict 2860958 marks 既に {rarely used kanji form}, read すんでに, glossed "almost; nearly".
- (c) 旦: 一旦 (JMdict usually kana, archaic "one morning"), 元旦 (sense 2 "orig. meaning"), 旦那 (檀那 rarely used), 旦つく "husband"; the title is excluded against 朝.
- (d) 日 早 者 as distractors for both 旨 and 暑.
- (e) 暦: 延暦 えんりゃく for リャク; 暦数 gloss; the 西暦 edit.
- (g) 条: Daijisen gives only ジョウ (デウ, go'on) with すじ as kun and え, えだ and なが as name readings, which matches the card's チョウ and えだ statements.
- (h) 架: 架空 かくう/がくう restriction; 架ける "usually kana, sometimes 掛ける"; 懸かる and 懸る rarely used kanji forms; 掛ける/懸ける usually kana; 賭ける not tagged. The 掛け, 懸け and 賭け part-of-run matches are just the Joyo ⇔ notes.
- (i) 柄: 横柄 is in the Joyo table under ヘイ; え and つか are standalone JMdict entries (1508290, 1508310); 木 本 休 are plausible but wrong; 休 has 木 at the right.
- (j) 染: usually-kana tags on 染みる and 染み and none on 染める and 染まる; じみる is correctly described; the 染め and 抜き matches are Joyo examples.
- (k) 雌雄異株 しゆういしゅ under シュ; くい and くいぜ (JMdict 1279450, 2645440).
- (n) The reading-exposure count is right: 旋 せ ×1, 朗 あき and お ×2, 柄 ら, いきおい and つく × 2 prompts = 6, 桜 さ ×1, total 10. There are 0 production, padded or one-holder hits, so no attested reading is drawable as a wrong option in the shipped pools.

## Limits

- **Tool calls:** I made exactly one tool call per response and no parallel calls. One command produced more output than the tool returns inline, so the harness saved it to a temporary file. I did not open that file; I re-ran a narrower query instead.
- **Files not opened:** evidence\kanjidic2-records.xml, quiz-safety.txt, reading-options.txt, okurigana-scan.txt and app-code. KANJIDIC2 facts rest on source-metadata.json and the reading-exposure audit. C7's real-world drawability is therefore unverified.
- **Daijisen:** claims rest on the packet's frozen Weblio extracts. I did not re-fetch live pages, except for the one Joyo front-matter search used for C1. I accepted the 暦 Daijisen paraphrase ("…or one's fortune") on the extract I read earlier; my notes recorded it as matching.
- **凱旋 diff:** it shows doubled line spacing. I took this to be the file's existing line endings, not a batch change, because the changed content line is a pure link wrap.
- **Lint warnings:** the four "Dictionary: line cites no JMdict entry id" warnings are not defects as far as I saw. In 西暦.md the entry id 1381140 is on the next line of the same Dictionary: paragraph.
- **Interpretation:** I took "listed in metadata" to mean the card's front-matter on and kun lists. ゼン and the 株 くい/くいぜ readings are not in those lists, so I judged them as optional, sourced extras.
