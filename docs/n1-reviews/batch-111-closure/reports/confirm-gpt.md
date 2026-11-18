Snapshot: bf9ee9622723078438a021d54cac5ce8252f95d8, compared with 3b30803e33438dab7a1071aea34ceb7764189c1f. Reviewer: GPT-6.1 Sol (model ID: gpt-6.1-sol).

Scope:

The six revised cards were read completely, including unchanged passages, and every changed hunk was checked against all four facets. The nine unchanged cards retain their initial content review; their meaning options and reading prompts were checked again in this round. No word article or stroke file changed.

Files opened in `confirm-111-bf9ee962-gpt`:

- **Full:** `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`, and `evidence\README.md`.
- **Full:** `snapshot\kanji\房.md`, `snapshot\kanji\敷.md`, `snapshot\kanji\節.md`, `snapshot\kanji\義.md`, `snapshot\kanji\評.md`, and `snapshot\kanji\鏡.md`.
- **Full:** `checks\quiz-safety.txt`, `checks\reading-options.txt`, `checks\reading-exposure.txt`, and `checks\link-targets.tsv`.
- **Full:** `evidence\QuizBuilder.kt`, `evidence\KanjiReadings.kt`, `evidence\Words.kt`, and `evidence\kanjidic2-judge.xml`.
- **Full:** `evidence\joyo\p34.txt`, `p39.txt`, `p93.txt`, `p132.txt`, `p134.txt`, and `p142.txt`.
- **Partial:** `evidence\jmdict-cited-entries.xml`; inspected complete entries 1291990, 1386140, 1490070, 1497020, 1497030, 1497040, 1497060, 1500150, 2845184, and 2862467.

Files opened in the original `batch-111-3b30803e` packet:

- **Partial:** `titles\kanji-titles.tsv`, 76 relevant title records; `titles\word-titles.tsv`, the four records for 敷く, 敷地, 座敷, and 風呂敷.
- **Partial:** `snapshot\kanji\句.md` and `snapshot\kanji\旬.md`, lines 1-16; `repo\kanji\税.md`, lines 1-22; `repo\kanji\混.md`, lines 43-52.
- **Complete file processed, selected output inspected:** `snapshot\kanji\義.md`, for the original paragraph/token counts and exclusion line.
- **Targeted lookup:** `evidence\jmdict-families.xml`, streamed for exact written forms 房州 and 房総 only; unrelated entries were discarded. Neither written form occurs in that pinned extract.

