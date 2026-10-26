## Snapshot
**66364c849c41507a674454aadb1b6cb018595541**, read from frozen-snapshot.json, with parent 69b59c315993e788cb9a0131b5c690881381b198. I reviewed committed content only. File tools cannot run Git, so the snapshot hashes and the claim that 武士 is unchanged from the parent were author-executed. I could not re-check them independently.

## Scope
- **Model:** claude-opus-5.5, matching the requested model. No agents, delegation or edits.
- **Guidance read:** copilot-instructions; content-structure instructions; content-format.md:18-103.
- **Assigned files read completely:** all twenty assigned articles, kanji\符.md, kanji\武.md and related.patch.
- **TSV:** line 1 and lines 1462–1481 only.
- **Private files read completely:** frozen-snapshot, mappings (20), principals (20 families, 42 senses), components (33), labels (211), the supplement (もぐもぐ 2009920, 3 senses; katakana forms search-only), and public-bodies.txt.
- **Private files read partly:** review-evidence.json (lines 1–80 and 440–560) and public-bodies.json (lines 1–60).
- **Private files not read:** family-inspection-01 to 17 and old-body-inspection-01 to 15.
- **Comparison bodies read (18):** 覆う, でこぼこ, アクセサリー, 怠ける, 浴びせる, ささやく, ぽつぽつ, ひそひそ, 粒, ぶくぶく, うなる, 帽子, 栓, カバー, 信号, 記号, 久しぶり, 故障.
- **Existence checks:** I globbed words\ and kanji\ for candidate words.
- **Not read:** docs\confusable-words.md, docs\jlpt-levels.md, docs\n2-vocabulary-snapshot.json and docs\n2-source-snapshot.json.
- **Prohibited files:** none read.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1462 | 符号 | UNVERIFIED | CLEAN | CLEAN | 地図の符号 is not established (see Limits); the maths example is fine |
| N2:1463 | 夫妻 | CLEAN | CLEAN | CLEAN | Matches Daijisen 補説; excludes 夫婦 |
| N2:1464 | 塞がる | CLEAN | CLEAN | CLEAN | Godan intransitive verb; JMdict senses 1–3 |
| N2:1465 | 塞ぐ | NEEDS FIX | CLEAN | CLEAN | B74-01 |
| N2:1466 | ふざける (blank spelling) | CLEAN | CLEAN | CLEAN | Kana spelling kept; sense 4 is recognition-only |
| N2:1467 | 無沙汰 | CLEAN | CLEAN | CLEAN | Excluding 怠る and 不通 is sound |
| N2:1468 | 武士 | CLEAN | CLEAN | CLEAN | Reused baseline left untouched |
| N2:1469 | 部首 | CLEAN | CLEAN | CLEAN | — |
| N2:1470 | 襖 | CLEAN | CLEAN | CLEAN | Garment readings correctly ignored |
| N2:1471 | 附属 | CLEAN | CLEAN | CLEAN | One family covers 附属 and 付属 |
| N2:1472 | 蓋 | CLEAN | CLEAN | CLEAN | Excludes カバー and 栓 |
| N2:1473 | 不通 | CLEAN | CLEAN | CLEAN | Not excluded against 普通 (homophone only) — correct |
| N2:1474 | ぶつかる (blank spelling) | CLEAN | CLEAN | CLEAN | Sense 5 is recognition-only |
| N2:1475 | ぶつける (blank spelling) | CLEAN | CLEAN | CLEAN | See Optional ("nail on") |
| N2:1476 | 物騒 | CLEAN | CLEAN | CLEAN | Etymology is properly hedged |
| N2:1477 | ぶつぶつ (blank spelling) | CLEAN | CLEAN | CLEAN | Senses 3–4 are recognition-only |
| N2:1478 | 船便 | CLEAN | CLEAN | CLEAN | Kun-first wago qualification explicit; alternate せんびん noted |
| N2:1479 | 部品 | NEEDS FIX | CLEAN | NEEDS FIX | B74-02 |
| N2:1480 | 吹雪 | CLEAN | CLEAN | CLEAN | Teaches ふぶき as a whole word |
| N2:1481 | 父母 | CLEAN | CLEAN | CLEAN | — |

