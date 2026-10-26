## Snapshot
The frozen commit is `da41f6ef4025d64580008f97051637a74522025b` (parent `3f88cca3e759ec8dd348f408f86a2c34d6952b8e`). The frozen receipt marks it as clean committed content. My file tools cannot run Git or compute hashes, so I could not independently confirm the commit, its cleanliness or the author's equivalence checks.

## Scope
**Model:** claude-opus-5.5 (Claude family). I read files one at a time and made no edits.

**Assigned and related reads (all complete):**
- `frozen-snapshot.json`, the three instruction files (content-format.md lines 18–103 only), the TSV header and rows 1542–1561.
- All 20 mappings, all 20 principal families (45 senses), all 31 component records and all 268 comparison labels.
- `related.patch` and `mining-comparison-reading.txt` (採掘, entry 1294750, one sense).
- `public-bodies.txt` (461 lines, through end of file) and `extra-public-bodies.txt`.
- All 20 assigned articles and all 6 related kanji cards.

**Older bodies:** I read `words\坊さん.md` in full. The three reused articles (濠, 干す, 募集) were read in their current form, with the patch supplying the pre-change context. For 畑, 角度, 道, 南極 and 北.md, plus the existence and level checks on kanji cards, I used targeted searches only. Those are not full-body reads.

**Family coverage:** 21 families and 46 senses (the 20 principals plus 採掘). This is not the author's 387/904 union.

**Not read:**
- `review-evidence.json`
- `family-inspection-01` to `-14`
- `old-body-inspection-01` to `-22`
- `related-kanji-inspection-01`
- the `public-bodies.json` and `extra-public-bodies.json` files (I read the equivalent `.txt` versions)
- `docs\confusable-words.md` and `docs\jlpt-levels.md`
- `docs\n2-vocabulary-snapshot.json` and `docs\n2-source-snapshot.json`

I made no web fetches.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1542 | 防犯 | CLEAN | CLEAN | CLEAN | Matches Daijisen (犯罪を防ぐこと); 防 link is reciprocal |
| N2:1543 | 方面 | CLEAN | CLEAN | CLEAN | Senses 1–2 taught; 畑 guard backed by 畑.md:32 |
| N2:1544 | 坊や | CLEAN | CLEAN | CLEAN | Daijisen senses 1–2; 坊さん guard justified (坊さん.md "boy" sense) |
| N2:1545 | 放る | CLEAN | CLEAN | CLEAN | Daijisen ほうる 1–3; leaving 放す unguarded is correct |
| N2:1546 | ボーナス | CLEAN | CLEAN | CLEAN | Daijisen 賞与 / 追加の特典 |
| N2:1547 | 朗らか | CLEAN | CLEAN | CLEAN | Daijisen senses 1–2 |
| N2:1548 | 牧場 | CLEAN | CLEAN | CLEAN | ぼくじょう and まきば both match Daijisen |
| N2:1549 | 牧畜 | CLEAN | CLEAN | CLEAN | 畜 link is reciprocal |
| N2:1550 | 保健 | CLEAN | CLEAN | CLEAN | Matches Daijisen |
| N2:1551 | 募集 | CLEAN | CLEAN | CLEAN | Reuse: N2 level, senses 1–3, 集金 guard; prior teaching kept |
| N2:1552 | 干す | CLEAN | CLEAN | CLEAN | Reuse: senses 2–4 recognized per Daijisen 2–4; 飲む and 奪う guards defensible |
| N2:1553 | ポスター | CLEAN | CLEAN | CLEAN | Daijisen はり紙 |
| N2:1554 | 北極 | CLEAN | CLEAN | CLEAN | 極 link is reciprocal; 北極圏 shortening matches Daijisen |
| N2:1555 | 坊っちゃん | CLEAN | CLEAN | CLEAN | Lexical heading from the supplemental 坊ちゃん capture; novel not used as evidence |
| N2:1556 | ほどく | CLEAN | CLEAN | CLEAN | Kept separate from 解く/とく (1198890); を/が contrast with ほどける |
| N2:1557 | 濠 | CLEAN | NEEDS FIX | NEEDS FIX | B78-F1 |
| N2:1558 | 掘る | CLEAN | CLEAN | CLEAN | Practical senses 1–3; vulgar sense 4 omitted; 掘 link is reciprocal |
| N2:1559 | 彫る | CLEAN | CLEAN | NEEDS FIX | B78-F2 |
| N2:1560 | ぼろ | CLEAN | CLEAN | CLEAN | Daijisen 襤褸 senses 1–4; ぼろ- prefix kept separate |
| N2:1561 | 盆 | CLEAN | CLEAN | CLEAN | Household guards rest on JMdict sense 2 "family; household" (not flagged) |

