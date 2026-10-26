## Snapshot
**Revised commit:** 376b4ef640bb1df32337f538c4f3277c1ccb091e. **Parent:** 2c2ed2623f04773c93bc97c6820e3ef7131b8fea.

This is a non-blind check of the author's fixes, against committed content only as the author supplied it. I made no tool calls in this round. Everything below rests on the evidence pasted into the request plus what I had already read in this session. I ran no Git, hash or extraction checks, so the link between the supplied text and the commit rests on the author's assertion.

## Scope
**Model:** claude-opus-5.5, Claude family.

**This round:** zero tool calls. I reviewed the supplied material:
- the correction diff and the author's adjudication;
- both original reports;
- the twenty current mappings and twenty current word bodies;
- the four related kanji bodies (印, 刊, 郵, 軟) and the 35 component records;
- 34 complete dictionary families (65 senses):
  - 20 primary families, 32 senses;
  - 14 corrective families, 33 senses: 1136480, 1274810, 1320140, 1346150, 1350600, 1350610, 1350710, 1350730, 1469570, 1533000, 1538330, 1582900, 2057030 and 2859761;
- the pre-fix text of the seven changed cards;
- eleven older comparison bodies: 公務, 失敗, めちゃくちゃ, 勝つ, 訳, 燃える, 燃やす, 焦がす, 焦げる, 焼く and 焼ける;
- the unchanged 351-line Daijisen capture.

**Checks I made myself:**
- The supplied pre-fix text of the changed lines matches my own earlier reads. Line 9 (quiz_exclusions) matches for 役目, 火傷, やたら and やっつける; 家主.md:39 and 夜行.md:23 match my earlier grep.
- The current bodies contain 134 quiz_exclusion declarations, by my count. That is 129 before the fix plus the five new guards.

**Original process (unchanged):**
- 61 native calls started across both runs; 58 returned. The three that started together in the first run were interrupted and returned nothing.
- Up to three calls were outstanding at once.
- The 57th continuation call broke the 56-call budget.
- The earlier 3-start receipt does not describe the full first attempt, which had 4 starts with up to 3 outstanding.
- My earlier reading covered the 20 primary families (32 senses) and no comparison families. I read 6 older bodies in full: めちゃくちゃ, 勝つ, 夕飯, 訳, 公務 and 仕方.

**Provenance of my original report:**
- The full report exists as CLI stdout. The final native assistant message holds only its last 10,662 characters.
- The preserved text includes a malformed, duplicated table-header fragment ("| Source row | Article | Correctness | Scoped co| Source row …"). I keep it as is and do not guess its cause.

**Blindness:** both original reviews saw the author's prose in the permitted TSV `source_note` column, so neither was fully blind to author comments. This round is non-blind. The author's family and body counts are theirs, not mine.

## Verdicts
**Final: ACCEPT.** "Clean" means no actionable defect within this scope; it is not exhaustive certification.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1702 | words\役所.md | CLEAN | CLEAN | CLEAN | Unchanged. やくしょ means a public office; the separate やくどころ entry is not imported. |
| N2:1703 | words\訳す.md | CLEAN | CLEAN | CLEAN | 訳 guard added (F04). Primary わけ identity and the separate やく identity are both respected. |
| N2:1704 | words\役人.md | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1705 | words\薬品.md | CLEAN | CLEAN | CLEAN | Unchanged. Senses 1–2 (medicine, chemical agent) are both taught. |
| N2:1706 | words\役目.md | CLEAN | CLEAN | CLEAN | 公務 guard added (F01). |
| N2:1707 | words\火傷.md | CLEAN | CLEAN | CLEAN | 失敗 guard added (GPT-F02). The かしょう sentence is correctly limited (L01). No combustion-verb guard is needed (L02). |
| N2:1708 | words\夜行.md | CLEAN | CLEAN | CLEAN | Now teaches 夜行する (F06). Night-train use stays a やこう noun; the やぎょう senses are not imported. |
| N2:1709 | words\矢印.md | CLEAN | CLEAN | CLEAN | Unchanged. The colloquial "interest" sense stays marked as extra. |
| N2:1710 | words\やたら.md | CLEAN | CLEAN | CLEAN | めちゃくちゃ guard added (F02). |
| N2:1711 | words\薬局.md | CLEAN | CLEAN | CLEAN | Existing article; only `jlpt: 2` was added. |
| N2:1712 | words\やっつける.md | CLEAN | CLEAN | CLEAN | 勝つ guard added (F03). The "get done" use is openly sourced to Daijisen sense 1. |
| N2:1713 | words\家主.md | CLEAN | CLEAN | CLEAN | Line 39 now calls いえぬし a native reading (F05). |
| N2:1714 | words\破く.md | CLEAN | CLEAN | CLEAN | Unchanged. The empty raw source gloss is kept empty. |
| N2:1715 | words\破れる.md | CLEAN | CLEAN | CLEAN | Unchanged. Kept separate from 敗れる and from the potential form of 破る. |
| N2:1716 | words\やむをえない.md | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1717 | words\軟らかい.md | CLEAN | CLEAN | CLEAN | Existing article; level-only change. Its 21 existing exclusions are preserved, not newly researched. |
| N2:1718 | words\遊園地.md | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1719 | words\夕刊.md | CLEAN | CLEAN | CLEAN | Unchanged. Typed wago, following the existing 夕飯 card. |
| N2:1720 | words\友好.md | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1721 | words\郵送.md | CLEAN | CLEAN | CLEAN | Unchanged. |

