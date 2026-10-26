I found no problem with the snapshot, the kanji edits, the reciprocal links or the mappings. Four articles have quiz-exclusion problems: 目下 (Moderate), 恵まれる (Minor), 巡る and 命ずる (Low). The other 16 rows are CLEAN.

## Snapshot
Frozen commit: **f6a02bca0885a78dac2568e8da448be0954756df** (parent eff70d79e7eb56ec408eed141629a70d606febe6), committed content only. File tools cannot run Git, so the commit, hashes and equivalence checks are as reported by the author; I did not re-run them.

## Scope
Model: claude-opus-5.5 (claude family), one tool call at a time, read-only.

**Read in full:**
- frozen-snapshot.json and related.patch.
- .github\copilot-instructions.md, content-structure.instructions.md, and docs\content-format.md lines 18–103.
- All 20 assigned articles and the kanji bodies 刺, 詞, 印 and 群.
- Mappings 1–10 and 11–20, principals 1–10 and 11–20, components 1–14 and 15–28, and labels in all five ranges up to 268. Every return was complete.
- TSV header (line 1) and rows 1642–1661 only.
- public-bodies.txt (one untruncated return) and canonical-public-bodies.txt.
- Older bodies: 恩恵, 現在, 望む, 土産.

**Read in part:**
- 創作.md lines 1–12.
- review-evidence.json lines 1–120 (author notes, not relied on).

**Other checks:**
- Globs in kanji\ and words\ for card existence.
- Web: two Weblio pages for 目覚ます/めざます (failed: one Wiktionary stub, one with no body) and Jisho (failed). Kotobank 目覚ます succeeded (Digital Daijisen and Nikkoku Seisen).

**Not read:**
- family-inspection 01–11 (including the もっか 1535330, 回る 1604300 and 目標 1535650 families).
- old-body-inspection 01–17, related-kanji-inspection, the supplemental files, and the .json public bodies.
- 今, 回る and 目標 bodies (I relied on their labels).
- Most guard-target bodies.

The author's figures (415 families available; 309 families, 158 bodies and 268 labels read) are their reads, not mine.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1642 | 紫 | CLEAN | CLEAN | CLEAN | Daijisen confirms the plant's white flowers, the dye root and the soy-sauce sense. |
| N2:1643 | 群れ | CLEAN | CLEAN | CLEAN | Only `jlpt: 2` added; body and 12 exclusions unchanged; 群 link holds. |
| N2:1644 | 姪 | CLEAN | CLEAN | CLEAN | Line 16 placement is polish only (see Optional). |
| N2:1645 | 名作 | CLEAN | CLEAN | CLEAN | 傑作 guard present. |
| N2:1646 | 名刺 | CLEAN | CLEAN | CLEAN | The 刺 name-slip explanation matches Daijisen. |
| N2:1647 | 名詞 | CLEAN | CLEAN | CLEAN | The pronoun note matches the Daijisen 補説. |
| N2:1648 | 名所 | CLEAN | CLEAN | CLEAN | めいしょ only; old などころ uses correctly set aside. |
| N2:1649 | 命ずる | NEEDS FIX | CLEAN | CLEAN | Excessive 望む guard (B83-C4). |
| N2:1650 | 迷信 | CLEAN | CLEAN | CLEAN | — |
| N2:1651 | 名物 | CLEAN | CLEAN | CLEAN | 特徴 guard is borderline. |
| N2:1652 | めいめい | CLEAN | CLEAN | CLEAN | 銘々/銘銘 explicitly recognized; the 面面 origin and 進路 example match Daijisen. |
| N2:1653 | 目上 | CLEAN | CLEAN | CLEAN | 上司 has no card, so plain text is correct. |
| N2:1654 | メーター | CLEAN | CLEAN | CLEAN | メートル guard covers the metre sense. |
| N2:1655 | 恵まれる | NEEDS FIX | CLEAN | CLEAN | Missing 恩恵 guard (B83-C2). |
| N2:1656 | 巡る | NEEDS FIX | CLEAN | CLEAN | Excessive shape-noun guards (B83-C3); 回る distinction correct. |
| N2:1657 | 目指す | CLEAN | CLEAN | CLEAN | — |
| N2:1658 | 目覚まし | CLEAN | CLEAN | CLEAN | 目覚し recognized; failed source wrapper noted; canonical capture plus Kotobank confirm the 目覚ます (めざます) claim. |
| N2:1659 | 目下 | NEEDS FIX | CLEAN | CLEAN | めした identity and もっか contrast are correct; quiz guard missing (B83-C1). |
| N2:1660 | 目印 | CLEAN | CLEAN | CLEAN | 印, 標識, 記号 and 目標 guarded; 目標's navigation use is not denied. |
| N2:1661 | 目立つ | CLEAN | CLEAN | CLEAN | — |

