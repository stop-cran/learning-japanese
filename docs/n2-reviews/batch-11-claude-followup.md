## Snapshot
- **Revised:** d47b7bcdf38197653989bf160bb744bd70b8fd51, committed files only. Original: 586989dc37529aaa66ff39ba9d84d0560f2a244d.
- **No Git:** I had file tools only. The commit identities, the clean checkpoint and the ten-file scope rest on the author's word.
- **Diff check:** every added line in the six-hunk diff matches the current files I read.

## Scope
- **Model:** claude-opus-5.5 (claude family). Worked sequentially; no edits and no delegation.
- **Read:**
  - my own initial report, docs\n2-reviews\batch-11-claude-initial.md;
  - the full correction diff (session file n2-batch-11-correction.diff);
  - kanji\栄.md, kanji\極.md, words\栄える.md and words\極める.md in full;
  - batch-11.json: lines 505-575 (the 極 source packet), 740-785 (1578350), 1083-1135 (1600620) and 2546-2711 (1254180);
  - docs\content-format.md:78-96;
  - the front matter of 輝く, 光る, 決める, 決まる, 選ぶ and 似合う;
  - title searches across words\ for "shine/glow/attractive" and "decide/settle/choose";
  - Kanjipedia kanji/0001577800 and its legend popup_kanji.html.
- **Not read:** the other family's report, the review and authoring ledgers, the other files in the ten-file commit, and the unchanged pages.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\栄.md | CLEAN | CLEAN | CLEAN |
| kanji\極.md | CLEAN | CLEAN | CLEAN |
| words\栄える.md | CLEAN | CLEAN | CLEAN |
| words\極める.md | CLEAN | CLEAN | CLEAN |

## Findings

**B11-01 (栄 え qualification): resolved.**
- 栄.md:36 now names 見栄 みえ with its "show; vanity" sense. It says JMdict's ateji label applies to the whole spelling, which matches batch-11.json:744-745 and 766-777.
- It states explicitly that 見栄 is fine for everyday use. That was the false implication I flagged, and the old "not recommendations… everyday spelling" sentence is gone.
- ヨウ is still example-less, which is accurate.
- **Calibration of my original report:**
  - My subclaim "栄 used for its sound え" went beyond the evidence. The ateji flag is on the whole spelling and does not establish how the reading divides between the two characters.
  - My remedy (put 見栄 in the え row) was one acceptable option, not a requirement. Keeping え lookup-only with an honest note is sound.
- Confidence: high.

**B11-02 (極 Jōyō marking and 決める wording): resolved.**
- The single-row marker is gone from 極.md:36.
- The new note at line 49 matches the fetched Kanjipedia page:
  - キョク・ゴク and きわめる・きわまる・きわみ are shown in red with 中 icons;
  - きめる・きまる are shown in black after a 外 icon;
  - the legend defines red as 表内音訓 (readings in the Jōyō table) and 外 plus black text as 表外音訓 (readings outside it).
- Line 48 now says neutrally that JMdict lists "both 決める and 極める", in the same order as batch-11.json:2709-2711.
- The packet record at batch-11.json:544-559 and the gloss at line 565 are consistent with the card.
- **Calibration of my original report:** I said -ぎ.め and きわ.まり were "equally outside the table". Kanjipedia does not mark them, so the revision is right not to infer their status. The wording point was about emphasis, not a factual error.
- Confidence: high.

**B11-03 (栄える quiz exclusions): resolved.**
- 栄える.md:8 now excludes 輝く ("shine; sparkle; glow") and 光る ("to shine; glitter").
- Both overlap はえる sense 1 "to shine; to glow" (1600620, with the 栄える spelling unflagged), a meaning the app itself teaches at 栄.md:33 and 栄える.md:43-45.
- **Calibration of my original report:** I called 光る optional because of its low score. content-format.md:95 tests reasonable acceptance, not whether the scorer can reach the word, so 光る belongs.

**Previously cleared 極める / 決める: my clearance is withdrawn and the new exclusion is correct.**
- I had cleared this pair only because 決める's automatic score was low.
- In fact JMdict 1254180 lists the 極める spelling, unflagged, with sense 1 "to decide… to settle". The app teaches that reading at 極.md:34 and 極める.md:46-48. So in the Japanese-to-English quiz, a learner shown 極める could reasonably accept "decide; settle" (決める's title).
- 極める.md:8 now excludes 決める.

**Regression check: none found.**
- **English-to-Japanese direction:** options show the reading, e.g. "栄える (さかえる)", so the new exclusions only remove distractors that were never ambiguous there. That is harmless.
- **Pairwise effects:** 輝く/光る were already excluded from each other. The new pairs add no transitive side effects.
- **References:** 輝く, 光る and 決める all exist with matching `word` fields.
- **Pool size:** both candidate pools stay large.
- **Unchanged evidence:** the diff touches no character metadata or JMdict pair records.

## Optional
These are nonblocking:
- **栄える / 似合う:** 似合う "suit; look good on" partly overlaps はえる sense 2 "to look attractive; to look nice; to be set off (by)". It is borderline, because "suit (a wearer)" is a different relation.
- **極める / 選ぶ:** 選ぶ "choose" matches only the second of the eleven glosses in きめる sense 1. The app teaches only "decide; settle". Also borderline.
- **極.md:49-50:** the two lines repeat the きまる outside-table point and could be merged.

## Limits
- **Git:** none. Commit identities and the diff provenance were not verified independently.
- **Kanjipedia icon:** the 外 icon's file is named icon_loanword.png, while the legend shows icon_gai.png. The alt text "外" and the black text color agree with the legend, so I treat this as immaterial.
- **App behaviour:** exclusion-aware behaviour is taken from content-format.md, not from app code.
- **Evidence scope:** batch-11.json is selected evidence, not the full JMdict.
- **Certification:** no native-speaker or linguistic certification.
