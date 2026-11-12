# Evidence for the follow-up round

Everything here is supplied so that the corrected pool facts in `RESPONSE.md` can be checked against sources, not taken on
trust. Sections 1 to 4 are source material; section 5 is the author's own analysis (claims to verify, not evidence).

## 1. Android client sources (`android\`)

The reading quiz of the app is built from the Android repository `stop-cran/kanji-cards-android` (public) at ONE pinned commit:
`10d98d0db61dcde621463460e6a1e59941b4042b`. The files below are the exact git blobs of that commit (LF line ends, no edits). The table gives each file's size,
SHA-256, git blob id and the public raw URL where the same bytes can be fetched anonymously
(`https://raw.githubusercontent.com/stop-cran/kanji-cards-android/10d98d0db61dcde621463460e6a1e59941b4042b/<path>`); "raw check" says whether the author compared the bytes served at that URL with the blob on
2026-11-12. What each file shows (line numbers are of the file in this packet):

- `android\app\src\main\java\io\github\stopcran\kanji\ui\KanjiReadingViewModel.kt` (10070 bytes, sha256 `92a90bce8b6b8dcf292090086bb53455c8952ca8076cb1a873bf4e3be9e7bb76`, blob `1801c9f854f83659ab4974282eeb531e5b13f305`, raw check: identical): VM. 83-85 the pool is `content.inStack(stack)`; 92-95 `practiceMinimum()` and `readingData` (its cards become `readingCards`); 97-98 a short Practice-more session is padded; 109-133 `pad`, where borrowed cards are added to `readingCards` (125-128); 151 the only production call that builds a displayed reading question
- `android\app\src\main\java\io\github\stopcran\kanji\ui\KanjiReadingScreen.kt` (6652 bytes, sha256 `49d8218b2f0809fbb7de1a4a871b77e06c76fe1bfcf7bb3b0cfec49066ecb95c`, blob `9a109144b5b5c4e35d74716cea21aea9a6d6470e`, raw check: identical): SCR. 33 the session key `kreading:<timestamp>[:extra]`; 36 `ensureStarted(sessionKey.endsWith(":extra"))`; 50 the Practice-more button
- `android\app\src\main\java\io\github\stopcran\kanji\data\ReadingData.kt` (2914 bytes, sha256 `55f9596274c5bfea2fd2a4bd692e42d8eb7f46406b7830eb6a52deda022e99be`, blob `97089c47390ef6877f14277209f1b3b121c8cdf2`, raw check: identical): RD. 13-18 `toReadingCard()` (the ask lists are `quizOnyomi` and `quizKunyomi` when present, otherwise the full lists); 25-28 `ReadingRequest`; 30-53 `readingData`, where 36 maps every card of the stack to a `ReadingCard`
- `android\app\src\main\java\io\github\stopcran\kanji\data\Padding.kt` (2901 bytes, sha256 `32177ebf9bb9db4f2b7c0ddf1873925ab2eea02789215f7306ef28ebb60e0675`, blob `b59995d01fae1962678724fc1b5e5238cb46c0cb`, raw check: identical): PAD. 9-12 `practiceMinimum()`; 18-25 `padCandidates`: 19 returns nothing for the All stack and every JLPT stack, 22-23 take started cards of other stacks that are not in the current stack; 32-35 `padWordCandidates` (word sessions)
- `android\app\src\main\java\io\github\stopcran\kanji\data\SrsMapping.kt` (4032 bytes, sha256 `660de449acb8a30a50f72787749355b70fd6ddf9f1db141a9e49cda4cd931a25`, blob `7c3bc63232ad9afb21e40ee530fd1f20d8dc0c0e`, raw check: identical): SRS. 35-38 `inStack` keeps the cards for which `Stacks.includes` holds
- `android\app\src\main\java\io\github\stopcran\kanji\data\Database.kt` (46455 bytes, sha256 `863b5bd76b38e21d2d1a4bae49da13a1eb9481c4d7b0088687efaf71d3b12c6a`, blob `40adc184a5510d140c977d306db96f1ab468bad2`, raw check: identical): DB. 557-559 `borrowable`: started cards (phase not New) of the same source and mode in another stack, never from the All stack
- `android\app\src\main\java\io\github\stopcran\kanji\data\KanjiReviews.kt` (7218 bytes, sha256 `43f4451507ee16699260d1ca34a3e587443b4e257ff7e859e5f9f5ab36534b53`, blob `b3cdce085e8fa8f00ea750b5a8308b8225f2e9d7`, raw check: identical): KRV. 110-121 availability check only (`Random(0)`, null test) for a cross-level reading; no question is displayed
- `android\app\src\main\java\io\github\stopcran\kanji\data\Unlock.kt` (3487 bytes, sha256 `9e09d30ad4903318e8430831746ab86f0d72a13fa108dd3e04f2f5ef55f94d6b`, blob `2a1f6a9560f76a405e11b21fa203a4f96945f3f7`, raw check: identical): Context only. 38-49 `focusStatus` maps the stack's cards to reading cards (availability, no displayed question)
- `android\app\src\main\java\io\github\stopcran\kanji\data\HomeRepository.kt` (5925 bytes, sha256 `a898d6816d98ce66e202f4a6787cc0ad8642eb74b4b61c783c6b134494cd30fb`, blob `0cc14d3c6e468c556d885ede02284cd6383b14b2`, raw check: identical): Context only. 88-91 the home screen asks `padCandidates` whether a mode can be padded
- `android\app\src\main\java\io\github\stopcran\kanji\ui\HomeData.kt` (13296 bytes, sha256 `280c59304e65e1e6e180f89210f7688bdc406b3284dc19ead0ad152f5be84301`, blob `e2840f9fc93f3aac992f8d1db362951efed69e0b`, raw check: identical): Context only. 219-224 the home screen builds the readings queue from the stack's cards (counts; no question is built)
- `android\app\src\main\java\io\github\stopcran\kanji\ui\DrawViewModel.kt` (15765 bytes, sha256 `24ce5287910a3d0945d2d41a42ee102e288c43bc6676262076c052ed57364555`, blob `73d5852f5eb5c3ede731575862b8b9329874589f`, raw check: identical): Context only. 201-206 `pad` for the drawing session (`StudyMode.Draw`); the file never refers to `KanjiReadingQuiz` or `ReadingCard`
- `android\app\src\main\java\io\github\stopcran\kanji\ui\QuizViewModel.kt` (10114 bytes, sha256 `2054006fb5fdddf8cce9d89024e87226cbf7ced6eaf54139b65f699904e0caa5`, blob `1c5435e14f2fe05eff4fde289bfa746e37a984d0`, raw check: identical): Context only. 126-131 `pad` for the meaning-quiz session (`StudyMode.Quiz`); the file never refers to `KanjiReadingQuiz` or `ReadingCard`
- `android\app\src\main\java\io\github\stopcran\kanji\MainActivity.kt` (20399 bytes, sha256 `cbbbb3e20150490911837a7fdde9dde1d793bb89d570e8b235af3b70c4b0ce41`, blob `5577b1e32c344882a110caf76545fa24e070b707`, raw check: identical): Context only. 89-92 session route prefixes (`kreading:`); 366-372 the readings route and its `onPracticeMore` (371); 409 the home screen's entry to the readings screen
- `android\core\src\main\kotlin\io\github\stopcran\kanji\core\srs\Stacks.kt` (1874 bytes, sha256 `041d124fb39e833d0fa7e50dbfb7edea7da98bd6ad500568680841f4bbcfb903`, blob `a8f2ef9915ba8bc6d87e1ecd091d837f9bac4e14`, raw check: identical): ST. 9-23 the stacks (All, N5 to N1, Starter); 25-30 `jlptLevel` and `stateId`; 33-36 `includes`: a JLPT stack contains its own level and every easier level
- `android\core\src\main\kotlin\io\github\stopcran\kanji\core\srs\PracticePadding.kt` (2356 bytes, sha256 `680630b5635907a5b29ec76d0d1858d4af3b707cdeeba87357aa5996f203ad80`, blob `b0ff4ad943bda55366cd3ecaf179b2a14737d554`, raw check: identical): PP. 33-42 `fill`: started cards (phase not New) that are not excluded, weakest retrievability first, `take(need)`
- `android\core\src\main\kotlin\io\github\stopcran\kanji\core\focus\FocusBatch.kt` (2716 bytes, sha256 `ce7cc89c51d7c1254a555568a206bd735c44fa2c55aff3fe5a26cb71a296d877`, blob `d3c9d6f66b5ed4db23b047b000276923f826460c`, raw check: identical): FB. 22-29 `requiredReadingKeys`; 25 availability check only (`Random(0)`, null test)
- `android\core\src\main\kotlin\io\github\stopcran\kanji\core\reading\KanjiReadings.kt` (13346 bytes, sha256 `0632fcbb014d8644fcf1ab8fe0bd7b22d89df70a4b6e3c4d0838b129f76e4d74`, blob `492a43c315816fbdf2079ee8c0bb05c731136b5c`, raw check: identical): KR. 46-54 `ReadingCard`; 57-61 `quizReadings` and `quizKeys`; 79-88 `KanjiReadingQuiz` and `excludedKeys`; 91-116 `question`: 98-101 `add` (100: a wrong option must not be in `excludedKeys`), 102-106 `closeness`, 110 curated distractors, 111 closeness fallback, 112 final fallback, 113 null when no wrong option was found; the queue code starts at 146
- `android\core\src\main\kotlin\io\github\stopcran\kanji\core\words\Words.kt` (15086 bytes, sha256 `2b6105b17f70a0e11de21a7d40fcff506a59eade1202f276dcb435bc436bd6ce`, blob `a99919ab78e67bc8e1d4c3a9b733293fdcd38910`, raw check: identical): WD. 160-166 `WordQuizBuilder.options` (the word quizzes; 164 builds the reading options of a word); 209-214 `ReadingOptions`; 226-238 `mutations`: 237 keeps only variants of at least two kana
- `android\core\src\test\kotlin\io\github\stopcran\kanji\core\KanjiReadingsTest.kt` (13183 bytes, sha256 `9bb1d9f1e048ba6b13935ba80f04e7bec3c1b99196da17d9b4bbaf3b8270d711`, blob `180135c808243835b5dc7d929336c9664eff9af9`, raw check: identical): KT. 207-233 the content-snapshot test: every reading card has a valid question and no wrong option is in `excludedKeys` (which knows only the listed readings)

