## Snapshot
- **Corrected commit:** `c23eb2ff4638c41dac20a187c43d81bfeeb1dfaf`. It directly follows `ac708ffd2a4153211b420e63c2b0b8766319342d`.
- **Ref check:** the files show `.git\HEAD` pointing to `jlpt-n2-vocabulary`, and that branch file contains `c23eb2ff…`.
- **Provenance limit:** I ran no Git commands. Ancestry, a clean working tree and every SHA256 come from the author's snapshot; I did not check them myself.

## Scope
- **Model:** claude-opus-5.5 (Claude family), working alone, with no agents and no edits.
- **Changed cards, read in full:** おおざっぱ, おおよそ, お代わり, お気の毒に, オートメーション, お先に.
- **Comparison cards, read in full:** およそ, 一応, ばかり, 程度, ころ, 代わり, すみません, ごめんなさい, 自動, どうぞ. I also read the link target `kanji\替.md`.
- **Packet (`batch-09.json`):**
  - The seven added families (14872–15456) and their placement under `reviewEvidence`.
  - The six reused families: 1161170, 1189130, 1318340, 1523450, 1590770 and 2607630 (the separate がわり suffix).
  - The evidence behind the cards: 1002280 for お先に, 1412950 for おおざっぱ, and 1612800, whose お替わり spelling is unrestricted.
- **Jisho receipts:** I fetched both. The ばかり entry gives sense 2 as "approximately; about", and its example placement is misaligned, as the receipt says. The 程度 API result includes "about; approximately".

## Verdicts
Each cell gives correctness / scoped coverage / comprehensibility.

| Item | Verdict |
|---|---|
| おおざっぱ | CLEAN / CLEAN / CLEAN |
| おおよそ | CLEAN / CLEAN / CLEAN |
| お代わり | CLEAN / CLEAN / CLEAN |
| お気の毒に | CLEAN / CLEAN / CLEAN |
| オートメーション | CLEAN / CLEAN / CLEAN |
| お先に | CLEAN / CLEAN / CLEAN |
| Packet correction | CLEAN / CLEAN / CLEAN |

- **Guards:** all ten are new pairs that rest on genuine overlap in the English titles:
  - "roughly" appears in both おおざっぱ and 一応.
  - おおざっぱ's "general" overlaps およそ's "generally".
  - おおよそ's "approximately" overlaps ばかり's "about", 程度's "approximate amount" and ころ's "around".
  - お代わり's "refill" is also 1590770 sense 4 of 代わり, marked usu. as お～.
  - "I am sorry" fits both すみません and ごめんなさい.
  - オートメーション's "automation" overlaps 自動's "automatic operation".
  - お先に's "ahead" overlaps どうぞ's "go ahead".
- **Integrity:** every target exists, with no duplicates, self-references or overlaps with `quiz_distractors`.
- **Packet:** it is append-only. Original rows, mappings and selected senses are unchanged. The provenance text keeps the two unrelated ころ homographs and the がわり suffix out of the evidence.

## Findings
- **F1 (お気の毒に and すみません / ごめんなさい):** resolved at `お気の毒に.md:9`.
- **F2 (オートメーション and 自動):** resolved at `オートメーション.md:9`.
- **F3 (お先に "historical" wording):** resolved at `お先に.md:42-43`. The new sentence matches 1002280 sense 1 ("before; previously", marked only as polite) and makes no claim about register.
- **Original optional suggestions:**
  - The どうぞ and ころ exclusions and the 替 link (`お代わり.md:29`) were adopted, so they are resolved.
  - My suggestion to add kana to the お先に examples at lines 19 and 21 is withdrawn. They contain only the headword, whose reading is already given.
- **Regressions:** none.

## Optional
- **およそ (outside the assigned scope):** the existing およそ card has the same title overlap with ばかり and ころ that justified the new おおよそ guards. Exclusions are not transitive, so those two pairs remain unguarded. Confidence is low.
- **Carried over from my original report, not part of this correction:**
  - a note on お元気で in 元気でね
  - a 菜 link in おかず
  - a mention of 把 in おおざっぱ

## Limits
- **Manifest and validation:** `manifest.json` is not in the supplied diff. I could not recompute hashes or run `validate.py` or `build_manifest.py`, so whether the manifest is current and whether validation passes is unverified.
- **Quiz behaviour:** I did not run the quiz builder; how often these pairs appear together is not established.
- **Jisho:** both receipts are current retrievals backed by JMdict, so they are not independent dictionaries.
- **Naturalness:** these are reviewer judgments, not native-speaker certification.
