## Snapshot
- **Frozen commit:** `ac708ffd2a4153211b420e63c2b0b8766319342d` (parent `5afbc88a0bc01a38f287973aea878916846ea3b0`).
- The local branch ref `jlpt-n2-vocabulary` contains this commit, and `.git\HEAD` points to that branch.
- I had file tools only, no Git execution. I could not confirm that the working tree is clean, check the commit's parent, or recompute the receipt hashes. "Committed content" therefore rests on the receipt plus that ref match.

## Scope
- **Model:** claude-opus-5.5 (Claude family), a fresh process working sequentially, with no agents and no edits.
- **New articles:** all 19 read completely.
- **Related edits:** the eight patched passages, checked in their surrounding context.
- **Reuse claim:** `奥さん.md`.
- **Sources checked:**
  - TSV rows N2:162–181 (`n2-vocabulary-sources.tsv`).
  - The pinned CSV, fetched raw.
  - `batch-09.json`: source rows, main and comparison entries, KANJIDIC components, author inspection receipts and source-access limits.
  - The four Kotobank pages the articles cite, which I fetched myself.
  - Existing word and kanji cards that are link, comparison or quiz targets.
- **Omissions:**
  - Unchanged teaching elsewhere in the eight related files is not reviewed.
  - The forbidden notes, reviews, ledgers and reports were not read.
  - I did not run a whole-repository search.

## Verdicts
Each cell gives correctness / scoped coverage / comprehensibility.

| Article | Verdict |
|---|---|
| おおざっぱ | CLEAN / CLEAN / CLEAN |
| 大通り | CLEAN / CLEAN / CLEAN |
| オートメーション | NEEDS FIX (F2) / CLEAN / CLEAN |
| オーバーコート | CLEAN / CLEAN / CLEAN |
| おおよそ | CLEAN / CLEAN / CLEAN |
| お帰り | CLEAN / CLEAN / CLEAN |
| おかけください | CLEAN / CLEAN / CLEAN |
| おかげさまで | CLEAN / CLEAN / CLEAN |
| おかず | CLEAN / CLEAN / CLEAN |
| 拝む | CLEAN / CLEAN / CLEAN |
| お代わり | CLEAN / CLEAN / CLEAN |
| 補う | CLEAN / CLEAN / CLEAN |
| お気の毒に | NEEDS FIX (F1) / CLEAN / CLEAN |
| 屋外 | CLEAN / CLEAN / CLEAN |
| 送り仮名 | CLEAN / CLEAN / CLEAN |
| 元気でね | CLEAN / CLEAN / CLEAN |
| 怠る | CLEAN / CLEAN / CLEAN |
| 押さえる | CLEAN / CLEAN / CLEAN |
| お先に | CLEAN / CLEAN / NEEDS FIX (F3) |

**Related edits: CLEAN / CLEAN / CLEAN for all eight.**
- 拝 and 補 now link their kunyomi table rows and Common-words entries.
- 毒 adds one Common-words line for お気の毒に and adds JMdict entry 2167510 to its metadata.
- おかげ, オーバー, コート, 外 and 気の毒 each gain a single navigation link.
- Every target exists, and the edits make no new teaching claims.

**Reuse claim (奥さん): CLEAN / CLEAN / CLEAN.**
- The card teaches おくさん (JMdict 1179330) at N5, as someone's wife and as a form of address for a married woman.
- No changed passage touches it. "Unchanged" rests on the receipt and patch file lists, since I could not run a Git diff.

**Explicit mappings: CLEAN / CLEAN / CLEAN.**
- **大凡 → おおよそ:** taught at `おおよそ.md:26-27`. JMdict marks the kanji forms rare and the word usually kana.
- **押える → 押さえる:** taught at `押さえる.md:19`. Seisenban Nihon Kokugo Daijiten (fetched myself) also lists 押える at おさえる.
- **元気でね:** the pinned CSV row is `2847540,げんきでね,元気でね,` with a blank gloss.
  - It sits between おくりがな and おこたる, an anomalous position in a list sorted by kana that suggests an お-initial sort key.
  - The article teaches the row's actual reading げんきでね, and mentions お元気で at line 33 without claiming the two are the same.
