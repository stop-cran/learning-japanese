I found one actionable defect and one minor comprehensibility issue across the 20 rows. またぐ wrongly says the verb also means "sitting astride," and one 真っ黒 example sentence doesn't make clear which sense it shows. The other 18 rows, both kanji edits, both reused cards, all three kanji/word link pairs and all 20 mappings came out clean.

## Snapshot
**Frozen commit:** 6102eb03c5be228d73a5584972bcbd88d138c60c (parent 09310e308ec2becf8ab405f8be37bc57188a1b56), as given in frozen-snapshot.json. I reviewed committed content only. My file tools can't run Git, so I couldn't confirm that the working tree matches the commit or that 混ぜる.md and または.md are byte-for-byte unchanged. Those points rest on the frozen receipt and on the content being consistent with it.

## Scope
**Model:** claude-opus-5.5 (family claude). I read serially, used no agents and made no edits.

**Read completely:**
- frozen-snapshot.json and related.patch.
- .github\copilot-instructions.md, content-structure.instructions.md and docs\content-format.md:18-103.
- All 20 assigned word articles and the 角, 祭 and 混 kanji bodies.
- Mappings 1-10 and 11-20; principals 1-10 and 11-20 (20 families, 35 senses).
- Components 1-10, 11-20 and 21-30.
- Labels 1-65, 66-130, 131-195 and 196-262 (EOF).
- extra-comparison-reading.txt (29 lines: 5 families, 9 senses).
- public-bodies.txt (lines 1-253, through EOF).
- The TSV header [1,1] and rows [1582,1601] only.
- words\空.md.

**Read in part:**
- review-evidence.json: lines 1-60, 2714-about 3480 (truncated), 4131-4414 and 49383-EOF. I did not read its embedded families (lines 376-1826 and 4414-45752).
- Pattern-only greps, not full bodies: 渡す, 白, 白い, 頭, コレクション, 採る, plus the quiz_exclusions lines in words\ (which showed あるいは, それとも, 混ざる and 混じる).
- I globbed kanji\ and words\ to confirm links exist and there are no duplicate cards.

**External check:** I fetched kotobank 跨ぐ, which carries Digital Daijisen and 精選版 日本国語大辞典 (the shorter edition of Nihon Kokugo Daijiten).

**Not read:**
- family-inspection-01 to 14, old-body-inspection-01 to 21, related-kanji-inspection-01 and public-bodies.json.
- The 479 available prepared families.
- docs\n2-vocabulary-snapshot.json, docs\n2-source-snapshot.json, docs\confusable-words.md and docs\jlpt-levels.md.

The author's 331/870 family/sense union and 168 older bodies are the author's reads, not mine.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1582 | 混ぜる | CLEAN | CLEAN | CLEAN | Unchanged reuse; source spelling 交ぜる taught (:22); raw intransitive gloss not adopted |
| N2:1583 | またぐ | NEEDS FIX | CLEAN | NEEDS FIX | B80-01 |
| N2:1584 | または | CLEAN | CLEAN | CLEAN | Stays N4; teaches 又は and は pronounced わ; あるいは and それとも already exclude it |
| N2:1585 | 待合室 | CLEAN | CLEAN | CLEAN | Mixed reading まちあい + しつ explained; tagged mixed-reading |
| N2:1586 | 待ち合わせる | CLEAN | CLEAN | CLEAN | 人と / 場所で / 時刻に pattern is accurate |
| N2:1587 | 街角 | CLEAN | CLEAN | CLEAN | Mentions 町角; 街 correctly plain text (no card) |
| N2:1588 | 真っ暗 | CLEAN | CLEAN | CLEAN | Teaches dark and hopeless senses; 目の前が真っ暗 is idiomatic |
| N2:1589 | 真っ黒 | CLEAN | CLEAN | NEEDS FIX | B80-02 |
| N2:1590 | 真っ青 | CLEAN | CLEAN | CLEAN | Reading まっさお; pale-face sense taught |
| N2:1591 | 真っ先 | CLEAN | CLEAN | CLEAN | 真っ先に pattern taught; distinguished from 初めて |
| N2:1592 | 真っ白 | CLEAN | CLEAN | CLEAN | ましろ limited to 真白 is correct; 空 exclusion is backed by 空.md's から "empty" section |
| N2:1593 | 祭る | CLEAN | CLEAN | CLEAN | Transitive godan verb; 祀る taught; links to 祭 both ways |
| N2:1594 | 窓口 | CLEAN | CLEAN | CLEAN | Both senses with natural examples |
| N2:1595 | まとまる | CLEAN | CLEAN | CLEAN | 纏まる taught; intransitive godan; kana usual |
| N2:1596 | まとめる | CLEAN | CLEAN | CLEAN | 纏める marked rare; senses 1-4 covered |
| N2:1597 | 真似る | CLEAN | CLEAN | CLEAN | Kanji framed as a spelling aid; contrasted with 似る |
| N2:1598 | まぶしい | CLEAN | CLEAN | CLEAN | 眩しい and まぼしい mentioned; figurative sense backed by Daijisen 2 |
| N2:1599 | まぶた | CLEAN | CLEAN | CLEAN | うわまぶた / したまぶた match entries 1354550 / 1186660 |
| N2:1600 | マフラー | CLEAN | CLEAN | CLEAN | Scarf and exhaust muffler, separated by context |
| N2:1601 | まもなく | CLEAN | CLEAN | CLEAN | 間も無く taught; sense 2 (dictionary-form verb + 間もなく) taught separately |

