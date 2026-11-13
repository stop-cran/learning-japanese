# B113 independent initial review

Snapshot: fdec1c02f9b02f29659b56551cd0a1fd927cced1

Base: c42d80306926e99ec6436c80c0574e3a858a4286

Grant: RU-N1-B113-REVIEW-20261113-003

Model: runtime-reported GPT-6.1 Sol (gpt-6.1-sol). Provider-side execution-model identity was not independently verified.

## Scope

This is one blind initial review, not an implementation or confirmation round. All paths below are relative to the B113 packet unless expressly identified otherwise.

Read completely:

- REVIEW.md, packet.json, both rubric files, and the applicable repo\docs\content-format.md:1-139.
- All 15 new snapshot\kanji cards: 慢 縫 飢 恩 盆 誕 隊 需 系 徹 討 謝 握 寧 援, plus snapshot\kanji\応.md and 統.md.
- All 15 corresponding snapshot\strokes JSON files, including their point arrays.
- All 420 lines of diffs\existing.diff and all 30 changed snapshot\words articles: 丁寧, 体系, 兵隊, 寧ろ, 徹夜, 徹底, 必需品, 応援, 恩, 恩恵, 感謝, 我慢, 握る, 握手, 援助, 検討, 盆, 盆地, 系統, 縫う, 自慢, 裁縫, 討つ, 誕生, 誕生日, 謝る, 軍隊, 需要, 飢える and 飢饉.
- All 11 supplied check outputs. Both reading audits were read through their final summaries: reading-exposure.txt:1-222 and reading-exposure-noextra.txt:1-210.
- source-metadata.json, dictionary-index.json, provenance.json, joyo-rows.json, all 1,061 lines of kanjidic2-records.xml, and all 2,266 lines of jmdict-families.xml, through the closing XML tag. This included all 91 complete families, not merely first senses.
- All 45 required C distractor cards, all 40 publicly declared D candidates, and 10 individually announced E exclusion targets, in full. Tables below record them.
- evidence\kanjivg\07e2b.svg, the complete pinned 縫 source, including its 16 paths and stroke-number elements.

The supplemental title index was read in exactly the prescribed two ranges, 1-603 and 604-1206. I saw line 603, `栄 flourish; glory`; line 604, `栗 chestnut`; and the final line, `齢 age; years lived`. I compared the new titles and their taught ordinary secondary senses against the complete index, including English head-word and near-synonym leads. All 45 C cards' displayed titles matched their index lines.

Local reads used named-file views only, serially. There were no searches, listings, scripts, builds, JVM/emulator/ADB work, subagents or other-session consultations. No B112 file, other review or author rationale was opened. The only write is this report.

Three publicly announced direct fetches were used: https://www.weblio.jp/content/慢, https://www.weblio.jp/content/寧 and https://www.weblio.jp/content/援. Each returned the complete relevant Digital Daijisen character entry before later page material was truncated at 5,000 characters. The remainder of each aggregator page was not read and is not claimed as evidence.

## Verdicts

**Overall: NEEDS FIX.**

| Facet | Verdict |
| --- | --- |
| Correctness | NEEDS FIX: 飢's categorical severity statement and conjugation explanation, F2-F3. Supplemental source-only claims identified in L2 remain UNVERIFIED. |
| Scoped coverage | CLEAN for the assigned teaching-file coverage: all required new cards, selected-reading examples, mapped words, existing edits and stroke JSONs were read. Closure of every additional title-overlap lead is UNVERIFIED under the comparison caps, L3. |
| Consistency / quiz safety | NEEDS FIX: F1's direct meaning-label pairs remain unhandled. The supplied full-pool curated meaning triples themselves are sound. Runtime and unrestricted-pool safety remain UNVERIFIED, L1. |
| Comprehensibility | NEEDS FIX: F2's explanation of what remains in an ichidan conjugation. Otherwise no consequential explanation defect was established in the inspected teaching text. |

CLEAN here means no actionable defect established in that stated, inspected scope. It does not certify unresolved source claims, additional unread candidates or execution behavior.

### Per-card results

These are content verdicts. The teaching-coverage column concerns the requested card sections, supported selected readings and mapped vocabulary, not exhaustive future title-collision closure. L1-L3 qualify the relevant verdicts throughout.

