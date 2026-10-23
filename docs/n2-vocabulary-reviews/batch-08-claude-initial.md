## Snapshot
**c3e705025de8ed252789968a9a37ab0535ddf3a3** (parent 9ceeb5366693090d9abd54de08d75970da59dda0). I reviewed committed content only.
- **What matched:** the branch file `.git\HEAD` points to (`jlpt-n2-vocabulary`) contains this commit.
- **What I couldn't check:** without Git I couldn't prove the working tree matches the commit or recompute the receipt's SHA-256 hashes.

## Scope
Model: claude-opus-5.5 (claude family).
- **Read in full:** all 19 new articles; the 15-file related patch; rows N2:142–161 in `docs\n2-vocabulary-sources.tsv`.
- **Checked in context:** the seven kanji link lines; the changed passages in 偉い, パーティー, 芝居, 女王, 追う, 延期 and 西洋; the whole 応じる article.
- **Read from batch-08.json:**
  - the source rows
  - all main entry families
  - comparison entries 1593070 (越える), 1179830 (応じる) and 1432370 (追い抜く)
  - the nine author inspection receipts
- **Also checked:** titles and quiz_exclusions of about 95 comparison and candidate cards; that every link target exists; the levels of the kanji cards involved.
- **Not reviewed:**
  - unchanged teaching on the related pages and the rest of the kanji cards
  - KANJIDIC2 component details
  - most of the 142 comparison entries
  - the forbidden docs

## Verdicts
| Row | Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| 143 | 宴会 | CLEAN | CLEAN | CLEAN |
| 144 | 園芸 | CLEAN | CLEAN | CLEAN |
| 145 | 演劇 | CLEAN | CLEAN | CLEAN |
| 146 | 円周 | CLEAN | CLEAN | CLEAN |
| 147 | 遠足 | CLEAN | CLEAN | CLEAN |
| 148 | 延長 | CLEAN | CLEAN | CLEAN |
| 149 | 煙突 | CLEAN | CLEAN | CLEAN |
| 150 | 追い掛ける | CLEAN | CLEAN | CLEAN |
| 151 | 追い越す | NEEDS FIX (F2) | CLEAN | CLEAN |
| 152 | オイル | CLEAN | CLEAN | CLEAN |
| 153 | 応援 | CLEAN | CLEAN | CLEAN |
| 154 | 王女 | CLEAN | CLEAN | CLEAN |
| 155 | 応ずる | CLEAN | CLEAN | CLEAN |
| 156 | 応接 | CLEAN | CLEAN | CLEAN |
| 157 | 応対 | CLEAN | CLEAN | CLEAN |
| 158 | 往復 | CLEAN | CLEAN | CLEAN |
| 159 | 欧米 | CLEAN | CLEAN | CLEAN |
| 160 | 応用 | CLEAN | CLEAN | CLEAN |
| 161 | オーケストラ | CLEAN | CLEAN | CLEAN |

- **Fifteen related edits: CLEAN on all three facets.**
  - The seven kanji links each use the article's reading and title: 芸:41, 劇:36, 周:37, 延:37, 接:39, 復:35, 欧:37.
  - パーティー:28, 芝居:35, 女王:28, 延期:34 and 西洋:27 turn existing comparisons into links.
  - 追う:31 links the explicitly taught spelling 追いかける to 追い掛ける.md.
  - 応じる:38-39 accurately says the 応じます and 応じて forms are shared.
- **偉い reuse claim: CLEAN.** The patch only adds `jlpt: 2`; there was no earlier, easier level. The page already teaches "admirable" and "important / high-ranking" at えらい (dictionary senses 1–2). The source gloss "terrible, awful" is fairly left unclaimed.
- **Explicit mappings (all 20 rows):** correctness NEEDS FIX (F1); coverage CLEAN; comprehensibility CLEAN.
- **Form checks:**
  - 追い掛ける teaches 追いかける as the same dictionary entry, with its own example.
  - 応ずる correctly teaches 応じます, 応じて, 応じた and 応じない, and warns against 応ずります.
  - The Digital Daijisen dictionary supports the 応接 example: 「次々と訪れる客に応接する」.

## Findings
**F1 — Minor; correctness of the explicit mapping.**
- **Where:** `docs\n2-vocabulary-sources.tsv:148` (last column) and `docs\n2-vocabulary-batch-sources\batch-08.json:134`.
- **Problem:** the N2:148 note excludes "historical-era, human-life or classical-music senses". JMdict entry 1176510 has no human-life or classical-music sense. The senses the note actually leaves out are 4 (mathematics: extending a line segment), 5 (philosophy: occupying space) and 6 (the Enchō era).
- **Impact:** the 延長 article itself is unaffected, but the coverage record is misleading.
- **Fix:** change the note to "no coverage claim for the mathematics, philosophy or Enchō-era senses (4–6)".
- **Evidence:** batch-08.json:943-1023.
- **Confidence:** high.

**F2 — Minor; correctness of quiz metadata.**
- **Where:** `words\追い越す.md:9` and `:38-40`.
- **Problem:** the title "overtake; surpass" excludes 越す ("cross over; pass beyond") but not 越える ("cross over; go beyond"), whose title is nearly identical. Exclusions aren't transitive, so 越す excluding 越える does not protect this pair.
- **Impact:** JMdict 1593070 sense 2 lists "to exceed; to surpass" (tagged "especially 超える", a preference, not a restriction). So 越える could be a defensible answer for "surpass", and 追い越す for "go beyond".
- **Fix:** add 越える to the 追い越す quiz_exclusions.
- **Evidence:** batch-08.json:11433-11500; 越える.md:4; 越す.md:4,9.
- **Confidence:** medium. 越える.md stresses crossing, and I didn't inspect how the app picks distractors.

## Optional
- **O1:** 応対.md:26 says "The second を…", but the examples contain only one を. Suggest "In the second example, を…".
- **O2:** 往復 ("return ticket") versus 帰り ("return journey"). They are different answers, and the article already explains the English "return" ambiguity. No exclusion is needed.

## Limits
- **No Git:** working-tree cleanliness and the receipt hashes are unverified.
- **Failed fetches:** an early batch of GitHub raw-file fetches used a fabricated commit hash and all returned 404. I didn't use them as evidence.
- **Author receipts:** I re-fetched only Kotobank 応接, and it confirmed the receipt. The other eight are author assertions I didn't independently retrieve. My 応ずる inflection judgement rests on JMdict's verb labels and standard conjugation, not a re-fetched page.
- **Evidence completeness:** the evidence file is a selection, not the whole dictionary.
- **Naturalness:** I judged naturalness from dictionaries and experience; this is not native-speaker certification.