Independent public sources inspected were the actual Daijisen entries on Weblio for [房](https://www.weblio.jp/content/%E6%88%BF), [敷](https://www.weblio.jp/content/%E6%95%B7), [判](https://www.weblio.jp/content/%E5%88%A4), and [鏡](https://www.weblio.jp/content/%E9%8F%A1), including 鏡's difficult-reading section; the relevant Jisho/JMdict entries returned for [眼鏡](https://jisho.org/api/v1/search/words?keyword=%E7%9C%BC%E9%8F%A1), [節](https://jisho.org/api/v1/search/words?keyword=%E7%AF%80), and [旬](https://jisho.org/api/v1/search/words?keyword=%E6%97%AC); and the [KANJIDIC2 DTD](https://www.edrdg.org/kanjidic/kanjidic2_dtdh.html). Dictionary pages/results were inspected in relevant parts, not as whole sites or result sets; the DTD was read in full.

The additional revisions are supported:

- 房:25 now uses the Daijisen's actual ボウ examples 房州 and 房総, separately attributing 安房 あわ to JMdict. This no longer presents あわ as a ボウ example.
- 敷:34-39 correctly distinguishes word-initial 敷地/敷居/敷金 from the final-element examples. The Daijisen actually prints the stated slash-separated groups; the card identifies their positions without pretending the dictionary labels those groups. Its account of the Joyo しく row, including 屋敷, matches page 134. The suffix explanation is consistent with the repository example inspected and does not over-attribute the hyphen's side to the DTD.
- 節:36,39's suffix wording agrees with the leading-dash convention. The additional noun sense at :25 is an exact JMdict gloss. The changes do not contradict the other reading rows or Joyo qualification.
- 鏡:25,39,56's separate 眼鏡 がんきょう entry and gloss are supported by JMdict 2862467 and the public entry. The Daijisen really lists 眼鏡 among キョウ compounds and separately as めがね. The revised explanation preserves the distinction from the whole-word reading めがね.

No changed hunk introduces a contradiction in the examples, sentences, mnemonic, coverage, or surrounding explanation. Changed-line links and quoted card titles were reconciled with the supplied link table and relevant title records.

All 15 meaning quizzes were inspected as complete four-choice sets: the target header supplies the correct title, and the three items after `options:` are the wrong choices. Every displayed wrong title remains defensibly wrong in both directions, including ordinary secondary senses and potential conflicts between wrong options. The reading review covered all 19 scheduled prompts in 18 card/kind pairs:

| Card | Meaning wrong choices | Reading prompts, on readings shown in katakana |
| --- | --- | --- |
| 修 | 秋, 州, 周 | シュウ |
| 句 | 包, 久, 苦 | ク |
| 房 | 戻, 防, 忙 | ボウ |
| 授 | 投, 樹, 押 | ジュ |
| 敷 | 放, 敬, 敗 | しく |
| 旬 | 純, 順, 旧 | ジュン |
| 標 | 兵, 氷, 秒 | ヒョウ |
| 独 | 毒, 読, 猫 | ドク; ひとり |
| 率 | 卒, 律, 栗 | ソツ; リツ |
| 節 | 雪, 殺, 笑 | セツ; ふし |
| 義 | 議, 疑, 技 | ギ |
| 製 | 世, 声, 袋 | セイ |
| 評 | 平, 氷, 表 | ヒョウ |
| 養 | 洋, 様, 葉 | ヨウ |
| 鏡 | 境, 銀, 鈍 | キョウ; かがみ |

Source inspection confirms that the meaning builder applies direct exclusions symmetrically to curated and fallback candidates, including against wrong options already chosen. It does not compute transitive exclusion groups. Reading selection instead uses normalized full metadata readings and their mutations, not meaning exclusions. Thus 義's three ギ distractor readings are skipped; 敷's selected kun forms share a scheduling stem and yield only the しく prompt.

An independent in-memory calculation from the reading audit, using the inspected normalization and mutation rules, matched all 19 reported protected-key counts and checked 777 visible curated/fallback candidate occurrences, including skip decisions and fallback tiers. This checks the displayed audit data, not omitted candidates, actual Android random draws, or caller-built pools.

Dispositions:

- #1 - RESOLVED - 節:14 adds precisely the direct 節/句 and 節/旬 pairs. The shared verse/season senses are independently supported; the displayed titles justify the exclusions. `QuizBuilder.kt`'s `excluded` and `tryAdd` guard both directions and both candidate paths. The unchanged 句 and 旬 metadata do not introduce a 句/旬 pair. All three cards retain three sound displayed distractors.
- #2 - RESOLVED - 税 is removed from 義:14 and :52, and the complete revised card contains no 税 reference. The unchanged 税 card explicitly means fiscal duty, not personal obligation; allowing this pair again is justified. 義's displayed distractors remain sound.
- OA - DECLINE ACCEPTED - Compression was optional, and the central teaching still precedes the supporting exclusion note. I independently obtain 101 whitespace-separated source tokens now and 105 before, including the bullet marker, and 81 tokens for the longest ordinary teaching paragraph. My initial estimate of roughly 200 English words was incorrect and is withdrawn.
- OB - RESOLVED - 評:35 now supplies the actual バン in 評判 ひょうばん. Both the pinned 判 record and the independent Daijisen entry attest バン as an on reading alongside ハン. This valid alternative fixes the learner-facing mismatch without requiring an unsupported historical account.
- L1 - PARTIALLY RESOLVED - The supplied meaning-builder source settles #1's custom-pool filtering consequence for every candidate passed to that implementation, independently of how `all` is constructed. What remains unverified is actual caller/pool construction, Android execution and random draws, and the installed build's compatibility. The supplied ports and sources cannot establish those facts, so L1 cannot be marked RESOLVED with nothing remaining open.

Verdicts:

- Correctness - CLEAN for the six revised cards; the nine unchanged cards retain their initial CLEAN verdict.
- Scoped coverage - CLEAN for all 15; no coverage regression established.
- Consistency and quiz safety - UNVERIFIED for runtime/pool-dependent claims across all 15 under L1. The revised content, direct exclusion guards, all displayed meaning quartets, and the inspected reading candidates pass the source-level review; no new content defect established.
- Comprehensibility - CLEAN for all 15; no regression established, and the suffix and 評判 explanations are clearer.

Confirmation: UNVERIFIED - #1 and #2 are fixed, OA's decline is accepted, OB is resolved, and no new actionable defect was established. The contract does not permit CONFIRMED while L1 remains partially resolved.

Findings: None.

Optional: None.

Limits:

- The Kotlin builders accept supplied card collections; the packet does not establish their actual caller-built stack/session pools or the version installed on a phone. No APK or running client was supplied or executed. The source proves the exclusion guard, not deployment or exact displayed runtime draws.
- The reading audits are author-written ports. Their six unchanged latent cases are 房 お and わ; 節 よ under two prompts; 養 や; and 鏡 あき. Their reported zero production/padded-session hits remain conditional on the supplied pool assumptions and sampling. I checked the source mechanics and all visible candidate lists, but did not independently reconstruct those pools, enumerate abbreviated candidate tails, or reproduce the author's all-card absence scan. These are not new findings.
- Joyo claims were checked against all six supplied page extracts, not independently rendered PDF pages. Live public dictionary entries were checked alongside the pinned entries, without assuming their versions are identical.
- No other reviewer's report was sought or opened. All tool calls were serial, one per response; no agents, other sessions, background jobs, recursive directory listings, or repository-checkout reads were used. The only file written was this report.
