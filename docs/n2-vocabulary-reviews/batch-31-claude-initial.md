## Snapshot
The full frozen commit is `e0c3e67907cd8aa09f1c610f70c840e6f64aee74` (parent `25c9f55e52fefeb36f15df22e3cd557969a0f4a3`), and only committed content was in scope. I have file tools only, so I could not run Git or compute hashes. I reviewed the files at the receipt's paths and am relying on the receipt's own (author-verified) statement that they match the commit.

## Scope
**Model:** claude-opus-5.5, Claude family. I worked sequentially with no delegation and no edits.

**What I read:**
- The receipt, the three instruction/format documents, the related patch, and mapping lines N2:602–621.
- All 19 new articles in full, plus `作者.md` and `kanji\刺.md`.
- From the evidence file: every source row, all 20 principal JMdict families, the component records, the existing comparison labels, the public-dictionary receipts, the failed さすが lookup and the quiz declarations.
- The 154 comparison families (lines 2933–18856) only through targeted searches, not in full.
- Existing titles in `words\` for possible quiz conflicts.
- Public dictionary pages on Kotobank: Daijisen for 刺す, 差す/注す/点す, 挿す and 差し引き, and Nikkoku for 匙 and 流石. Weblio pages returned no dictionary text.

**Not read:** any of the forbidden files.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 先程 | CLEAN | CLEAN | CLEAN |
| 裂く | CLEAN | CLEAN | CLEAN |
| 索引 | CLEAN | CLEAN | CLEAN |
| 削除 | NEEDS FIX (R-04) | CLEAN | CLEAN |
| 作成 | CLEAN | CLEAN | CLEAN |
| 作製 | CLEAN | CLEAN | CLEAN |
| 探る | CLEAN | CLEAN | CLEAN |
| ささやく | CLEAN | CLEAN | CLEAN |
| 刺さる | CLEAN | CLEAN | CLEAN |
| さじ | CLEAN | NEEDS FIX (R-06, nit) | CLEAN |
| 座敷 | CLEAN | CLEAN | CLEAN |
| 差し支え | CLEAN | CLEAN | CLEAN |
| 差し引き | CLEAN | NEEDS FIX (R-06, nit) | CLEAN |
| 刺身 | CLEAN | CLEAN | CLEAN |
| 刺す | CLEAN | NEEDS FIX (R-01) | NEEDS FIX (R-01) |
| 挿す | CLEAN | CLEAN | CLEAN |
| 注す | CLEAN | CLEAN | NEEDS FIX (R-05, nit) |
| 射す | CLEAN | CLEAN | CLEAN |
| さすが | NEEDS FIX (R-02) | CLEAN | NEEDS FIX (R-03) |

- **作者 reuse:** CLEAN on all three facets.
  - It teaches the 作者 spelling, the さくしゃ reading, and creators of both written and non-written works (JMdict 1297710, sense 1).
  - Its N2 level, title and 作家 exclusion are preserved. The receipt says the file is unchanged, and I could not diff it myself.
- **`kanji\刺.md` edit:** CLEAN on all three facets.
  - It adds links to 刺す at さ.す, 刺さる at さ.さる and 刺身 at さし.
  - All six reading rows (シ, さ.す, さ.さる, さ.し, さし, とげ) are kept, and the common-words glosses match the new articles.
- **Twenty mappings (N2:602–621):** CLEAN on all three facets.
  - Every entry ID, spelling, reading and selected/additional sense matches the article text.
  - Spelling restrictions are respected: 裂く senses 1/3 versus 割く-only sense 4, 注す versus 点す, and the search-only 螫す and 索隠.
  - The raw "to stab" gloss in N2:617 depends on the article gap in R-01.

## Findings
**B31-R-01 · Minor · coverage/comprehensibility · `words\刺す.md:16-22`**
- **Problem:** The article says only that "the pointed thing can take を and its destination に". It never teaches the more common pattern where the pierced target takes を and the instrument takes で. The passive example 蚊に刺されました has the active form 蚊が私を刺す, which is left unexplained, and the source gloss "to stab" (N2:617) is never shown.
- **Remedy:** Add a target-を line, for example ナイフで人を刺す or 蜂が腕を刺した.
- **Evidence:** Daijisen 刺す 1㋐ gives 「短刀で胸を刺す」 and 「指にとげを刺す」; 1㋑ gives 「ハチに刺される」.
- **Confidence:** High.

**B31-R-02 · Minor · correctness (metadata) · `words\さすが.md:6,8`**
- **Problem:** The article uses `type: jukujikun` and the tag `jukujikun` on a kana headword. That describes how the spelling 流石 is read, not where the word comes from. Repo precedent for kana-primary words with irregular or ateji spellings uses word origin:
  - まじめ, くたびれる, とにかく, すてき and かわいそう are all `wago`.
  - たばこ (煙草) is `gairaigo`.
- **Remedy:** Change the type and tag to `wago`, and keep the 流石 explanation at line 27.
- **Evidence:** Nikkoku derives さすが from native さ + す + がに.
- **Confidence:** Medium. `content-format.md:63` states no explicit rule for kana-primary words.

**B31-R-03 · Nit · comprehensibility · `words\さすが.md:45` (with `:39`)**
- **Problem:** Line 45 says 'English "still" here is not…', but "still" never appears earlier. Line 39 glosses さすがに only as "all the same; after all", so the reference dangles.
- **Remedy:** Add "still" to the gloss at line 39, or reword line 45.
- **Confidence:** High.

**B31-R-04 · Minor · correctness (quiz) · `words\削除.md:9`**
- **Problem:** 削除 and 削る do not exclude each other.
  - 削る's title is "shave; pare; cut down", but its body teaches deleting text (`削る.md:23-25`, 不要な一文を削りました) and it already excludes 消す ("erase").
  - When 削る is the prompt, 削除's title "deletion; erasure" is therefore a correct, taught meaning appearing as a wrong answer.
  - 削る is absent from the evidence's comparison labels.
- **Remedy:** Add 削る to 削除's `quiz_exclusions`.
- **Confidence:** Medium.

**B31-R-05 · Nit · comprehensibility · `words\注す.md:24`**
- **Problem:** "酒をさす … is serving or offering sake, not growing rice for it" contrasts with something no learner would assume. The phrase 酒をさす is also not attested verbatim; Daijisen's 差す/注す/点す sense 1 gives 「杯を―・す」 for offering sake.
- **Remedy:** Use 杯をさす ("offer someone a cup of sake") and drop the rice clause.
- **Confidence:** Medium. I am not claiming 酒をさす is unnatural.

**B31-R-06 · Nit · coverage (links) · `words\さじ.md:33`, `words\差し引き.md:39`**
- **Problem:** Two existing word cards are mentioned in comparison sections without links:
  - さじ mentions 箸, but `words\箸.md` exists.
  - 差し引き mentions 足す, but `words\足す.md` exists; 注す.md does link it.
- **Remedy:** Add the two links.
- **Confidence:** High.

**Checked and cleared:**
- **Exclusions:** These looked over-broad but are supported by JMdict senses:
  - 注す/引く: 引く "to apply (e.g. lipstick)".
  - 注す/こしらえる: "to put on (one's makeup)".
  - 刺さる/動く: "to be touched".
  - ささやく/流す: "to circulate (a rumour)".
- **Constructions:** These are supported by Daijisen:
  - 差し引き: 「前貸しの分を差し引きする」 and "体温の上がり下がり".
  - 挿す: 「腰に大小を挿す」.
  - さじ: the 茶匙 origin.

## Optional
- **Quiz exclusions to consider:**
  - 座敷/宴会: 座敷's taught party sense versus 宴会's "banquet; party".
  - 挿す/生け花: the flower-arranging use is taught, and 生け花 was captured but not excluded.
  - Borderline label pairs: さすが/はず, ささやく/ざわざわ and 差し支え/迷惑.
- **Content polish:**
  - Note that JMdict flags 差引 as irregular okurigana (`差し引き.md:33`).
  - Recognise figurative 刺す (Daijisen sense 6: 鼻を刺す, 胸を刺す).
- **Pre-existing, outside this batch:** 作者 and 著者 ("author") do not exclude each other.

## Limits
- I could not run Git or hashes; the match between the files I read and the commit rests on the receipt.
- I read the comparison families only through targeted searches, so other missing exclusions may exist.
- I did not run the app's quiz draws, and nothing here is a native-speaker certification.
- **Dictionary checks:**
  - Weblio pages returned no dictionary text.
  - I fetched Daijisen for only the five headwords listed under Scope and relied on JMdict for the rest.
  - The public receipts are the author's paraphrases, and the standalone さすがに lookup failed; I did not retry it.
