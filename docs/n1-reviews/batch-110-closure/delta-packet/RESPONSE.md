# Author's statement for the delta reviewer of N1 kanji batch 110, snapshot 30f2bd7c

Bound to commit `30f2bd7c7b57e0d244a1cb86ba51e5b86121d4f8`, a direct child of `10d7965266b69ed81703ab69f20cff873a0526e9`, the snapshot your follow-up report reviewed. **F1** is finding 1 of your confirmation report (嫌 and the contracted reading や). **FU1**, **FU2** and **FU3** are findings 1 to 3 of your follow-up report. **L1**, **L3** and **C1 to C13** are the limits and claims of those reports; they stand as you dispositioned them. **D1 to D6** are the author's dispositions below and **N1 to N10** are the new claims at the end of this file. Everything here is the author's claim about what is true and why: verify each claim against the files named, and do not rely on this text as evidence. Cited line numbers are lines of the packet copies of the files. Everything said about the Android client applies to the pinned commit `10d98d0db61dcde621463460e6a1e59941b4042b` only.

## Short names

Files of this packet (paths relative to the packet root):

| Name | File |
| --- | --- |
| CARD | `snapshot\kanji\嫌.md` (CRLF working-tree bytes; 64 lines) |
| CHG | `CHANGES.md` |
| DP | `diffs\delta.patch` |
| MP | `diffs\manifest-delta.patch` |
| TSV | `evidence\cards-reading-metadata.tsv` |
| JM | `evidence\jmdict-cited-entries.xml` |

Files of earlier packets, which are unchanged (their roots are in `INSTRUCTIONS.md`):

| Name | File |
| --- | --- |
| FRESP | the follow-up packet's `RESPONSE.md` |
| DJ | the original packet's `evidence\public-source\weblio-嫌.txt` |
| KD | the original packet's `evidence\kanjidic2-records.xml` |
| FMT | the original packet's `repo\docs\content-format.md` |

