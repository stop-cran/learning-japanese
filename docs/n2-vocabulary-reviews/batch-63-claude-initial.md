I found four fixable issues in three articles (為す, 生意気, 馴れる); the other seventeen rows, the three kanji edits and all twenty mappings check out.

## Snapshot
Frozen commit `0cc62d83b0e932b0d0c45e332f9f070a37d2b19c` (parent `12f471e4155da073f704feffe7e99f75a0d244ac`). I reviewed committed content only. My file tools cannot run Git, so the commit and hash/equality checks are the author's, not mine.

## Scope
**Model:** claude-opus-5.5. Read-only; no agents, delegation or edits.

**Read in full:**
- **Instructions:** both instruction files, plus `docs\content-format.md:18-103` and a targeted grep of that file for its `type` and `quiz_exclusions` rules.
- **Snapshot and edits:** `frozen-snapshot.json` and `related.patch`.
- **Evidence files:** the mappings (20), principals (20), components (30) and labels (224) JSONL files, and `public-bodies.txt`.
- **TSV:** the header and rows N2:1242–1261 only.
- **Family chunks:** all 15 (`family-inspection-01`…`13` and `supplement-family-inspection-01`…`02`).
- **New articles:** all twenty.
- **Kanji cards:** all of `kanji\仲.md`, `並.md` and `極.md`.
- **Older articles:** all of `words\慣れる.md`, `打つ.md` and `作る.md`.

