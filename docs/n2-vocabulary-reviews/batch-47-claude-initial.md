# Batch 47 review: N2:922–N2:941

## Snapshot
The frozen commit is **7f42dbaf6ee9651095fe53f7b0efaf32b346c068** (parent 65f15e38eccebb81b697be187c8702bf85265fa5), recorded as committed content only. I found that `.git\HEAD` points to `refs/heads/jlpt-n2-vocabulary`, and that ref file holds the same commit. My file tools can't run Git, so I did not check whether the working tree is clean, compare blob hashes, or confirm the author's equivalence checks. I read the working-tree files.

## Scope
- **Model:** claude-opus-5.5 (claude family). No agents, no edits.
- **Rules read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, `docs\content-format.md:18-126`.
- **Articles read in full:** all 19 new articles and the reused `words\そっと.md`.
- **Related files read in full:** the patch, the five kanji cards (般, 線, 減, 庫, 造) and the four link-only cards (広告, 頭, 扇子, 下駄).
- **Evidence read:**
  - Private files: frozen receipt, mappings JSONL, principal-reading.txt, labels JSONL (195), components JSONL (36), public-bodies.txt.
  - Parts of evidence.json: header, rows and inspection receipts.
  - Repository: the assigned `docs\n2-vocabulary-sources.tsv` rows and the snapshot header.