The Android sources are exact git blobs of commit `10d98d0db61dcde621463460e6a1e59941b4042b` of the public repository `stop-cran/kanji-cards-android`. They are not repeated in this packet. They are in the follow-up packet under `evidence\android\`, where `SOURCES.tsv` has each file's blob id, SHA-256 and public raw URL.

| Name | File under `evidence\android\` of the follow-up packet |
| --- | --- |
| VM | `app\src\main\java\io\github\stopcran\kanji\ui\KanjiReadingViewModel.kt` |
| RD | `app\src\main\java\io\github\stopcran\kanji\data\ReadingData.kt` |
| PAD | `app\src\main\java\io\github\stopcran\kanji\data\Padding.kt` |
| ST | `core\src\main\kotlin\io\github\stopcran\kanji\core\srs\Stacks.kt` |
| KR | `core\src\main\kotlin\io\github\stopcran\kanji\core\reading\KanjiReadings.kt` |
| WD | `core\src\main\kotlin\io\github\stopcran\kanji\core\words\Words.kt` |

The author's own analysis files are under `checks\` (claims to verify, not evidence; `evidence\README.md` says how each was produced). **RO** = `reading-options.txt` (the reading-option audit; its 嫌 section is RO:159-180). **RX** = `reading-exposure.txt` (the exposure model; its 嫌 section is RX:163-188). **RUN-N** = `kotlin-reading-run.txt` (the real Kotlin code on the N1 and All pools and on small pools). **RUN-S** = `kotlin-starter-run.txt` (the real Kotlin code on Starter practice sessions). **XC** = `kotlin-vs-exact.txt` (the drawn options of RUN-N and RUN-S compared with the options the Python model calls reachable). These five are byte copies of the author's output files, so the cited line numbers are those of the original files; the other files of `checks\` have their blank lines removed.

## Corrections to the author's earlier statements

1. The decline of F1 is withdrawn. The four reasons under "Why the author did not change the card text" in FRESP are superseded by the change in D1. Proposals A and B of FRESP (a client-side exclusion of attested readings, and a generic prefix or suffix rule) remain owner proposals and are not counted as protection.
2. FRESP:95 listed the absence of the curated cards 兼, 験 and 好 among conditions that must hold "all together". That was too restrictive (FU1; D2).
3. FRESP:193-194 said that variants of one-kana readings are not generated. That was wrong (FU2; D3).
4. FRESP:198-200 said that JMdict entry 1587610 lists the readings いや, や and イヤ for 嫌. That was wrong as worded (FU3; D4).

## D1. F1 (嫌 and the contracted reading や)

**Author action: the decline is withdrawn and the mitigation you named is applied in `30f2bd7c`.** Your follow-up report would accept one path: remove only いや from `quizKunyomi`, leaving `[きら.う, きら.い]`, update the practice-selection paragraph, and preserve `kunyomi: [きら.う, きら.い, いや]`, the いや teaching row and its vocabulary coverage. The author did that and nothing more:

- CARD:12 is now `quizKunyomi: [きら.う, きら.い]`. The other front-matter lines are unchanged, including `kunyomi: [きら.う, きら.い, いや]` (CARD:10), `quizOnyomi: [ゲン]` (CARD:11), `distractors` (CARD:13) and `quiz_exclusions` (CARD:14).
- The いや row (CARD:37) keeps both links and both glosses and gains the closing words "; not selected for questions here", the words that already close the ケン row (CARD:33).
- CARD:43 names ゲン, きら.う and きら.い as the selected readings. CARD:44 is a new blank line and CARD:45 is a new paragraph that says why いや is not selected either (N8).
- The vocabulary coverage of いや is unchanged: its two links at CARD:37 and the same two entries under Common words (CARD:53-54).

The remaining kun prompt is きらう, because the two retained entries share a stem (KR:58-59). 嫌 now has two prompts (on ゲン, kun きらう) and the batch has 25 prompts instead of 26 (RUN-N:82, RUN-S:57, XC:107). The card is new in this batch: an author claim, not checkable in this packet, is that `kanji/嫌.md` does not exist at the previous published commit `20f0db4c` (only `words/嫌.md` does), so no published content has a 嫌 reading card; FMT:135 covers the general case of formerly started reading keys.

## D2. FU1 (over-restrictive production preconditions)

**Author action: accepted; the statement is corrected.** You wrote: "Absence of all three curated cards is presented among conditions required 'all together.' That is too restrictive. A short Starter session can borrow both 嫌 and 兼, or 嫌/兼/験, while still offering や for いや. One or two filled curated slots do not suppress the remaining fallback slots." The author agrees. A pool without 兼, 験 and 好 is a sufficient example and not a necessary condition: each curated card that is present fills at most one slot (KR:110, through `add`, which still rejects excluded and duplicate keys) and the fallback fills the others (KR:111-112), so exposure can survive one or two curated cards. Only three usable curated choices fill all three slots, as in the N1 and All pools for きらう (16 outcomes; RX:180-181).

The author did not re-run your two witnesses, because both concern the kun prompt いや, which no longer exists. The disclosure that arbitrary multiple-borrower combinations were not enumerated is addressed for the two remaining prompts by argument and not by enumeration (N6); please judge that argument.

## D3. FU2 (the `mutations` length filter; your C4)

**Author action: accepted.** `mutations` (WD:226-238) builds variants of its input and keeps only generated variants of at least two kana: the filter `it.length >= 2` at WD:237 applies to the generated output (constants WD:222-224). It does not refuse one-kana input: your example, input お, gives おう by long-vowel insertion and おう is kept. The sentence at FRESP:193-194 is withdrawn. The excluded keys of 嫌 (RUN-N:45: いや, きらい, きらう, ぎらい, ぎらう, けん, げん) are unchanged by this delta and no reading of 嫌 is a single kana, so no statement about 嫌 depended on the misreading. や is not an excluded key: its safety in the two remaining prompts rests on it not being drawable (N5, N6) and not on the exclusion mechanism.

## D4. FU3 (attribution of the JMdict readings; your C5)

**Author action: accepted.** JMdict entry 1587610 has two kanji spellings, 嫌 (JM:6) and 厭 (JM:12, marked as a rarely used kanji form at JM:13), and three readings. いや (JM:16) and や (JM:22) carry neither `re_restr` nor `re_nokanji`, so they are readings of the kanji spellings. イヤ (JM:25) carries `<re_nokanji />` (JM:26): it is the entry's kana-only reading and not a reading of 嫌. The card never mentions イヤ; CARD:45 relies only on や, which JM:21-23 attributes to the kanji spellings. The sentence at FRESP:198-200 is withdrawn.

## D5. C11 and C12 remain limits

**Author action: none; the limits stand and nothing new is asked of you.**

- Scan (C11): the scan-all leads (RX:309-340) are heuristic and untriaged leads on cards outside this batch. After this change the scan has one prompt fewer and one padded-session hit fewer (887 prompts and 12 padded-session hits, instead of 888 and 13; the withdrawn いや prompt was the one; RX:309). No lead concerns 嫌.
- Phone build (C12): the last phone APK delivered to the owner was built from app commit `5c000bd` and its installation was not verified. It predates app commit `2edbf36` ("Honor explicit kanji meaning pair exclusions"), so it ignores kanji `quiz_exclusions`. Whether it honours `quizKunyomi`, and which wrong options its older pool construction can offer for 嫌, were not analysed (FRESP, C12). The mitigation protects only clients that honour `quizKunyomi`: a client that ignores it still asks every `kunyomi` entry, including いや (FMT:137).

## D6. L1 and L3

**Author action: none.** L1 stands as resolved (a bounded evidence limitation) and L3 as accepted (a disclosed, non-blocking limit), as in your follow-up report.

## Other disclosures

- No device, APK or UI test was run. Source-level analysis of the pinned commit only.
- The real-Kotlin runs (RUN-N, RUN-S) use a scratch test that was never committed to the Android repository. `packet-manifest.json` records the SHA-256 of the four tool files; they are byte-identical to the follow-up packet's `evidence\tools\`.
- The other 14 cards are byte-identical to the follow-up packet's and are not re-reviewed here, except as context for the pools.
- Only the five plain copies in `checks\` keep the original line numbers (see "The author's own analysis files" above).

## Claims to verify

- **N1. The delta is exactly one card and two manifest lines.** The change from `10d79652` to `30f2bd7c` is `kanji\嫌.md` (new-side lines 12, 37 and 43-45; 5 insertions, 3 deletions) and `manifest.json` (old and new lines 41 and 656; 2 insertions, 2 deletions): 7 insertions and 5 deletions in two files (CHG; `diffs\changed-files.txt`, `diffs\changed-lines.txt`, DP, MP). The other 14 cards are byte-identical to the follow-up packet's after normalising CRLF to LF (`unchangedMembers` in `packet-manifest.json`; blob ids in `snapshot-identity.txt`). MP lists no word article or stroke file, so none changed.
- **N2. The mitigation is exactly the one you named.** `quizKunyomi` is an ordered, exact-string subset of `kunyomi` (FMT:120-124; CARD:10, CARD:12) and only いや was removed. `quizOnyomi: [ゲン]` (CARD:11), `title`, `tags` and `distractors` are unchanged (DP).
- **N3. The change keeps the format contract and leaves no contradiction.** Each selected reading has its own `## Readings` row with a relative link to an existing word article (CARD:34-36; FMT:126-128). The reasons for the unselected source readings are recorded in the card (CARD:33 for ケン; CARD:37 and CARD:45 for いや; CARD:43 for the selection; FMT:132). At most three distinct stems per kind are selected (FMT:134). `checks\validate.txt` reports 0 errors; `checks\lint.txt` reports 0 errors and 17 warnings, none about `kanji\嫌.md`; `checks\link-targets.tsv` lists the two links of CARD:37 with none unresolved. The lines of the card that contain いや are CARD:10, 23, 25, 37, 39, 41, 45, 53 and 54. CARD:10, 23, 25, 39, 41, 53 and 54 mention いや only as a reading or a word; CARD:37 and CARD:45 say that it is not selected for questions. CARD:43 names the selected readings and does not contain いや. CARD:60 concerns 憎, 疑 and 怪 and the meaning quiz, not いや.
- **N4. 嫌 has two prompts after the change.** `askOn = (quizOnyomi ?: onyomi)` = [ゲン] and `askKun = (quizKunyomi ?: kunyomi)` = [きら.う, きら.い] (RD:15-16). The stem rule (KR:58-59) keeps one kun reading because both entries have the stem きら, so the prompts are on ゲン (key げん) and kun きらう (key きらう). RO has no kun prompt いや block: RO:162 is the on prompt and RO:171 the kun prompt きらう. The batch has 25 prompts (RUN-N:82, RUN-S:57). The seven excluded keys are unchanged (RUN-N:45; KR:80-88) and still include いや, because `excludedKeys` is built from the full `on` and `kun` lists.
- **N5. The pools the client builds never drew や for 嫌.** For the N1 pool (1,161 cards), the All pool (1,161 cards) and a Starter practice session with 嫌 as the only borrowed card (the 118 Starter cards plus 嫌), the real Kotlin code drew no や in 4,000 seeds per pool: RUN-N:46-49 (N1 and All, ゲン and きらう) and RUN-S:33-34 (Starter session). RX:169-188 gives the same for the Python model (2,000 seeds per pool) and XC:29-32, XC:94-95 and XC:107 compare the two ("0 problem(s)").
- **N6. No pool the client builds can offer や for either prompt.** (a) Pools: 嫌 is asked only in the N1 stack, the All stack and a Starter practice session that borrows it. The N2 to N5 stacks contain no `jlpt-n1` card (ST:32-36), the JLPT and All stacks borrow nothing (PAD:19) and there are no other stacks (ST:11-23). N1 and All hold all 1,161 cards. A Starter session holds the 118 cards tagged `starter` plus borrowed cards, and borrowing only adds cards (VM:125-128). So every pool in which 嫌 can be asked contains the 118 Starter cards, and the target is not among its own candidates (KR:109). (b) Holders of や in the TSV, where a reading counts if its key is や after folding katakana to hiragana and dropping `.`, `-`, `・` and spaces (KR:26): in `ask-on`, 冶, 夜 and 野, none tagged `starter`; in `ask-kun`, 八 (tagged `starter`; readings `や や.つ やっ.つ よう`), 家 (`いえ や うち`) and 屋 (`や`), the last two not tagged `starter`. 嫌, 兼, 験 and 好 are not tagged `starter` and 兼, 験 and 好 hold no や. (c) Closeness (KR:102-106) of a candidate key to the correct key is 2 if the lengths differ by at most one, plus 1 if the last kana is equal, plus 1 if the first kana is equal. For ゲン (key げん) や scores 2. For きらう (key きらう) や scores 0; the readings of 八 score や 0, やつ 2, やっつ 2 and よう 3, so its step-2 candidate is よう; those of 家 score いえ 2, や 0 and うち 2, so its candidate is いえ; 屋 has only や (0). A card's step-2 candidate is its first best reading (KR:111). (d) Supply: the 118 Starter cards alone have 25 distinct step-2 candidates of closeness 3 for ゲン. One of them, けん (嫌's own ケン), is an excluded key, which leaves 24 usable keys (あん いん えん かん きん ぎん げ げつ こん さん しん じん せん ぜん たん だん てん でん なん ねん はん ぶん ほん まん). For きらう they have 10 (あう おう おこなう かう かたらう きく きた きたる くう よう), none excluded. No Starter card has や as a step-2 candidate. (e) Argument: step 1 (KR:110) adds at most one key for each curated card present (兼, 験, 好), that is j keys with j at most 3, and never や. Step 2 (KR:111) adds candidates in descending closeness until three wrong options are chosen. At most j of the usable closeness-3 keys of (d) are already chosen, so at least 21 (ゲン) and 7 (きらう) remain, which is at least the 3 minus j slots left. The list is therefore full before any candidate of closeness 2 or lower is reached, and step 3 (KR:112), the only place where a non-best reading such as 八's や could enter, adds nothing once the list is full (KR:100). や has closeness 2 or less for both prompts, so it is never added. Borrowed cards only add candidates and cannot remove a closeness-3 key of the Starter cards, so the conclusion holds for every Starter session with any set of borrowed cards, and for the N1 and All pools, which contain the same 118 cards. (f) Corroboration: the real Starter run draws exactly the 24 and 10 keys of (d) (RUN-S:33-34), so 八 contributes よう and never や, and RX:175 and RX:185 report that adding any single holder to the Starter pool does not make や drawable. Scope: this is the displayed kanji-reading prompt (VM:151); word, drawing and meaning exercises are other paths.
- **N7. Small pools still show the risk class, but the client does not build them.** The same real code draws や for the retained prompts in artificial pools of 嫌 and one holder of や, for example 嫌+屋 and 嫌+八 on きらう and 嫌+夜 and 嫌+冶 on ゲン, and 嫌+冶 on きらう has no valid option at all (RUN-N:83-94; XC:53-64). These pools are not shipped. They are listed because the author does not claim a universal property. A permanent client mechanism (proposals A and B of FRESP) is an owner decision and no client change was made in this batch.
- **N8. CARD:45 is accurate; its wording is open.** CARD:45 (62 words) says: "いや also has linked word articles but is not selected either: JMdict lists や as a further reading of 嫌, Digital Daijisen explains it as a sound change of いや, KANJIDIC2 does not list it, and a question about いや could show や as a wrong option. This is a teaching selection, not a claim that いや is invalid, obsolete or rare." Sources: JMdict lists や as a reading of the spelling 嫌 (JM:21-23; D4). Daijisen has a separate entry や【▽嫌／×厭】 explained as 「いや（嫌）」の音変化 (DJ, line 6, which holds both Daijisen entries on one line). KANJIDIC2 lists ケン, ゲン, きら.う, きら.い and いや and no や (KD:371-375). The last clause is what your C8 reproduced for the withdrawn prompt (や in 1,310 of 4,000 seeds with the real code). A wording fact, as an author claim about the whole tree at `30f2bd7c` (outside this packet): "wrong option" appears only on this line; 16 other cards say "wrong answer"; every card of this batch says "quiz options" (the last Notes bullet, for example CARD:60). Please judge accuracy and learner comprehension, and say whether "wrong option" should be "wrong answer"; the author will change it if you prefer.
- **N9. The manifest delta is exactly two lines.** MP changes `contentVersion` (old and new line 41: `eb332dd7994dd3ba` to `18d0f3df4071aa30`) and the entry of `kanji/嫌.md` (line 656: `622980074175867923a1f1a6a569721295ce74f247327637ce36073700f3f302` to `033867582ec3df45d00a0311caf74d0594c22bfb8ff7f18428ed82ac94842312`). The new hash is the SHA-256 of the card after normalising CRLF to LF, which is also the git blob content (blob `52a73a70028b01a97295820ff08eb78ee7487287`; `snapshot-identity.txt`). The CRLF copy in `snapshot\kanji\` has a different SHA-256, which is why the comparison is made after normalising. `checks\manifest.txt` is the author's rebuild check: it rebuilds the manifest and fails if the committed file differs.
- **N10. The gates of `30f2bd7c` passed.** These are the author's gate logs in `checks\`: `summary.txt` (six gates, each exit 0), `lint.txt` (0 errors, 17 warnings, two of them about the existing word articles 嫌い and 嫌がる and none about the card), `unittest.txt` (431 tests OK), `validate.txt` (0 errors), `budget.txt`, `vocabulary.txt` (2122/2431 reviewed prompts, stage pilot), `manifest.txt` (version `18d0f3df4071aa30`), `quiz-safety.txt` (0 errors, 0 warnings), `reading-options.txt` (0 problems), and the Android JVM runs `jvm.txt`, `jvm-readings.txt`, `gradle-kotlin-reading.txt` and `gradle-kotlin-starter.txt` (BUILD SUCCESSFUL). CHG has the before and after values.

## What the author asks of you

- Disposition F1, FU1, FU2 and FU3 as the instructions describe.
- Judge CARD:37, CARD:43 and CARD:45 for correctness, consistency and comprehension (N8), including "wrong option" against "wrong answer".
- Verify N4, N5 and N6 by hand from CARD, the TSV and the Android sources, and N9 from MP.
- Report any other line of the card, or any claim here, that still contradicts the withdrawal of いや from practice.
