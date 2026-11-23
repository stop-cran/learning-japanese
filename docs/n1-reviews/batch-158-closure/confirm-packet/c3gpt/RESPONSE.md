# Author's statement for the reviewer of `b158-confirm-reports2\gpt.md`

Your confirmation report on 348c4f70 was UNVERIFIED. You found no defect and accepted or resolved F1, F2 and O1. Only L1 remained: the actual manifest, the signed Git objects and the kanji-reading builder were not available, so you could not verify them independently. This packet adds them. This statement answers L1 and one wording change that another reviewer proposed.

- **Labels:** L1 is your Limit L1, which you marked PARTIALLY RESOLVED. N1 is the new wording change.
- **Your report file:** you could not write your report to the requested file. The author saved your final message, unchanged, as that report.
- **What this text is:** the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence.
- **Line numbers** refer to the revised files in this packet.
- **What changed:** `words\升.md` (one body line) and the regenerated `manifest.json`. See `CHANGES.md`.

Give a disposition for each of L1 and N1, and say whether the revision introduces any new defect.

## Limit answered

### L1: the manifest, signed Git objects and kanji-reading builder were not available

Author action: **the objects are now in the packet, with a read-only checker**. The folder is `evidence\integrity\`; its `README.md` describes each file. Run:

```
python -B evidence\integrity\verify.py --prior-packet C:\Users\romanko\AppData\Local\Temp\b158-confirm2-gpt
```

`verify.py` reads only this packet and, with `--prior-packet`, the earlier packet's `snapshot\` and `packet-manifest.json`. It writes nothing. It runs `gpgv` with `--homedir` set to a directory that does not exist and `--keyring` set to the key in the folder, so it reads and writes no GnuPG state. The author's run is `evidence\integrity-verify-transcript.txt`. Read the script before running it, or check the objects by hand.

- **Signed Git objects:** `commits\` holds the raw commit objects of the whole chain, ef00345d → 348c4f70 → ccc046bb → 6605a8b0 → 60d2cd5a → ad1694c1. Each one comes as the object, the signed payload and the signature.
  - The script checks that each object hashes to its name, that the parent chain is linear, and that `gpgv` accepts each signature.
  - The public key in `key\` is the one GitHub publishes for the account at https://github.com/stop-cran.gpg (fingerprint D4C9A275A218AF747B787AFA9D94B9D311BD26A7). You can compare it there.
  - The base ad1694c1 is public on GitHub. The later commits are not, until publication.
- **Binding to the reviewed text:** `trees\` holds the tree objects at 348c4f70 and ef00345d for `/`, `kanji`, `words`, `docs`, `docs/n1-sources` and `tools`.
  - The script checks that the root tree is the one named in the signed commit.
  - It then checks that every file in this packet's `snapshot\` is the blob of the signed tree at ef00345d.
  - With `--prior-packet`, it checks the same for your earlier packet's `snapshot\` at 348c4f70.
- **The actual manifest:** `manifest\` holds the `manifest.json` blob at both commits. The script checks four things:
  - each file is the blob in the signed root tree;
  - its `contentVersion` recomputes with the algorithm of `tools/build_manifest.py` (also bound to the signed tree, in `blobs\`);
  - its file list equals the `kanji/` and `words/` files of the signed tree;
  - each snapshot card's SHA-256 in it matches the snapshot text after CRLF → LF, as `build_manifest.py` and the app both compute it.

  It also prints the manifest entries that differ between the two commits.
- **The kanji-reading builder:** `app-code\` holds 14 Kotlin files of the public app repository https://github.com/stop-cran/kanji-cards-android at commit 91e1d4b578859f7bfb582f7b9c6acf48c6ca6a75, the head of `main`.
  - `app-code\SOURCES.json` gives each file's Git blob id and public URL, and the script rehashes each copy.
  - The reading builder is `KanjiReadingQuiz.question` in `KanjiReadings.kt` (lines 91–116). It is called from `KanjiReadingViewModel.kt:151`.
  - The app verifies each card's SHA-256 against the manifest when it loads content (`ContentParser.kt:225-231` and `241-249`).
  - The script also confirms that `evidence\QuizBuilder.kt` and `evidence\Words.kt` are byte-identical to the app's files.
- **The Python ports:** `ports\` holds `reading_exposure.py`, `reading_options.py` and their shared `n1lib.py`, the code that produced `checks\reading-exposure.txt` and `checks\reading-options.txt`. You can compare them with the Kotlin. They are the author's tools and have no public copy.
- **What remains a limit** (also in the README):
  - Only the snapshot files are bound by content. For the other files in `kanji/` and `words/`, the trees bind only the file names. Their manifest hashes rest on `checks\manifest.txt`.
  - The Kotlin code is supplied as source. It was not compiled or tested here, and no phone test was done.
  - The publication ZIP does not exist until publication.

## New change

### N1: `words\升.md:28` names 升 in the 腰掛け contrast

Author action: **reworded one sentence**, following another reviewer's optional note.

- **Before:** “In its second sense, 升 is a whole box of seating, such as a 升席, not a single seat or bench.”
- **After:** “The second sense of 升 is a whole box of seating, such as a 升席, not a single seat or bench.”
- **Why:** the sentence before it is about 腰掛け, so “its” could be read as 腰掛け. JMdict 1288370 has a second sense, a temporary job, that this article does not teach.
- **Unchanged:** the meaning of the sentence, the JMdict citation, the link, line 15, line 34 and the front matter. No quiz reads article bodies; `evidence\word-quiz.txt` and `checks\` are unchanged apart from their header lines.
