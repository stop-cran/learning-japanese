# evidence\integrity\: signed objects, manifest and app code (limit L1)

This folder answers limit L1 of the earlier GPT confirmation reports. The packets so far gave transcripts only. This folder
gives the signed Git objects, the actual manifest, the app's kanji-reading builder and the Python ports. A reviewer can
check the transcripts against these objects. Nothing here needs network access except the optional public cross-checks
named below.

## Run

```
python -B evidence\integrity\verify.py --prior-packet <path of the earlier confirmation packet>
```

`verify.py` only reads. It reads files under this packet, plus the earlier packet's `snapshot\` and `packet-manifest.json`
when you pass `--prior-packet`. If it finds `gpgv`, it runs gpgv with `--homedir` set to a directory that does not exist
(gpgv does not create it) and `--keyring` set to `key\signing-key.gpg`. No GnuPG state is read or written. The author's run is
in `evidence\integrity-verify-transcript.txt`.

## Contents

- `commits\<sha>.commit`: the raw commit objects (`git cat-file commit`) of the batch chain, newest first:
  ef00345d -> 348c4f70 -> ccc046bb -> 6605a8b0 -> 60d2cd5a -> ad1694c1.
  - `<sha>.payload` is the object without its `gpgsig` header. That is the exact text Git signs.
  - `<sha>.sig` is the de-indented armored signature.
  - `verify.py` checks three things: that each object hashes to its name (`sha1("commit <len>\0" + bytes)`), that the split
    is exact, and that the parent chain is linear.
- `key\signing-key.asc`: the public key published at https://github.com/stop-cran.gpg, fetched on 2026-11-23.
  - Its fingerprint is D4C9A275A218AF747B787AFA9D94B9D311BD26A7 (ed25519, created 2026-04-14).
  - `key\signing-key.gpg` is the same key dearmored, because gpgv needs a binary keyring. `verify.py` checks that the two
    are the same key.
  - Optional public cross-check: open the URL and compare it with this file. If the bytes differ, compare the
    fingerprint that gpgv reports instead.
- `trees\<sha>.tree`: raw tree objects at 348c4f70 and ef00345d for `/`, `kanji`, `words`, `docs`, `docs/n1-sources` and
  `tools`. `integrity.json` maps each commit and path to its tree.
  - `verify.py` hashes each tree.
  - It checks that the root tree is the one named in the signed commit, and that each subtree is the entry of its parent.
  - Through these trees it binds this packet's `snapshot\` (and, with `--prior-packet`, the earlier packet's `snapshot\`)
    to the signed commits.
  - It accepts the file bytes as stored in the blob, or after CRLF -> LF.
- `manifest\348c4f70.manifest.json` and `manifest\ef00345d.manifest.json`: the actual `manifest.json` blobs. `verify.py`
  checks four things:
  - each is the `manifest.json` entry of the signed root tree;
  - its `contentVersion` recomputes with the algorithm of `blobs\tools\build_manifest.py`, which is itself bound to the
    signed tree;
  - its `files` map lists exactly the files of `kanji/` and `words/` in the signed tree;
  - every snapshot file under `kanji/` and `words/` has its manifest SHA-256, computed after CRLF -> LF as both
    `build_manifest.py` and the app do.

  It also prints which manifest entries differ between the two commits.
- `app-code\`: 14 Kotlin files of https://github.com/stop-cran/kanji-cards-android at commit
  91e1d4b578859f7bfb582f7b9c6acf48c6ca6a75. That is the head of `main` on 2026-11-23; its last commit is dated 2026-11-21.
  - `app-code\SOURCES.json` gives each file's Git blob id, raw URL and web URL. Any file can be cross-checked publicly.
    `verify.py` rehashes every copy, and checks that `evidence\QuizBuilder.kt` and `evidence\Words.kt` are byte-identical to
    the copies here.
  - Kanji reading questions: `core\...\reading\KanjiReadings.kt`, `KanjiReadingQuiz.question` at lines 91-116.
    - It never offers the card's own readings or their `ReadingOptions.mutations` as wrong options (`excludedKeys`, lines
      80-88).
    - It fills the wrong options first from the card's curated distractors (line 110). Next come the other cards' closest
      readings (line 111). Any other reading comes last (line 112).
  - Session padding and calls: `app\...\ui\KanjiReadingViewModel.kt`.
    - Line 114 pads with `padCandidates` from `app\...\data\Padding.kt` (types from `core\...\srs\PracticePadding.kt`).
      `Padding.kt:19` returns no padding for the All stack and the JLPT stacks (`core\...\srs\Stacks.kt`).
    - Line 151 calls `KanjiReadingQuiz.question`.
  - Meaning options: `core\...\quiz\QuizBuilder.kt`, called at `QuizViewModel.kt:169`. Word options:
    `WordQuizBuilder.options` in `core\...\words\Words.kt`, called at `WordQuizViewModel.kt:308`.
  - Parsing of the card fields these use (`FrontMatter.kt`, `ContentParser.kt`, `Models.kt`,
    `KanjiMeaningMetadata.kt`):
    - `ContentParser.kt:225-231` skips, and records as a problem, every manifest file whose SHA-256 differs
      (`textPathProblem`, lines 241-249, "hash mismatch" at line 247).
    - `ContentParser.kt:653-657` normalizes CRLF -> LF before hashing, as `build_manifest.py:18-19` does.
  - `ContentSync.kt` loads a parsed source into the app.
- `ports\`: `reading_exposure.py`, `reading_options.py` and the shared `n1lib.py`. These are the Python ports that
  produced `checks\reading-exposure.txt` and `checks\reading-options.txt`. Their docstrings name the Kotlin functions they
  port, so a reviewer can compare them with `app-code\`. They are the author's tools and are not in either repository;
  `ports\SOURCES.json` only ties these copies to the ones the checks ran.

## What this does not establish

- Commits after ad1694c1 are local until publication. The objects in this folder are the only copy a reviewer can read.
  The base ad1694c1 is public at https://github.com/stop-cran/learning-japanese/commit/ad1694c1fe537a090c712065e77c480deb9edf4d.
- Only the snapshot files are bound by content. For the other files in `kanji/` and `words/`, the trees bind only the path
  set. Their manifest hashes rest on `checks\manifest.txt`: a rebuild at the snapshot left `manifest.json` byte-identical.
- The app code is read, not compiled or run here. There is no JDK, the Kotlin tests were not run, and no phone test was
  done. Which app build a phone runs is outside the packet.
- The publication ZIP does not exist yet. CI builds it at publication, and the closure records its receipt.
