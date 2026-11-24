**Snapshot:** cbf5c2c5ca52758812aff3e61ae421e72fadd9e7 (base ac5304ba), as supplied in the packet. This is not a git repository, so I could not check the hash. No uncommitted changes were identified.

**Scope:** One reviewer, powered by claude-sonnet-5.5 (no second family). Facets assigned: correctness and scoped coverage. Comprehensibility was not assigned. I read, one view call per turn:
- all of kanji-1..4, words-1..4, changed.txt, comparison-words.txt, rubric, snapshot, sources.json, quiz.txt and labels.txt;
- families-1..7;
- primary.xml (requested lines 1–400; the returned text ended at entry 1732370, which I took as EOF).

**Verdicts** (comprehensibility: not assigned for any card)

| Article | Correctness | Coverage |
|---|---|---|
| 廷 | CLEAN | CLEAN |
| 弊 | CLEAN | CLEAN |
| 弓 (kanji) | NEEDS FIX (Q4) | CLEAN |
| 弔 | NEEDS FIX (Q1) | CLEAN |
| 弥 | NEEDS FIX (Q3); ビ exception UNVERIFIED | CLEAN |
| 弦 | NEEDS FIX (minor, F4) | CLEAN |
| 彩 | CLEAN | CLEAN |
| 彰 | CLEAN | CLEAN |
| 征 | NEEDS FIX (Q5) | CLEAN |
| 忌 | NEEDS FIX (Q1, Q2) | CLEAN |
| 法廷 | CLEAN | CLEAN |
| 弊害 | NEEDS FIX (Q6, F6) | CLEAN |
| 弓 (word) | NEEDS FIX (Q4, F3) | CLEAN |
| 弔問 | CLEAN | CLEAN |
| 弥縫策 | CLEAN | CLEAN |
| 弦楽 | NEEDS FIX (F1) | CLEAN |
| 色彩 | CLEAN; Daijisen figurative claim UNVERIFIED | CLEAN |
| 表彰 | CLEAN | CLEAN (optional active example) |
| 征服 | NEEDS FIX (minor, F5) | CLEAN |
| 回忌 | NEEDS FIX (minor, F2) | CLEAN |
| 10 changed kanji | CLEAN | CLEAN |

Evidence for the CLEAN verdicts:
- **New kanji:** strokes, radicals, grades and front-matter readings match sources.json.
- **New kanji:** every metadata reading appears in its reading table or has a qualified source-only explanation.
- **New kanji:** the quiz projections match the front matter.
- **Word cards:** JMdict senses, restrictions and tags match primary.xml and the families files.
- **Changed kanji:** the diffs add the required reciprocal links with correct readings.
- **Changed kanji:** the entry lists match the new words. I could not confirm that 縫.md's body uses the newly listed entry 1332170 (修繕).

**Findings**

*Q. Quiz ambiguity (moderate).* Overlapping displayed labels sit in cards that are not excluded. Evidence is labels.txt plus JMdict. Confidence is medium to high unless noted. Whether exclusions are symmetric is unknown (see Limits). If they are one-directional, the reverse entries are also needed.

- **Q1.** 弔 "mourn; condolence" and 忌 "mourning; abhor; death anniversary" do not exclude each other. 悔 "regret; repent; mourn" overlaps both.
  - Remedy: set `kanji/弔` exclusions to `[悲,哀,葬,喪,忌,悔]`.
- **Q2.** 忌 "abhor" overlaps 憎 "hate; detest". The 忌 card itself glosses 忌む as "detest" and 忌まわしい as "detestable".
  - Remedy: set `kanji/忌` exclusions to `[嫌,避,禁,喪,弔,憎,悔]`.
- **Q3.** 弥 "patch up" overlaps 継 "…; patch". 継 already excludes 縫, 修 and 補, but 弥 does not list 継.
  - Remedy: add 継 to `kanji/弥` exclusions.
- **Q4.** 弓 "bow (for arrows…)" and the word 弓 "bow (…or a violin)" overlap 礼 "bow; thanks" and お辞儀 "bow; bowing".
  - Remedy: add 礼 to `kanji/弓`, and 礼 and お辞儀 to `words/弓`. Medium confidence, because the parenthetical partly disambiguates.
