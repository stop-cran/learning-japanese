# Batch 095 combined 697: report on the 子 nominal-ending changes

**Result:** All eleven changed files are CLEAN for correctness, scoped coverage and comprehensibility. The source headings I fetched support every changed claim, and I found no proved defects. Two optional points are below.

## Snapshot
- **Signed HEAD:** 6c9450427e476fd60437520cdedae693d77bbdcc; combined merge d5a6823c; manifest 3eebfff0fdad5e28.
- **Reviewed delta:** d6a261903f26 → da374717b6f8, as supplied in the packet.
- **Uncommitted teaching:** none, according to the coordinator. I had no shell, so I could not check this or the file SHA256 values myself.
- **Unchanged files:** 剖 and 解剖 are not part of this delta.

## Scope
- **Model and session:** claude-opus-5.5 (Claude Opus 5.5), session ede78c28-e889-47b5-be0b-21533da61551. This is a dependent check, not a blind review. Every tool call was serial, one per response.
- **Packets:** 01–06 read whole, in order. They cover:
  - the diff for all eleven files;
  - the complete current articles;
  - the comparison articles 王子, 女子 and 電子;
  - ten frozen JMdict families;
  - the upstream source-navigation record;
  - the format and JLPT policy text.
- **Daijisen 子:** the result overflowed to a temp file. One full-read attempt was refused for size; a forceRead then returned the first 20,000 characters. That included the full Daijisen し【子】 kanji heading (senses 1–10, ス marked 唐, the 〈こ〉 entries) and the こ, し, ね and す headings. Later dictionaries on the page were not read.
- **Gogen-yurai 帽子, 椅子 and ゆず:** each page read in full.
- **菓子:** the result overflowed, and I read only the preview. It shows Nipponica's former fruit sense (果子, and Nippo Jisho 果実、とくに食後の果物). I did not inspect Daijisen's own 菓子 heading.
- **障子:** first 8,000 characters. That covers Daijisen, Seisenban Nihon Kokugo Daijiten and Nipponica; the 世界大百科 section was cut off.
- **柚:** Daijisen ゆ, ゆず【柚／柚子】 and ゆう; Seisenban ゆず, ゆ and ゆう; Jitsū; and a plant-name reading dictionary.
- **Wiktionary, revision 1925322:** the Japanese section is headed 和語の漢字表記, 柚子（ゆず）, "ゆずの漢字表記".

## Verdicts
Each cell gives correctness / scoped coverage / comprehensibility.

| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji/子.md | CLEAN | CLEAN | CLEAN |
| words/いす.md | CLEAN | CLEAN | CLEAN |
| words/お菓子.md | CLEAN | CLEAN | CLEAN |
| words/冊子.md | CLEAN | CLEAN | CLEAN |
| words/帽子.md | CLEAN | CLEAN | CLEAN |
| words/扇子.md | CLEAN | CLEAN | CLEAN |
| words/柚.md | CLEAN | CLEAN | CLEAN |
| words/様子.md | CLEAN | CLEAN | CLEAN |
| words/菓子.md | CLEAN | CLEAN | CLEAN |
| words/調子.md | CLEAN | CLEAN | CLEAN |
| words/障子.md | CLEAN | CLEAN | CLEAN |

How the source evidence supports these verdicts:

- **子.md:21–34 (three roles).** These match Daijisen's separate senses:
  - sense 1 (child, offspring), which lists 王子;
  - sense 7 (小さいもの, small things), which lists 電子;
  - sense 9 (物の名に付けたり、意味なく添えたりする語, a word added to names of things or added without meaning), which lists 菓子, 冊子, 障子, 調子 and 帽子;
  - 〈ス〉 "same as 9", which lists 椅子, 扇子 and 様子.
- **Nominal ending.** The articles say the ending is Chinese-derived; they never claim each whole word was borrowed. 障子.md:25 is the most cautious ("used in Chinese-derived word formation"). Lines 32–34 rule out a smallness rule, a separate English "thing", and free productivity. 電子 is kept apart from the empty ending as a technical particle sense.
- **子.md:58.** "ス is a later Sino-Japanese reading (唐音)" matches ［音］シ（呉）（漢）ス（唐）. The ス row in the reading table (椅子, 様子, 扇子) agrees with Daijisen's 〈ス〉 list.
- **いす.md:23.** "Read す, not し or こ" is correct for the modern reading. Gogen-yurai's account of 倚子 いし (Kan-on) later becoming す (Tō-on) is consistent with it.
- **菓子.md:25 and :36.** The former fruit sense is supported by Nipponica.
- **障子.md:25.** "Components do not specify the modern fitting" is supported by Daijisen sense 1 (a general term for fittings; 近年は明かり障子, recently the translucent-paper kind) and by Seisenban.
- **様子.md:28 and 調子.md:25.** "Not limited to physical or small objects" is consistent with Daijisen's list, which includes 様子, 調子 and 拍子.
- **扇子.md:27.** "No separate 'small fan' meaning" is consistent with Daijisen.
- **柚.md:24–26.** The reading identity is preserved:
  - ゆず is the whole-word reading;
  - JMdict restricts ゆ and ゆう to the spelling 柚 and flags them as outdated (line 38, unchanged; Daijisen and Seisenban agree);
  - "no freely reusable ず" is stated.
  The two origin accounts are kept separate:
  - The `wago` label is attributed to Wiktionary's grouping (verified) and is explicitly not presented as a settled origin.
  - Gogen-yurai's derivation from Chinese 柚子 is correctly reported as that source's account (verified). Gogen-yurai also rejects a 柚の酢 theory.
  - Nothing claims consensus.
- **Surrounding text.** I found no regressions in the surrounding constructions or translations within the shown contexts. The front matter is unchanged.

## Findings
None. No proved defects.

## Reconciliation
- **Original batch-095 items:** none falls within this delta. Hypothesis H1 (the citation line at 解.md:50) and optional items (a)–(c) are untouched by these eleven files, so they remain as before: a hypothesis and optional items. They are not resolved here.
- **Original 695 overlap:** stays rejected; the separate serial repair stands.

## Optional
1. **柚.md:26** links the live Wiktionary page. Pinning revision 1925322, which is what the navigation record uses, would stop the cited grouping from drifting.
2. **子.md:33 / 帽子.md:24** reject a smallness requirement. The cited Gogen-yurai 帽子 page, however, says 小さな物に添える接尾語 ("a suffix added to small things"). The rejection is supported by Daijisen sense 9 and the abstract nouns 様子 and 調子. A short note that the sources differ on this would make the tension visible.

## Limits
- **Sources only partly read:**
  - 菓子: preview only; Daijisen's own 菓子 heading was not inspected.
  - 障子: truncated at 8,000 characters.
  - Kotobank 子: truncated after the Daijisen headings.
- **Supplied rather than fetched:** the JMdict extraction is the coordinator's copy; I did not fetch it from upstream. I did no Git verification.
- **Not reviewed:**
  - the untouched corpus and any unrelated existing text in these files;
  - semantic ambiguity in quiz choices;
  - other words with 子 not in scope (for example 王子's ジ reading, which was not re-examined).
- **No new execution:** nothing was rendered, run on a device or tested. The 691/694/695 records are inherited with their limits.
- **No other claims:** nothing about a phone, MLKit, the full quiz pool, publication or a general release. CLEAN means no actionable defect was found within this bounded scope, not exhaustive certification.