| Card | Core correctness | Teaching coverage | Content quiz safety | Comprehensibility |
| --- | --- | --- | --- | --- |
| 慢 | CLEAN | CLEAN | NEEDS FIX, F1 | CLEAN |
| 縫 | CLEAN | CLEAN | NEEDS FIX, F1 | CLEAN |
| 飢 | NEEDS FIX, F2-F3 | CLEAN | CLEAN within inspected content/model scope | NEEDS FIX, F2 |
| 恩 | UNVERIFIED for the supplemental affection attribution, L2; main noun senses supported | CLEAN | NEEDS FIX as written, F1 | CLEAN |
| 盆 | CLEAN; O1 is qualification polish | CLEAN | NEEDS FIX, F1 | CLEAN |
| 誕 | CLEAN | CLEAN | NEEDS FIX, F1 | CLEAN |
| 隊 | CLEAN | CLEAN | CLEAN within inspected content/model scope | CLEAN |
| 需 | UNVERIFIED for extra kun claim, L2; main teaching supported | CLEAN | CLEAN within inspected content/model scope | CLEAN |
| 系 | CLEAN | CLEAN | NEEDS FIX, F1 | CLEAN |
| 徹 | UNVERIFIED for extra kun claims, L2; selected reading and vocabulary supported | CLEAN | NEEDS FIX, F1 | CLEAN |
| 討 | UNVERIFIED for extra kun claim, L2; selected readings and vocabulary supported | CLEAN | NEEDS FIX, F1 | CLEAN |
| 謝 | UNVERIFIED for 藉-substitution claim, L2; main senses and dated-sense restrictions supported | CLEAN | NEEDS FIX, F1 | CLEAN |
| 握 | CLEAN | CLEAN | NEEDS FIX, F1 | CLEAN |
| 寧 | CLEAN | CLEAN | NEEDS FIX, F1 | CLEAN |
| 援 | CLEAN | CLEAN | NEEDS FIX, F1 | CLEAN |

### Existing edits, metadata and geometry

The complete existing-file diff contains the expected 30 word-link additions, the obsolete no-card-text removal in 応援, and the two corresponding kanji remarks in 応 and 統. The new links point to the intended characters and preserve the applicable word identities and constituent readings. No actionable defect was established in those changes.

The 15 cards' source-reading arrays, radicals/numbers and primary stroke counts agree with the supplied complete KANJIDIC2 records and metadata. Selected readings have their own linked examples; whole-word changes such as てってい, たんじょう and たんじょうび are not presented as invented constituent readings. The selected kun absence on 寧 is deliberate, not loss of the source むし.ろ row.

All 15 generated JSONs carry the pinned revision and expected character, count, sequential stroke IDs and plausible in-box point data. The counts, in review order, are 14, 16, 10, 10, 9, 15, 12, 14, 7, 15, 10, 17, 12, 14 and 12. The complete 縫 SVG independently corroborates its 16-stroke structure, including the final three 辶 strokes; its path starts/ends correspond to the rounded JSON coordinates. I did not perform a full numeric reconstruction or visual/native tracing test for all geometry; L2 states the remaining source-read limit.

The full dictionary-family reads preserved important restrictions: かつえる is restricted to 飢える/餓える, not 饑える; 盆's family/household sense is untagged and its gambling-den sense is slang; 家系's lineage and ramen entries are separate; 貫徹's penetration sense is non-standard; 謝る's refusal/defeat senses are dated, unlike apology and the separate modern 謝絶 entry; and 寧ろ is usually kana, with 寧 an irregular-okurigana spelling. The cards mostly preserve these distinctions correctly.

## Findings

### F1 - Medium - Consistency / quiz safety: missing direct meaning-label exclusions

Locations: each listed snapshot\kanji\<character>.md:14 (`quiz_exclusions`), together with the corresponding taught senses and the actual comparison cards below.

The following 30 direct pairs are not declared at either endpoint. Their alternative displayed labels can express a taught ordinary sense, a close synonym, or a shared English head word. A learner given only the kanji lacks the context needed to reject that alternative. This is a content-authoring defect under repo\docs\content-format.md:94-139, not a claim that the supplied default full-pool triples already display these alternatives.

The counterpart cards were read completely; none has a reverse declaration that handles the listed pair. Existing exclusions via another character do not make these pairs transitive.

