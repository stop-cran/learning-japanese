# Batch 159 revision: what changed from bad899ea to 33c3b582

The revised snapshot is `33c3b582`, “N1 B159: link the new 又, 偏 and 即 cards from stale remarks”, one commit whose parent is `bad899ea`. The range has no merges. Every commit from the reviewed freeze `1a9bb910` through `33c3b582` is signed with key D4C9A275A218AF747B787AFA9D94B9D311BD26A7 (`evidence\verify-commit.txt`).

The author made this revision after all three confirmation reports on `bad899ea` confirmed it; no finding is open. Preparing the closure, the author ran a scan for sentences saying that a kanji has no card. The publication checks of B157 and B158 had not run this scan, so B158's review did not see it. It found five remarks that are no longer true: three name 又, which this batch adds a card for (in 及, 堅 and 暇), and two name 偏 (in 狭) and 即 (in 節), both carded in B158. This revision rewrites each of the five into a link to the new card. The scan is described below and is in this packet as `evidence\stale_remarks.py`.

`RESPONSE.md` answers your own report only.

- **Changed:** one line in each of `kanji/及.md` (27), `kanji/堅.md` (29), `kanji/暇.md` (27), `kanji/狭.md` (46) and `kanji/節.md` (55). In the ledger `docs/n1-sources/batch-159-progress.json`: five new entries at the end of `changedReusedPassages` (lines 268–292; `diffs\changed-lines.txt` gives 267–291 because Git aligns the inserted block one line earlier), `mechanicalChecks.batchAudit` (line 971), the new `mechanicalChecks.staleRemarks` (line 972) and `mechanicalChecks.n1Lint` (line 974).
- **Unchanged:** the ten batch cards, the nine new word articles, every other card and word article, the rest of the ledger, `tools/`, and the pinned JMdict selection and extract.
- **Generated file:** `manifest.json` is rebuilt; its contentVersion changes from `18c1f24ea8d2caf8` to `44a04d20d52264cd` because five cards changed.

## The five card lines

Each rewrite replaces the “no card” wording with a link to the card, followed by that card's title in quotation marks. This is the form these lines already use for other parts, for example `[臣](臣.md), "retainer; subject,"` on `kanji/堅.md:29`. The titles are those of `kanji/又.md` (“again; also; or”), `kanji/偏.md` (“lean to one side; biased”) and `kanji/即.md` (“immediate; at once”). The rest of each line, including the mnemonic disclaimers, is unchanged.

- `kanji/及.md:27`: “Its key is 又, which has no card here.” becomes “Its key is [又](又.md), "again; also; or."”
- `kanji/堅.md:29`: “又, a small hand-like shape with no card here, at the top right” becomes “[又](又.md), "again; also; or," a small hand-like shape, at the top right”.
- `kanji/暇.md:27`: “with 又 at its lower right; neither 又 nor the whole right-hand shape has a card yet.” becomes “with [又](又.md), "again; also; or," at its lower right; the whole right-hand shape has no card yet.” The whole right-hand shape (叚 in KanjiVG) still has no card.
- `kanji/狭.md:46`: “偏狭 uses 偏, which has no card here.” becomes “偏狭 uses [偏](偏.md), "lean to one side; biased."”
- `kanji/節.md:55`: “The 即 below the bamboo does not have a kanji card here.” becomes “The part below the bamboo is [即](即.md), "immediate; at once."”

No component statement is new: each line names the same part in the same place as before. The KanjiVG records at the pinned revision show these parts: `evidence\kanjivg\053ca.svg` (及: 丿 and 又), `05805.svg` (堅: 臣, 又 and 土), `06687.svg` (暇: 日 and 叚, with 又 inside 叚) and `07bc0.svg` (節: 竹 over 即).

## The ledger

