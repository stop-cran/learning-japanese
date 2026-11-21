Snapshot: `a7cc61e27261c62e84c3bd1f28e8a9254d9dcb04`, compared with `3c5ef8450e38051682dab2bea5fce320b992e5ea` through merge `e37ad00b796ed16dc752f5e60f0fd119f14dfa5e`. Reviewer: OpenAI ChatGPT, GPT-family; the exact serving-model identifier is not exposed.

Scope:

- Fully read this packet's `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `changed-files.txt`, `changed-lines.txt`, and `evidence\README.md`; also my authorized prior `reports-156-hold\confirm-gpt.md`.
- Fully read all ten revised `snapshot\kanji\` cards. Compared the complete five changed cards with their earlier-confirmation counterparts: only the specified Metadata lines differ. The other five cards and the supplied word snapshots `亜熱帯.md`, `仁.md`, and `甲乙.md` are byte-identical to their earlier-confirmation counterparts.
- Fully read the six complete entries in `evidence\jmdict-cited-entries.xml`, both Metadata scans, `meta_scan.py`, `merge-scope.txt`, `QuizBuilder.kt`, and all supplied meaning/reading option and exposure outputs. Read the named validation outputs and `link-targets.tsv` completely.
- Earlier-confirmation context: fully read `evidence\compound-sound-changes.md`. Original-packet context: read the rubric through line 160, `KanjiReadings.kt:1–150`, `Words.kt:216–250`, and selected complete JMdict entries 1149820, 1193420 and 1500220. Compared the two rounds' word-quiz outputs by bytes, without treating that comparison as a fresh semantic audit.
- Independently fetched the actual public [Jisho/JMdict 伯母さん entry](https://jisho.org/search/%E4%BC%AF%E6%AF%8D%E3%81%95%E3%82%93), including its reading, aunt sense, spelling restriction and link identifying entry 2261500; no search snippet was used as verification.

Dispositions:

- P1 - DECLINE ACCEPTED - The earlier suggestion was explicitly nonblocking. The inspected shared article explains h-to-p change but does not demonstrate the nasal environment; deferring that teaching expansion is reasonable for this Metadata-only revision. `diffs\changed-files.txt` contains no article, and the full merge-path list likewise contains no `articles/compound-sound-changes.md`. Unchanged status is supported by the supplied Git evidence, not a fresh checkout comparison.
- A1 - RESOLVED - The actual old/new comparison reproduces the five hunks in `diffs\fix.patch`: exactly six IDs were inserted at 乙:60, 亜:53, 仁:55, 仙:51 and 伯:53, with every other character on those lines and every other card line unchanged. The six complete XML entries identify the named words correctly:
  - 1862630: 乙種, おつしゅ, “B-grade; second-class”.
  - 1149860: 亜麻, あま, “flax; linseed”. The additional アマ reading has `re_nokanji`; it is not an unrestricted kanji-spelling reading.
  - 1369740: 仁術, じんじゅつ, “benevolent act; healing act”.
  - 1387150: 仙骨/薦骨, せんこつ, “sacrum; sacral bone”; the hermitry/appearance senses are restricted to 仙骨.
  - 1329130: 酒仙, しゅせん, “heavy drinker”.
  - 2261500: 伯母さん/叔母さん, おばさん, “aunt”, with the older/younger-than-parent spelling distinction.
  The first five named words occur only as written examples in the cards, without asserted readings or glosses. 伯:33 and :38 give おばさん, and :38 gives “aunt”; both agree with the complete entry and public corroboration.
  The six before-scan omissions match the old cards' named words and Metadata lists; all six IDs are present afterward. Each remaining substring match is acceptable: 熱帯 occurs inside 亜熱帯, 歌舞 inside 歌舞伎, 伏せ inside 伏せる, and 母さん inside 伯母さん. Their longer words have entries 1149820, 1193420, 1500220 and 2261500 respectively, and the shorter forms are not separately named words on these cards.
  `merge-scope.txt` supplies the stated merge parents and an empty batch-restricted diff; its 102-path full list does not include a batch content path. The check outputs agree with CHANGES: lint 0 errors/1 潜る warning; 439 tests OK; validation, link-plan and kanji-remarks checks report zero problems; manifest before/after hashes match with a reported clean tree; retained bytes are 56,608,909. Six seven-digit IDs plus separators account for 54 added bytes. Vocabulary, meaning-quiz and word-quiz outputs are byte-identical to the earlier packet; both reading outputs are identical after their first line.

Verdicts:

- Correctness: CLEAN - All six added citations are appropriate; no new factual defect established in 乙, 亜, 仁, 仙 or 伯.
- Scoped coverage: CLEAN - The citation gaps are repaired without removing or expanding learner-facing coverage.
- Consistency and quiz safety: CLEAN - All ten displayed meaning sets remain distinct from their correct answers and do not conflict with the cards' direct exclusions. `QuizBuilder.kt` checks exclusions symmetrically, including between chosen options; it does not transitively expand them. Reading mechanics exclude listed on/kun readings and mutations and use curated candidates before fallback. The unchanged 伯 は HIT remains latent: its three curated cards fill the wrong slots in the supplied production pools. No new reachable collision established.
- Comprehensibility: CLEAN - Only source IDs changed; learner-facing explanations and examples are unchanged. No card-specific new ambiguity established.

Confirmation: CONFIRMED - P1 is DECLINE ACCEPTED, A1 is RESOLVED, and no new actionable defect was established.

Findings: none.

Optional: none beyond the already dispositioned P1 follow-up.

Limits:

- Exact serving-model version unavailable. CLEAN is bounded, not exhaustive linguistic correctness.
- No repository checkout, fresh Git history verification, full pinned dictionary, corpus scan, or test rerun was used. Supplied merge/check logs support their stated results but do not independently prove their execution provenance. The full-dictionary uniqueness claim and absence of every possible additional Metadata gap were not independently established; the six specific repairs and four reported substring cases were checked directly.
- The scan omits kana-only and single-kanji words. Its required `n1lib` is unavailable here. Three longer-word entries were selected by parsing the supplied XML excerpt, rather than reading that large excerpt in line ranges.
- Reading audits cover their stated pools, samples and one-holder padding cases, not every possible borrowed-card combination. Their unchanged latent-collision counts are not new findings. Different meaning titles alone do not guarantee different senses. The byte-identical word audit was not independently re-adjudicated in full.
- No native Android/JVM execution, stroke rendering or actual phone-layout test was performed; the packet explicitly reports JVM tests were not run.
- One initial bounded comparison command failed on Windows output encoding and was retried successfully with UTF-8. Exactly one tool call was issued per tool-bearing response; there were no parallel calls, combined shell commands, delegation, background jobs, other sessions, recursive listings or unauthorized local reads. Single Python invocations performed bounded packet comparisons/extractions. Only this authorized report file was created.