| New card | Missing counterparts and actual labels | Established overlap and evidence |
| --- | --- | --- |
| 慢 | 軽 `lightweight; slight` | The fetched Daijisen entry's third sense explicitly concerns looking down on others. 軽 teaches making light of / looking down on someone, and its displayed `slight` supplies the English alternative. This is not a claim that arrogance means low physical weight. |
| 縫 | 結 `tie; join; conclude`; 接 `touch; join`; 修 `repair; amend; cultivate` | 縫's opening explicitly teaches joining or mending cloth; 縫合 is sewing together. `join` and `repair` are defensible alternatives for those uses. Complete JMdict families 1517700 and 1517710; actual 結, 接 and 修 articles. Knitting is treated separately below. |
| 恩 | 愛 `love` | As written, 恩 explicitly teaches `affection; benevolence`; 愛 explicitly includes affection and care, not just romance. Thus `love` is not safely wrong relative to the lesson as presented. JMdict 1183090 sense 2 independently supports kindness/benevolence; the exact Daijisen affection attribution remains L2, so either verify and exclude the pair or correct that unsupported wording. |
| 盆 | 缶 `tin can; container` | A shallow vessel/basin is a container. One need not accept `tin can` to recognize the alternative `container`. The actual 缶 title is broader than its can examples. The new card's vessel sense and JMdict 1523700's tray sense establish the relevant object, not merely a shared 皿 shape. |
| 誕 | 造 `make; construct`; 始 `begin, start`; 緒 `cord; beginning` | The taught coming-into-existence/origin branch has making and beginning senses. Complete JMdict 1419080 sense 2 explicitly includes creation, formation, origin and making; the new card quotes it. Excluding 作/創/元/本/原 does not exclude these other actual labels. |
| 系 | 種 `seed; kind`; 般 `general; kind; category` | The ordinary colloquial suffix sense is explicitly `-type; -ish`; the group/type branch makes `kind` and `category` defensible. Complete JMdict 1251000 and the actual 種/般 articles. The seed or generality alternatives do not cancel the colliding kind sense. |
| 徹 | 到 `arrive; attain`; 終 `end; finish`; 済 `settle; finish`; 卒 `graduate; finish`; 専 `specialize; exclusive` | Carrying through to completion/attainment overlaps the first four; 徹する's doing something exclusively overlaps 専. Complete JMdict 1215090, primary accomplishment sense, and 1598340, exclusive-devotion sense, plus 1437670/1437680. This does not rely on 貫徹's non-standard penetration sense. |
| 討 | 思 `think, feel`; 話 `talk, speak`; 評 `appraise; reputation` | Consideration involves thought; discussion is talking; examination/review of a proposal includes appraisal. The card expressly teaches these deliberative uses. Complete JMdict 1258000, 1449960 and 1449980, and the actual three comparison articles. `reputation` is not claimed as a meaning of 討. |
| 謝 | 変 `change; strange`; 給 `pay; bestow` | Replacement/renewal involves change; honorarium/tuition-fee senses admit pay. Complete JMdict 1411920, 1323070 and 1255690; actual 変 and 給 articles. These are the modern replacement/payment branches, not an unrestricted extension of dated 謝る. |
| 握 | 扱 `handle; deal with`; 管 `pipe; supervise`; 知 `know`; 識 `knowledge; awareness` | The lesson teaches 握り as a handle, control/dominance, and grasping/understanding a situation or holding its answer. `handle` is also an English noun/verb collision; supervision and knowing/awareness overlap the control and intellectual-grasp branches. Complete JMdict 1152660, 1152720 and 1470910; actual four comparison cards. |
| 寧 | 御 `honorific; govern`; 和 `harmony; Japanese style`; 念 `thought; attention` | Courtesy/polite wording overlaps 御's explicitly respectful/polite uses; settled peace overlaps harmony; careful attention overlaps 念's attention. Complete JMdict 1427360 senses 1-2 and 1154190, the fetched Daijisen 寧 entry, and the actual three cards. This does not equate every polite form with a narrow grammatical honorific. |
| 援 | 守 `guard; obey`; 防 `defend; ward off` | The lesson's save/protect branch is broader than cheering alone. KANJIDIC2 gives `save`, JMdict 1229070 gives relief/rescue, and the card itself uses protection to justify 保. 守 explicitly teaches protection/guarding and 防 protection/defense, so those nearby labels also need direct handling. Not every act of assistance is asserted to be defense. |