**Kanji and baseline preservation: CLEAN.** The patch only links 名刺 in 刺, adds 目印 and 1535300 to 印, and adds 名詞 and 1531570 to 詞. 群 is untouched.

**Components: CLEAN.**
- All 17 linked kanji cards exist.
- 紫, 姪, 恵, 巡 and 銘 have no cards, so leaving them as plain text is correct.
- No invented links.

**Reciprocal links: CLEAN.** 名刺/刺, 名詞/詞, 目印/印 and the existing 群れ/群 all link both ways.

**Mappings: CLEAN.** All 20 match the TSV. 銘々→めいめい (1532810) and 目覚し→目覚まし (1535340) are explicit. For 目下, the raw gloss is kept as data, and the めした (1535320) identity is kept separate from もっか (1535330).

## Findings
**B83-C1 — 目下: missing guards against 現在 and 今**
- Severity: Moderate. Facet: correctness (quiz). Location: words\目下.md:9 and 39–43.
- Problem: the written form 目下 read もっか means "at present; now", and the article and the source gloss both say so. 現在 ("the present; currently") and 今 ("now") are therefore defensible answers when the prompt shows 目下.
- Fix: add 現在 and 今 to `quiz_exclusions`.
- Evidence: Daijisen もっか sense 2 is 「ただいま。さしあたり。現在。」; 現在.md:4.
- Confidence: medium. It depends on whether the quiz shows the reading.

**B83-C2 — 恵まれる: missing guard against 恩恵**
- Severity: Minor. Facet: correctness (quiz). Location: 恵まれる.md:9.
- Problem: "be blessed with" and 恩恵's "benefit; blessing" share the kanji 恵 and the idea of blessing. The article already guards the nouns 幸運 and 幸い.
- Fix: add 恩恵.
- Evidence: 恩恵.md:4 and 恵まれる.md:28–36.
- Confidence: medium.

**B83-C3 — 巡る: excessive guards 丸, 円 and 輪 (行く is weak)**
- Severity: Low. Facet: correctness (quiz). Location: 巡る.md:9.
- Problem: these shape nouns are only topically close to "go around; recur; concern". Neither the title nor any sense overlaps.
- Fix: remove 丸, 円 and 輪.
- Confidence: medium.

**B83-C4 — 命ずる: excessive 望む guard**
- Severity: Low. Facet: correctness (quiz). Location: 命ずる.md:9 and 43–44.
- Problem: the only link is the English idiom "command a view", which appears in neither title nor in 望む's body (望む.md:4 and 22–24).
- Fix: remove 望む. Deleting the sentence is optional.
- Confidence: medium.

## Optional
- 姪.md:16: move the 姪の子 caution after 姪っ子 is introduced.
- めいめい.md:24: say "each carries their own" instead of "distributes the luggage".
- 巡る: guard coverage is uneven (くるり and 観光 are not guarded while くるくる and 旅行 are).
- 目上: consider a "superior" guard against 優れる.
- 名作/創作 and 名物/特徴: both pairings are borderline.
- 命ずる: an example in the distinctive 命ずる form would help.

## Limits
- Git, hashes and equivalence checks were not independently executed.
- I could not confirm whether the quiz displays readings, which affects how serious B83-C1 is.
- The もっか, 回る and 目標 families and most guard-target bodies were not read; I relied on labels for them.
- Twenty positive captures (19 original plus the canonical 目覚まし) come from one authority, Daijisen; the failed 目覚し wrapper is not counted as corroboration.
- Naturalness of the examples is not certified by a native speaker.
