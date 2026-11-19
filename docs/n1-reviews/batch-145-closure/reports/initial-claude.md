# Batch 145 blind review: initial-claude

## Snapshot

- Commit: 845aefbb37e40aeb737f32de8066959968cc2cf6 (batch 145; new kanji cards 湧 源 滅 滑 滞 漫 漬 潔 潜 澄 濁 瀬 災 炎 為).
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-145-845aefbb` (packet-manifest.json sha256 78b790f2d213e6de96ddb144054b6498864ea40caacb80cb8ae406579a96bd09, as given in the assignment; I did not re-hash it).
- Reviewer: Claude, a model by Anthropic. The exact model version string is not exposed to me. I am the first of two blind reviewers. I worked read-only and alone, with no sub-agents.

## Scope

Unit reviewed: the 15 new cards in `snapshot\kanji\`, the 15 files in `snapshot\strokes\`, the 22 diffs in `diffs\` (20 word-article link-wraps, plus the remark edits on 渋 and 暑), and the changed lines of 渋.md and 暑.md together with the passages around them.

Packet files opened:

| File | Extent |
| --- | --- |
| INSTRUCTIONS.md | full |
| Packet top level and its direct subfolders | non-recursive listings only |
| mechanical-checks.md | full (as truncated by the packet) |
| evidence\joyo-pages.md | full |
| evidence\source-metadata.json | full |
| evidence\public-source\weblio-*.txt (one per new kanji) | full |
| evidence\daijisen-heads.txt | full |
| evidence\kanjipedia-outside-readings.json | full |
| evidence\jmdict-families.xml | part: about 130 entries pulled out by ent_seq, covering every JMdict id cited by the 15 cards plus a few extra (源氏, 浪漫 and others) |
| evidence\jmdict-digest.tsv | part: grep by kanji and id (瀬, 漫, 潜, 為, 漬, 澄, 濁 and others) |
| evidence\kanjidic2-records.xml | full, read through a script that summarises readings, nanori, strokes, grade and radical for each record |
| evidence\app-code\ | part: grep for exclusion handling (QuizBuilder.kt, line 26 area); KanjiReadings.kt lines 1-160 |
| evidence\audits\reading-exposure.txt | part: every "attested reading" line plus the last lines |
| evidence\audits\reading-options.txt | part: command line, plus the blocks for 滅, 漫, 炎 and 為 and the HIT lines |
| snapshot\kanji\ 湧 源 滅 滑 滞 漫 漬 潔 潜 澄 濁 瀬 災 炎 為 | full |
| snapshot\kanji\渋.md and 暑.md | part: front matter and the full Notes section |
| snapshot\strokes\*.json (15 files) | all parsed for keys and stroke count; first 600 characters of 災.json read directly |
| diffs\ (22 files) | all changed lines |
| titles\kanji-titles.tsv | part: script lookups of about 120 quoted titles, plus a shared-English-word scan of the title column |
| repo\kanji\ 海 水 火 日 川 黒 魚 | first 16 lines (front matter) |
| repo\docs\content-format.md | heading grep, plus lines 86-154 (Kanji card, Quiz authoring, Curated reading questions) |

Not opened:
- evidence\audits\quiz-safety.txt: the quiz-simulation tail in mechanical-checks.md was sufficient.
- titles\word-titles.tsv
- rubric\, evidence\okurigana-scan.txt and evidence\audits\kanji_remarks.py
- The word articles under snapshot\words\: only their diffs were reviewed, as instructed.

Web: the live Weblio / Digital Daijisen page for 漫 (https://www.weblio.jp/content/漫).

## Verdicts

Overall facet verdicts:

| Facet | Verdict |
| --- | --- |
| 1. Correctness | **Minor defects.** Nine small factual or quotation errors (C1, C3-C10) and one inaccurate declared remark edit (C2). None changes a quizzed reading, a quizzed word or a link target. |
| 2. Scoped coverage | **Pass with one gap.** Every metadata reading has a row or is qualified as source-only. The 為 card never says that the Joyo table gives no kun reading, so the quizzed な.す lies outside the table (C6). |
| 3. Consistency and quiz safety | **Pass, with one cross-card inconsistency.** The 暑 and 炎 cards describe their pair inconsistently (C2). Everything else checked passes: titles are unique; distractors are defensibly wrong in both directions; exclusions are direct pairs; links resolve; stroke counts match; section order follows content-format.md; the reading-audit accounting is right. |
| 4. Comprehensibility | **Pass, with polish items** (see Optional). |

Checks that passed on all 15 cards:
- Front matter matches source-metadata.json and KANJIDIC2 on grade, strokes, classical radical and the on and kun lists, including 漬 -づ.け / -づけ and 漫 みだり.に / そぞ.ろ. The 15 stroke files have strokeCount equal to the card strokes (12, 13, 13, 13, 13, 14, 14, 15, 15, 15, 16, 19, 7, 8, 9).
- Every quizOnyomi / quizKunyomi reading has a row with a linked word.
- Every quoted kanji title I checked (about 120) is exact.
- Every mnemonic is labelled "Modern-shape mnemonic, not etymology". The component statements are true: 巛 + 火 in 災 (3 + 4 = 7); 糸 at the bottom of 潔; 虫 at the bottom of 濁 and at the right of 触; the 頼 right-hand part in 瀬; two 火 in 炎; 灬 at the bottom of 為, 黒 and 魚.

Per-card verdicts (facets 1 / 2 / 3 / 4) and judgements on the leads:

- **湧:** pass / pass / pass / pass.
  - (a) 湧く's four senses, 湧水 (formal or literary), 湧出 (ゆうしゅつ and ようしゅつ) and the rarely-used 涌く are all correct.
  - Joyo p.150 and Daijisen ユウ(呉) ヨウ(漢) match the card.
  - 港 濃 漁 are visual 氵 options with no meaning overlap; the exclusions are direct overlaps.
- **源:** pass / pass / pass / pass.
  - (b) 資源, 源 みなもと (two senses), 源氏 (sense 2, "the Minamoto family"), 源流, 水源, 語源 and the suffix げん are all verified.
  - Daijisen's みなもと note is reported as a word etymology, not a kanji etymology. Joyo p.49 matches.
  - 源 does not list 湧, but 湧 lists 源, and the pair is excluded symmetrically.
- **滅:** pass / pass / pass / pass.
  - (c) All JMdict tags are verified: 滅多に ateji, 滅茶 ateji, 滅金 rarely used, the 滅ぼす / 亡ぼす forms, 仏滅 and 絶滅.
  - The Starter options 海 水 火 cannot be defended as "perish; destroy; die out", and the reverse direction is also safe.
  - The ベツ latent collision with 別 cannot be drawn (see the reading-audit item below).
- **滑:** pass / pass / pass / pass. (d) 滑る (seven senses), 辷る, 滑らか, ぬめる (2016150), 円滑, 滑稽, 滑走 and 滑降 are verified. See the wording note O6.
- **滞:** pass / pass / pass / pass.
  - (e) 滞在, 渋滞 and 滞る are verified. The テイ row is correctly marked source-only.
  - The lead's "なず.む" is not in KANJIDIC2 or in the card's metadata. It appears only as an extra in the reading-options command line, so it is not a card issue.
  - The 渋 link is correct (see the diffs item below).
- **漫:** facet 1 has minor defects (C1, C3); pass / pass / pass on the other facets.
  - (f) 漫画 (マンガ spec1), 漫歩, 散漫, 爛漫, みだりに "without authority" with all spellings rarely used, 漫ろ and 滑稽 1208660 are verified.
  - The Starter options 海 水 日 are safe.
- **漬:** facet 1 has a minor defect (C8); pass / pass / pass on the other facets.
  - (g) The stagk on sense 2 of 漬ける, 漬かる with 浸かる spec1, 塩漬け, 茶漬け, the 粕漬 spellings, 浸漬 (しんし / しんせき) and 漬す (rarely used under 浸す) are verified. Joyo p.112 matches.
- **潔:** pass / pass / pass / pass.
  - (h) 不潔, 清潔, 潔白, 潔癖, 潔斎, 簡潔, 純潔 and 高潔 are verified. 潔い's three senses, with the dated and archaic tags and the search-only forms, are verified.
  - 漁 溶 渡 are safe. The exclusions are direct.
- **潜:** facet 1 has a minor defect (C9); pass / pass / pass on the other facets.
  - (i) もぐる (three senses, むぐる obsolete), くぐる (four kana-usually senses with the xref), 潜む (out-dated 潛む / 濳む), 潜める, 潜り込む, 地下に潜る, 潜伏, 潜在的 and 潜航 are verified.
  - かく.れる is correctly source-only: the only JMdict hit, 隠れ潜む, reads 潜 as ひそ.
- **澄:** pass / pass / pass / pass.
  - (j) 澄む (four senses; 清む), 澄ます (four senses; 清ます), 聞き澄ます, 研ぎ澄ます, 上澄み (irregular-okurigana 上澄), 澄まし顔, 清澄, 澄明 and 明澄 are verified.
  - Joyo p.110 matches. The name readings すみ and み are latent collisions only (see below).
- **濁:** facet 1 has a minor defect (C4); pass / pass / pass on the other facets.
  - (k) All 15 JMdict entries are verified, including 濁世 (three readings), 五濁, 濁酒 どぶろく / だくしゅ and 濁声.
  - "voiced" is a real sense: 濁る sense 4, 濁音 and 濁点. It is guarded by the exclusions of 音 and 声.
  - 触 湯 渡 are safe.
- **瀬:** pass / pass (see O4) / pass / pass.
  - (l) 瀬 (four senses), 瀬戸物 (two senses, "orig. meaning"), 瀬戸, 浅瀬, 川瀬, 早瀬, 立つ瀬 ("usu. as 〜がない") and 瀬戸際 are verified.
  - ライ is correctly source-only, and Joyo p.89 matches.
  - 滝 "waterfall; rapids" and 位 "rank; position" share a title word with 瀬 and are both excluded.
- **災:** facet 1 has minor defects (C7, C10); pass / pass / pass on the other facets.
  - (m) 火災, 災難, 災い (禍; 殃 rarely used), 災害, 災厄, 震災, 天災 and 人災 are verified.
  - 巡 炊 灰 are safe.
- **炎:** pass / pass / facet 3 shares C2 / pass (see O1).
  - (n) 炎 ほのお / ほむら (two senses), the suffix えん, 胃炎, 肺炎, 炎症, 火炎, 炎上 (colloquial sense), 気炎, 炎天, 炎暑 and 陽炎 (gikun) are verified.
  - 淡 談 炊 are safe.
- **為:** facet 1 has a minor defect (C5, C10); facet 2 has a gap (C6); pass on facet 3; facet 4 is a pass (see O2).
  - (o) 為す 2861111, 為替 1157330 (gikun; かわし obsolete), ため 1157080, 為に, 成る / 為る, する / 為る, 成り / 為り (shogi), 成す (sense 5, "also written as 為す"), 行為, 作為, 人為, 為政者 and 無為 are verified.
  - The 為替 treatment (a whole-word reading, not split) is correct and matches Joyo p.12 and p.103.
  - The 21 exclusions are each tied to a displayed sense of "do; act; for the sake of" or to an ordinary secondary sense of ため ("cause; reason", "purpose"). They are direct pairs, not a transitive clique. 幕 is needed because it shares the word "act".
  - The Starter options 黒 魚 火 are safe.
- **(p) Shared curated distractors and Starter cards:** none of the shared options (漁, 渡, 溶, 湖, 濃, 港, 湯, 湿, 炊) has a title that could be defended for the target, or the other way round. The Starter cards 海 水 火 日 川 黒 魚 are each named and justified in the card's Notes bullet (a 氵, water, 火 or 灬 resemblance).
- **(q) One-sided exclusions:** 湧/源, 滑/滞, 漫/滑, 漬/潜 and 潔/澄 are fine because the app reads them symmetrically (QuizBuilder; content-format.md, "symmetric but not transitive").
  - Unexcluded shared English words: 漬 "steep" with 険 "steep; perilous", 為 "for the sake of" with 酒 "alcohol; sake", and 瀬 "position" with 就 "take a position; undertake".
  - All three are different senses that no learner could defend as correct. Every other shared word (source, origin, destroy, stay, clean, pure, clear, transparent, cloudy, shallow, rapids, calamity, misfortune, blaze, do, act) is excluded on one side or the other.
- **(r) Reading audits:** the accounting is correct.
  - Every curated option, and every Starter option (which has no quiz list, so all its readings are usable), contributes a reading of the asked kind. So the three curated slots fill for 滅 (メツ: カイ, スイ, カ) and 漫 (マン), and べつ (別) and ばん (万 判 晩 板 満 番 盤) cannot be drawn. The two labelled HITs are therefore latent.
  - For 炎 (ほのお), any fallback slot is filled from the closest tier first, so もえる (燃) and ぬく (抜 温) are not reached.
  - For 為 (な.す) with 黒 魚 火, and for 澄 and 瀬 with all-kun curated options, the latent す / た, すみ / み and せい are not drawable either.
  - I found no attested reading that can be drawn.
  - Side note: the audit's list of attested readings for 漫 includes "すず (card text)", which comes from the error in C1.
- **Diffs:** all 20 word diffs change exactly one line and add exactly one link, to the intended kanji: `../kanji/<kanji>.md` for 潔 ×2, 滞 ×2, 湧, 滅, 滑, 漫, 漬, 潜, 澄, 濁, 瀬, 災 ×2, 炎, 為 ×2, 滅 and 源. No other characters changed.
  - 瀬戸物 now renders as "[瀬]戸 (せと)", which is accurate but splits 瀬戸 visually.
  - The 渋 edit is true: 滞 supplies タイ in 渋滞, and the following sentence still reads correctly.
  - The 暑 edit: see C2.

## Findings

Established defects, most consequential first.

**C2 (correctness and consistency, 暑 declared remark edit and 炎 Notes): "[炎](炎.md), “flame,” was checked; it names fire rather than weather heat" is not true as stated, and it disagrees with the 炎 card.**
- 炎 does name weather heat in ordinary words:
  - 炎天 えんてん, JMdict 1177140 "blazing heat; scorching sun", which is one of the Joyo table's own three examples for エン (p.16);
  - 炎暑 えんしょ, JMdict 1177090 "heat wave; intense heat";
  - Daijisen's sense "burning hot", which the new 炎 card itself lists.
- The new 炎 card excludes 暑 precisely because "熱 … 暑 … overlap heat, which is the sense of 炎暑 and 炎天". It then paraphrases the 暑 card as saying "炎 names fire rather than weather heat".
- The 暑 sentence also follows "These cards are excluded as meaning choices". This implies 炎 was checked and left unexcluded, but the app excludes the 暑/炎 pair through 炎's declaration.
- The link target is right, and "flame" is a valid KANJIDIC2 meaning and JMdict gloss.
- Suggested fix for 暑: "[炎](炎.md), “flame,” names fire, but it also means blazing heat in 炎天 and 炎暑, so the 炎 card keeps 暑 out of its meaning choices." Then adjust the 炎 Notes clause "the 暑 card notes that 炎 names fire rather than weather heat" to match.

**C1 (correctness, 漫 Readings paragraph): "Daijisen's entry also lists すず and そぞろ as kun readings."**
- The live Weblio / Daijisen 漫 page shows ［訓］すずろ そぞろ. "すず" is a fragment of the linked word すずろ in the packet's text extract.
- The card's own JMdict sentence just before this one gives すずろ.
- The wrong form has propagated into the reading-options audit as an attested reading, "すず (card text)".
- Fix: "すずろ and そぞろ".

**C3 (correctness, 漫 Daijisen sense list): "浪漫 ろうまん, JMdict ateji (phonetic) reading …".**
- In JMdict 1147940 the readings are ロマン (gai1), ローマン and ろうまん, and ろうまん is tagged "rarely used kana form".
- A learner will take ろうまん as the word's reading, but the word is normally ロマン, which is in fact why it is "usually written using kana alone".
- Fix: give ロマン as the reading and mention ろうまん only as a rare kana form, or say that 漫 gives マン in ロマン.

**C4 (correctness, 濁 Readings paragraph): "The table gives no ジョク example, though KANJIDIC2 and Kanjipedia list it."**
- Joyo p.104 does not list ジョク at all: its rows are ダク, にごる and にごす only. Kanjipedia marks ジョク as 外, outside the table.
- "No example" implies that ジョク is a table reading that simply lacks an example.
- Fix: "The table does not list ジョク; KANJIDIC2 lists it, and Kanjipedia marks it as outside the table."

**C5 (correctness, 為 Meaning and origin):**
- (i) "JMdict glosses its first sense 'to do; to commit; to carry out; to bring about'". 為す 2861111 has only one sense, so "first" is wrong.
- (ii) "Daijisen also gives the kun readings なす, する, なる and ため for the same doing". Daijisen simply lists ［訓］なす する なる ため. ため is not a "doing" reading, as the card's own next clause and the title's "for the sake of" show.
- Fix: "its sense" in (i), and drop "for the same doing" in (ii).

**C6 (scoped coverage and comprehensibility, 為 Readings paragraph): the card never says that the official Joyo table gives 為 no kun reading.**
- The quizzed な.す, and also ため, する and なる, are therefore all outside the table.
- Kanjipedia marks every kun reading of 為 as 外. Daijisen marks the ため, す and た headwords with ▽.
- The 漫 and 漬 cards state the corresponding fact explicitly ("It lists no kun reading for 漫"; "It lists no on reading for 漬"). For 為 it is more important, because a kun reading outside the table is the only reading quizzed.
- Fix: add "The table lists no kun reading for 為; な.す and the other kun readings are outside the table and are usually written in kana."

**C7 (correctness, 災 Daijisen paragraph): 防災 is quoted as "… protection against disasters".**
- JMdict 1520360 reads "protection against disaster" (singular).
- Fix: correct the quoted gloss.

**C8 (correctness, 漬 Readings paragraph): "漬物 … is JMdict entry 漬け物, with 漬物 and 漬け物 as spellings".**
- JMdict 1433700 lists 漬物 first, then 漬け物, then 漬けもの (search-only). The entry is headed 漬物.
- Fix: "is JMdict entry 漬物, with 漬け物 as another spelling and 漬けもの as 'search-only kanji form'".

**C9 (correctness and quotation, 潜 Meaning and origin): 原潜 げんせん is glossed as JMdict "abbreviation nuclear submarine".**
- "abbreviation" is a misc tag, not part of the gloss. JMdict 1262040's gloss is "nuclear submarine".
- Fix: 'JMdict "nuclear submarine," tagged "abbreviation"'.

**C10 (correctness against the quoted-gloss rule, 災 and 為): Daijisen paraphrases are given in double quotes as if they were glosses.**
- 災: "unhappiness brought on a person" and "something unpleasant" (Daijisen わざわい: 人に不幸をもたらす物事 … ／不快であること).
- 為: "something that benefits", "cause; reason", "an aim" and "for someone" (Daijisen ため 1-4). The last is also a loose rendering of 一定の関係のあること。…にとっては ("in relation to; for (someone)").
- None of these is a JMdict gloss, a KANJIDIC2 meaning or a card title, which is the packet's rule for double-quoted text.
- Fix: present them unquoted as paraphrases ("Daijisen describes … as …").

## Optional

- **O1 (炎 Notes):** "[熱](熱.md), “heat; fever,” [暑](暑.md), “hot weather; …,” overlap heat" is missing "and" between the two items.
- **O2 (為 Readings):** "The repo's reading checker labels the な of 為す as な.る …" is internal tooling detail that means nothing to a learner. Consider "な.る and な.す share the stem な; 為す uses な.す."
- **O3 (漬):** "JMdict marks the second sense stagk=漬ける" is raw schema jargon. "JMdict restricts the pickling sense to the spelling 漬ける" says the same thing plainly.
- **O4 (瀬 coverage):** 年の瀬 としのせ, "the year end; end of the year", is a common news2 word with the せ reading and is not mentioned. It would be a natural extra example beside 瀬戸際.
- **O5 (漫 coverage):** 漫才 まんざい (news1), "manzai; comic dialogue", directly supports the "comic" part of the title and is not mentioned.
- **O6 (滑):** "Kanjipedia lists ぬめ.る outside KANJIDIC2" could say plainly that Kanjipedia marks ぬめ.る as 外 (outside the Joyo table).
- **O7 (滞 Notes):** the card says 滑 is kept out, although the pair is declared only on the 滑 card. This is functionally true because exclusions are symmetric, but "the 滑 card keeps them apart" would be more exact.
- **O8 (為 exclusions):** the 21 exclusions are defensible. 業 ("work, occupation") and 理 ("reason, logic") are the weakest links, because they depend on secondary senses. Trimming them would not create an ambiguity, but they are not wrong.
- **O9 (瀬戸物 diff):** the link "[瀬](../kanji/瀬.md)戸 (せと)" splits the place name visually. It is acceptable and matches the link-wrap rule, but "[瀬](../kanji/瀬.md) in 瀬戸 (せと)" would read more smoothly if a later edit is ever made.

## Limits

- **Tool calls:** I issued exactly one tool call per response throughout and never issued parallel calls.
- **Temp file:** one early powershell call, which printed the Weblio extracts together, produced more output than the tool returns. The tool saved that output automatically to a temporary file outside the packet. I did not open that file. I re-read the same extracts in two smaller calls inside the packet.
- **Partial reads:**
  - quiz-safety.txt was not opened; I relied on the mechanical-checks.md simulation tail and on my own reading of QuizBuilder and KanjiReadings.
  - The reading audits were read only in part (attested-reading lines, tail, HIT blocks).
  - jmdict-families.xml was read entry by entry, not in full.
  - I did not open the 20 word articles beyond their diffs, word-titles.tsv, the rubric, okurigana-scan.txt or kanji_remarks.py.
- **Live web check:** only one Daijisen page was re-checked live (漫, which confirmed C1). For the other Daijisen and Kanjipedia claims I relied on the packet's extracts (evidence\public-source\, daijisen-heads.txt and kanjipedia-outside-readings.json). Those extracts can split linked words, as the すず / すずろ case shows. Claims I could not see in an extract are not marked CLEAN beyond what those files show.
- **Reading-audit verdict:** this rests on my reading of KanjiReadings.kt lines 1-160 and on the audit output. As stated in the packet, the Kotlin cross-check and the Android tests were not run.
- **Assumption on the 漫 lead:** I took the lead's "バン" (and "なず.む" for 滞) as readings that appear only in card text or audit extras. Neither is in KANJIDIC2 or in the cards' metadata.
- **Assumption on C10:** I read the packet's rule on double-quoted glosses as applying to Daijisen paraphrases as well. If the house style allows quoted translations of Daijisen, C10 becomes optional polish.