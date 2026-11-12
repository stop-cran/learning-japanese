# Evidence for the delta round

This packet contains only what is new since your follow-up round; everything else stays where it was (section 0). What is
here is supplied so that the claims in `RESPONSE.md` can be checked against sources, not taken on trust. Sections 1 to 4
are source material; section 5 is the author's own analysis (claims to verify, not evidence). The base of the delta is
commit `10d7965266b69ed81703ab69f20cff873a0526e9` (`10d79652`, the snapshot of your follow-up report); the revised snapshot is commit `30f2bd7c7b57e0d244a1cb86ba51e5b86121d4f8` (`30f2bd7c`).
The short names used in `RESPONSE.md` (CARD, CHG, DP, MP, TSV, JM, RO, RX, RUN-N, RUN-S, XC, FRESP, DJ, KD, FMT, VM, RD,
PAD, ST, KR, WD) are defined at its top; this file says which file of which packet each one is.

## 0. What this packet does not repeat

- The pinned Android sources are NOT copied. They are in your follow-up packet (`followup-110-10d79652-gpt`; its absolute
  path is in `INSTRUCTIONS.md`), folder `evidence\android\`, at the one pinned commit
  `10d98d0db61dcde621463460e6a1e59941b4042b`: section 1 of that packet's `evidence\README.md` and `evidence\android\SOURCES.tsv`
  give each file's size, SHA-256, blob id and raw URL; `call-sites.txt`, `routes.txt` and `compare-5c000bd-to-10d98d0d.txt` / `.patch`
  are there too. That packet is unchanged; the SHA-256 of its `packet-manifest.json`, which lists the SHA-256 of every file
  in it, is `4640e88aec9c1acc59a9b6229f952acdce69b7352f59dc0b11543513c03923b9`. The line numbers that `RESPONSE.md` cites for VM, RD, PAD, ST, KR and WD are line numbers
  of those files.
- Three statements of that packet's `evidence\README.md` are superseded (see D3 and D4 in `RESPONSE.md`): its description of
  `Words.kt` says that line 237 "keeps only variants of at least two kana" (line 237 filters the OUTPUT variants that `mutations`
  generates, not its input); its section 3 lists "いや, や, イヤ" as one group of readings of the entry 1587610 (イヤ is a
  kana-only reading, や is a reading without restriction; section 3 below gives the lines); and its scan line range "317-349" is
  lines 309-340 of `checks\reading-exposure.txt` here, because the 8-line block of the withdrawn prompt (before the scan) and one scan line (the padded-session hit for 嫌 いや) are gone.
- The original packet (`batch-110-453af714`) keeps the source extracts of the batch; the delta touches no meaning, stroke,
  component or title claim, so they are not repeated. The ones that matter here: DJ `evidence\public-source\weblio-嫌.txt`; KD
  `evidence\kanjidic2-records.xml`; `evidence\jmdict-digest.tsv` (line 2032 is the 嫌 row); FMT `repo\docs\content-format.md`
  (blob `d194707958817d71a6a807b680b14e35fdac1659`, the same blob at the original freeze and at this snapshot; the packet builder compared them
  after normalising CRLF to LF).
- Your earlier reports (`initial-gpt.md`, `confirm-gpt.md`, `followup-gpt.md` in `reports-110-gpt`) and the confirmation and
  follow-up packets are unchanged.

## 1. Android client sources

Not copied (section 0). Everything cited from them is in the follow-up packet at the one pinned commit.

## 2. Content metadata (`evidence\cards-reading-metadata.tsv`)

Every card of the revised snapshot (the whole shipped content at commit `30f2bd7c7b57e0d244a1cb86ba51e5b86121d4f8`), one row per card: kanji, tags, onyomi,
kunyomi, ask-on, ask-kun, distractors, quiz_exclusions; list values are space-separated and the first line names the
columns. "ask-on" and "ask-kun" are what the app asks (`quizOnyomi` / `quizKunyomi` when the card has them, otherwise the full
lists, as `toReadingCard()` does in RD). The pools can be rebuilt from the tags: the N1 stack holds every card tagged `jlpt-n1` to
`jlpt-n5`, All every card, Starter every card tagged `starter`. The file differs from the copy in your follow-up packet in exactly
one row, the 嫌 row: ask-kun is now `きら.う きら.い` (was `きら.う きら.い いや`); its kunyomi column still lists いや, and the other
columns are unchanged. The packet builder aborts if any other row differs.

## 3. Dictionary entries (`evidence\jmdict-cited-entries.xml`) and the other dictionary sources

Complete JMdict entries 1587610 and 2711110, byte-identical to the copy in your follow-up packet (the builder compared them;
the second entry, 応, is only context). Pinned input `n1-implementation-JMdict_e.gz` (sha256 `2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d`). Lines of this file (JM):

- Entry 1587610 starts with its `ent_seq` on line 4 and ends on line 53.
- `k_ele` 嫌 is lines 5-10 and `k_ele` 厭 lines 11-14 (its `ke_inf` "rarely used kanji form" is line 13).
- `r_ele` いや is lines 15-20; `r_ele` や is lines 21-23, with no `re_restr` and no `re_nokanji`; `r_ele` イヤ is lines 24-28, with
  `re_nokanji` on line 26.
- The three senses are lines 29-35, 36-45 and 46-52 (the third is the interjection; its `misc` "word usually written using kana
  alone" is line 48).
- Entry 2711110 (応) follows from line 54; its おお reading is restricted to a search-only form.

Pinned KANJIDIC2 input: `n1-planning-kanjidic2.xml.gz` (sha256 `af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed`). Its 嫌 record is lines 324-393 of KD (readings on 371-375: ケン,
ゲン, きら.う, きら.い, いや; meanings on 376-378), and it lists no や. DJ is a 7-line file whose line 6 holds both Digital Daijisen
entries together: the character entry of 嫌 (readings and the words 嫌気, 嫌味) and the entry や, which explains it as a sound
change of いや.

## 4. Snapshot and diffs (`snapshot\kanji\`, `snapshot-identity.txt`, `diffs\`)

`snapshot\kanji\` holds the 15 cards of commit `30f2bd7c7b57e0d244a1cb86ba51e5b86121d4f8` as the raw working-tree bytes of the author's checkout (CRLF line ends).
The git blob ids in `snapshot-identity.txt` and the SHA-256 values in `manifest.json` are those of the same bytes after
normalising CRLF to LF; `packet-manifest.json`, which hashes the raw files, therefore lists other SHA-256 values for these
files. Fourteen cards are byte-identical to the copies in your follow-up and confirmation packets; `snapshot\kanji\嫌.md` is the
only changed card (blob `52a73a70028b01a97295820ff08eb78ee7487287`, base blob `13acf1ee9a693d6d5da019d72d97336f02b1c052`).
`snapshot-identity.txt` gives commit, tree, parent, base and the blob id of each card.

`diffs\`:
- `changed-files.txt`: name and status of the changed files (tab-separated): `kanji/嫌.md` and `manifest.json`, both modified.
- `changed-lines.txt`: the changed line numbers on the revised side of the card.
- `delta.patch`: `git diff` from `10d79652` to `30f2bd7c` for every file except `manifest.json` (the card only).
- `manifest-delta.patch`: the two-line change of `manifest.json` (the `contentVersion` and the SHA-256 of `kanji/嫌.md`). To check
  that hash, normalise CRLF to LF in `snapshot\kanji\嫌.md`, take the SHA-256 and compare it with the `+` line for `kanji/嫌.md`.
- `checks-vs-followup.diff` and `reading-options-vs-confirm.diff`: every difference between the five plain check copies of this
  packet and the earlier packets' copies (section 5).

## 5. Author's analysis (`checks\`): claims to verify, not evidence

`checks\` (name, size, SHA-256):

- `checks\budget.txt` (150 bytes, sha256 `ddb4da61ec6d7fdcc62c53b6dfbed024625521b1d34a1c053d7e51f30729d4b2`)
- `checks\gradle-kotlin-reading.txt` (735 bytes, sha256 `d3c3dbd9f66a98ddc8a11eb5b4303ec494916f8a44f4203ebe56aadf302f83de`)
- `checks\gradle-kotlin-starter.txt` (743 bytes, sha256 `0270e47921c2c1e9a1202d9545d4ab164023dc57e47907366b05bd9c8dfad299`)
- `checks\jvm-readings.txt` (743 bytes, sha256 `c85d4e34bd7a1f0b9942b9b9ea0dfb9c08f18605dc21ee9791debd7ade9e13f0`)
- `checks\jvm.txt` (2650 bytes, sha256 `92ef1d3d6b3974190415f4505058d64e35e23ea45f3319f51ffb1a2a283c0ce0`)
- `checks\kotlin-reading-run.txt` (21900 bytes, sha256 `f6b3003a2113b848bb19f4851401f62665fbe160268955e50d531ddede9f9cc2`)
- `checks\kotlin-starter-run.txt` (11438 bytes, sha256 `c15bde50adcf0608e8dfb3c505c4285deff58b588e941343912396415b39732d`)
- `checks\kotlin-vs-exact.txt` (11782 bytes, sha256 `8fac18d4abb71954b308080c40b2c6b4898e08ca28e552312aca3b47b079b9ca`)
- `checks\link-targets.tsv` (288 bytes, sha256 `afe4339272e281669089a88c10404087741106de045c463a71583c261c5cf5d7`)
- `checks\lint.txt` (1170 bytes, sha256 `bdfcd720774ca84793b8ede8af74392942498e404b6ca1d7629d0a5956e796c8`)
- `checks\manifest.txt` (261 bytes, sha256 `f31ba1b7e66701395a915981e3cc61c6ed822fb9077ee1e779106606af38296d`)
- `checks\quiz-safety.txt` (4782 bytes, sha256 `b9c04d760dc40029721d8f50387c636dbd3e6661ac858bfa5c1db256f9e1f8bd`)
- `checks\reading-exposure.txt` (35976 bytes, sha256 `398b6b8446c0a62e3d543d43d943756dbdcc63cdc11e20b769c888be90dcf44e`)
- `checks\reading-options.txt` (25032 bytes, sha256 `3019b43029dc33bab2d669182d99c0609c63d0d577ab053fb6ca761b2c44ccf9`)
- `checks\summary.txt` (131 bytes, sha256 `63c6e50a2c19d9439febdb2d9a4170a7e4d7fba41ba9a2993fd3bd41061ce593`)
- `checks\unittest.txt` (99 bytes, sha256 `1684ecbfdb3fca794a919f37b07f27d07b70778d238c97264a6399ddfef8abee`)
- `checks\validate.txt` (11 bytes, sha256 `d76219a16ae024518727cd88255c3c11316194b0b7181b95aa3bb3d46a6472db`)
- `checks\vocabulary.txt` (61 bytes, sha256 `c2362f303180a98576f2928f2a1f8e60ac6c625910a068fdd401aeb1b3261e73`)

Five files are plain byte copies of the author's outputs and keep their own line numbers, which are the ones `RESPONSE.md`
cites: `reading-options.txt` (RO, 301 lines), `reading-exposure.txt` (RX, 340 lines), `kotlin-reading-run.txt` (RUN-N, 108 lines),
`kotlin-starter-run.txt` (RUN-S, 57 lines) and `kotlin-vs-exact.txt` (XC, 107 lines). RO, RX and XC have CRLF line ends, RUN-N
and RUN-S have LF. Every other file in `checks\` has its blank lines removed (so its line numbers differ from the original log),
`unittest.txt` is cut to its last three lines, `gradle-kotlin-reading.txt` and `gradle-kotlin-starter.txt` are the Gradle logs of
the two scratch runs, and `link-targets.tsv` is written by the packet builder: one row per internal link on a changed line, with
the columns card:line, link text, resolved path, exists, target title, quoted gloss after link and quoted equals title, and a
last line with the totals.

How the files were produced, all by the author on the snapshot `30f2bd7c`:
- `lint.txt`, `unittest.txt`, `validate.txt`, `budget.txt`, `vocabulary.txt`, `manifest.txt` and `summary.txt`: the author's gate script. lint is
  the author's batch lint (`n1_batch_tool.py lint`, not part of this packet); the others are `python -m unittest discover -s tools -p "test_*.py"`,
  `python tools/validate.py`, `python tools/check_content_budget.py`, `python tools/grammar_vocabulary.py check` and
  `python tools/build_manifest.py` followed by `git diff --exit-code manifest.json` (the committed manifest must equal a rebuild);
  `summary.txt` lists the six exit codes and times.
- `quiz-safety.txt`: the author's `quiz_safety.py` simulation of the quiz for the 15 cards (not part of this packet).
- `jvm.txt`: the Android checkout's real-content test and rare-han test over this content
  (`:core:cleanTest :core:test --tests '*RealContentTest*' :app:cleanTestDebugUnitTest :app:testDebugUnitTest --tests '*RareHanTest*'`);
  `jvm-readings.txt`: `:core:cleanTest :core:test --tests '*KanjiReadingsTest*'`. They show BUILD SUCCESSFUL and nothing more; the test
  report files are overwritten by later runs, so no test counts are claimed.
- `reading-options.txt` (RO): `python reading_options.py --seeds 200 --extra 素=もとより --extra 応=いらえる --extra 基=きりすと --extra 縮=ちり,ちじむ --extra 騒=さい --extra 級=しな --extra 嫌=や 張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖`.
- `reading-exposure.txt` (RX): `python reading_exposure.py --seeds 2000 --scan-all` with the same seven `--extra` options and the same 15 kanji. Its scan of all cards
  is lines 309-340. `--extra` adds readings that the card text prints but the metadata does not list; the one new here is `嫌=や`, because
  line 45 of the card now names や.
- `kotlin-reading-run.txt` (RUN-N) and `kotlin-starter-run.txt` (RUN-S): the real Kotlin `KanjiReadingQuiz.question` of the pinned Android commit
  over the content of this snapshot, 4,000 seeds per prompt. `evidence\tools\ScratchReadingExposureTest.kt.txt` of the follow-up packet was copied as
  `ScratchReadingExposureTest.kt` into the core test folder of the Android checkout (never committed; deleted afterwards) and run with
  `:core:cleanTest :core:test --tests '*ScratchReadingExposureTest*'`; its environment variables are `N1_OUT` (result file),
  `N1_BATCH` (the 15 kanji), `N1_SEEDS` (4000), `N1_POOLS` and `N1_SMALL`. RUN-N used `N1_POOLS=stacks` (the N1 and All stack pools of 1,161 cards) and
  `N1_SMALL='嫌:屋,家,八,夜,冶,野;騒:催,再,西;基:供,共,友;張:割'` (pools of the target and one other card, 400 seeds); RUN-S used `N1_POOLS=starter`
  (the 118 Starter cards plus the borrowed target).
- `kotlin-vs-exact.txt` (XC): `python reading_exposure_crosscheck.py` with the same seven `--extra` options over both Kotlin runs.

`diffs\checks-vs-followup.diff` compares the copies of your follow-up packet with the copies here for RX, RUN-N, RUN-S and XC (its
line numbers are those of the plain files); `diffs\reading-options-vs-confirm.diff` compares the copy of your confirmation packet with RO
(your follow-up packet had none), with the blank lines of both sides removed, so its line numbers count non-blank lines.
The kinds of difference, and nothing else:
- The label of the attested reading や reads "(card text, JMdict 1587610)" (RX) or "(card text/JMdict 1587610)" (XC) instead of "(JMdict 1587610)",
  and RO now lists や as "(card text)" for 嫌 instead of "none". The cause is the new `--extra 嫌=や`; the readings and the pool facts are unchanged.
- Everything that belonged to the withdrawn prompt is gone: the block `kun prompt いや` of RX (8 lines, including its PAD-HIT line) and of RO; in RUN-N the two PROMPT lines of 嫌 いや for the N1 and All
  stacks and the six small-pool lines 嫌+屋, 嫌+家, 嫌+八, 嫌+夜, 嫌+冶, 嫌+野 for いや; in RUN-S the PROMPT line of 嫌 いや in the Starter session (the line in which や was drawn 1,310 times in 4,000 seeds);
  the matching cross-check lines in XC (the Starter-session one carries the PAD-HIT mark); the scan line of RX that reports the PAD-HIT for 嫌 いや; and the counts that follow: `PROMPTS` 26 to 25 (RUN-N and RUN-S), XC (52 whole-stack-pool prompts, 26
  Starter-session prompts and 32 small-pool prompts, 1 PAD-HIT, 4 NOTE) to (50, 25, 26, 0, 3), RX (1 padded-session hit(s), 888 prompts, 331 collisions,
  13 Starter-session-only hits) to (0, 887, 330, 12); the 19 whole-stack hits and the 5 latent collisions are unchanged.
- In RO the two lines "unlisted-reading check: none of the 0 unlisted readings is offered by any of the ... other cards" of the 嫌 prompts ゲン and きらう
  are replaced by one note each: や is offered only by 冶 夜 野 (ゲン) and by 八 家 屋 (きらう) and cannot be drawn from the full pool (lower closeness tier).
- The POOLS line of RUN-N (line 1) now also lists the Starter pool (118 cards). The two XC header lines now name the run files under `_checks-110-fix3` (the earlier copy named them under `scratch-110`), and the first of the two `pools:` lines of XC gives the
  pool sizes including Starter. The shipped harness writes the Starter entry on every run, and it is byte-identical in your follow-up
  packet and here; the follow-up copy of RUN-N lacks that entry, so that copy was written by an earlier revision of the harness (before the
  Starter pool was added to it). This run uses the shipped harness. The two 張+割 small-pool lines now come last in the small-pool block, in RUN-N and, correspondingly, in XC:
  the harness writes the small-pool lines in the order of its `N1_SMALL` specs and the `N1_SMALL` of the earlier run is not recorded, so a different spec order is the author's inference and not a recorded fact. Apart from the lines listed above, RUN-N is identical to the earlier copy.

`evidence\tools\` is NOT copied. The four tools of your follow-up packet are unchanged (the packet builder compared the bytes of the author's
copies with the follow-up packet's `evidence\tools\`); only their names, sizes and SHA-256 values are recorded here:

- `ScratchReadingExposureTest.kt.txt` (6008 bytes, sha256 `59db18104f2e949a543cd8cd0964b4468f04675a54d76ea016ecf63fcac86ad4`)
- `reading_exposure.py` (18761 bytes, sha256 `14823d230e3b3c8b821143e4b5d28aa724172ef4502f14de70823aaef1a6c247`)
- `reading_exposure_crosscheck.py` (6899 bytes, sha256 `931899ec63352953ead80137d5bb8df9bf84fceb96d34edaa8b1d43263426f77`)
- `reading_options.py` (13409 bytes, sha256 `cc3f23feda78de87cfb3e72c8c830da07f0fd12ee443bf25538f9ec87172b2a4`)

They read the cards and the pinned KANJIDIC2 and JMdict files of the author's checkout, so they cannot be run from this packet; read them in
the follow-up packet. `reading_exposure.py` is the exact reachability analysis behind RX; `reading_options.py` is the simulation of the
confirmation round (its inventory of attested readings has the gap described in `RESPONSE.md`); `reading_exposure_crosscheck.py` produced XC;
`ScratchReadingExposureTest.kt.txt` is the scratch Kotlin test behind RUN-N and RUN-S (its header describes its environment variables).