- **Kana-only rows おきのどくに and おさきに:** mapped to written forms in the same JMdict entries, and the kana is taught.
- **Other aliases:** 大雑把/大ざっぱ, お掛け下さい/おかけ下さい and お替わり are each taught explicitly in their articles.

## Findings
**F1 — Minor; correctness (quiz metadata). Confidence: medium.**
- **Where:** `words\お気の毒に.md:4,9,17,21,44`.
- **Problem:** neither ごめんなさい ("I am sorry", `ごめんなさい.md:4`) nor すみません ("excuse me; I am sorry", `すみません.md:4`) is excluded from お気の毒に's quiz choices.
  - The article teaches "I'm sorry to hear that" (lines 17 and 21), and so do `気の毒.md:18` and the new line in 毒.
  - English "I'm sorry" is a standard way to express sympathy.
  - In the Japanese-to-English quiz, a learner could reasonably choose "I am sorry" for お気の毒に and be marked wrong.
  - All three cards share the `expression` tag, so the quiz is likely to put them together.
  - The article itself warns against confusing it with すみません (line 44), and the author already excluded あいにく ("sorry, but").
- **Fix:** add すみません and ごめんなさい to the `quiz_exclusions` on line 9.

**F2 — Minor; correctness (quiz metadata). Confidence: medium.**
- **Where:** `words\オートメーション.md:2-9`. The front matter has no `quiz_exclusions`.
- **Problem:** the title "automation" overlaps with 自動's title "automatic operation" (`自動.md:4`). The common English definition of automation is essentially automatic operation, so a learner could reasonably accept either answer in both directions.
- **Evidence:** both cards carry the `technology` tag. JMdict glosses オートメーション (1032180) as "automation" and 自動 (1318340, sense 1) as "automatic". The article's own lines 33–34 contrast the two words.
- **Fix:** add `quiz_exclusions: [自動]` to オートメーション.md.

**F3 — Minor; comprehensibility (possible register mislabel). Confidence: medium that the sentence is unclear, low that learners would be materially misled.**
- **Where:** `words\お先に.md:42`, which reads: `Do not translate every お先に as historical "previously."`
- **Problem:** the article never teaches "previously" (line 16 gives only "before; ahead"). "Historical" is unexplained and may suggest the sense is archaic.
- **Evidence:** in `batch-09.json:402-407`, JMdict 1002280 sense 1, "before; previously", is tagged only as polite and carries no dated or archaic tag.
- **Fix:** state that the dictionary also glosses it "previously", but in invitations and departures it means "first/ahead". Drop "historical".

## Optional
- **お先に vs どうぞ:** consider an exclusion. どうぞ's title is "please; go ahead", its tags match お先に's, and the お先に article's own example renders どうぞ、お先に as "Please, go ahead." Confidence is low.
- **おおよそ vs ころ:** consider an exclusion. ころ's title is "approximate time; around". Confidence is low.
- **元気でね:** note that お元気で is the politer, non-familiar farewell.
- **Kanji links:**
  - お代わり could link the N2 card 替 where it mentions お替わり.
  - おかず could link the N2 card 菜 for the rare spelling お菜.
  - おおざっぱ could mention 把 in 大雑把.
- **お先に.md:19 and :21:** add kana glosses to the two examples that lack them, for consistency.

## Limits
- **Git:** HEAD matches the frozen commit, but I could not confirm the working tree is clean, the commit's ancestry, or the receipt hashes.
- **CSV:** I confirmed the relative order of the 20 rows; absolute line numbers rely on the TSV. The original Waller item behind 元気でね (possibly お元気で) is unverified.
- **Batch evidence:** `batch-09.json` holds only selected entries and is not the whole dictionary. KANJIDIC2 hashes were not recomputed.
- **Inspection receipts:** the author's receipts are assertions, not proof. I independently fetched the four cited Kotobank pages (current, not pinned), and they support the article claims.
- **Quiz behaviour:** I did not run the quiz candidate builder. How often pairs co-occur is inferred from the documented tag and kanji scoring.
- **Naturalness:** these are reviewer judgments, not native-speaker certification.