Remedy: add the applicable direct pairs, at either endpoint according to the repository convention, and keep the explanations precise about which sense or English label overlaps. Alternatively narrow an actually overbroad taught/displayed gloss with source support. Do not rely on exclusions through a third card. Recheck both target directions and wrong-option coexistence; meaning exclusions do not protect reading prompts.

Confidence: high for the exact labels, inspected texts and absence of direct relations; medium-to-high for the linguistic/English-label overlap judgments. The 恩/愛 item is an established inconsistency in the lesson as written, not independent verification of its supplemental quotation.

### F2 - Medium - Comprehensibility / correctness: the conjugation explanation says the wrong substring remains

Location: snapshot\kanji\飢.md:47-48.

The text says that, because 飢える is ichidan, `える stays in forms such as 飢えて and 飢えない`. Neither form retains える: the dictionary-form final る is replaced, while the stem うえ- remains. The examples themselves are correct, but the stated rule contradicts them and can teach the wrong conjugation operation.

Remedy: say that え remains in the kana stem and final る changes, for example `うえる -> うえて / うえない`. The complete reused snapshot\words\飢える.md already explains dropping the final る and keeping うえ- correctly.

Evidence: complete JMdict 1224080 identifies an intransitive ichidan verb; the actual reused word article and the card's own two written forms establish the contradiction. Confidence: high.

### F3 - Medium - Correctness / comprehensibility: an absolute starvation threshold overnarrows 飢

Location: snapshot\kanji\飢.md:23-27, especially `hunger severe enough to amount to starvation`.

The opening makes starvation-level severity a condition of the character's meaning. KANJIDIC2 includes `hungry`, and complete JMdict 1224080 sense 1 includes being hungry as well as being famished/starving. The reused 飢える article correctly retains that breadth while warning that ordinary lunchtime hunger is not the default register/use of this word. A strong-deprivation tendency is not an absolute starvation threshold.

Remedy: teach hunger/deprivation, often severe, and retain the useful usage contrast with ordinary お腹が空く rather than defining away the broader hungry sense. Confidence: high on the overstatement; this does not recommend using 飢える for every casual hunger statement.

## Curated distractor review: C = 45/45

Every displayed title below matched its index line. Each assigned meaning triple is safe against its own new target in the inspected teaching senses. There is no exact shared selected reading in any assigned triple. Cross-card overlaps discovered in this set are still reported in F1.

| Target | Actual curated displayed titles | Reading / cross-card result |
| --- | --- | --- |
| 慢 | 慣 `accustomed`; 憎 `hate; detest`; 怪 `suspicious; uncanny` | No shared マン. |
| 縫 | 縮 `shrink; contract`; 練 `practice; refine`; 緒 `cord; beginning` | No shared ホウ or ぬう. 緒's beginning collides with 誕, not 縫: F1. |
| 飢 | 凡 `commonplace; mediocre`; 処 `deal with; dispose`; 館 `hall; large building` | No shared キ or うえる. 凡 has no selected kun; the model fills one kun slot by fallback. |
| 恩 | 因 `cause; factor`; 思 `think, feel`; 患 `be ill; suffer` | No shared オン. 思's thought sense collides with 討: F1. |
| 盆 | 分 `minute, part`; 盗 `steal`; 貧 `poor; impoverished` | No shared ボン. 貧 is already directly excluded by 飢. |
| 誕 | 延 `prolong; postpone`; 談 `converse; consult`; 誌 `written record; journal` | 談 has ダン, a voiced near-variant of selected タン; the supplied model rejects it and uses fallback. It is not evidence that 誕 itself selects ダン. |
| 隊 | 除 `remove; exclude`; 象 `elephant; image; shape`; 陽 `sunshine` | No shared タイ. |
| 需 | 震 `quake; tremble`; 零 `zero; spill`; 雲 `cloud` | No shared ジュ. |
| 系 | 糸 `thread; yarn`; 約 `promise; approximately`; 絶 `sever; cease` | No shared ケイ. A component/thread image is not itself a 系 meaning. |
| 徹 | 微 `minute; faint`; 育 `grow up; raise`; 御 `honorific; govern` | No shared テツ. 御 is excluded by 握 but not 寧: F1. |
| 討 | 計 `measure; plan`; 村 `village`; 寺 `Buddhist temple` | No shared トウ or うつ. Planning is not automatically a translation of discussing a plan. |
| 謝 | 診 `diagnose; examine medically`; 訪 `visit; call on`; 守 `guard; obey` | No shared シャ or あやまる. 診/談 are directly excluded by 討; 守 has the cross-card protection overlap with 援, F1. |
| 握 | 屋 `roof, shop`; 掘 `dig; excavate`; 掲 `put up; display; publish` | No shared アク or にぎる. 掲 has no selected kun; the model uses fallback. |
| 寧 | 寝 `lie down; sleep`; 宝 `treasure; valuables`; 寒 `cold weather` | No shared selected ネイ. 寝 is already excluded by 誕 for English `lie`. |
| 援 | 暖 `warm; warm up`; 授 `grant; impart; teach`; 担 `shoulder; take on` | No shared エン. 授's verbal granting/teaching is not a financial-grant noun or an unrestricted synonym for assistance. |