**Read in part:**
- `review-evidence.json`.
- Title, level and `quiz_exclusions` lines of about 100 other `words\` articles.
- Targeted body searches of 12 comparison articles (弾く, 演奏, 文句, 訴える, おとなしい, 無くす, 何とか, いろいろ, 何か, 叩く, 打つ, 作る).
- Several older articles with mixed kun+on readings, to check the `type` convention.
- A glob of `kanji\` to see which cards exist.

**Not read:**
- The 18 old-body chunks. I read the relevant older articles directly instead.
- Ledgers and `batch-63.json`.

**Web:** I fetched Weblio's Daijisen 為す page and its なせるわざ example-sentence page.

## Verdicts
Cells are correctness / scoped coverage / comprehensibility.

| Row | Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:1242 | 仲良し | CLEAN | CLEAN | CLEAN |
| N2:1243 | 慰める | CLEAN | CLEAN | CLEAN |
| N2:1244 | 亡くす | CLEAN | CLEAN | CLEAN |
| N2:1245 | なぐる | CLEAN | CLEAN | CLEAN |
| N2:1246 | 為す | **NEEDS FIX** (C-01, C-04) | CLEAN | CLEAN |
| N2:1247 | 謎謎 | CLEAN | CLEAN | CLEAN |
| N2:1248 | なだらか | CLEAN | CLEAN | CLEAN |
| N2:1249 | 懐かしい | CLEAN | CLEAN | CLEAN |
| N2:1250 | 撫でる | CLEAN | CLEAN | CLEAN |
| N2:1251 | 斜め | CLEAN | CLEAN | CLEAN |
| N2:1252 | なにしろ | CLEAN | CLEAN | CLEAN |
| N2:1253 | 何々 | CLEAN | CLEAN | CLEAN |
| N2:1254 | 何分 | CLEAN | CLEAN | CLEAN |
| N2:1255 | 生意気 | **NEEDS FIX** (C-02) | CLEAN | CLEAN |
| N2:1256 | 並木 | CLEAN | CLEAN | CLEAN |
| N2:1257 | 倣う | CLEAN | CLEAN | CLEAN |
| N2:1258 | 鳴らす | CLEAN | CLEAN | CLEAN |
| N2:1259 | 生る | CLEAN | CLEAN | CLEAN |
| N2:1260 | 馴れる | **NEEDS FIX** (C-03) | CLEAN | CLEAN |
| N2:1261 | 南極 | CLEAN | CLEAN | CLEAN |

Notes on specific rows:
- **何分:** なんぷん (entry 1189320) is kept separate, which is correct.
- **生る:** it is kept separate from なる "become", 成る and 鳴る.
- **馴れる:** the claimed extra tame-sense coverage is real. 慣れる.md cites only sense 1 of 1212670 and never teaches "tame."

**Kanji edits:** CLEAN for all three.
- 仲: 仲.md:31 (なか row), :38 (Common words), :46 (entry 1426100).
- 並: 並.md:31 (なみ row), :43, :50 (entry 1599640).
- 極: 極.md:28 (キョク row), :44, :55 (entry 1460180).
- Headers are preserved and the readings are the actual whole-word readings.
- Word-side links are substantive. Cards that don't exist (為, 慰, 懐, 撫, 斜, 倣, 馴, 謎, 殴) are listed in metadata but not linked.

**Baseline preservation:** CLEAN within scope. The patch only adds to the three kanji cards, and the 慣れる body teaches only the accustomed sense.

**Mappings:** 20/20 CLEAN. Every article's dictionary line matches its selected and additional senses.

## Findings
**B63-C-01** (moderate; correctness)
- **Location:** 為す.md:24-25.
- **Claim and impact:** The article says "The potential なせる appears in なせる業 … a feat or result that something can bring about." In 〜のなせる業, なせる is understood as classical なす + perfective り, not the modern potential. The phrase means "the work or doing of X," so the gloss teaches a false "capability" reading.
- **Remedy:** Gloss it as a fixed classical phrase, "the work of X" (e.g. 若さのなせる業), or delete the sentence.
- **Evidence:** Weblio examples 天のなせるわざ ("the work of heaven") and 大自然のなせるわざ ("the work of nature"). The Daijisen page does list a modern potential なせる, so only the phrase's analysis is wrong.
- **Confidence:** high on meaning; medium-high on the grammatical label.

**B63-C-02** (minor; correctness)
- **Location:** 生意気.md:29-30.
- **Claim and impact:** "The native reading combines 生 なま with 意 い and 気 き." い and き are on-readings, so なまいき is a mixed kun+on word.
- **Remedy:** Change it to "The mixed reading combines native なま with on-readings い and き." Keep `type: wago`.
- **Evidence:** 場所.md:24, 生地.md:25 and 荷物.md:21 all call this pattern mixed. content-format.md:63 says the body should say the word is mixed.
- **Confidence:** high.

**B63-C-03** (low; correctness)
- **Location:** 馴れる.md:36-37.
- **Claim and impact:** It says 慣れる "emphasizes getting used to something or becoming experienced in the existing article." The existing article does not teach "becoming experienced."
- **Remedy:** Delete "or becoming experienced in the existing article."
- **Evidence:** 慣れる.md:15 teaches getting used to something, :37 says "not necessarily … becoming highly skilled", and :41 cites only sense 1.
- **Confidence:** medium-high.

**B63-C-04** (low; correctness, quiz exclusions)
- **Location:** 為す.md:9 (`打つ`, `作る`).
- **Claim and impact:** Neither the titles nor the bodies overlap with 為す's "do; carry out." 打つ is "hit; strike" (physical sense only), and 作る is "make; prepare." 為す.md:42-46 explicitly keeps 成す's "form/make" meanings out. These guards rely on obscure, untaught senses (打つ sense 11, 作る sense 14), so they needlessly remove valid distractors.
- **Remedy:** Remove both entries.
- **Confidence:** medium.

## Optional
- **何々 exclusions:** `いろいろ` ("various") has weak support and may be inherited from the あれこれ group.
- **何々 examples:** line 20 is a contrived placeholder sentence, and line 21 could end in ？ instead of 、.
- **鳴らす exclusions:** `演奏` is a thin match; `弾く` is defensible because instruments can be 鳴らす'd.
- **Pairs I checked that need no guard:** 亡くす/無くす, 為す/なさる/致す and なだらか/坂. Their titles already tell them apart.

## Limits
- **Git:** I could not run Git, so I could not diff old words against the baseline.
- **Old-body chunks:** none of the 18 were read. Most comparison articles were checked only by title, exclusions or targeted searches.
- **Single authority:** all twenty public captures come from Daijisen via Weblio.
- **なせる業 sourcing:**
  - Several fetches failed: Weblio 404s for 為せる業, なせる業 and 成せる業, an irrelevant kotobank page, and an empty jisho result.
  - The Weblio example sentences are machine-collected.
  - The り analysis is my own judgment; no fetched source confirms it.
- **何分 source row:** its raw gloss "what minute?" conflicts with the kana なにぶん and entry 1189310. The mapping follows the kana and entry number; I can't establish what the list's compiler intended.
- **Native naturalness:** no native-speaker certification of example naturalness.
