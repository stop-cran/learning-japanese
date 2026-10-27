**Snapshot:** 408be09e0156fc6ed3c0ed1b1b0ac67f592eb1a9, committed files only. I had file-reading tools only and ran no Git commands. I did not check that the worktree is clean (the author confirmed it is), and I did not diff against baseline 2cf65f40.

**Scope:** Model claude-opus-5.5 (Claude family).
- **Read in full:** all 15 kanji cards (券 刺 則 副 劇 効 勇 募 勢 包 匹 区 卒 協 占) and all 3 new word articles (副作用, 募集, 匹敵).
- **Rules and evidence:** the three rule files at the assigned line ranges, and the whole of batch-03.json.
- **Supporting pages:** all 45 distractor cards, the legacy cards that only have two answer choices, the link targets, the close-meaning word articles and their front matter, and docs\counter-pilot.md.
- **Public pages fetched:** Daijisen 則, Kanjipedia 卒, Tofugu 匹, and the kotobank and weblio pages for 副作用.
- **Related word articles:** for all 20, I checked only the "How the kanji combine" link.
- **Not reviewed:** stroke JSON drawing paths, the manifest, unrelated legacy content, and the excluded documents.

**Verdicts:**

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 券 | CLEAN | CLEAN | CLEAN |
| 刺 | CLEAN | CLEAN | CLEAN |
| 則 | CLEAN | CLEAN | CLEAN |
| 副 | CLEAN | CLEAN | CLEAN |
| 劇 | CLEAN | CLEAN | CLEAN |
| 効 | CLEAN | CLEAN | CLEAN |
| 勇 | CLEAN | CLEAN | CLEAN |
| 募 | CLEAN | CLEAN | CLEAN |
| 勢 | CLEAN | CLEAN | CLEAN |
| 包 | CLEAN | CLEAN | CLEAN |
| 匹 | CLEAN | CLEAN | NEEDS FIX |
| 区 | CLEAN | CLEAN | CLEAN |
| 卒 | CLEAN | CLEAN | CLEAN |
| 協 | CLEAN | CLEAN | CLEAN |
| 占 | CLEAN | CLEAN | CLEAN |
| words\副作用 | CLEAN | CLEAN | CLEAN |
| words\募集 | CLEAN | CLEAN | CLEAN |
| words\匹敵 | CLEAN | CLEAN | CLEAN |

What passed:
- **Card metadata:** readings, stroke counts, radicals, radical numbers and grades on all 15 cards match the KANJIDIC2 records in batch-03.
- **Wrong answer choices:** all 45 exist and none is a synonym of its target. No legacy card offers a new kanji as a wrong answer. The legacy two-choice cards share no tags with the new cards.
- **Word articles:** none of the three has a `jlpt` field, and their kanji lists are correct.
- **20 related word articles:** each links the new kanji at its first substantive mention with a valid path.

**Findings:**

**F-01**
- **Severity / facet:** Minor; comprehensibility.
- **Location:** kanji\匹.md:31 and 40.
- **Claim and impact:** The note at line 40 says counter pronunciations change with the number but gives no forms. This is the kanji's main everyday use, so learners are left knowing only that plain ひき is sometimes wrong.
- **Remedy:** Add a few forms, e.g. 一匹 いっぴき, 三匹 さんびき, 六匹 ろっぴき, 何匹 なんびき.
- **Evidence:** Tofugu's 匹 counter table (the repo's own counter-pilot.md uses it as a source) lists いっぴき, さんびき, ろっぴき, はっぴき/はちひき, じゅっぴき and なんびき. The existing words\虫.md:31 already shows 一匹 (いっぴき).
- **Confidence:** High.

**Optional:**
- **O-1, 刺.md:33:** "(noun; sense 3)" points at a JMdict sense number learners can't see. Line 47 explains the choice, but naming the sense ("piercing sense") or giving a compound like 串刺し would read better.
- **O-2, 勢.md:47:** "勢い is a noun" leaves out JMdict 1375040's adverb sense 4 (naturally; inevitably). Rewording to "mainly a noun; not an i-adjective" would cover it.
- **O-3, 卒.md:31:** consider mentioning the alternative reading そっきょ for 卒去. Kanjipedia indexes 卒去 as ソッキョ.
- **O-4, 匹敵.md:8:** If 同じ "same" was worth excluding, 同様 "same; similar" (which shares the comparison tag) is at least as close. Adding it, and possibly 同一, would be consistent. This is not a required exclusion.
- **O-5, 募集.md:8:** JMdict sense 1 includes the gloss "invitation". 招く "invite" and 誘う "invite; entice" would be conservative companions to the existing 招待 exclusion. Also not required.

**Limits:**
- **No Git:** I couldn't check that the 20 related articles changed only in their links, or that their teaching text and metadata are otherwise unchanged.
- **Stroke files:** not audited.
- **則 のり (則.md:32):** I couldn't establish whether standalone のり is literary. The JMdict record has no register flag, and Daijisen's kanji entry only lists the reading. I left the verdict CLEAN because line 45 already presents it as a dictionary reading.
- **副作用.md:33:** the claim about figurative use outside medicine is plausible but unverified. JMdict and the fetched pages only show the medical sense.
- **Coverage:** batch-03 is a selected packet, not the whole dictionary. Nothing here is a native-speaker certification.
