# Batch 107 native review — addendum (bounded clarification)

**Model:** Claude Opus 5.5 (`claude-opus-5.5`)

**Snapshot:** `1d341ac022bb652ac38a6c39a589bce5cc51261f`
- I read the three pointers myself: `.git` → worktree `HEAD` → `refs/heads/n1/resume-after-106-476f429` = `1d341ac…`. That shows only where the ref points.
- Checking the signature is the coordinator's job; I did not do it.

**Reads for this addendum (serial, one call each):**
- `sampled-jmdict.xml`, read in full in an earlier turn of this addendum.
- `sampled-kanjidic2.xml`, read in full (database version 2026-306).
- `image-manifest.json`, read in full (65 entries).

**Omissions:**
- I did not re-read any PNG, either source module beyond the files above, any other reviewer's report, or any ledger.
- I made no edits and used no shell.

## 1. The 38 representative PNGs I viewed

All are under `docs\n1-reviews\batch-107-native-853\native\`, all named `n1-107-<name>.png`, and I viewed each one serially in the native round.

| Group | Representatives |
|---|---|
| All-pool quiz | all-meaning-feedback, all-meaning-question, all-reading-feedback, all-reading-question, all-selection |
| Article | article-00, article-02, article-06, article-07, article-10, article-17 |
| Curated reading | curated-on-feedback, curated-on-question, curated-sole-on-done |
| Drawing | drawing-feedback, drawing-recall-feedback, drawing-trace |
| Font panels | font-panel-1 to font-panel-8 |
| N1 quiz | meaning-feedback, meaning-question, selection |
| Components | pair-0-components, pair-1-components, pair-2-components |
| Reused lines | reused-定-new-line, reused-違-new-line |
| Word pages | word-0-01, word-0-06, word-1-01, word-1-06, word-2-01 |

The total is 5 + 6 + 3 + 3 + 8 + 3 + 3 + 2 + 5 = 38.

## 2. The 27 duplicate captures, grouped by representative

I did not open these files. Each duplicate's SHA-256 and byte size match its representative's values as written in the manifest (hash prefix and size shown below).

| Representative (hash prefix, bytes) | Duplicates |
|---|---|
| article-02 (`367d69…`, 275671) | article-03, article-04 |
| article-07 (`c74909…`, 273844) | article-08 |
| article-10 (`8bea5d…`, 320822) | article-11, -12, -14, -15, -16 |
| word-0-01 (`18725d…`, 318221) | word-0-02, -03, -04 |
| word-0-06 (`77ed50…`, 345261) | word-0-08 |
| pair-0-components (`bf9a4c…`, 344591) | word-0-10, word-0-11 |
| word-1-01 (`abbd7a…`, 308590) | word-1-02, -03, -04 |
| pair-1-components (`110ac2…`, 320044) | word-1-08, -10, -11 |
| word-2-01 (`6ca3fc…`, 335744) | word-2-02, -03, -04 |
| pair-2-components (`4339d5…`, 323993) | word-2-06, -08, -10, -11 |

The total is 2 + 1 + 5 + 3 + 1 + 2 + 3 + 3 + 3 + 4 = 27, and 38 + 27 = 65 manifest entries.

**What the manifest claims versus what I saw:**
- The hashes, byte counts, `originalNativePng: true` flags and duplicate mappings are claims made by the manifest. I computed no hashes and did not compare duplicates byte-for-byte.
- Everything I report about image content comes from looking at the 38 representatives, which arrived downscaled to about 900×2000.
- article-17 is listed as distinct from article-10 (`a4ed3d…`, 320832 bytes against 320822). To my eye the two looked identical. I can't tell from looking what the 10-byte difference is.

## 3. The "heavier-looking fallback" remark

This describes **apparent appearance only, not the actual font face**.
- In panels 6–8, 宀, 辵, 辶 and 韋 looked heavier or larger than the glyphs around them in some style rows.
- I inspected no font name, cmap or font-file data, and the panel itself says "Cmap presence and hashes are not readability."
- The difference could be fallback to another face, or just how those glyphs are designed or scaled. I can't tell which.
- Because the images were downscaled, this remains a hypothesis for physical-device review, not a confirmed fallback.

## 4. The six new distractors, judged against 勘

**The target:**
- KANJIDIC2 gives 勘 only the on reading カン, with the meanings intuition, perception, check, compare and sixth sense.
- In JMdict, 勘 1210590 means perception, intuition, the sixth sense.
- Its secondary "check/compare/calculate" side shows up in 勘定 1210750 and in the rare spelling 勘える under 考える 1281020.

Each distractor was therefore checked against two things: the intuition sense, and the checking/calculating sense.

| Kanji (displayed label) | KANJIDIC2 meanings (2026-306) | JMdict entries in the frozen sample | Reasoning | Confidence |
|---|---|---|---|---|
| 剤 "medicinal preparation; chemical agent" | dose, medicine, drug | 1296370; 薬剤 1538220; 錠剤 1357120; 洗剤 1390950; 調剤 1429160; 製剤 2276330; 推進剤 2569220; 粘剤 2837804 | All senses are substances. Its "dose" meaning is a measured quantity, not checking or calculating. Its kun reading けず.る has nothing to do with meaning. | High |
| 剛 "sturdy; unyielding strength" | sturdy, strength | 2080860 (strength, toughness, bravery, boldness); 剛健 1284120; 剛性 1284130; 剛毛 1284160 | Physical or moral strength only. The only nearby sense, "good at, skilled, knowledgeable" (sense 3), belongs to 強い 1236070, where 剛い is a search-only spelling. It is not a sense of 剛, and the displayed label doesn't suggest it. | Medium–high |
| 凶 "ill fortune; evil" | villain, evil, bad luck, disaster | 1235400; 凶兆 1235470 "evil omen"; 凶作 1235440; 凶悪 1591510; 凶器 1591540; 大凶 1785310 | 凶兆 is a sign that bad fortune is coming, not a person's hunch. No sense involves perception or checking. | Medium–high |
| 冒 "brave danger; venture" | risk, face, defy, dare, damage, assume (a name) | 冒す 1519820; 冒険 1519830; 冒頭 1519860; 危険を冒す 1868850; 病に冒される 1855070 | Risk, desecration, illness and "beginning" are all unrelated to intuition or calculation. | High |
| 免 "exempt; be spared" | excuse, dismissal (kun まぬか.れる / まぬが.れる) | 1533050; 免許 1533130; 免税 1533230; 免れる 1584670 | Exemption and escape. No overlap. | High |
| 凹 "concave; sunken" | concave, hollow, sunken (kun くぼ.む / へこ.む / ぼこ) | 1179150; 凹む 1179200 (sense 3 "disheartened"); 窪む/凹む 1246840; 窪/凹 2756450; 凹レンズ 1179220; 凹凸 1179280; 凸凹 1582410 | Being disheartened is an emotion, not cognition. The displayed label is purely about shape. | High |

**Limit on this table:** these JMdict entries come from the frozen sampled excerpt. They are not a fresh upstream retrieval, and I have not confirmed that each kanji's JMdict family in the sample is complete.

## 5. Prior conclusions, unchanged

1. Batch 107 caused no new defect within the reviewed scope.
2. 勘/識 is a low-confidence, unguarded hypothesis. KANJIDIC2 lists 識 as "discriminating, know, write".
3. These earlier gaps remain unresolved but do not block this batch:
   - On 定, the reading さだ.か is unexplained.
   - On 違, the readings ちが.える, -ちが.える, たが.う and たが.える are unexplained, and the app still offers たが.う as a stem.
   - The 支払う/支払 pair is unchanged.
4. Optional: 予定 has two different glosses on kanji/定.
5. Limits:
   - The screenshots came from an emulator (sdk_gphone64, Android 15).
   - The quiz and test samples were supplied to me, not run by me.
   - The images were downscaled.

This addendum does not claim native-speaker, physical-phone, merged-tree, publication or global semantic acceptance.