**Kanji and existing-article preservation: CLEAN.**
- The diff touches only seven word files. No kanji card, 薬局, 軟らかい, mapping, selected sense, identity, reading or title changed.
- The supplied 印, 刊, 郵 and 軟 bodies match my earlier reads.
- I have not read the 柔らかい body. Its N4 level rests on the patch and diff leaving it untouched.

**Components: CLEAN.**
- The 27 primary kanji all appear in card metadata. The 25 that have kanji cards are linked; 傷 and 矢 have no cards and are listed without invented links.
- The kana-only cards have empty kanji lists.
- The other 8 component records cover alternative-spelling characters: 遣, 止, 柔, 鱈, 得, 熱, 付 and 已.

**Two-way links: CLEAN.** 印/矢印, 刊/夕刊 and 郵/郵送 link both ways, and the existing 軟/軟らかい pair is intact.

**Mappings: CLEAN.** All twenty rows still point at the exact dictionary entry, at level 2, with unchanged selected and extra senses.

## Findings
No new actionable defect was found, and the seven changed lines introduce no regression.

**B86-F01 — Minor — quiz exclusions — 役目.md:9 — RESOLVED** (confidence: high)
- 公務 is now excluded. A guard on one side covers both directions.
- Basis: 役目 (1538080:1) is "duty; role; function", and 公務 (1274810:1) is "official business; public business". The 公務 card teaches official public duties.
- Correction to my own reasoning: the eight exclusions both cards share were not valid proof, because guards are not transitive. The direct meaning overlap is enough on its own.
- Facet: I filed this under Correctness; GPT filed it under Scoped coverage. That difference does not change the outcome.

**B86-F02 — Minor — quiz exclusions — やたら.md:9 — RESOLVED** (confidence: high)
- やたら (1537780:1–2) covers "recklessly… excessively"; めちゃくちゃ (1533000) covers "extreme… reckless" (sense 2) and "incredibly" (sense 4).
- Daijisen's entry for やたら itself glosses it as めちゃくちゃ.
- The shared degree-word guards are not the proof here either.

**B86-F03 — Minor — quiz exclusions — やっつける.md:9 — RESOLVED** (confidence: medium-high)
- やっつける (1612950:1) means "to beat"; 勝つ (1346150:1) means "to win", as an intransitive godan verb.
- The 勝つ card itself translates 兄に勝つ as "beat my older brother".
- The difference in transitivity is not a reason to skip the guard.

**B86-F04 — Minor — quiz exclusions — 訳す.md:9 — RESOLVED, qualified** (confidence: medium)
- 訳 as わけ (1538330, senses 1–5) has no translation sense, so 訳's primary identity does not justify the guard.
- The basis is the separate entry 訳 as やく (2057030:1, "translation; version"). The 訳 card teaches it explicitly at 訳.md:29–33 and 37, and already excludes 翻訳 for that reason.
- 訳す (1538350) is the verb "translate", so the overlap with a taught meaning is direct; it is not a matter of shared sound.
- I withdraw my original reasoning through neighbouring guards.
- The guard is conservative, and I found no evidence that it is excessive. I did not inspect how the quiz renders readings.

