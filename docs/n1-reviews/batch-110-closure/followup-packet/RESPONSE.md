# Author's statement for the follow-up reviewer of N1 kanji batch 110, snapshot 10d79652

Bound to commit `10d7965266b69ed81703ab69f20cff873a0526e9`, unchanged since your confirmation report. **F1** is finding 1
of your confirmation report (嫌 and the contracted reading や). **L1** and **L3** are the two limits of that report that you
marked PARTIALLY RESOLVED (IDs as in the confirmation packet's `RESPONSE.md`). **C1 to C13** are the claims at the end of this
file. Everything here is the author's claim about what is true and why: verify each claim against the files named, and do not
rely on this text as evidence. Cited line numbers are lines of the packet copies of the files.

## Short names

The Android sources are exact git blobs of commit `10d98d0db61dcde621463460e6a1e59941b4042b` of the public repository
`stop-cran/kanji-cards-android` (the tip of its `main` branch when this packet was built). All paths in the table are under
`evidence\android\`; `SOURCES.tsv` there has each file's blob id, SHA-256 and public raw URL.

| Name | File |
| --- | --- |
| VM | `app\src\main\java\io\github\stopcran\kanji\ui\KanjiReadingViewModel.kt` |
| SCR | `app\src\main\java\io\github\stopcran\kanji\ui\KanjiReadingScreen.kt` |
| RD | `app\src\main\java\io\github\stopcran\kanji\data\ReadingData.kt` |
| PAD | `app\src\main\java\io\github\stopcran\kanji\data\Padding.kt` |
| SRS | `app\src\main\java\io\github\stopcran\kanji\data\SrsMapping.kt` |
| DB | `app\src\main\java\io\github\stopcran\kanji\data\Database.kt` |
| KRV | `app\src\main\java\io\github\stopcran\kanji\data\KanjiReviews.kt` |
| KR | `core\src\main\kotlin\io\github\stopcran\kanji\core\reading\KanjiReadings.kt` |
| WD | `core\src\main\kotlin\io\github\stopcran\kanji\core\words\Words.kt` |
| ST | `core\src\main\kotlin\io\github\stopcran\kanji\core\srs\Stacks.kt` |
| PP | `core\src\main\kotlin\io\github\stopcran\kanji\core\srs\PracticePadding.kt` |
| FB | `core\src\main\kotlin\io\github\stopcran\kanji\core\focus\FocusBatch.kt` |
| KT | `core\src\test\kotlin\io\github\stopcran\kanji\core\KanjiReadingsTest.kt` |

The author's own analysis files (claims to verify, not evidence) are under `checks\`: **RX** = `reading-exposure.txt` (exact
reachability audit in Python); **RUN-N** = `kotlin-reading-run.txt` (the real Kotlin code on the N1 and All stack pools, plus
small pools); **RUN-S** = `kotlin-starter-run.txt` (the real Kotlin code on a Starter session pool); **XC** =
`kotlin-vs-exact.txt` (the two Kotlin runs compared with the Python analysis).

## Corrections to the author's earlier statements

1. The confirmation packet's `RESPONSE.md` (L1, "Caveats", line 116) and `CHANGES.md` (lines 98 to 99) say that the audit pool
   is every card in `kanji\` while "the app draws from the cards the learner has studied". That is inaccurate. For the N1 and
   All stacks the readings screen builds its pool from the WHOLE stack, all 1,161 cards of this snapshot (C1); only a short
   Starter "Practice more" session has another pool (C3). Your phrase "the learner's smaller studied pool" followed from that
   sentence.
2. The audit's "0 problem(s)" and its statement that no unlisted reading is attested for 嫌 were wrong: its inventory of
   attested readings lacked the single-kanji entries of JMdict. The corrected inventory lists や (RX:167-168; C10). The older
   `checks\reading-options.txt` of the confirmation packet is unchanged and still has that gap.
3. An intermediate conclusion of the author's own analysis, that や cannot be drawn in any pool the shipped app builds, was
   wrong: it had missed the padding path (C3, C8). It is withdrawn; nothing in this packet relies on it.

## F1: 嫌 and the contracted reading や

**Author action: card text not changed (a decline). The audit and its inventory are corrected, the remaining path is
disclosed, and a change in the client is proposed.** Please judge whether that is acceptable (see the end of this section).

### What the author accepts

- や is an attested contracted native reading of 嫌. JMdict entry 1587610 lists the reading や for 嫌 without restriction
  (`evidence\jmdict-cited-entries.xml`), and the Digital Daijisen has a separate entry や【▽嫌／×厭】 "「いや（嫌）」の音変化"
  (original packet, `evidence\public-source\weblio-嫌.txt`) (C5).
- Your source-level case is real. In the pool `[嫌, 屋]` the kun'yomi prompts きらう and いや each have the single wrong option
  や, in 400 of 400 seeds of the real Kotlin code (RUN-N:86-87) (C6). That pool is a hypothetical content-sized pool; no shipped
  stack builds it.
- The only protection against an attested but unlisted reading is `excludedKeys`, which is built from the target card's own
  `onyomi` and `kunyomi` lists (KR:80-88) (C4).

### Which pools the app really builds for 嫌 (C1 to C3, C7, C8)

Every displayed reading question comes from one call, VM:151. Its pool is the stack's whole card list, plus borrowed cards in
one case.

| Session | Pool | ゲン (On) | きらう (Kun) | いや (Kun) |
| --- | --- | --- | --- | --- |
| N1 stack | all 1,161 cards | 55 possible wrong options (1 curated, 54 fallback); no や in 4,000 seeds | 9 (all curated); no や | 9 (all curated); no や |
| All stack | the same 1,161 cards | same | same | same |
| Starter stack, short "Practice more" session that borrows 嫌 | 118 Starter cards plus 嫌 | 24; no や in 4,000 seeds | 10; no や | 9; **や in 1,310 of 4,000 seeds** |

Sources: RX:170-172, 180-182, 190-193; RUN-N:46-51; RUN-S:33-35.

- ゲン in the N1 and All stacks: the curated 兼 and 験 are ケン readings whose key `けん` is excluded, so two slots come from the
  closeness fallback. や scores 2 there (KR:102-106), and many two-kana readings ending in ん (かん, しん, はん, …) score 3 and
  fill the open slots first.
- きらう and いや in the N1 and All stacks: the curated 兼, 験 and 好 fill all three wrong slots in every outcome, so the fallback
  (KR:111-112) is never consulted.
- Starter session: none of 兼, 験, 好 is Starter-tagged (RUN-S:31), so all three slots come from the fallback. For いや the nine
  candidates at the top closeness score tie (eight start with い; や ends with the same kana as いや), and three are drawn at
  random. The real run draws や in 1,310 of 4,000 seeds and each of the other eight options in 1,321 to 1,366.

### Conditions for the one remaining path (all together)

1. The learner has selected the Starter stack and taps "Practice more" on the readings exercise (route
   `kreading:<timestamp>:extra`; SCR:33-36; `routes.txt`).
2. The session's ordinary queue has fewer than `practiceMinimum()` items, that is the batch-size setting but at least 10
   (PAD:9-12; VM:92, 97-98).
3. The いや reading of 嫌 is a started card in another stack (not Starter, not All) and is among the weakest started cards,
   because padding takes them by lowest retrievability (DB:557-559; PAD:19-24; PP:33-42; VM:109-133).
4. The curated 兼, 験 and 好 are not in the session's pool (each would fill a curated slot, and none is Starter-tagged).
5. Only the いや prompt is exposed: the ゲン and きらう prompts did not draw や in the same pool (RUN-S:33-34).

The author considers this narrow but not negligible. It depends on learner state, so the author did not estimate how often it
happens, and does not claim it is rare. A learner who knows the contraction and picks や is marked wrong.

### Why the author did not change the card text

1. **Fidelity.** Your own remedy says to preserve the pinned KANJIDIC2 metadata rather than present an extra value as part of
   that source record. The only content change that reaches `excludedKeys` is adding や to `kunyomi`, because the exclusion set
   is built from the `onyomi` and `kunyomi` lists (KR:80-88). That would break the fidelity of the front matter (the content
   repository's batch audit, `tools/audit_n1_batch.py:487-496`, which is not in this packet, requires both lists to equal the
   frozen KANJIDIC2 source metadata) and would also show や in headers, search and
   feedback.
2. **No content mechanism exists** for extra attested readings (C4). A new optional field needs changes in the client's parser
   and database and in the repository's schema validator, and the repository's open issue #61 (EN/RU content schema)
   concerns that same schema. It is not a content-only fix.
3. **The class is not specific to this batch** (C11): the exploratory scan finds the same pattern in 19 whole-stack hits and
   12 further Starter-session hits, all on cards outside this batch. The author did not triage or change them.
4. **Alternatives the author considered and rejected:** (a) Starter-tagged curated distractors that fill the slots: this
   distorts the meaning quiz, whose look-alike distractors come from the same field, and 八, itself a Starter card, offers や;
   (b) dropping いや from `quizKunyomi`: this removes the only exposed prompt but also a Joyo-listed reading prompt, and the
   きらう prompt keeps the small-pool collision of C9; (c) a new content field (see 2).

### What the author will record (not part of the snapshot)

The closure README of this batch (limits) and a checkpoint comment on issue #60 will state the finding, the corrected audit, the
Starter-session path with its conditions, the exploratory scan (as untriaged leads) and two proposals for the owner of the
client: (A) a data-driven list of attested extra readings that only `excludedKeys` reads, so `onyomi` and `kunyomi` stay equal
to KANJIDIC2 (a new content field, the parser, the schema, coordinated with issue #61); (B) a generic rule that rejects a wrong
option that is a prefix or suffix of a reading of the target, a shortened or contracted form. B needs no content field and
would catch this case and, for example, 寝 い.ぬ→い and 神 かみ→み from the scan, but not 前 まえ→さき. The client's own
content-snapshot test (KT:207-233) sees only listed readings, so it passes today. Whether to open a client work item is the
owner's decision; the author opens none.

### What the author asks of you (F1)

Is a documented limitation plus a proposed client change an acceptable answer to F1 (`DECLINE ACCEPTED`) or not
(`DECLINE REJECTED`)? If you reject it, please name the content mitigation you would accept. The author sees only these, each
with the cost given above: adding や to `kunyomi`; dropping いや from `quizKunyomi`; changing the curated distractors. Please say
if you know a better one.

## L1: the reading-option audit (your disposition: PARTIALLY RESOLVED)

Your two points were that the inventory of attested readings was incomplete (嫌 や) and that the all-card, 200-seed result is not
a safety proof for the pools a learner really gets. The author's answer:

- **Inventory.** It is now KANJIDIC2 on, kun and nanori readings, the single-kanji entries of JMdict (entries restricted to
  another kanji form or marked search-only are skipped) and readings printed in the card text. The results for all 15 cards are
  in RX; 嫌 is RX:163-196. Besides 嫌, the audit reports only name-only (nanori) readings as information, for example 応 お in
  the N1 and All stacks (XC:15-16), which you already judged not to be a valid on'yomi answer.
- **Pools.** The audit no longer samples all cards: for each of the 26 prompts it lists which wrong options each pool the app
  builds can offer (N1 stack, All stack, Starter session with the target borrowed), and the real Kotlin code was run on the same
  pools with 4,000 seeds (C7, C8, C13). Pools of 嫌 plus one other card were added (C9; RX:175, 185).
- **Still not shown.** (1) Starter sessions that borrow several cards: the sets depend on learner state and were not
  enumerated, and a borrowed card can add candidates or fill curated slots. (2) Installed-client behaviour: no APK or UI test
  was done; the analysis is of source at one commit. (3) The installed phone build (C12). (4) Attestations outside the
  inventory, for example dictionary entries that are not in JMdict. (5) The scan in C11 is heuristic and untriaged.

Please give a disposition for L1: `RESOLVED` if this answers your two points, otherwise what remains.

## L3: Joyo claims compared with text extracts (your disposition: PARTIALLY RESOLVED)

No new author action. The Joyo-table claims of the 15 cards were compared with text extracts of the table's PDF (the confirmation
packet's `evidence\joyo\`). The 器 claim, which depends on the U+FA38 form, was also compared with page images (the confirmation
packet's `evidence\joyo-p33-utsuwa.png` and `evidence\joyo-p33-utsuwa-pair.png`). The author has not inspected every page of the
PDF visually either. Please state whether this remaining limit blocks
your confirmation and, if it does, what evidence would resolve it; or whether you accept it as a disclosed limit.

## Other disclosures

- **Scope of the analysis.** C1 to C13 describe the Android sources at the pinned commit only. The sources were fetched from the
  public repository without credentials, and each blob was compared with its public raw URL when the packet was built. The real
  Kotlin runs read this snapshot's cards from the content working tree at `10d79652`, using a scratch test
  (`evidence\tools\ScratchReadingExposureTest.kt.txt`) that was never committed anywhere; it needs the Android checkout and
  cannot be run from this packet.
- **No device test.** No APK, emulator or UI test of the quiz was done.

## Claims to verify

- **C1. The readings screen's pool is the whole stack.** VM:83-85 builds `all = content.inStack(stack)`; VM:94 passes it to
  `readingData`; RD:36 maps every card of it to a `ReadingCard`; VM:95 keeps them as `readingCards`. `inStack` keeps a card when
  `Stacks.includes` holds (SRS:35-38); for a JLPT stack that is any tag from that level down to N5 (ST:33-36). Every card of the
  snapshot has exactly one tag from `jlpt-n1` to `jlpt-n5` (170, 374, 371, 166 and 80 cards;
  `evidence\cards-reading-metadata.tsv`), so the N1 stack and the All stack both hold 1,161 cards (RUN-N:1).
- **C2. One display path.** The only production call that builds a displayed reading question is VM:151, with `readingCards` as
  the pool. The other calls only test that a question exists (KRV:114-120 and FB:25, both with `Random(0)` and a null check);
  see `evidence\android\call-sites.txt`. The other production hits in that file are not kanji reading questions: WD:160-166
  builds the options of the word quizzes (`WordQuizBuilder`, an exercise on word cards), PAD:32-35 pads word sessions, and
  `DrawViewModel.kt:205` and `QuizViewModel.kt:130` pad the drawing and the meaning-quiz sessions (`StudyMode.Draw`,
  `StudyMode.Quiz`; neither file refers to `KanjiReadingQuiz` or `ReadingCard`). The pattern was run over every `.kt` file of
  the commit.
- **C3. Padding.** PAD:19 returns no candidates for the All stack and every JLPT stack, so only the Starter stack is padded
  among the stacks that contain 嫌's prompts. VM:97-98 pads a "Practice more" session that has fewer than `practiceMinimum()`
  items (PAD:9-12). VM:109-133 adds weak started cards of other stacks (DB:557-559: another stack, not `all`, phase not New;
  PAD:22-24 drops cards of the current stack) and adds each borrowed card to `readingCards` (VM:125-128). The pool of such a
  session is the Starter stack plus the borrowed cards.
- **C4. Option mechanism.** `ReadingCard` carries only `on`, `kun`, `askOn`, `askKun` and `distractors` (KR:47-54).
  `excludedKeys` is the key of every `on` and `kun` reading plus their variants (KR:80-88), and variants of one-kana readings
  are not generated (WD:237 keeps only variants of at least two kana). `question` fills slots from the curated distractors
  first (KR:110: each offers one random usable reading; a slot lost to an excluded key is not retried), then a
  closeness-ranked fallback (KR:102-106, 111), then a final fallback (KR:112). A wrong option must not be in `excludedKeys`
  (KR:100).
- **C5. Attestation.** JMdict entry 1587610 lists the readings いや, や and イヤ for 嫌 (`evidence\jmdict-cited-entries.xml`); the
  Daijisen text is in the original packet's `evidence\public-source\weblio-嫌.txt`. や is not in the card's `kunyomi` (the
  front matter equals the pinned KANJIDIC2 readings).
- **C6. Source-level case.** In the pool `[嫌, 屋]` the prompts きらう and いや offer the single wrong option や in 400 of 400
  seeds (RUN-N:86-87). By hand: `excludedKeys` of 嫌 is `いや きらい きらう ぎらい ぎらう けん げん` (RUN-N:45), 屋 offers its
  kun reading や, and no curated card is in the pool.
- **C7. N1 and All stack runs.** RUN-N:46-51: for ゲン, きらう and いや, in both pools, 4,000 seeds each, no null question, the
  correct answer always present once, four options always. The wrong options drawn are 55 distinct readings for ゲン, nine for
  きらう and nine for いや, and none is や. RX:170-171 and KR:102-106, 111 explain why や is not reached for ゲン.
- **C8. Starter session run.** RUN-S:1 and 31-35: the pool is the 118 Starter cards plus 嫌 alone. ゲン draws 24 distinct wrong
  options and きらう 10, none is や. いや draws nine distinct wrong options, and や is drawn in 1,310 of 4,000 seeds (RUN-S:35).
  A real session may borrow further cards, and each changes the pool, so 1,310 of 4,000 is a property of this pool, not a
  probability for the app.
- **C9. Small pools (class of risk, not shipped pools).** RUN-N:85-102: in pools made of 嫌 and one other card, や is drawn as a
  wrong option when that card is 屋, 家 or 八 (kun'yomi prompts) or 夜, 冶 or 野 (ゲン); with 冶 the kun'yomi prompts have no valid
  question (null in 400 of 400 seeds). They show how the mechanism behaves when the pool is tiny.
- **C10. Corrected inventory.** RX:167-168 lists JMdict 1587610 and "unlisted readings attested for 嫌: や".
- **C11. Exploratory scan.** RX:317-349: over every card of the snapshot, using the JMdict single-kanji readings that a card does
  not list, the scan finds 19 hits in whole-stack pools (N1, All, Starter stack; RX:318-336; one line per prompt and pool, nine
  prompts of 冠 前 寝 日 片 真 神 酒) and 13 hits
  that occur only in a Starter session that borrows the card (RX:337-349; one is 嫌, the other twelve are prompts of cards outside this
  batch). It is heuristic and untriaged: the author has not judged which of those readings deserve protection.
- **C12. The installed phone build differs.** The last user-requested phone APK was built from app commit `5c000bd` and copied to
  the phone; installation was not verified. `evidence\android\compare-5c000bd-to-10d98d0d.txt` and `.patch` show: the option
  code (`KanjiReadingQuiz`, `ReadingOptions`) is identical (the diff of `KanjiReadings.kt` starts at line 146, in the queue code;
  `Words.kt` and `FocusBatch.kt` are identical); but pool construction differs. At `5c000bd`, `Padding.kt` returned no
  candidates only for the All stack, so a short N1 session could be padded, and `Stacks.kt` had no cumulative `includes()`
  (`inStack` used `Stack.contains`), so the N1 stack held only the 170 cards tagged `jlpt-n1`. It also predates app commit
  `2edbf36` ("Honor explicit kanji meaning pair exclusions"), so it ignores kanji `quiz_exclusions`, which concerns the meaning
  quiz and not this finding. The author did NOT analyze which wrong options that older pool construction can offer for 嫌.
- **C13. The Python analysis agrees with the Kotlin runs.** XC:2 and 88 (pool sizes match), XC:116: 52 whole-stack prompts, 26
  Starter-session prompts and 32 small-pool prompts checked, 0 problems; 0 whole-stack prompts drew an attested unlisted
  reading, 1 Starter-session prompt did (XC:104, 嫌 いや); 4 prompts have reachable options that were never drawn. The Python
  tool enumerates the reachable options exactly except in the deepest closeness tier, where it treats every remaining reading
  as reachable (a superset); this explains the 4 prompts.