**Kanji and baseline preservation: CLEAN.** related.patch only adds links:
- 祭 gains a 祭る link in the まつ.る reading row, Common words and Notes.
- 角 gains 街角 in the かど row and Common words, and 1204580 in the entry list.

Front matter and all other teaching are unchanged. 混, 混ぜる and または show no batch-80 edits (byte-level check not possible; see Snapshot).

**Component links: CLEAN.** Every primary written kanji appears in metadata. Every existing kanji card is linked, and plain-text 街 is right because it has no card. All linked word articles exist, and I made up no missing cards.

**Reciprocal N2 links: CLEAN.** 街角 ↔ 角, 祭る ↔ 祭 and the rechecked 混ぜる ↔ 混 all link in both directions.

**Mappings: CLEAN.** All 20 TSV rows match the mappings, entries and sense selections. Raw values are unchanged.

## Findings
**B80-01**
- **Severity / facet:** Medium; correctness and comprehensibility.
- **Location:** words\またぐ.md:16-17, 24-25 and 41-42.
- **Claim / impact:** The card says またぐ also means "sitting astride" and calls that use "established." Yet lines 24-25 assign sitting astride to またがる. Learners may write 馬をまたぐ instead of 馬にまたがる.
- **Minimal remedy:** Change "or sitting astride it" to spanning or crossing a boundary (for example 県境をまたぐ). At 41-42, say "the spanning use." Keep the またがる contrast.
- **Evidence:**
  - JMdict 1267830: sense 1 "step over"; sense 2 "stretch over; span; bridge; saddle; straddle."
  - Daijisen: "１足を開いて物の上を越える ２かけ渡す。またがる。「谷を跨ぐつり橋」."
  - Nihon Kokugo Daijiten: "①股をひろげて物の上を越える ②一方から他方へと、隔てるものを越える."
  - KANJIDIC's "sit astride" for 跨 describes the character, not this word.
- **Confidence:** High.

**B80-02**
- **Severity / facet:** Low; comprehensibility.
- **Location:** words\真っ黒.md:20 (against :40-41).
- **Claim / impact:** 外で遊んで、顔が真っ黒になりました is translated as "deeply tanned." The Japanese fits both the tan sense and the dirt sense, which contradicts the card's own rule that the object and cause identify the use.
- **Minimal remedy:** Use 夏休みに毎日外で遊んで、真っ黒に日焼けしました (or similar).
- **Evidence:** JMdict 1604050 senses 2 and 3; Daijisen 2 「海水浴帰りの―な顔」 vs Daijisen 3 「汚れて黒ずんでいる」.
- **Confidence:** Medium.

## Optional
- **More coverage:**
  - またぐ: 年をまたぐ (into the new year).
  - まもなく: 〜て間もなく "shortly after," as in Daijisen 「君が帰って、―彼が来た」.
  - 街角: Daijisen sense 2, 街頭 (out on the street).
  - 待ち合わせる: the railway use 特急の通過を待ち合わせる.
- **Wording:** まとまる:22 「費用がまとまった」 could also be read as "the costs were settled"; お金がまとまった is clearer.
- **Weak but defensible exclusions (no fix needed):** 真っ先/頭, またぐ/渡す, まとまる/コレクション and 採る, 真っ青/白. 待ち合わせる/打ち合わせ does not need an exclusion, because their titles don't make either answer ambiguous.
- **Out of scope:** 混ぜる's tags lack wago, but that dates from batch 79 and the reuse is meant to stay unchanged.

## Limits
- I couldn't run Git, so the commit and the unchanged status of the reuses are not independently verified.
- I read only one comparison article in full; the others only in part.
- Example naturalness is not native-speaker certified.
- Public dictionary evidence is Daijisen alone, plus Nihon Kokugo Daijiten for 跨ぐ only.