## Candidate and exclusion-target dispositions

D = 40 distinct candidates, exactly the publicly declared fixed list. E = 10 distinct targets, each publicly named with its reason immediately before its read. The overlapping C/exclusion characters 寝, 御, 診, 談 and 貧 are counted only under C.

`Needs exclusion` means F1; `already handled` means a direct exclusion exists; `harmless` means no actionable collision was established for the tested displayed label and verified sense, not a universal dictionary claim.

### D candidates

| # | Character | Actual displayed title | Related new card | Reason and disposition |
| --- | --- | --- | --- | --- |
| 1 | 軽 | lightweight; slight | 慢 | Contempt / slight: needs exclusion. |
| 2 | 笑 | laugh | 慢 | Harmless: laughing/smiling is not established as an ordinary 慢 sense merely by the loose raw gloss `ridicule`. Looking down on someone need not involve laughter. |
| 3 | 編 | knit; compile | 縫 | Harmless: knitting/braiding differs from sewing; weaving through a crowd is not literal textile weaving. |
| 4 | 結 | tie; join; conclude | 縫 | Joining sewn pieces: needs exclusion. |
| 5 | 接 | touch; join | 縫 | Joining sewn pieces: needs exclusion. |
| 6 | 修 | repair; amend; cultivate | 縫 | Mending / repair: needs exclusion; 修's existing exclusions do not include 縫. |
| 7 | 望 | hope | 飢 | Harmless on verified senses: hoping for an outcome is not itself deprivation or hunger for it. |
| 8 | 愛 | love | 恩 | The lesson's affection wording: needs exclusion as written; source-attribution limit L2. |
| 9 | 情 | emotion; circumstances | 恩 | Harmless: a generic emotion/circumstance is not the favor or kindness received. Metadata なさけ alone does not change the displayed title. |
| 10 | 盤 | board; disc | 盆 | Harmless for this displayed label: a shared vessel domain does not establish that 盆 means board or disc. Its secondary vessel wording does not change the actual option label. |
| 11 | 缶 | tin can; container | 盆 | Container / shallow vessel: needs exclusion. |
| 12 | 造 | make; construct | 誕 | Making / creation: needs exclusion. |
| 13 | 始 | begin, start | 誕 | Beginning of existence: needs exclusion. |
| 14 | 集 | gather | 隊 | Harmless: the act of gathering is not the organized body/unit itself. |
| 15 | 種 | seed; kind | 系 | Type / kind: needs exclusion. |
| 16 | 般 | general; kind; category | 系 | Type / kind/category: needs exclusion. |
| 17 | 関 | involve; barrier | 系 | Harmless on established labels: involvement or a barrier is not simply lineage/system. Similar relationship vocabulary alone is insufficient. |
| 18 | 到 | arrive; attain | 徹 | Reaching / attainment: needs exclusion. |
| 19 | 終 | end; finish | 徹 | Carrying through to the end: needs exclusion. |
| 20 | 済 | settle; finish | 徹 | Completion: needs exclusion. |
| 21 | 卒 | graduate; finish | 徹 | Finishing: needs exclusion; this does not make 徹 an education word. |
| 22 | 専 | specialize; exclusive | 徹 | Exclusive devotion: needs exclusion. |
| 23 | 突 | thrust; sudden | 徹 | Harmless on verified senses: thrusting/poking is a motion, not necessarily through-going penetration; suddenness is not established for 徹. |
| 24 | 話 | talk, speak | 討 | Discussion / talking: needs exclusion. |
| 25 | 評 | appraise; reputation | 討 | Appraisal / critical examination: needs exclusion; 評 has no reverse 討 exclusion. |
| 26 | 試 | test; try | 討 | Harmless: testing/attempting is not established by every use of examination/consideration; do not merge school exams with deliberation from an English gloss alone. |
| 27 | 察 | observe; infer | 討 | Harmless on verified senses: inquiry does not make every observation or inference a translation of 討. |
| 28 | 問 | ask, question | 討 | Harmless on verified senses: the extra source-only たずねる claim does not independently establish all asking senses; L2 retains that source-verification gap. |
| 29 | 探 | search | 討 | Harmless on verified senses: seeking an object is not automatically discussion or examination of an issue. The unverified extra kun claim alone is insufficient. |
| 30 | 変 | change; strange | 謝 | Replacement / change: needs exclusion. |
| 31 | 改 | revise; reform | 謝 | Harmless on established labels: revising/reforming an existing thing is not automatically the old/new replacement sense of 代謝. |
| 32 | 辞 | words; resign | 謝 | Harmless: leaving an existing position is not established merely by 謝絶's refusal or dated 謝る's declining sense. |
| 33 | 給 | pay; bestow | 謝 | Fees / remuneration: needs exclusion. |
| 34 | 扱 | handle; deal with | 握 | Handle noun/verb and handling/control: needs exclusion. |
| 35 | 管 | pipe; supervise | 握 | Control / supervision: needs exclusion. |
| 36 | 知 | know | 握 | Holding an answer / grasping a situation: needs exclusion. |
| 37 | 識 | knowledge; awareness | 握 | Intellectual grasp / awareness: needs exclusion. |
| 38 | 和 | harmony; Japanese style | 寧 | Settled peace / harmony: needs exclusion. |
| 39 | 念 | thought; attention | 寧 | Careful attention: needs exclusion. |
| 40 | 防 | defend; ward off | 援 | Protection / save branch: needs exclusion. |