- **Kanji 符 — CLEAN.** The meaning (:20), reading row フ (:30) and common-word list (:35) link 符号 ふごう. Footer entry 1497710 matches the 符号 article. The header and 切符 are preserved.
- **Kanji 武 — CLEAN.** Reading row ブ (:28) adds 武士 ぶし. The common-word list (:38) is preserved. Footer entry 1583680 matches the 武士 article. The header is unchanged.
- **武士 baseline — CLEAN.** It keeps jlpt 2, kango, kanji [武, 士], reading ぶし, its title, no exclusions and its footer. The patch does not touch it.
- **Mappings — CLEAN.** All 20 match the TSV rows, entry IDs, selected and additional senses, and article footers.
- **Metadata and links:** all written Han characters appear in metadata. There are no invented cards for 塞, 無, 沙, 汰, 襖, 附, 属, 蓋 or 騒.

## Findings
- **B74-01** — Minor — Correctness (quiz exclusions)
  - **Location:** words\塞ぐ.md:4, 9, 16, 18-19
  - **Claim:** 塞ぐ explicitly teaches "cover", but 覆う ("cover; conceal") is not excluded in either file. A correct quiz answer could be marked wrong.
  - **Remedy:** add 覆う to 塞ぐ quiz_exclusions.
  - **Evidence:** 塞ぐ.md:16 says "block, plug, cover or occupy". :18 says "I covered the hole". :19 says "I covered my ears". JMdict 1602590 sense 1 includes "to cover (ears, eyes, etc.)". 覆う.md:4 is "cover; conceal", and :9 lists only 隠す.
  - **Confidence:** medium.
- **B74-02** — Minor — Correctness and Comprehensibility
  - **Location:** words\部品.md:4, 9, 12, 16
  - **Claim:** the title gloss "accessories" is unexplained (:16 says only that the dictionary includes it). It overlaps アクセサリー ("accessory; jewelry"), which explicitly covers equipment accessories. Neither file excludes the other.
  - **Remedy:** drop "accessories" from the title, the H1 and line 16. If it stays, add アクセサリー to quiz_exclusions.
  - **Evidence:** JMdict 1499480 glosses "parts; accessories; components". The Daijisen capture (public-bodies.txt:445) gives only 「部分品」の略. アクセサリー.md:15 says "accessories used with equipment, cars, or cameras", and :29 has カメラのアクセサリー.
  - **Confidence:** medium-high for the overlap; medium for the gloss.

## Optional
- 符号: use モールス符号 instead of the map example. Daijisen sense 2 attests it, and 記号.md uses 地図の記号.
- ぶつぶつ: optional exclusions for ささやく ("murmur" vs "mutter") and でこぼこ ("bumpy"); low confidence. The guards against 煮る and 煮える are weak extras that do little harm.
- ぶつける.md:24 refers to a "source gloss" ("nail on") that does not appear in JMdict entry 2742080; consider rewording.
- 塞がる.md:16: "It is also usually written ふさがる" could be reworded.
- 武.md:28: the semicolon separates both glosses and words, which is ambiguous.
- Other ideas: a 吹雪 note on 花吹雪 and 紙吹雪; a 父母 register note (no source found yet).

## Limits
- The naturalness of 地図の符号 is unresolved. Daijisen's 記号［用法］ note could not be retrieved: the Weblio fetch returned Wikipedia, and Kotobank returned encyclopedia entries.
- Public evidence comes from one authority: Digital Daijisen via Weblio.
- Unread private files may hold further comparison material. Not finding an issue here does not prove there is none.
- I could not verify snapshot hashes or parent identity without Git.
- This is not a native-speaker certification.