- **Other existing cards:** I checked actual titles and quiz_exclusions by searching `words\`, including 激増, 表, 正面, 下駄, 車庫, 小屋, 騒ぎ, ざわざわ, 騒がしい, 勤め, サービス and いちばん. I also checked that link targets and kanji cards exist.
- **One fresh fetch:** Weblio そういえば.
- **Not read:**
  - Private evidence: selected-families 01–12, additional-comparison-reading.txt, principals.jsonl and public-bodies.json.
  - `docs\n2-source-snapshot.json`.
  - The rest of evidence.json.
  - All forbidden files.

## Verdicts

Cells are correctness / scoped coverage / comprehensibility.

| Row | Article | Verdict |
|---|---|---|
| N2:922 | センチ (new) | CLEAN / CLEAN / CLEAN |
| N2:923 | 宣伝 (new) | CLEAN / CLEAN / CLEAN |
| N2:924 | 先頭 (new) | NEEDS FIX (F3) / CLEAN / CLEAN |
| N2:925 | 全般 (new) | CLEAN / CLEAN / CLEAN |
| N2:926 | 扇風機 (new) | CLEAN / CLEAN / CLEAN |
| N2:927 | 線路 (new) | CLEAN / CLEAN / CLEAN |
| N2:928 | 相違 (new) | CLEAN / CLEAN / CLEAN |
| N2:929 | そういえば (new) | CLEAN / CLEAN / CLEAN (supported by JMdict only; see Limits) |
| N2:930 | 雑巾 (new) | CLEAN / CLEAN / CLEAN |
| N2:931 | 増減 (new) | CLEAN / CLEAN / CLEAN |
| N2:932 | 倉庫 (new) | CLEAN / CLEAN / CLEAN |
| N2:933 | 相互 (new) | CLEAN / CLEAN / CLEAN |
| N2:934 | 創作 (new) | CLEAN / CLEAN / CLEAN |
| N2:935 | 葬式 (new) | CLEAN / CLEAN / CLEAN |
| N2:936 | 造船 (new) | CLEAN / CLEAN / CLEAN |
| N2:937 | 騒々しい (new) | NEEDS FIX (F4) / CLEAN / NEEDS FIX (F4) |
| N2:938 | 増大 (new) | NEEDS FIX (F2) / CLEAN / CLEAN |
| N2:939 | そっと (reused) | CLEAN / CLEAN / CLEAN |
| N2:940 | 送別 (new) | CLEAN / CLEAN / CLEAN |
| N2:941 | 草履 (new) | NEEDS FIX (F1) / CLEAN / CLEAN |

- **Five kanji edits (般, 線, 減, 庫, 造):** CLEAN. Each new word sits in the right reading row (般's ハン row notes it appears as パン; 線 セン, 減 ゲン, 庫 コ, 造 ゾウ) and in Common words, and each JMdict entry ID was added.
- **Four link-only edits (広告→宣伝, 頭→先頭, 扇子→扇風機, 下駄→草履):** CLEAN. All are additive and accurate.
- **Preservation of そっと:** CLEAN. The ID, reading, title, `jlpt: 3`, tags and original teaching are unchanged. The そうっと paragraph, the example and the Daijisen link are additive. Daijisen's 「そっと」を強めた言い方 ("an emphatic form of そっと") and JMdict's unrestricted alias readings support it.
- **Mappings:** CLEAN for all twenty.
  - The one-based selections match the principal records.
  - N2:939 keeps its blank kanji and gloss and maps to the level-3 article.
  - N2:922's sense 3 is qualified as not independently assigned to N2.
  - The 造船 article keeps the JMdict intransitive label and the Daijisen タンカーを造船する example as separate observations.

## Findings

**B47-F1** (Minor; quiz guard; medium-high confidence)
- **Location:** `words\草履.md:4,9`.
- **Problem:** The title "zori; traditional Japanese sandals" and 下駄's title "wooden sandal" are both acceptable answers for 下駄. 下駄's own body (`words\下駄.md:15`) calls geta "traditional Japanese wooden sandals". The two cards share the kango, noun and clothing tags, so they are likely to appear as each other's distractors.
- **Fix:** Add 下駄 to `quiz_exclusions` (or narrow the title, for example to "zori; flat thonged sandals").

**B47-F2** (Minor; quiz guard; high confidence)
- **Location:** `words\増大.md:9`.
- **Problem:** 増大 is not guarded against 激増 ("sharp increase; sudden rise"). 激増 already excludes 増加 ("increase; rise") because "increase" fits both, and the same reasoning applies to 増大's "enlargement; increase". The two cards share the 増 kanji and four tags.
- **Fix:** Add 激増.

**B47-F3** (Minor; quiz guard; medium confidence)
- **Location:** `words\先頭.md:9`.
- **Problem:** 先頭 excludes 正面 ("front; frontage") and 前, but not 表 ("front; outward-facing side"). 正面 itself excludes 表, so the repository already treats a shared "front" as needing a guard.
- **Fix:** Add 表.

**B47-F4** (Minor; metadata and explanation; medium confidence)
- **Location:** `words\騒々しい.md:6,8,32-33`.
- **Problem:** The card has `type: wago` and a `wago` tag, and the body says "The native-adjective classification…". But そう is 騒's on reading ソウ (KANJIDIC ja_on), repeated as ぞう. `docs\content-format.md:63` says to use `kango` for an on-first word and to state in the body that it is mixed. The body also never contrasts this with the native さわ in 騒ぐ/騒がしい, which learners need to tell そうぞうしい from さわがしい. No existing `*しい` card is typed kango, so there is no precedent either way.
- **Fix:** Use `kango` and a kango tag. Replace lines 32-33 with: "そう is the on reading ソウ of 騒 plus the adjective ending しい; compare the native さわ in 騒ぐ."

## Optional
- `words\そっと.md:26`: "not separate verbs" would read better as "not separate words" (そっと is an adverb).
- 宣伝 could mention Daijisen sense 2, boastful overstating (自分の手柄のように宣伝する). JMdict has only one sense.
- 相違 could mention the separate expression 〜に相違ない.
- 葬式's exclusion of サービス is only weakly needed. It mirrors 儀式 and is harmless.

## Limits
- I ran no Git commands, hash checks or equivalence checks.
- The public bodies are the author's captures. For そういえば the author's capture failed, and my own fresh fetch of the Weblio page also showed no dictionary text, so its only support is JMdict.
- I didn't read the selected-family renderings, the supplemental comparison file or the full 194-family union. Guard conclusions rest on actual card titles and exclusions, not the remaining JMdict family records.
- I didn't run the automatic distractor selection, so tag-based pairing is inferred.
- This is not a native-speaker certification.
