"""Builds the batch-110 follow-up packet for the GPT reviewer (arguments of n1_followup_packet.py for this round)."""
import os, subprocess, sys

W = r"C:\Users\stop-\n1-kanji-workspace"
L = W + r"\lean"
RP = W + r"\review-packets"
SC = W + r"\scratch-110"
A = W + r"\rollout-recovered\kanji-cards-android"
b = "app/src/main/java/io/github/stopcran/kanji/"
k = "core/src/main/kotlin/io/github/stopcran/kanji/core/"

files = [
    (b + "ui/KanjiReadingViewModel.kt", "VM. 83-85 the pool is `content.inStack(stack)`; 92-95 `practiceMinimum()` and `readingData` (its cards become `readingCards`); 97-98 a short Practice-more session is padded; 109-133 `pad`, where borrowed cards are added to `readingCards` (125-128); 151 the only production call that builds a displayed reading question"),
    (b + "ui/KanjiReadingScreen.kt", "SCR. 33 the session key `kreading:<timestamp>[:extra]`; 36 `ensureStarted(sessionKey.endsWith(\":extra\"))`; 50 the Practice-more button"),
    (b + "data/ReadingData.kt", "RD. 13-18 `toReadingCard()` (the ask lists are `quizOnyomi` and `quizKunyomi` when present, otherwise the full lists); 25-28 `ReadingRequest`; 30-53 `readingData`, where 36 maps every card of the stack to a `ReadingCard`"),
    (b + "data/Padding.kt", "PAD. 9-12 `practiceMinimum()`; 18-25 `padCandidates`: 19 returns nothing for the All stack and every JLPT stack, 22-23 take started cards of other stacks that are not in the current stack; 32-35 `padWordCandidates` (word sessions)"),
    (b + "data/SrsMapping.kt", "SRS. 35-38 `inStack` keeps the cards for which `Stacks.includes` holds"),
    (b + "data/Database.kt", "DB. 557-559 `borrowable`: started cards (phase not New) of the same source and mode in another stack, never from the All stack"),
    (b + "data/KanjiReviews.kt", "KRV. 110-121 availability check only (`Random(0)`, null test) for a cross-level reading; no question is displayed"),
    (b + "data/Unlock.kt", "Context only. 38-49 `focusStatus` maps the stack's cards to reading cards (availability, no displayed question)"),
    (b + "data/HomeRepository.kt", "Context only. 88-91 the home screen asks `padCandidates` whether a mode can be padded"),
    (b + "ui/HomeData.kt", "Context only. 219-224 the home screen builds the readings queue from the stack's cards (counts; no question is built)"),
    (b + "ui/DrawViewModel.kt", "Context only. 201-206 `pad` for the drawing session (`StudyMode.Draw`); the file never refers to `KanjiReadingQuiz` or `ReadingCard`"),
    (b + "ui/QuizViewModel.kt", "Context only. 126-131 `pad` for the meaning-quiz session (`StudyMode.Quiz`); the file never refers to `KanjiReadingQuiz` or `ReadingCard`"),
    (b + "MainActivity.kt", "Context only. 89-92 session route prefixes (`kreading:`); 366-372 the readings route and its `onPracticeMore` (371); 409 the home screen's entry to the readings screen"),
    (k + "srs/Stacks.kt", "ST. 9-23 the stacks (All, N5 to N1, Starter); 25-30 `jlptLevel` and `stateId`; 33-36 `includes`: a JLPT stack contains its own level and every easier level"),
    (k + "srs/PracticePadding.kt", "PP. 33-42 `fill`: started cards (phase not New) that are not excluded, weakest retrievability first, `take(need)`"),
    (k + "focus/FocusBatch.kt", "FB. 22-29 `requiredReadingKeys`; 25 availability check only (`Random(0)`, null test)"),
    (k + "reading/KanjiReadings.kt", "KR. 46-54 `ReadingCard`; 57-61 `quizReadings` and `quizKeys`; 79-88 `KanjiReadingQuiz` and `excludedKeys`; 91-116 `question`: 98-101 `add` (100: a wrong option must not be in `excludedKeys`), 102-106 `closeness`, 110 curated distractors, 111 closeness fallback, 112 final fallback, 113 null when no wrong option was found; the queue code starts at 146"),
    (k + "words/Words.kt", "WD. 160-166 `WordQuizBuilder.options` (the word quizzes; 164 builds the reading options of a word); 209-214 `ReadingOptions`; 226-238 `mutations`: 237 keeps only variants of at least two kana"),
    ("core/src/test/kotlin/io/github/stopcran/kanji/core/KanjiReadingsTest.kt", "KT. 207-233 the content-snapshot test: every reading card has a valid question and no wrong option is in `excludedKeys` (which knows only the listed readings)"),
]
compare = [b + "data/Padding.kt", k + "srs/Stacks.kt", k + "reading/KanjiReadings.kt", b + "data/ReadingData.kt", b + "ui/KanjiReadingViewModel.kt",
           k + "srs/PracticePadding.kt", k + "words/Words.kt", k + "focus/FocusBatch.kt", b + "data/SrsMapping.kt", b + "data/Database.kt",
           b + "data/Unlock.kt", b + "ui/HomeData.kt", b + "data/HomeRepository.kt", b + "data/KanjiReviews.kt"]