**B86-F05 — Minor polish — comprehensibility — 家主.md:39 — RESOLVED** (confidence: high)
- The new wording is accurate. Component records give 家 as いえ/や and 主 as ぬし, both native readings, and dictionary entry 1191990 and Daijisen both list やぬし and いえぬし.
- Calibration: the original sentence never actually rejected いえぬし; it was only confusing.

**B86-F06 — Minor — comprehensibility — 夜行.md:23 — RESOLVED** (confidence: high)
- Sense 1 of 1584820 is a noun that takes する and is intransitive, with no reading restriction. Daijisen marks やこう as ［名］(スル).
- The note keeps the train abbreviation as a noun, which the dictionary restricts to やこう. It does not import the やぎょう readings or the nocturnal-activity use.

**GPT-F02 — Minor — quiz exclusions — 火傷.md:9 — ACCEPTED** (confidence: high)
- My original review missed this one.
- 1577310:2 records the figurative "getting one's fingers burned". Daijisen's やけど sense 2 is 「失敗したり、手痛い経験をしたりすること」.
- 失敗 (1320140:1) is failure or mistake, and 火傷.md:41 already teaches the figurative use. The guard is not extended to every adverse event.

**B86-L01 — 火傷 かしょう sentence — my UNVERIFIED withdrawn; CLEAN** (confidence: medium-high)
- The exact sentence at 火傷.md:39 is: "Do not read this spelling as かしょう in the ordinary やけど expressions taught here."
- Entry 2859761 is a separate entry: 火傷 read かしょう, "burn; scald", cross-referenced to やけど sense 1. Daijisen's かしょう heading says 「やけど」に同じ.
- The sentence is limited to the card's own やけど expressions, which carry the やけど reading in their furigana. It does not deny that the separate entry exists, and the mapping still covers only 1577310.
- I retract my earlier description of かしょう as "formal". Neither source gives it a register label.

**B86-L02 — 火傷 vs burning verbs — withdrawn; no missing or excessive guard** (confidence: medium)
- 燃える (1469570) and 燃やす (1582900) mean combustion or emotional fire, with no injury sense. 火傷.md:35 contrasts them explicitly.
- The existing 火傷 guards are each defensible on their own meanings:
  - 焼く: 1350600:5, "to tan; to burn";
  - 焼ける: 1350610:3, "to be sunburnt";
  - 焦がす and 焦げる: singe, scorch and burn.
- The one remaining overlap is the bare word "burn" in 燃える's title. Against 火傷's qualified title "burn injury; scald", that overlap is weak.

## Optional
These are non-blocking and do not affect acceptance:
- **火傷.md:39:** optionally say that かしょう is a separate recognized entry (2859761) with the same meaning, so learners do not read it as a misreading. Do not add a register claim.
- **訳す:** optionally add a recognition note for the noun 訳 (やく, "translation; version") and for the older verb 訳する.
- **夜行 and やっつける:** expanding to 夜行 nocturnal activity and やっつける "eat/drink" stays deferred.
- **やむをえない:** I withdraw my "most common spelling" suggestion; there is no frequency evidence for it.
- **矢印 and 役目 guards:** the 矢印 guards (関心, 興味, 方向) and the 役目 guards (用事, 作業) need no change.

## Limits
- **Commit binding:** no Git was run. The link between the supplied text and commit 376b4ef rests on the author.
- **Unchanged cards:** I could compare the 13 unchanged cards only against my condensed notes, not against exact earlier text.
- **Quiz rendering:** I did not inspect how the quiz renders cards, including whether readings appear. This mostly affects how much the 訳 guard matters.
- **Comparison entries:** I did not verify the comparison entries cited in やっつける (1471200 and 1511790). I have also not read the 柔らかい body.
- **Comparison coverage:** comparison families beyond the 34 supplied were not inspected. There is no exhaustive check of the quiz pool or native-speaker certification. Daijisen is the only public authority, and its sense numbering does not line up with the pinned dictionary.
- **破れる example:** the naturalness of 交渉が破れました rests on the negotiations gloss in dictionary sense 1471210:2. Daijisen's similar examples use 恋 and 夢, and no corpus was checked.
- **Process caveats:** the original call-budget overrun, concurrent starts, compacted notes, the preserved partial native message with its malformed header, and exposure to TSV author prose all still apply. This confirmation round is non-blind.