**Six kanji and baseline preservation: CLEAN.** The patch only adds links and entry numbers to 防, 畜, 極 and 掘, and leaves their metadata unchanged. 募 and 干 already linked their words. For the reused words:
- 募集 and 干す gain N2 levels and the added recognition and exclusions.
- 濠 keeps N3, its title, filename and 濠 headword, and gains the 運河 guard.

**Component links: CLEAN.**
- Every existing card for a written kanji in the metadata is linked: 防, 犯, 方, 面, 放, 場, 畜, 募, 集, 干, 北, 極 and 掘.
- 坊, 朗, 牧, 保, 健, 彫, 盆 and 濠 have no cards, so they correctly stay as plain text.
- ほどく and ぼろ are kana headwords, so `kanji: []` is correct.

**Reciprocal N2 links: CLEAN.** I confirmed the kanji-side links directly; the word-side links are 防犯.md:25, 牧畜.md:25, 北極.md:24, 掘る.md:25, 募集.md:25 and 干す.md:26.
- 防犯 ↔ 防.md:30,38
- 牧畜 ↔ 畜.md:28,33
- 北極 ↔ 極.md:28,45
- 掘る ↔ 掘.md:20,31,36,41
- 募集 ↔ 募.md:30,35
- 干す ↔ 干.md:29,36

**Mappings: CLEAN.** All 20 entries and selected senses match the TSV. Raw 堀 maps to 濠 (entry 1522060, reading ほり, article level 3), which is consistent with the principal record.

## Findings
**B78-F1**
- **Severity:** Low.
- **Facets:** Scoped coverage and comprehensibility.
- **Location:** `words\濠.md:25,33,35`.
- **Claim:** The article never says that 堀 (the N2 source spelling) is the usual written form, and no example uses 堀.
  - Line 25 ("retain 濠 when recognizing this article's spelling") reads like process wording rather than teaching.
  - Line 33 says the card "foregrounds the source-assigned moat sense", but the source glosses ほり as both "moat" and "canal". The canal sense appears only as a gloss mention.
- **Impact:** Learners may treat the non-Jōyō 濠 as the default spelling.
- **Minimal remedy:** Keep N3, the title, filename and headword. State that 堀 is the usual Jōyō spelling and that 濠 and 壕 are less common. Reword line 33 to say the source gives "moat, canal".
- **Evidence:**
  - TSV N2:1557: `堀 ほり moat,canal … words/濠.md 3 … 1,2`.
  - JMdict priorities: 堀 has ichi1/news1/nf07; 濠 and 壕 have none.
  - Daijisen heading: ほり【堀／×濠／×壕】, sense 1 掘り割り (channel), sense 2 castle moat.
- **Confidence:** High for the omission; medium for the impact.

**B78-F2**
- **Severity:** Low.
- **Facet:** Comprehensibility (participant marking).
- **Location:** `words\彫る.md:16`, compared with lines 18–19.
- **Claim:** Line 16 says "に can mark the material or surface", but the article's own example marks the material with で (木で人形を彫りました), and で/から is never explained. に actually marks the surface engraved into.
- **Impact:** Learners might produce 木に人形を彫った to mean "carved a doll from wood".
- **Minimal remedy:** Say that を marks what is carved, に marks the surface engraved into, and で or から marks the material a figure is carved from.
- **Evidence:** Daijisen ほる【彫る】1: 「木・石・金属などに文字や模様…を刻み込む」, with the examples 「墓碑に名前を―・る」 and 「仏像を―・る」.
- **Confidence:** Medium.

## Optional
- **Titles:** 牧場 ("livestock farm; pasture") and 牧畜 ("livestock farming") read almost identically. "Ranch; pasture" for 牧場 would separate them.
- **放る.md:25:** Could say that ほう here is native (historically はふる) and only sounds like the on-reading ホウ.
- **Examples (non-native judgment):**
  - ぼろ: ぼろで靴を磨く or 靴がぼろぼろになった may sound more idiomatic.
  - 濠: the pre-existing 濠に水が流れています could become standing water.
- **Excess or extra guards:**
  - 開く in ほどく's exclusions and 角度 in 方面's look borrowed from neighboring exclusion lists and are probably unneeded.
  - Possible extra guards to consider: 防犯/安全, 盆/祭/お祭り and 干す/失う.
- **Links:** 南極.md:35 and 乾.md:34 could link the existing 北極 and 干す cards.

## Limits
- Git, hash and committed-content checks are not independently verified.
- Exclusion judgments rest on the 268 complete labels plus only a few full older bodies. I did not read the family-inspection or old-body-inspection files.
- All dictionary evidence comes from one source, Digital Daijisen via Weblio. 坊っちゃん has lexical support only from the supplemental 坊ちゃん heading.
- Naturalness judgments are non-native and low confidence.