cmd = [sys.executable, L + r"\n1_followup_packet.py", "--batch", "110", "--snapshot", "10d79652",
       "--out", RP + r"\followup-110-10d79652-gpt",
       "--instructions", RP + r"\confirm-inputs-110\FOLLOWUP-INSTRUCTIONS-gpt.md",
       "--response", RP + r"\confirm-inputs-110\FOLLOWUP-RESPONSE-gpt.md",
       "--report", RP + r"\reports-110-gpt\followup-gpt.md",
       "--orig-packet", RP + r"\batch-110-453af714",
       "--confirm-packet", RP + r"\confirm-110-10d79652-gpt",
       "--prior-report", RP + r"\reports-110-gpt\initial-gpt.md",
       "--prior-report", RP + r"\reports-110-gpt\confirm-gpt.md",
       "--android-repo", A, "--android-commit", "10d98d0db61dcde621463460e6a1e59941b4042b",
       "--android-slug", "stop-cran/kanji-cards-android", "--verify-raw",
       "--compare-rev", "5c000bd",
       "--jm-id", "1587610", "--jm-id", "2711110",
       "--check", "reading-exposure.txt=" + SC + r"\reading-exposure-starter2.txt",
       "--check", "kotlin-reading-run.txt=" + SC + r"\kotlin-reading-run.txt",
       "--check", "kotlin-starter-run.txt=" + SC + r"\kotlin-starter-run.txt",
       "--check", "kotlin-vs-exact.txt=" + SC + r"\kotlin-vs-exact-final.txt",
       "--check-note", "`reading-exposure.txt` (RX in `RESPONSE.md`): the output of `evidence\\tools\\reading_exposure.py` for the 15 cards: for every prompt, the wrong options each pool can offer, the inventory of attested readings (KANJIDIC2, JMdict single-kanji entries, readings printed in the card text) and, in lines 317-349, the exploratory scan of all cards. Command: `python reading_exposure.py --seeds 2000 --scan-all --extra 素=もとより --extra 応=いらえる --extra 基=きりすと --extra 縮=ちり,ちじむ --extra 騒=さい --extra 級=しな 張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖`.",
       "--check-note", "`kotlin-reading-run.txt` (RUN-N): the real Kotlin `KanjiReadingQuiz.question` of the pinned Android commit over the content of this snapshot: the N1 and All stack pools (1,161 cards each), 4,000 seeds per prompt, and pools of one kanji and one other card (400 seeds). Produced by `evidence\\tools\\ScratchReadingExposureTest.kt.txt`.",
       "--check-note", "`kotlin-starter-run.txt` (RUN-S): the same test for a Starter Practice-more session that borrows only the target (the 118 Starter cards plus the target), 4,000 seeds per prompt.",
       "--check-note", "`kotlin-vs-exact.txt` (XC): `evidence\\tools\\reading_exposure_crosscheck.py` compares both Kotlin runs with the Python analysis.",
       "--tool", L + r"\reading_exposure.py", "--tool", L + r"\reading_options.py",
       "--tool", L + r"\reading_exposure_crosscheck.py", "--tool", L + r"\ScratchReadingExposureTest.kt.txt",
       "--tool-note", "`reading_exposure.py`: the exact reachability analysis behind `checks\\reading-exposure.txt`. It reads the cards and the pinned KANJIDIC2 and JMdict files of the author's checkout, so it cannot be run from this packet.",
       "--tool-note", "`reading_options.py`: the simulation of the confirmation round (its inventory of attested readings has the gap described in `RESPONSE.md`); kept so that the change can be seen.",
       "--tool-note", "`reading_exposure_crosscheck.py`: the cross-check that produced `checks\\kotlin-vs-exact.txt`.",
       "--tool-note", "`ScratchReadingExposureTest.kt.txt`: the scratch Kotlin test that produced the two Kotlin runs. It was placed in the Android checkout's core test folder for the runs and never committed; its header describes its environment variables.",
       ]
for p, n in files:
    cmd += ["--android-file", p + "|" + n]
for p in compare:
    cmd += ["--compare-file", p]

env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1", N1_REPO=W + r"\rollout-recovered\learning-japanese")
r = subprocess.run(cmd, cwd=L, env=env, capture_output=True)
print("exit", r.returncode)
print(r.stdout.decode("utf-8", "replace")[-3000:])
print(r.stderr.decode("utf-8", "replace")[-3000:])
sys.exit(r.returncode)