`android\SOURCES.tsv` has the same table as tab-separated values.

- `android\call-sites.txt`: `git grep` over every `*.kt` file of the commit for the quiz entry points and pool builders
  (`KanjiReadingQuiz\.|ReadingOptions\.|padCandidates\(|\.borrowable\(|toReadingCard\(\)`). Files under `src/test` and `src/androidTest` are tests, not production paths.
- `android\routes.txt`: `git grep` for the `kreading` route of the readings screen (`kreading`).
- `android\compare-5c000bd-to-10d98d0d.txt` and `.patch`: whether the files that build the reading pools differ between `5c000bd5596d2189ef878da572687bd01ab3bb5f` (the commit of the phone build mentioned in the author's statement) and the pinned commit, and the exact patch. Context for one statement of limits only.

## 2. Content metadata (`cards-reading-metadata.tsv`)

Every card of the snapshot (the whole shipped content at commit `10d7965266b69ed81703ab69f20cff873a0526e9`), one row per card: kanji, tags,
onyomi, kunyomi, ask-on, ask-kun, distractors, quiz_exclusions; list values are space-separated. "ask-on" and "ask-kun" are what the
app asks (`quizOnyomi` / `quizKunyomi` when the card has them, otherwise the full lists, as `toReadingCard()` does in
`android\app\src\main\java\io\github\stopcran\kanji\data\ReadingData.kt`). The pools can be rebuilt from the
tags: the N1 stack holds every card tagged `jlpt-n1` to `jlpt-n5`, All every card, Starter every card tagged `starter`.

## 3. Dictionary entries (`jmdict-cited-entries.xml`)

Complete JMdict entries 1587610, 2711110: 1587610 (嫌 / 厭: いや, や, イヤ) is the attestation of や; 2711110 is the 応 entry whose
おお reading is restricted to a search-only form (not counted as an attested reading). Pinned input `n1-implementation-JMdict_e.gz`
(sha256 2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d). The Digital Daijisen text for 嫌 that your confirmation report cites is in the original packet
(`evidence\public-source\`) and at weblio.

## 4. Snapshot (`snapshot\kanji\`, `snapshot-identity.txt`)

The 15 cards of commit `10d7965266b69ed81703ab69f20cff873a0526e9` (10d79652 is the reviewed snapshot of your confirmation round). Byte-identical to
the cards in your confirmation packet; `snapshot-identity.txt` lists the git blob id of each.

## 5. Author's analysis (`checks\`, `evidence\tools\`): claims to verify, not evidence

`checks\`:
- `reading-exposure.txt` (RX in `RESPONSE.md`): the output of `evidence\tools\reading_exposure.py` for the 15 cards: for every prompt, the wrong options each pool can offer, the inventory of attested readings (KANJIDIC2, JMdict single-kanji entries, readings printed in the card text) and, in lines 317-349, the exploratory scan of all cards. Command: `python reading_exposure.py --seeds 2000 --scan-all --extra 素=もとより --extra 応=いらえる --extra 基=きりすと --extra 縮=ちり,ちじむ --extra 騒=さい --extra 級=しな 張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖`.
- `kotlin-reading-run.txt` (RUN-N): the real Kotlin `KanjiReadingQuiz.question` of the pinned Android commit over the content of this snapshot: the N1 and All stack pools (1,161 cards each), 4,000 seeds per prompt, and pools of one kanji and one other card (400 seeds). Produced by `evidence\tools\ScratchReadingExposureTest.kt.txt`.
- `kotlin-starter-run.txt` (RUN-S): the same test for a Starter Practice-more session that borrows only the target (the 118 Starter cards plus the target), 4,000 seeds per prompt.
- `kotlin-vs-exact.txt` (XC): `evidence\tools\reading_exposure_crosscheck.py` compares both Kotlin runs with the Python analysis.

`evidence\tools\`:
- `reading_exposure.py`: the exact reachability analysis behind `checks\reading-exposure.txt`. It reads the cards and the pinned KANJIDIC2 and JMdict files of the author's checkout, so it cannot be run from this packet.
- `reading_options.py`: the simulation of the confirmation round (its inventory of attested readings has the gap described in `RESPONSE.md`); kept so that the change can be seen.
- `reading_exposure_crosscheck.py`: the cross-check that produced `checks\kotlin-vs-exact.txt`.
- `ScratchReadingExposureTest.kt.txt`: the scratch Kotlin test that produced the two Kotlin runs. It was placed in the Android checkout's core test folder for the runs and never committed; its header describes its environment variables.