### E exclusion targets

| Character | Actual displayed title | Related new card | Reason and disposition |
| --- | --- | --- | --- |
| 遅 | late; slow | 慢 | Sluggish pace: already handled. |
| 通 | pass through; commute | 縫, 徹 | Passage / going through: already handled at both new cards. |
| 乏 | scarce; lacking | 飢 | Deprivation / shortage: already handled. |
| 享 | enjoy; receive benefits | 恩 | Receiving a benefit: already handled. |
| 氏 | clan; family name | 盆, 系 | Family/household or lineage: already handled at both new cards. |
| 生 | life, birth | 誕 | Birth: already handled. |
| 群 | flock; cluster; crowd | 隊 | Group/body: already handled, without equating every flock with a military squad. |
| 求 | seek; request | 需 | Demand/request: already handled. |
| 細 | slender; fine; detailed | 寧 | Care / detail: already handled. |
| 引 | pull; draw | 援 | Drawing in examples/citation: already handled. |

## Host evidence and reading safety

The host reports zero validation errors, 431 passing Python tests, matching manifest/rebuild output at contentVersion 520b87f6a026b41e, and 30 expected/added word-link pairs with zero link-plan problems. Lint reports zero errors and ten warnings. The five warnings on changed word articles cite wrapped Dictionary lines whose entry IDs are present on following lines; I verified those in the complete changed articles. The other five concern untouched articles and were not expanded into a new audit.

The reading-model outputs were read in full, including the differing extra-reading inputs. They report zero hits in the modeled full N1/All pools and single-borrow Starter pools. The extra-input run reports seven latent entries: three 謝 nanori-only entries, outside lexical teaching scope, and four other readings for 縫/討/寧/援. The no-extra run reports three latent nanori entries. The 徹 `つ` info line is also name-only, not an established lexical teaching defect.