- **Q5.** 征 "conquer" overlaps 克 "overcome". JMdict 克服 itself glosses "conquest (of a difficulty)". The word card 征服 already excludes 克服, but the kanji card does not exclude 克.
  - Remedy: add 克 to `kanji/征` exclusions.
- **Q6.** 弊害 "harmful effect" overlaps 毒 "poison; harmful influence". JMdict 1508270 glosses 弊害 as "harmful influence".
  - Remedy: add 毒 to `words/弊害` exclusions.

*Other findings*

- **F1 (minor-moderate, correctness).** `words/弦楽`, Synonyms: "[オーケストラ]… its kanji word is 管弦楽" is unsupported. JMdict 1214130 glosses 管弦楽 only as "orchestral music", and nothing in the packet covers オーケストラ. The ensemble name 管弦楽団 comes from my own knowledge, not the packet.
  - Remedy: say "管弦楽 (かんげんがく) is orchestral music" or drop the clause.
- **F2 (minor, qualified claim).** `words/回忌` says "Both 一周忌 and 一回忌 name the first anniversary". JMdict 1161330 marks 一回忌 (いっかいき) as "usu. 一周忌".
  - Remedy: add the reading and "一周忌 is the usual form".
  - Remedy: cite 1814080 (三回忌, "second anniversary") and 1161330/1163200 on the Dictionary line. The "as JMdict does" claim currently cites only 1199390.
  - The off-by-one rule itself is correct.
- **F3 (minor, naturalness).** `words/弓`, example 2 "高校の部活で弓を習っている" is used to demonstrate JMdict sense 2 (archery). The collocation is unattested in the packet, and 弓道 is the usual modern term. The sentence "not learning about one object" is also unclear.
  - Remedy: either demonstrate sense 2 with an attested phrase, or label 弓を習う as understandable but with 弓道 more usual.
  - Confidence is low to medium.
- **F4 (minor).** `kanji/弦`, つる row: "it can also be the arched handle of a pot". JMdict 1578400 marks this sense "esp. 鉉".
  - Remedy: add "this sense is usually written 鉉".
- **F5 (minor, translation).** `words/征服`, example 2: 三日かけて is translated "After three days".
  - Remedy: "Taking three days, they finally conquered the mountain."
- **F6 (minor).** `words/弊害`: "損害 is the damage or loss caused". JMdict gives "damage; injury; loss" with no direction of cause, which blurs the contrast with 被害.
  - Remedy: "damage or loss itself, often counted in money".

**Optional**
- 表彰: add an active example, such as 市長が功労者を表彰した.
- 弥縫策: 弥縫策を重ねる is unattested in the packet. 講じる or に終始する may be more idiomatic, but this is unverified.
- 弦楽: 絃楽 is described as "older", but JMdict does not mark it. "Alternative spelling" is safer.
- 弥: the shape note writes 尔, but the Japanese glyph is probably 尓 (about 70% confident).
- 弥: add a sentence noting that Kanjipedia lists あまね.し, ひさ.しい and つくろ.う, which the senses "far-reaching/lasting/patch" rest on.
- Other exclusions to consider: 彰 vs 賛 ("commend" vs "praise") and 叙; 色彩 vs 紅葉 and 絵の具; 弔問 vs 香典.
- 回忌: add one longer example such as 七回忌 or 三十三回忌.

**Limits**
- No external pages were consulted. Daijisen/Weblio text, Kanjipedia, the standard-use table PDF and the JLPT lists are unverified. sources.json records only that headings were checked, so statements attributed to Daijisen are unverified.
- Those statements are 法廷 "usually inside a courthouse", the 色彩 figurative use (保守的色彩), and the 回忌 account of first and second anniversaries.
- No native-speaker or device verification. My naturalness judgments are unverified intuition.
- The 弥 reading ビ is taught from an untagged word, 弥縫策, while the standard table gives only や. This is a documented exception under the "issue #60" policy, which is not in the packet, so I leave it to the adjudicator.
- Exclusion symmetry is unknown. If it is one-directional, add the reverse entries in 克服 (征服), 見舞い (弔問) and the other older cards named in Q1–Q6.
- labels.txt is a selection, not the whole deck.
- Relative-link targets such as オーケストラ, お見舞い, 損害 and many kanji notes are not in the packet.
- The ten changed kanji were seen only as diffs.
- Single reviewer, no multi-model comparison.