- **`changedReusedPassages`, lines 268–292:** five new entries, one per card above, each with the full old line (`before`) and the full new line (`after`). They should equal the diff.
- **`batchAudit`, line 971.** It said “10 changed existing articles (including the reused kana-headed articles または and また, …)”. It now says “15 changed existing articles (eight reused cards that add or link one Common words line, the reused kana-headed articles または and また, which now record the kanji spellings 又は and 又 in their support mappings, and the five cards 及, 堅, 暇, 狭 and 節, whose stale “no card” remarks now link the 又, 偏 and 即 cards)”. The rest is unchanged.
- **`staleRemarks`, line 972 (new):** “lean stale_remarks.py over all kanji and word articles: 0 stale remarks. It finds each sentence with a card-absence phrase such as “has no card here” or “does not have a kanji card here”, takes as the remark's subject the last kanji written outside a link before the phrase, other than the card's own kanji, and flags the remark as stale if that kanji has a card. Remarks worded outside its phrase list are not found. The five remarks B159 rewrites (又 in 及, 堅 and 暇; 偏 in 狭 and 即 in 節, both carded in B158) are no longer flagged. One reviewed exception: kanji/悟.md line 46 says the right part of 悟, 五 over 口, has no card of its own; it is about that whole part, which has no card, not about 口. The scan lists the other 37 remarks with a subject; the author read each, and each is about a kanji or part that has no card. It also lists 8 remarks with no kanji before the phrase, which it cannot check; the author read them: seven are about parts or kanji that have no card (the left part of 敵, the right-hand parts of 暇 and 瞬, the shape below the two trees in 礎, and 塞, 櫛 and 釘 in their word articles), and the one in words/こっそり.md is about a greeting card.”
- **`n1Lint`, line 974.** It said “Of the 42 warnings, 40 are on reused cards and words. … B159 changes none of these fields, because it only adds or links one Common words line on each of those cards and does not change those word articles.” It now says “Of the 44 warnings, 42 are on reused cards and on word articles that lint checks because a changed card lists them; words/普及.md and words/調節.md are listed by 及 and 節. … B159 changes none of these fields: on eight reused cards it only adds or links one Common words line, on 及, 堅, 暇, 狭 and 節 it only rewrites one stale “no card” remark into a link, and it does not change those word articles.” The three errors and the two warnings on `kanji/又.md` are described as before.

## The stale-remark scan

`evidence\stale_remarks.py` is the lean pipeline's scanner; it is not part of the repository's `tools/`. `checks\stale-remarks.txt` is its output on `33c3b582`, run by the check runner with one reviewed exception (`kanji/悟.md:46`). It scanned 6831 articles (1608 kanji cards) and reports 0 stale remarks, the 悟 exception, 37 remarks whose subject has no card, and 8 remarks with no kanji before the phrase, which it lists with their sentences but does not check. It exits 1 if a remark is stale or a reviewed exception is unused. The scan finds only the phrases in its list, so a remark worded differently is not found.

## Checks run on the revised snapshot (outputs in `checks\`)

The outputs below differ from the `bad899ea` outputs. Every other output of the check runner, and every regenerated file in `evidence\` (`word-quiz.txt`, `distractor-use.tsv`, `distractor-senses.txt`, `corpus-attested.txt` and `meta-scan.txt`), is identical apart from the header line.

- **audit** (`tools\audit_n1_batch.py --batch 159`): exit 0; `changedReusedArticles` 10 → 15; 87 complete JMdict families; the manifest is fresh (`44a04d20d52264cd`).
- **budget:** retained 56,881,479 bytes (+53), inflated 57,317,551 (+53) and local ZIP 36,535,569 (+50). The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **lint:** exit 1 with the same 3 errors (on the reused cards 太 and 情, present at the batch base `2787e43b`) and 44 warnings (was 42). Lint now checks 23 kanji and 76 words (was 18 and 66) because five more cards changed. The two new warnings are “Dictionary: line cites no JMdict entry id” on `words/普及.md` and `words/調節.md`, which B159 does not change; the changed cards 及 and 節 list them.
- **manifest:** the rebuild leaves `manifest.json` unchanged (sha256 `01433AC8…6CC5` before and after); its version is `44a04d20d52264cd`.
- **stale-remarks:** new in this round; see above.
- **unittest:** 444 tests OK (only the run time differs).
- **Identical:** quiz-safety (0 errors, 0 warnings), reading-exposure (0 production hits, 0 padded-session hits), reading-options (0 problems), diffcheck (clean from the batch base `2787e43b`), validate (0 errors) and vocabulary (3201/3539).
- `checks\link-targets.tsv` is not a check output: the packet builder writes it for the changed lines of this packet's range only, so it differs between packets by design. In this packet it lists the 13 links on the five changed card lines: the five new links and the eight that were already on those lines. Each resolves, and the quoted gloss after it equals the target card's title.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Evidence

- `evidence\verify-commit.txt` adds `git verify-commit -v 33c3b582` and extends the `git log --show-signature` range to `33c3b582`.
- `evidence\reused-lint-diff.txt` is regenerated for `33c3b582` and now covers 22 files: the 20 earlier files and `words/普及.md` and `words/調節.md`, which B159 does not change (they do not appear in its diff). The diffs of the 20 earlier files are identical to those of the earlier file.
- `evidence\kanjivg\*.svg` (the four records named above), `evidence\stale_remarks.py`, and `evidence\kanji-偏.md` and `evidence\kanji-即.md` (the two B158 cards that the new links in 狭 and 節 point to; `kanji/又.md` is in `snapshot\`) are new.
- `evidence\jmdict-scan-c8.txt` and `evidence\support-selection.json` are identical to the earlier round's files.