The three full-pool fallback cases are correctly qualified: 飢 うえる and 握 にぎる have an empty-kun curated card, while 誕 タン loses 談 ダン under the helper's near-reading treatment. All other full-pool prompts are reported as curated-filled. Starter cases use fallback. These are host-model observations, not Kotlin execution results.

The helper's `(card text)` attribution is not trustworthy as provenance: some extras came from saved Wiktionary snippets rather than the cards. The three public fetches corroborated 慢's ordinary character senses, 寧's ニョウ reading and cordial/calm senses, and 援's たすける/ひく and substitute-character note. I do not turn unselected or snippet-only readings into required new quiz selections.

## Optional

O1 - Low - Qualification polish, snapshot\kanji\盆.md:23-27 and its Common words section. The opening `Polite お盆 ... either the festival or a tray` is broader in wording than the later correct `Obon festival; tray (polite)` bullet. JMdict 1002690 attaches the polite flag to the tray sense, not the festival sense. Prefer sense-local wording in the opening too. This is not a claim that the prefix お has no politeness-related origin or that ordinary お盆 is an invalid festival name.

## Limits

L1 - Execution and pool limits. No Python audit was rerun and no Kotlin, JVM, native, phone or emulator execution occurred. The provided model does not establish custom/caller-built Starter behavior, multiple borrowed Starter cards, all caller-built pools, actual random draws, native/phone acceptance or compatibility with the older delivered 5c000bd APK. That APK predates kanji quiz_exclusions. The hypothetical extra-holder 援/おん exposure with 恩, 温 or 音 is a reported model scenario, not a phone reproduction. F1 is the static missing-relation finding under the authoring contract, not proof of a currently reproduced full-pool screen.

L2 - Source limits. The binary Joyo PDF was not read or rendered; its extracted rows were read completely, but their fidelity and physical PDF page anchors were not independently verified. The other 14 KanjiVG SVGs were not opened; all 15 generated JSONs and dictionary counts were read, but full source-to-sampled-geometry reconstruction and visual acceptance remain unverified. Of the 15 public character pages, only 慢, 寧 and 援 were fetched. The other 12 exact character-entry transcriptions/attributions were not independently refetched. Most core teaching is separately supported by the complete supplied dictionaries, but particularly 需's もとめる, 徹's とおる/とおす, 討's たずねる, 謝's substitution for 藉, and the exact affection wording attributed under 恩 remain UNVERIFIED rather than authenticated by a citation alone.

L3 - Capped comparison follow-up. All 40 frozen D candidates were read; the list was not extended. Other leads considered but not read are 願 (飢, wish/longing), 絡 (縫, intertwining/weaving), 宅 (盆, household/residence), 浅 (盆, shallow), 様 (系, type/manner), 楽 and 休 (寧 or 慢, ease/rest/peace/slackness), 払 and 退 (謝, pay or withdrawal/declining), 権 (握, power/control), 優 (寧, gentleness/courtesy), and 択/選 (寧ろ, preference/choice). Later unverified leads also included 贈/与 (恩/謝/援, giving/favors), 費/報 (謝, expense/payment/reward), and 抜 (縫う's passage use). Their actual complete card texts were not read, and no collision, current displayed-title wording or remedy is asserted for them. The 40-card frozen-list rule and 10-target cap prevent further local comparison reads in this pass. Some are likely only topical, grammatical or other-constituent associations, not true kanji meanings; they are disclosed rather than silently promoted to findings. The fully read new-card pair 恩/援 was considered, but a further mandatory exclusion was not established merely because assistance can be received as a favor.

L4 - Integrity and model identity. The supplied packet-index digest is aea68d97bfc52944dc6e63fc309e47d08c328990c997cc73fb651ab6b73554d0; the supplemental-index digest is db2bdb13227ca6bef0a7c0d43160ae566e1c10ff6918f9f55eb7816093d71054. These are binding supplied identifiers, not reviewer-computed hashes. No hash command was run, including on this report; the coordinator is to hash it after the required read-back. Runtime-reported model identity is recorded above without an independent provider-side execution trace.

Read counts: C 45/45; D 40/40 permitted; E 10/10 permitted; web fetches 3/3 permitted. No required text-file read remains partial. Unread binary/source/comparison scope is explicitly recorded above. This report does not authorize implementation, a confirmation round or release of the shared reviewer slot.
