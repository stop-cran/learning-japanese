## Snapshot
- **Corrected commit:** `ac0cd0dad60a22949c65d11e9f1c016e6d6c8a4d`
- **Parent:** `7f42dbaf6ee9651095fe53f7b0efaf32b346c068`
- **Basis:** the commit comes from `batch-47-correction-snapshot.json`. I reviewed committed content only, as described by that receipt.
- **Git limit:** file tools cannot check Git, cleanliness, blob hashes or equivalence. I did not inspect `.git`.

## Scope
**Model:** claude-opus-5.5 (Claude family). This is a resumed confirmation of my own initial review, not a fresh blind review.

**Completely reread (corrected working tree):**
- `words\先頭.md`, `全般.md`, `創作.md`, `草履.md`, `騒々しい.md`, `増大.md`, `そっと.md`

**Evidence read this round:**
- The correction receipt and `batch-47-correction.patch`.
- `batch-47-corrections-comparison-reading.txt`: complete JMdict families for ざわざわ, 下駄, 架空, 丸 (まる and がん), 激増, 表 (1489340 and 1489350) and 騒々しい.
- `batch-47-corrections-existing-reading.txt`: complete old bodies of 激増, 丸, 下駄, ざわざわ, 架空 and 表.
- `batch-47-corrections-public-inspection.json`.
- From `batch-47-corrected-review-evidence.json`: the author's fresh-inspection block, the adjudications and the start of `currentQuizDeclarations` (lines 21840–21960 only).

**My own fetch:** Kotobank 精選版日本国語大辞典 「騒騒しい」. It returned the full lexical body and the etymology note (補助注記).

**Spot-checks (grep only, not rereads):**
- Front matter of the six guard-partner cards.
- TSV rows N2:922, 936, 939 and 941.
- The reciprocal lines in the 般, 線, 減, 庫 and 造 kanji cards.
- The link lines in 広告, 頭, 扇子 and 下駄.

**Inherited from my initial review (not reread):**
- The 13 unchanged new articles: センチ, 宣伝, 扇風機, 線路, 相違, そういえば, 雑巾, 増減, 倉庫, 相互, 葬式, 造船, 送別.
- The five kanji edits, the four link-only edits and all twenty mappings.

**Not read:** the selected-family renderings 01–12 and the rest of the corrected evidence JSON. I also did not read any forbidden notes, reviews, reports, receipts, `batch-47.json` or the other reviewer's output.

## Verdicts
Each row gives correctness / scoped coverage / comprehensibility.

| Row | Article | Status | Correctness | Coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:922 | センチ | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:923 | 宣伝 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:924 | 先頭 | new, **reread** | CLEAN | CLEAN | CLEAN |
| N2:925 | 全般 | new, **reread** | CLEAN | CLEAN | CLEAN |
| N2:926 | 扇風機 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:927 | 線路 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:928 | 相違 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:929 | そういえば | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:930 | 雑巾 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:931 | 増減 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:932 | 倉庫 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:933 | 相互 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:934 | 創作 | new, **reread** | CLEAN | CLEAN | CLEAN |
| N2:935 | 葬式 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:936 | 造船 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:937 | 騒々しい | new, **reread** | CLEAN | CLEAN | CLEAN |
| N2:938 | 増大 | new, **reread** | CLEAN | CLEAN | CLEAN |
| N2:939 | そうっと → そっと | **reused**, **reread** | CLEAN | CLEAN | CLEAN |
| N2:940 | 送別 | new, inherited | CLEAN | CLEAN | CLEAN |
| N2:941 | 草履 | new, **reread** | CLEAN | CLEAN | CLEAN |

- **Five kanji (般, 線, 減, 庫, 造):** CLEAN, inherited. The spot-check found the reading-row and Common-words links at ハン (written パン in the word), セン, ゲン, コ and ゾウ.
- **Four old links (広告, 頭, 扇子, 下駄):** CLEAN, inherited and spot-checked.
- **Reused そっと:** CLEAN, reread. ID, reading そっと, title, N3 level, wago type and tags, and the original teaching are preserved. The only change is line 26.
- **Mappings:** CLEAN, inherited. In the spot-checked rows the blank raw gloss, the そうっと aliases, the separately qualified センチ sense 3 and the two 造船 POS observations are unchanged.

## Findings
- **B47-F1 (草履/下駄): RESOLVED.** `草履.md:9` now excludes 下駄. 下駄's body describes "traditional Japanese wooden sandals", which overlaps the 草履 title.
- **B47-F2 (増大/激増): RESOLVED.** `増大.md:9` now excludes 激増 ("sharp increase").
- **B47-F3 (先頭/表): RESOLVED.** `先頭.md:9` now excludes 表. Both titles share "front" (表 = JMdict 1489340 sense 3). The old 正面/表 guard is not relied on.
- **B47-F4 (騒々しい classification): RESOLVED.**
  - `騒々しい.md:6,8` now use kango, following `content-format.md:63` for on-first mixed words.
  - Lines 32–37 call it a mixed formation, deny any settled historical claim, and contrast さわ in 騒がしい.
  - My own Kotobank fetch confirms the body: it says 「騒騒」は当て字か, lists 騒々し, 躁々し and a sound-change (音便) theory from さわさわ, leans toward 忩々 (also on-based), and notes the 日葡辞書 spelling sôzô.
  - The title's "unsettled" matches the entry's 世の中が不安で落ち着かない.
- **Optional そっと wording: RESOLVED** (`そっと.md:26`, "separate words").
- **New guards, all assessed CLEAN and not excessive:**
  - 全般/丸: shared "whole"; 丸 sense 2 and its taught 丸一年 use.
  - 創作/架空: 創作's "fabrication" against 架空's "imaginary". The かくう-only restriction is respected.
  - 騒々しい/ざわざわ: commotion noise (1005430:1).
  - Each guard is declared once, applies symmetrically, and is not chained to other guards.
- **New actionable findings:** none.

## Optional
- 宣伝 boastful-exaggeration sense, and 〜に相違ない under 相違. The author declined both; they remain nonblocking.
- 葬式/サービス stays a weak but harmless precaution.
- 騒々しい could name 忩々 as the theory the dictionary leans toward. This is not needed.

## Limits
- I could not verify the commit, cleanliness or hashes from Git.
- Inherited judgments rely on my initial reads; those files were not reread this round.
- I did not read selected-family renderings 01–12 this round.
- そういえば still has no public lexical body.
- My Kotobank read used a tool-rendered page, so it is not byte-authenticated.
- I ran no live quiz test, and nothing here is native-speaker certification.
