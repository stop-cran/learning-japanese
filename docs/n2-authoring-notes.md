# N2 expansion notes

## Scope and evidence

The [source snapshot](n2-source-snapshot.json) fixes the kanjiapi.dev N2 community set retrieved on 2026-10-21:
367 characters, including the existing cards for 珍 and 短. The expansion therefore needs 365 additions, not an assumed
generic N2 count. Modern JLPT does not publish an exhaustive kanji syllabus.

The baseline is `7a92dde23107173af8aabef51971dbc66b754a93`. Existing cards and word identities are preserved.
Use existing word articles where useful; add supporting articles only where needed. A kanji's level does not establish
a word's vocabulary level. Dictionary readings and senses must respect spelling, reading and sense restrictions.
Per-batch records under [n2-batch-sources](n2-batch-sources) retain the inspected metadata and dictionary entries.

The canonical [format](content-format.md), [authoring checks](../.github/instructions/content-structure.instructions.md),
[review guidance](../.github/copilot-instructions.md) and [JLPT policy](jlpt-levels.md) apply; this note does not replace them.

## Observed authoring pitfalls

- Candidate dictionary examples need inspection: an existing filename can teach a different reading or lexical identity.
  For example, the companion 仲間 なかま is not the historical 仲間 ちゅうげん.
- Adding a kanji card activates link checks in existing word articles that declare that kanji. Link the existing substantive
  component explanation; a new card's forward link to the word does not satisfy that separate check.
- Dictionary inclusion is not evidence of everyday frequency. Preserve unusual source readings without manufacturing
  ordinary examples. The pilot retains the unmatched readings of 並 and 乱 as character-dictionary-only lookup information.
- Inspect non-initial positions before declaring a reading source-only. The pilot's word-initial candidate heuristic
  missed 胡乱 うろん for 乱's ロン. Candidate discovery now also considers word-final matches; a kana match is still not
  proof of character-by-character reading allocation. The proposed 乱りに example does not by itself establish `みだ.る`.
- Keep spelling, pronunciation and register qualifications separate. JMdict's rare-spelling flag on 依る does not make
  よる a rare pronunciation; missing priority flags do not prove that a word is rare. Batch records retain spelling and
  reading priorities separately, with their union used only for candidate navigation.
- Preserve evidence for additional pairs asserted in notes, not only the reading-table examples. The pilot now records
  仏語 ぶつご, 乳房 ちぶさ and 依存 いそん explicitly. For external dictionaries, inspect the exact headword and any notation
  guide needed to interpret symbols; the 乾 usage notes cite the entries and Daijisen's outside-Joyo reading marker.
- The current validator enforces explained kunyomi only for N5/N4. N2 needs an explicit metadata-to-reading-table audit,
  even after structural validation passes.
- Three curated wrong answers avoid default four-choice fallback for new cards. Review the meanings, not just title strings.
  The pilot also gives existing 下 and 長 a third wrong answer because new low/long-time answers could otherwise appear
  as defensible random fallback choices.
- Use labelled modern-shape mnemonics when historical or phonetic analysis has not been established. Keep canonical radical
  metadata and explain visible variants rather than replacing the indexing radical.
- Batch 02's 傾く かたぶく has an outdated-reading flag, not an outdated-spelling flag. Keep the two annotation
  types separate, just as for rare spelling versus rare pronunciation.
- A successful dictionary URL can resolve to the wrong headword: the 刷く page on Kotobank resolved to はだく,
  and 凍る resolved to こおる, not the outstanding こごる reading. The inspected Kanjipedia はく entry
  permits 刷く only for light brush application, not its separate sweeping sense.
- New supporting vocabulary also needs quiz review. Batch 02 adds direct exclusions for the overlapping labels of
  兆候/印/現れ, 児童/子/子供, 兵士/武士, 冊子/本/書物 and 刊行/出版/発行.
  These are declared pairs on the new cards, not transitive groups or unrestricted substitution rules.
- A title-only overlap search is navigation, not a semantic audit. Batch 02's initial search missed plural
  "symptoms" and サイン's secondary sign/indication sense. Inspect relevant article meanings and ordinary
  number-neutral uses, then add direct pairs: a shared exclusion through 本 does not exclude 冊子/図書.
- Distinguish a useful alternate-reading clarification from an incorrect-reading finding. Batch 02's
  兵法 ひょうほう was valid before adding へいほう; dictionary order alone does not establish relative frequency.
- Batch 03's 卒える is flagged as a search-only spelling. Such an index form is not an ordinary example merely because
  it occurs in a dictionary record. Exclude search-only forms from Common words and label any retained index evidence.
- Verify the written okurigana boundary as well as the whole-word kana. 効き目 ききめ and 勢み はずみ do not establish
  that a single 効 or 勢 ordinarily spells the entire reading. For 卒's `お.わる`, Kanjipedia explicitly lists 卒わる;
  JMdict's different rare spelling 卒る does not by itself demonstrate that boundary.
- Automatic word links must match the article's primary reading, not just its filename. Batch 03's 包む くるむ
  must not link to the existing つつむ article; 大勢 たいせい must not link as though it were おおぜい.
- The current candidate cache retains only spellings containing selected N2 characters. Its missing non-N2 aliases
  are an extraction limit, not evidence that those spellings or independent entries are absent from JMdict.
- Web-search generated prose can disagree with its own citation URLs. In batch 03, a purported 副作用 URL resolved
  to 文七元結. Inspect the fetched headword and actual definition; do not treat the generated quotation as dictionary evidence.
- A bound counter needs a usable count, not only the isolated dictionary suffix and a warning. Both batch 03 reviewers
  requested concrete 匹 forms; the correction gives 一匹, 二匹 and 三匹 with kana and separate pronunciation evidence.
- The equality family needs direct exclusions beyond 同じ. Both batch 03 reports raised 匹敵/同様 and 匹敵/同一,
  albeit with different severity. A shared exclusion through 同じ would not protect either pair.
- A part-of-speech observation should identify its sense when the word has others. 勢い is a noun in the force/momentum
  sense discussed on its card; JMdict also records an adverb sense. The clarification does not require teaching every sense.
- Compare each named neighbor on its own relevant dimension. Batch 03's first 匹敵 correction distinguished matching
  from 同一's identity but not from 同様's contextual similarity. The revised comparison contrasts reaching a level
  (`Bに匹敵する`) with kind or manner (`Bと同様`), without claiming their meanings can never overlap.
- Missing exact standalone matches are not missing bound-stem examples. Batch 04 uses 双子 ふたご for 双's ふた.
  A broader spelling search also finds rare 双ぶ ならぶ despite the source's undotted reading, while 双つ ふたつ
  is search-only and remains index evidence. Inspect the written kana instead of trusting the candidate heuristic.
- A legacy component explanation may mention only the complete word, as with 布団. Link 団 inside that existing
  spelling at its substantive introduction rather than manufacturing an isolated meaning or rewriting the article.
- Recheck two-distractor fallbacks as overlapping characters arrive. Batch 04 adds a third curated wrong answer to
  毎, because the new 各 card's each/every answer could otherwise be defensible in a fallback choice.
- A selected spelling can hide a useful alternative. Following batch 04 review, the full pinned JMdict entry for
  巧咲 was inspected and its spellings 巧笑/巧咲 retained. Explain the alternative without treating dictionary order
  as a frequency ranking, or an alternative spelling as an invalid word.
- Separate a whole-word ateji label from a claim about each character's purely phonetic role. Batch 04's 布団 note
  now states the source's whole-spelling label without inventing a component-by-component derivation.
- Narrowing an overbroad technical explanation should not remove the term's only learner-facing gloss. The first
  batch 04 団 correction did that to "ateji"; the follow-up restores a short qualified explanation while retaining
  the whole-word versus component-role distinction.
- An occurrence of a kana sequence is not a character-reading allocation. Batch 05 does not use the えん in
  圧延 あつえん as evidence for 圧's エン, or the くま within 奥まる おくまる as evidence for 奥's くま.
  Unestablished readings remain qualified lookup information rather than manufactured examples.
- Identical spelling does not imply identical primary reading or sense restrictions. Batch 05 keeps 埋める
  うめる separate from うずめる, and restricts 埋まる's vacancy/debt senses to うまる. Its 塩 link teaches しお,
  not the separately documented chemical noun えん.
- Preserve sensitive-usage labels even when the example is needed only for a character reading. The ショウ row
  of 姓 identifies 百姓's farmer sense as sensitive and its separate derogatory sense, not as neutral farm vocabulary.
- Missing JMdict register flags do not prove current neutral use. In batch 05 review, an exact Nipponica entry
  supplied historical context for 傾城's courtesan sense despite its unflagged JMdict record. Inspect the actual
  headword when an aggregator also contains a different pronunciation or a separately named work. Translate
  inclusive chronology precisely: 明治以後 is from Meiji onward, not necessarily after the period ended.
- Identical kana does not establish a reading's historical layer. Batch 07 preserves 州's on ス as
  source-only rather than recycling the native sandbank word す as independent evidence of an on-reading word.
  A useful bound example also need not be a standalone match: 布地 きれじ demonstrates 布's きれ.
- Adding 巨 activates a direct size synonym in the old 大 card's automatic fallback. Give 大 a third
  curated wrong answer; do not demand unrelated repairs merely because two characters have a loose association.
- Inspect sense-level spelling notes even when the dictionary's formal spelling restrictions are empty.
  Batch 07's 布く is indexed with 敷く, but the explicit 布く notes concern promulgating, railway tracks
  and troop deployment, not the first sense's futon example. Automatic first-sense glosses can mislead.
- A bound-reading example must not imply it is the only reading of the whole spelling. Batch 07 adds
  布地 ぬのじ alongside the きれじ example and retains 切れ地 as an alternative spelling. Dictionary
  order, missing priorities and a rare label on another sense do not establish their relative frequency.
- English answer labels can collide even when the Japanese words are not synonyms. Batch 07 excludes
  巻く/風 because the bare English label "wind" can be read as a verb or a weather noun. Check the
  displayed text in both quiz directions; a Japanese part-of-speech distinction is not always visible.
- Verify official reading-table status directly rather than treating a dictionary spelling list as a frequency
  ranking. Batch 08's government Joyo table lists 庫's コ/ク but not くら, and 承's ショウ/うけたまわる
  but not ジョウ/うける. The recognition qualifications do not claim that table absence proves rarity.
- Preserve the force of spelling-specific notes. Batch 08's JMdict notes say "esp." for 延ばす's
  postponement sense and ウケる's amusement sense; "especially" is not an exclusive spelling restriction.
- Preserve both written okurigana and usable affix examples. Batch 09 distinguishes 損なう from the
  irregular spelling 損う without inventing different pronunciations, and illustrates the suffix rows
  with 取り損なう and 見損ねる rather than only repeating an independent verb.
- New upward-movement vocabulary also activates a legacy fallback: batch 09 gives 上 a third curated
  wrong answer so 昇's rising answer cannot fill its default fourth slot. Useful semantic comparisons
  remain in teaching text rather than becoming wrong answers.
- Test English polysemy in both word-quiz directions. Batch 09 adds direct 挟む exclusions for grasp,
  catch and the noun/verb label sandwich. It narrows 昇る's answer to "rise (sun/moon); be promoted"
  without restricting the body's broader natural-rising explanation or adding every increase/posture word.
- An uncommon source reading does not establish a numeric sound change. Batch 10 keeps 枚's バイ
  in the explicitly archaic expression 枚を含む; 一枚, 二枚 and 三枚 all use まい, with full sentence examples.
- Separate a written bound form from a grammatical stem. Batch 10 illustrates 替's `か.え-` in 替え歌
  and 柔's `やわ.ら` with the separately listed martial-arts noun 柔ら, not the i-adjective's stem.
  柔らか and 柔らかい also require different attachment explanations before a noun.
- Canonical radical distinctions can be subtle: 替 is indexed under 曰, no. 73, not 日, no. 72.
  Keep the inspected indexing metadata even when the lower enclosure looks like 日.
- Batch 10 gives legacy 木 a third curated wrong answer because new 材 supplies a direct timber/wood
  synonym that could otherwise fill its default fourth slot. 林's woodland meaning is distinguished
  from wood as material rather than treated as proof of an exact size boundary between 林 and 森.
- Batch 10's 板木 examples distinguish はんぎ, a printing block, from the separate ばんぎ signal board.
  The original sense-qualified ハン example was valid; the added homograph context prevents a
  one-spelling/one-reading shortcut. Resolve this as a context improvement, not proof that the
  documented reading is incorrect. 枝葉's えだは alternative is optional additional context.
- Batch 11 again requires an exact written boundary: JMdict's deciding/settling family has 極る
  きまる, while the inspected Kanjipedia entry explicitly gives 極まる きまる. Preserve that
  independent evidence and its outside-Joyo marker; the marker alone does not establish rarity.
  Keep both readings of 極める separate from the linked article's primary きわめる.
- A word-final sound is not enough to establish its historical reading layer. Batch 11's 見栄 みえ
  record carries a whole-word ateji label, not independent proof of a regular native-reading allocation.
  Nevertheless, omitting this attested spelling from the え qualification made the lookup-only wording
  overbroad. Name the spelling and explain the narrower unresolved allocation; do not imply that an
  everyday spelling is unsuitable. 栄耀 えよう retains its outdated-kana flag. Generated search
  explanations are not evidence for either character's historical allocation.
- A written-form-only meaning question can admit a homograph's other reading even when the article's
  primary reading is explicit. Batch 11 excludes 栄える from 輝く and 光る because its separate はえる
  entry means shine; 極める excludes 決める and 選ぶ because its separate きめる entry includes decide,
  settle and choose. An exact applicable gloss is not disqualified by being one of several glosses.
  Curate the direct ambiguity, not a supposedly permanent low candidate score. Exclusions are not transitive.
- An isolated outside-Joyo marker can imply an unintended contrast with adjacent unmarked rows.
  Batch 11 gives Kanjipedia's actual 極 reading list and its explicit きめる/きまる outside-table marks
  in one note, without inventing a status for every derived form or treating table status as frequency.
- Batch 12 retains 況's `まし.て` as qualified lookup information: the attested 況して まして
  spelling does not establish that exact boundary, but must not be described as a missing word.
  A meaning list containing おもむき likewise does not establish an ordinary standalone word example.
- A shorter on-reading cannot be established by truncating the compound's sound. Batch 12 uses
  汚泥 おでい for デイ, not デ; 泥's デ/ニ remain qualified after inspecting actual candidates.
  Preserve 泥洹 ないおん as a specialized religious example without inventing a historical derivation.
- 汚す's dictionary note says especially けがす for disgrace/defile, not exclusively that reading.
  The same spelling 汚れる has separately indexed よごれる and けがれる entries; a link to the
  existing primary よごれる article must not quietly stand in for both.
- New river character 河 activates 川's direct-synonym fallback, so batch 12 gives 川 a third
  curated wrong answer. The new 汚す word's English soil also needs a direct exclusion from the
  noun 土, despite their different parts of speech. Its 沈める counterpart directly excludes 沈む.
- An idiom recommendation must not become a false grammatical ban. Batch 12's linked noun article
  teaches 汗をかく, but the pinned dictionary also attests 汗する あせする. State the alternatives
  without inventing a frequency ranking from an unflagged record. Check the linked article's own
  warning as well as the new kanji card; correcting only one can leave contradictory advice.
- Label a godan verb's 汚し form as its masu-stem, not its sole conjugation stem; 汚さない
  uses another stem. Name an invoked homophone explicitly, as with 沈める versus 静める/鎮める.
- English transitivity is not guaranteed by Japanese transitivity. Both soil and stain have intransitive
  English uses, so 汚す directly excludes 汚れる; put up overnight can describe the guest's stay,
  so 泊める's answer explicitly says put someone up. 沈める's separately applicable lower sense
  also needs direct exclusions from 下げる, 下ろす and 降ろす, regardless of their mutual pairs.
- Batch 13 found an existing 浴びる lesson under the kana headword あびる with `kanji: []`.
  Inventory searches by written kanji therefore missed it. Link that lesson rather than duplicating it
  or changing its metadata to pretend that the headword contains a kanji.
- Both 浴びる and 浴びせる are transitive ichidan verbs; their subjects have different roles.
  English receiving/passive wording does not make 浴びる intransitive. The latter's pouring answer
  also needs a direct guard against 掛ける's applicable secondary pouring sense, even though the
  existing 掛ける lesson and title introduce hanging.
- Preserve the exact reading being illustrated: 温い ぬるい does not establish bare ぬく.
  Pinned entry 2567890 does attest 温 ぬく, but as an archaic derogatory noun; it is explicitly
  recognition-only, not an everyday noun for warmth. Do not infer a suitable word from a reading list.
- Mixed spelling/reading families require local qualifications: 清朝's Qing sense is restricted to
  しんちょう, while the typeface sense is especially せいちょう; 清浄 accepts せいじょう and
  しょうじょう. 準える is usually kana, and 準じる/準ずる's source-field kun labels are not
  an etymological claim about the vocabulary's origin.
- 湿る しめる is godan, not ichidan. The suffix -ま.じり needs a real compound and the
  suffix's contribution, not merely an unsegmented headword. Batch 13 uses 雨混じり あめまじり.
- A generated search answer proposed irrelevant dictionary URLs and universal absence claims.
  Actual fetched 湾 and 準 headwords did not establish the proposed unusual word examples.
  Batch 13 retains eleven exact readings as scoped lookup-only information, without claiming
  that no attestation exists anywhere. A character's meaning list is not a lexical example.
- Adding 湯 creates a potential hot-water overlap with the English title water. Batch 13 gives
  the older two-choice 水 card a third curated wrong answer; its existing cold/hot-water teaching
  distinction and all other content remain unchanged.
- Batch 13's GPT review established 流す's relevant pouring use, not merely an abstract
  causing-to-flow association: pinned entry 1552120 includes pour, and the actual fetched
  Seisenban Nihon Kokugo Daijiten I.4 describes washing the body by pouring water over it.
  Add the direct 浴びせる/流す exclusion; their separate exclusions through 注ぐ do not suffice.
- Claude's batch 13 review found missing substantive comparison links on six cards.
  Check antonyms and warnings as well as primary word tables. Its optional mnemonic polish
  also removes the English rule/ruler bridge in 測 without pretending 則 means a measuring tool.
- The bare 温 ぬく example and 温もり ぬくもり are different lexical items. Retain both
  source records when explaining the latter's usually-kana warmth sense; the archaic
  standalone example is not evidence that every occurrence of the ぬく element is an insult.
- Batch 14 distinguishes exact spelling/reading pairs: 灯/あかり is search-only in its
  inspected family, but 灯/ひ and 灯/ともしび have separate ordinary entries.
  Keep 灯影 ほかげ as evidence for bound ほ-; do not invent a standalone ほ noun.
- Preserve the complete 溶ける/融ける/解ける melting family alongside the existing
  undo/solve 解ける lesson. Its informal money/time-used-up sense also warrants direct
  quiz exclusions with 無くなる, 切れる and 消える, not unrestricted synonym claims.
- 濯ぐ's ゆすぐ reading does not inherit the revenge/wiping-disgrace sense of the
  broader すすぐ/そそぐ family. Check spelling, reading and sense restrictions together.
- 燥ぐ is a rare spelling of はしゃぐ, not evidence that the spoken verb is rare.
  Conversely, the inspected 燃す もす pair has no source rarity flag; do not infer one.
- 乾燥する has both transitive and intransitive source classifications. Illustrate
  actual 木材を乾燥する as well as 空気が乾燥する; a causative-only example would
  not demonstrate the former. 照らす's comparison/reference construction has both
  pinned lexical evidence and an actually fetched native-dictionary explanation.
- 片/かた is a prefix in the inspected entry, not an ordinary standalone noun.
  Use 片手 to explain both native metadata rows. 版 also has a ばん suffix use and
  a printing-block spelling overlap with 板; preserve ハン-only character metadata
  without denying those word uses or treating 板 as a universally wrong answer.
- Batch 14 gives 火 and 分 a third curated distractor rather than relying on
  automatic choices around the new burning/fragment meanings. These are exact
  one-line changes; fifteen older word edits add links only.
- GPT's batch 14 review found direct 乾燥 exclusions missing for figurative
  dullness (つまらない/退屈) and 切れる's narrower moisture-draining use.
  The author verified the actual Daijisen HTML definitions and pinned senses.
  Add direct pairs even when another pair through 乾く or つまらない already
  exists; retain the differences rather than teaching unrestricted synonymy.
- Batch 15 keeps 略's five unmatched native readings, 畳's チョウ/かさ.なる
  and 県's か.ける as eight explicitly scoped lookup rows. In particular,
  重畳 ちょうじょう does not allocate its initial ちょう to the final 畳.
  Preserve a source reading without inventing an everyday spelling.
- 玉's bound rows use 玉砂利 and 百円玉, with the part's contribution
  explained. The inspected Daijisen entry confirms the gravel's rounded shape.
  畳's counter row also gives a usable 六畳 ろくじょう construction rather
  than only an isolated suffix.
- 甘い あまい is not the separate usually-kana うまい entry, even though
  甘い is one of the latter's spellings. Its tasty sense has different
  spelling notes from its skilled sense. 磨る's rare-spelling label likewise
  does not make the godan pronunciation する rare or turn it into irregular
  する, do.
- Both batch 15 reviewers found that 王 is a defensible meaning answer for 玉:
  玉 ぎょく abbreviates the shogi king in pinned entry 1921990, sense 7,
  and the inspected Daijisen sense 5. Keep the useful visual comparison but
  replace 王 with 全 as the wrong option. A specialized attested standalone
  sense still matters when the quiz supplies no disambiguating context.
- Claude's batch 15 review found substantive comparisons left unlinked:
  ほぼ, 上手い and the 固い/堅い spelling alternatives. Link their actual
  word articles without changing the demonstrated reading or pretending
  their spelling preferences are absolute sense restrictions.
- Batch 16 preserves 祭's まつ.り/まつり spelling distinction without
  inventing two nouns. 祀る is an alternate spelling of the verb 祭る,
  not of the festival noun. 祭日 and 祝日 have overlapping holiday senses;
  the characters alone do not establish a strict modern calendar divide.
- 童 わらべ is explicitly dated. The renderer's automatic annotations do
  not cover every register flag, so inspect the actual applicable senses
  and include a necessary qualification in the authored gloss.
- 競べる くらべる is search-only in the pinned record, despite an occasional
  competing-spelling note. Keep its source reading for lookup, not as a
  recommended everyday example. 競る is godan, not a causative of 競う.
- 算's そろ remains lookup-only. The actual Kanjipedia character and 算盤
  word headwords confirm the whole word そろばん, not a freely usable
  standalone そろ. Do not import another dictionary's extra character
  readings into the pinned KANJIDIC2 metadata or cite a search summary as
  verification of their allocation.
- 竹's pinned second sense is the middle option in 松・竹・梅, not flute.
  The new word article guards the four directly overlapping middle labels
  中/中央/半ば/真ん中, without declaring them unrestricted Japanese
  synonyms or manufacturing exclusions from every English token match.
- Existing 児童 was added after the baseline inventory. Discover component
  links from the current word files, not just the original inventory.
  Batch 16 changes 27 component passages and the 松/梅 comparisons by
  links only, preserving all their lexical metadata and teaching text.
- GPT's batch 16 review found an English-label ambiguity: 察's observe
  can also mean celebrating a festival, as confirmed in the actual Oxford
  headword, sense 5. Replace that 祭 distractor with 禁; this does not
  declare the Japanese characters 察 and 祭 synonymous.
- Claude suggested qualifying 筆's 万年筆 example. Its pinned complete
  entry family also lists まんねんぴつ and まんねんふで. Scope the ヒツ
  comparison to the linked article's まんねんひつ reading and retain the
  attested alternatives without inferring their frequency.
- Batch 17 preserves 粉's katakana デシメートル exactly where the pinned
  KANJIDIC2 record places it, in the kun field. JMdict confirms the rare
  unit spelling and usually-kana qualification. Do not silently normalize
  the source classification or call it a native powder word. The private
  reading audit now recognizes both kana scripts rather than rejecting
  this legitimate katakana example.
- 総べて is search-only, while 総て is a rare kanji spelling of a
  usually-kana word. Preserve the two source boundaries without calling
  them different words or promoting the index form into Common words.
  簡's えら.ぶ and 線's すじ remain explicitly scoped lookup-only rows;
  筋 すじ does not establish a reading of the different spelling 線.
- 紅's cosmetic sense is restricted to べに, not くれない. In 木綿's
  full family, もめん is restricted to 木綿 and the cotton-material
  sense; do not transfer the きわた tree-name sense. 綿's usually-kana
  plant flag does not automatically qualify every padding use.
- 細か and 細かい have distinct adjective forms and source okurigana
  boundaries. 絡む and 絡まる are both intransitive godan verbs, not a
  transitivity pair. These differences require examples, not just lists
  of similar-looking kana.
- The new 書籍, 粒 and 総額 lessons use direct word-quiz exclusions for
  actual book/publication, grain/drop and monetary-total overlaps. English
  object/activity ambiguity does not establish unrestricted Japanese
  synonymy; pairwise protections are not transitive.
- Adding 細 activates a small/fine overlap in 小's older two-choice
  fallback. A third curated 糸 option preserves the original two choices
  and all prose. 線's word article has no literal character mention in
  its component paragraph; link the substantive definition instead of
  rewriting unchanged teaching text to satisfy a helper.
- Batch 17's independent reviews caught complementary issues. A word's
  secondary lexical reading can make an answer label ambiguous: 粒 needs
  separate direct exclusions with both 玉 and 球, whose たま entry includes
  beads or drops. An exclusion between 玉 and 球 does not cover either
  pair with 粒. Verify the applicable sense, not just the primary reading.
- Preserve the on/kun notation in cross-character explanations too:
  毛糸 uses 毛's kun reading け, not an on reading suggested by ケ.
  Keep a sense-specific kana-use flag next to the illustrated sense;
  綿's わた row now illustrates the plant alone, while the meaning and
  Notes retain the separate padding use.

- Batch 18 preserves bound readings as metadata while illustrating actual
  spellings: 編's -あ.み uses 手編み, 胸's むな- uses 胸元, and
  肯's がえんじ.る uses the attested 肯んじる, not an invented 肯る.
  Kana-only alternates and irregular-okurigana flags belong to their
  exact spelling/reading pairs, not every spelling in a family.
- Distinguish lexical senses rather than inventing frequency claims:
  缶 かま is a boiler, 羽 は differs from the はね spelling family,
  強肩 is a strong throwing arm, and 肌膚 supports キ without establishing
  everyday frequency. 翌日 is the next day relative to a reference date,
  not automatically tomorrow.
- Keep transitivity scoped to the illustrated use. 練る's kneading and
  planning uses take an object, but its procession sense is intransitive;
  群れる and 群がる are both intransitive. 署名する takes a document
  with に in the illustrated construction, not an invented を rule.
- New word-quiz protections include secondary applicable senses and
  English labels: 編む/組む share braiding, 群れ overlaps group/crowd
  labels, 肯定 overlaps affirmation/agreement labels, and 脂 needs
  separate 油 and 石油 safeguards. These are direct answer-label
  protections, not unrestricted Japanese synonym groups or solid/liquid
  and animal/plant rules.
- Link 缶's substantive existing definition when its component paragraph
  has no standalone character. Preserve all old wording. Check new-word
  citation IDs against exact selected records too: 耕す, 耕作 and 耕地
  have separate entries 1280950, 1280970 and 1280990.
- Batch 18's GPT review caught two word-quiz gaps that the author's
  label scan and Claude's initial review missed. 群れ's animal-group
  sense includes English school, colliding with 学校's unqualified
  label without implying an educational-institution meaning for 群れ.
  起す and 打つ have applicable tillage senses despite their beginner
  wake/hit labels; protect each direct pair with 耕す.
- Check register at sense level even in comparison notes. Claude's
  optional suggestion correctly identifies 石油's kerosene sense as
  colloquial; that qualifier is now explicit on both new 脂 pages.
  A general next/following label on 次 does not itself establish the
  specific following-day meaning of 翌日.
- Claude's changed-passage review found another 耕す overlap: 作る has
  an unrestricted tillage sense in entry 1597890, sense 4. Neither
  initial reviewer, the author nor GPT's first confirmation caught it.
  A pinned-dictionary sweep across all existing written word forms and
  permitted readings found the full direct tillage set: 起す, 打つ,
  作る and 耕す. Check the defect class after a fix; do not stop at
  the first named instances or mistake a temporal till for tilling soil.

- Batch 19 keeps six exact source readings as explicitly qualified lookup
  information: 脳's ドウ/のうずる, 臓's はらわた, and 芸's
  う.える/のり/わざ. Negative checks of particular word spellings
  are bounded evidence, not proof that no compound could illustrate them.
  芸香 うんこう supplies ウン without a frequency inference.
- 膚's はだ example has a rare spelling, not a rare pronunciation.
  Keep the full 肌/膚 spelling family and its reading restrictions.
  舟's ふな- and -ぶね use actual 舟橋/小舟 compounds;
  舟/船's small-craft distinction is a tendency, not an absolute rule.
- Separate 著する's arrival sense from 著る's rare wear spelling.
  負荷's noun load/workload sense does not inherit the formal/literary
  flag of its separate suru sense. Use sense-scoped records rather than
  a headword-wide register label.
- Twelve old word articles gain substantive component links. Eleven
  preserve every nonlink character; 野菜 also loses the exact obsolete
  clause claiming that 菜 has no card. That exception is mechanically
  declared rather than hidden under a links-only claim.
- Batch 19's GPT review found missing direct protections for 脳/気,
  舟's container/aircraft uses and 荒れる/かさかさ. A bounded
  pinned-dictionary candidate sweep also established 脳's direct mind
  overlaps with 胸 and 腹. Different primary body-part labels do not
  remove applicable figurative noun senses; do not credit the author's
  later extensions as independent reviewer discoveries.
- Both reviewers noticed the 舟/缶 container concern, although Claude
  treated it as optional and low risk. Compare all report sections
  before calling a contribution unique. Claude independently supplied
  two useful teaching-clarity changes: align 脳's label with its taught
  mind sense, and connect 般's ハン with the パン in 一般/全般.
  The former is not a claim that KANJIDIC2's memory gloss is false.
- Claude's batch-19 changed-passage review caught an additional
  ざらざら tactile-roughness gap that its initial review and GPT's
  confirmation missed. Add the direct pair, not a transitive path
  through かさかさ. Rechecking the bounded disorder candidates also
  justified the author's direct 混雑 precaution from its second sense;
  do not infer unruly behavior from crowding alone.

## Review and checkpoint protocol

Work in the source snapshot's batches, sequentially. Checkpoint content and regenerated manifests before review, then
commit confirmed fixes and their reconciliation. Git author and committer are `stop-cran`.

Each batch receives independent GPT and Claude review of the same frozen snapshot, files, facets and evidence.
Run one short-lived reviewer process at a time and confirm exit before starting another; there is no explicit agent-unload
tool in this environment. Initial reports stay blind to one another and to the author's preferred adjudication.
Record actual models and review limits in the [review ledger](n2-review.md).

Reconcile against evidence, not votes. Retain the initial reports and mark findings resolved, partially resolved, unresolved,
withdrawn or optional. Review changed passages for regressions. Compare model contributions only after deduplicating
equivalent observations across findings, optional suggestions, limits and per-card notes.

## Current limits

Source records and structural checks are not native-speaker certification or exhaustive historical analysis.
Dual-model usefulness is an observation about the reviewed sample, not proof that model bias has been eliminated.
The first nineteen batches' GPT/Claude reports are preserved in the review ledger, including changed-passage confirmations
where teaching text was corrected. They found
complementary issues, but also supplied unsupported frequency inferences and optional expansions. Neither family caught
every issue established across the reviewed sample. Both confirmed the final corrected passages without an actionable
remaining defect in that scope; batch 06 required no teaching correction.
Batch 11 also preserves a final narrow confirmation of the direct 極める/選ぶ homograph exclusion.
Batch 12's 15 additional kanji and three supporting verb articles have independent initial reports
and confirmed corrections, including the linked 汗 article's consistency repair.
Batch 13 has independent initial reports for all eighteen new pages. Both original reviewers
confirmed the eight revised teaching pages without a remaining actionable defect. Its 21 legacy word changes are component links
only, including the kana-headword あびる lesson.
Batch 14's fifteen kanji and five supporting word articles have independent initial reviews.
Both original reviewers confirmed the four revised pages, resolving the source-grounded quiz
correction and optional citation-label polish without a remaining actionable defect.
Its source/reading audit brings the total to 210 additions and 655 exact reading rows; another 155 additions remain unauthored.
Batch 15 is review-closed: fifteen more kanji and two supporting
word articles bring the authored total to 225 additions and 701 exact reading rows.
The deck now has 845 kanji, 3,251 word articles and 227 selected N2 characters;
140 selected characters remain unauthored. Nineteen older word edits are links only.
The shared 玉/王 quiz finding and Claude's three linking findings are corrected;
both original reviewers confirmed all five revised teaching pages without a remaining
actionable defect. Claude's final pronoun-polish suggestion remains nonblocking and
unadopted; the shogi sentence supplies the 玉/王 context.
Batch 16 is review-closed: fifteen more kanji and
one supporting 竹 article bring the authored total to 240 additions and
733 exact reading rows. The deck now has 860 kanji, 3,252 words and 242
selected N2 characters, with 125 additions unauthored. Its 32 reading rows
contain 30 lexical examples and two explicitly qualified lookup-only rows;
29 older word edits are links only. GPT's 祭 quiz-label finding is corrected,
and Claude's optional 筆 reading qualification is adopted. Both original
reviewers confirmed both revised pages CLEAN on all three facets.
Claude accepted the previously missed English-label ambiguity; its additional
際/occasion observation did not establish a direct synonym or actionable defect.
The remaining counter and history suggestions are optional expansions, not
unresolved findings.
Batch 17 is review-closed: fifteen kanji and
three supporting word articles bring the authored total to 255 additions
and 774 exact reading rows. Counts are 875 kanji, 3,255 words and 257
selected N2 characters, with 110 additions unauthored. Its 41 reading rows
contain 38 lexical examples and three explicitly qualified lookup-only
rows. Fifteen older word changes are links only; 小 gains only a third
wrong answer. The corrected source packet retains 76 exact pairs and 66
complete entry families. GPT uniquely established the 粒/玉/球 answer-label
defect; Claude uniquely established the 毛 reading-notation defect and
supplied the adopted optional 綿 qualifier clarification. Neither initial
reviewer caught the other's actionable issue. Both original reviewers
confirmed all four changed pages CLEAN on all three facets against the
committed correction diff. Claude acknowledged the missed word-quiz overlap;
its later wording/comparison suggestions remain optional, not unresolved
defects. These observations concern this shared sample, not a general
ranking or proof of eliminated bias.

Batch 18 has independent initial reviews, first changed-passage
reports and final narrow confirmations of the 耕す/作る safeguard and
its citation-only kanji edit. Both original reviewers mark the final
two-page change CLEAN on all three facets. Its fifteen
kanji and six supporting words bring the authored total to 270 additions
and 808 exact source-reading rows. Counts are 890 kanji, 3,261 words and
272 selected N2 characters, with 95 additions unauthored. All 34 new
reading rows have lexical examples; the corrected packet retains 79 exact
pairs and 76 complete entry families, including genuinely kana-only families.
Ten older word changes are links only; no older kanji or stroke changes.
The first eighteen batches are review-closed. The four new direct
quiz safeguards and optional register clarification are recorded in the
ledger. GPT supplied the initial actionable findings; Claude supplied
the adopted qualifier and the later 作る catch. This is complementary
signal from different stages, not a blind initial-review win for the
later finding or an exhaustive synonymy guarantee.

Reviewer file permissions are separate from tool permissions: `--allow-all-tools` alone did not authorize a diff in the
parent session's artifact directory. The event record showed a noninteractive path-approval failure, not content exclusion.
Grant only that artifact directory with `--add-dir`. Reviewer session IDs can be recovered from the local session store
for same-task follow-up; `--resume` and `--trust-folder` cannot be combined. Exit each resumed process before the next.

Batch 19 has independent initial reports and both original reviewers'
confirmations of the corrected passages. Its fifteen
kanji and four supporting words bring the authored total to 285 additions
and 848 exact source-reading rows. Counts are 905 kanji, 3,265 words and
287 selected N2 characters, with 80 additions unauthored. Its 40 reading
rows contain 34 lexical examples and six qualified lookup-only rows;
the corrected packet has 77 exact records from 75 complete entry families.
Twenty-three direct word-quiz pairs protect the confirmed overlaps.
Twelve old word edits have the precisely declared
preservation scope above; no old kanji or stroke changes.
The first nineteen batches are review-closed. The ledger distinguishes
the shared container observation, initial model-specific contributions,
Claude's later roughness finding and the author's additional safeguards.
Neither the final confirmations nor the bounded candidate sweeps
establish exhaustive synonymy or native-fluency certification.

Batch 20 has independent initial reviews and changed-passage confirmations. Its fifteen kanji
and one supporting word, 蒸す, bring the authored total to 300 additions
and 907 exact reading rows. Counts are 920 kanji, 3,266 words and 302
selected N2 characters; 65 additions remain unauthored. The 59 new rows
contain 54 lexical examples and five qualified source-only/index rows.
The corrected packet retains 85 exact pairs from 81 complete entry families.
Twenty-one old word changes are links only; no old kanji or stroke
changes are needed.

The new examples distinguish 秘蔵's obsolete ひそう reading flag from
被う's rare spelling flag. 訓える and 訓む stay search-only index
evidence, not recommended examples. 触's undotted さわ is illustrated
inside 触り with its actual written kana boundary; 薄's bound forms
likewise have complete examples. A pinned spelling-family scan found
no 袋 spelling with a reading containing だい, but that bounded absence
does not prove a historical or compound reading impossible. 蒸す has
three direct humid-heat quiz safeguards and six English-label safeguards.
A bounded steam/sultry/humidity
sense sweep against existing card identities distinguishes these
overlaps from nouns for vapour, steam trains, and steaming-hot food
states; it is not exhaustive synonymy certification.

Both initial reviewers completed on the same blind snapshot, one
process at a time. GPT identified English weather senses of "sticky"
and "close"; Claude identified the omitted 布袋 ほてい homograph.
The corrections explicitly separate English-label ambiguity from
Japanese synonyms, and lexical recognition from comparative frequency.
Context-bound phrases such as "close friend" do not automatically
inherit every dictionary meaning of bare "close." Claude's optional
裏面 うらめん clarification and cleaner 補 distractor were also adopted.
These complementary observations are useful sample-specific evidence,
not a model ranking or a guarantee of completeness. Both original reviewers
subsequently marked all five corrected pages CLEAN on correctness, scoped
coverage and comprehensibility. The first twenty batches are review-closed;
optional citation/link polish was not used to prolong confirmation.

Batch 21's initial draft added fifteen kanji and
two supporting words, bringing the authored total to 315 additions and
942 exact source-reading rows. Counts are 935 kanji, 3,268 words and
317 selected N2 characters; 50 additions remain unauthored. Its 35
reading rows contain 33 lexical examples and two qualified lookup/index
rows. Twenty-three older word changes are component links only; no
older kanji or stroke changes. That draft's packet retained 71 exact records
from 67 complete entry families.

Distinguish 詞's rare spelling from an allegedly rare pronunciation,
and 谷まる's search-only index status from a recommended written form.
The pinned full-entry scan found no 詰 spelling paired with a reading
containing きち. That bounded absence cannot settle every historical
realization of キチ; contracted きっ alone cannot distinguish キチ from キツ.
豊前 is a historical place-name example, while 豊の秋 illustrates とよ
inside a complete expression, not a productive modern adjective.
貨's treasure-family membership establishes recognition, not equal
frequency with 宝. 貯える's shared entry with 蓄える does not establish
equal spelling preference in every collocation.

A full pinned-entry sweep for the new words' island-group and shell
labels considered applicable senses and primary article readings,
not just English titles. Two direct pairs on 貝 protect the broad
"outer covering" label on 皮 and the usually-kana specific-clam
abbreviation in the 馬鹿 family. These are separate safeguards, not
a claim that 皮 and 馬鹿 are synonyms or interchangeable with each
other. A mantle is a body part, not a whole shellfish; English
"shell" alone does not prove that a carapace identity shares the
specific seashell label. No broad substring or taxonomic clique is
inferred. The article distinguishes Japanese 貝's mollusc/shell
category from broader English shellfish, using the inspected opening
Kotobank definition as well as JMdict. The bounded sweep does not
certify exhaustive synonymy.

The same frozen batch-21 draft has now received independent initial
GPT/Claude review, with the first process exited before the next.
GPT identified the bare English "top" ambiguity activated by 貝's
other ばい identity, a spinning top; Claude marked that word page
CLEAN. Two additional direct safeguards protect トップ and 頂上,
without asserting that those Japanese words mean a spinning toy or
that かい names one. Context-bound "on top," "top and bottom" and
"top grade" labels are not treated as the bare noun. Existing
トップ/頂上 exclusions are not transitive. Dictionary recognition is
established; practical ambiguity of the complete multi-gloss labels
is medium-confidence, not a measured runtime failure.

Claude's optional distinction between characters and words in the
誌 comparison is adopted. The clam aside remains as an explanation
of a real guard; unrelated old reading-notation polish is not adopted.
The corrected packet has 73 exact records from 69 complete families
and four direct word pairs. Counts, reading rows, strokes and all
twenty-three links-only older-word changes are unchanged. The useful
initial actionable contribution was GPT's; Claude supplied the
optional clarity improvement. This is sample-specific evidence,
not a model ranking. Both original reviewers subsequently confirmed
the same committed two-page correction CLEAN on correctness, scoped
coverage and comprehensibility, with no established regression.

Claude's follow-up floated a low-confidence optional おもちゃ guard:
a spinning top is a toy, but that broader category alone did not
establish the same lexical answer overlap as bare "top". No additional
pair was added, and the decision does not depend on assuming that the
quiz displays the primary reading. Optional quiz-related prose polish
was also left alone. No actionable defect or consequential unresolved
claim remained in the changed passages. The first twenty-one batches
are review-closed; fifty additions remain unauthored.

Batch 22 adds fifteen kanji and the supporting 超過 and 軟らかい
articles. All 41 exact source readings have lexical examples,
including 軽's キョウ/キン, 輸's シュ, 辛's calendar かのと and
辺り ほとり. The latter is marked irregular okurigana and usually
kana, not incorrectly downgraded to search-only evidence.
賞める's rare-spelling flag does not make ordinary ほめる a rare
pronunciation. 軍 いくさ has an unmarked war/battle sense and an
archaic troops sense; do not transfer the latter flag to the whole
family. Unflagged alternate readings establish recognition, not equal
frequency. Complete families retain spelling/reading/sense restrictions.

The two new word pages receive no inferred JLPT level. 軟らかい
shares an unrestricted family with 柔らかい; separate 軟らか is a
na-adjective, not permission for 軟らかいな. The written 軟/らかい
boundary is not an inflectional stem boundary. 超過's dictionary
intransitive label and a natural limit-marking を construction must
not be reduced to "を always means affected transitive object."

A bounded softness/excess sweep produced candidates, not an automatic
synonym clique. Thirty direct safeguards protect actual applicable
senses and conservative English-label ambiguities. These include
secondary 出る "exceed," 豊か "well over," and あまり's restricted
surplus/over senses, not the alternate あんまり. Soft drink, turtle
shells, the skull's soft spot, qualified compound illumination labels,
mere excellence and negated "not exceeding" do not establish overlap.
Bare English light/soft/mild guards do not assert Japanese
interchangeability or a measured runtime failure. Even within the
retained pairs, warm air, low voice volume, low weight and illumination
remain distinct from softness. Surplus as available budget leeway is
not the same situation as exceeding that budget.

The packet retains 92 exact records from 85 complete families.
Twenty-two older-word changes are links only; no older kanji or
stroke changes. The author has read all seventeen new teaching pages
and all twenty-two older-word diffs. Validation reports zero errors;
the cumulative audit covers 330 additions and 983 reading rows.
Totals are 950 kanji, 3,270 words and 332 selected N2 characters,
with 35 additions still unauthored. Batch 22's independent review is
pending; the first twenty-one batches remain review-closed.

Batch 22's same-snapshot initial reviews are complete, sequentially.
Claude supplied two useful observations not present elsewhere in
GPT's report. The 跡 note was scoped to the displayed あしあと
example, but its imperative could be read as a wider ban; explicitly
retain the same spelling's そくせき reading without claiming equal
frequency. For a newly added spelling of an existing lexeme, inspect
incoming direct exclusions on the older spelling as well as English
gloss-search candidates. The glossary-only sweep missed もちもち's
springy/doughy/elastic record despite the actual article's soft-elastic
texture and supple-skin teaching. Its direct 柔らかい guard does not
transitively protect 軟らかい. A second conservative guard retains
もこもこ's fluffy-material overlap and existing same-lexeme precedent,
while expressly distinguishing lumpiness/bulging from softness.
These are pairwise, context-grounded decisions, not automatic copying
of every older exclusion or unrestricted synonym claims.

GPT separately inspected a real 出る/超える "exceed" overlap and
the pinned fallback algorithm. With the full frozen pool, 日 shares
three tags with 出 while 超 shares none, so it cannot take 出's
single default fallback slot. Additional 出 hardening is optional
for reduced pools, not an established default-quiz defect. Claude's
"unrelated" wording for all older two-choice meanings was too broad.
The two models therefore supplied complementary observations, not a
vote about correctness. Unsupported frequency/register additions and
an あんまり intensifier guard were not adopted.

The corrected packet has 95 exact records from 87 complete families,
including explicit 足跡 そくせき, and 32 direct word pairs.
All 41 rows, fifteen strokes, counts and twenty-two links-only older
word edits are unchanged. Both corrected pages have been reread;
scope verification and validation pass, and confirmation by the
original reviewers is pending.

Batch 22 is now review-closed. Both original sessions confirmed
the same corrected commit `fd607e1404e6b7891ff643d31b8a201eecc1b527`,
actual two-page diff and full changed pages, sequentially and with
zero edits. Both pages are CLEAN on all three facets. Claude also
corrected its initial blanket description of 出; no extra teaching
change was needed. All four reports are archived unchanged, both
reviewer processes have exited, and the final cumulative 63-file
scope preserves all older nonlink content. The manifest is unchanged
at `087a40fcf7840aab`. Thirty-five selected additions remain.

## Batch 23 authoring notes

The fifteen-character batch 述逆造郊郵量針鈍鉄鉱銅鋭録門防
adds supporting 鈍い and 鉱石 pages. The 39 exact metadata rows
have 38 lexical examples and one explicitly qualified 録しる.す
lookup row. A source-only qualification is more honest than borrowing
a differently spelled verb to fill the row. Complete family restrictions
matter for 録る's audio/video sense, 門と's shutter sense, 銅あかがね's
exclusion from the どう-only bronze abbreviation, and the separate
usually-kana 鈍いのろい family. 鈍ら is the complete なまくら word,
not a guessed 鈍くら spelling from the source dot.

The full packet contains 72 exact pairs as 73 records from 68 complete
families: a written/kana identity can still match two distinct entries.
Both しくしく families remain visible, with only the applicable
prolonged-dull-pain sense motivating its conservative guard. Do not
promote the separate archaic incessantly family into that meaning.
Likewise, an XML match for くらい's dark-adjective family does not
change the existing article's approximate-degree particle identity.
Regex dim must not accidentally match dimension or diminish.

Thirteen direct 鈍い safeguards preserve distinctions between lexical
overlap, contextual similarity and bare-English-dull ambiguity. 薄い's
pale/faint sense was inspected but did not by itself justify a dull-colour
guard. Gradualness, incrementality and speaking bluntly are not automatic
synonyms for sluggishness or a blunt edge. No ore/mineral/crystal
word candidate was established; broader stone and a metal are not
automatically ore. Neither new word gets an inferred vocabulary level.

Nineteen older words have links-only changes, preserving all metadata
and nonlink prose. The useful 門 link belongs in its existing Meaning
introduction because its combination section has no character mention;
do not add filler prose just to satisfy a linking helper.
All seventeen new pages and nineteen old-word diffs have been read.
Validation and the cumulative audit pass at 345 additions/1,022 rows;
the deterministic manifest is `63129c65a3f85e81`.
There are 965 kanji, 3,272 words and 347 selected N2 characters.
Twenty additions remain unauthored. Batch 23's independent review
is pending; batches 01-22 remain review-closed.

Both initial reviewers have now exited and their reports are archived
unchanged. GPT found no actionable defect. Claude uniquely identified
a dictionary spelling-scope disagreement for 門と. The original
shutter row follows pinned JMdict, so do not pretend the restriction
was missed there: Daijisen explicitly assigns the fitting sense to 戸,
while Nikkoku's earlier senses do not have the same division. The
author inspected the actual と headwords after discarding an unrelated
redirect from a guessed numeric URL. A successful fetch is not proof
that the fetched entry is relevant; the non-Joyo mark is not a
frequency measurement.

The correction uses the actual pinned 鳴門なると entry 1753350
for a lexical strait with roaring tides, not solely its proper-name
senses. The source notes the word's origin in 鳴門海峡; food and
place-name senses stay separate. The learner note retains the source
disagreement and ordinary 戸 contrast. The expanded packet has
73 pairs, 74 records and 69 complete families, including the original
門と record. Two optional 鉱石 comparison/example links are also
adopted; no more-familiar-example or register claim is assumed from
reviewer preference. Both original reviewers' changed-passage
confirmations are pending. This sample shows a useful unique Claude
contribution, not a general family ranking.

The corrected 58-file cumulative scope passes preservation, source
and reading audits; validation has zero errors. Repeated manifest
builds are byte-identical at `e59e527490d48a92`. Counts and 39
reading rows are unchanged. The actual two-page diff will accompany
the corrected commit in both original-reviewer confirmations.

Batch 23 is now review-closed at correction checkpoint
`b32b498c77ab63d635e63b573603882f423772d1`. Both original
reviewers confirmed the same two-page diff and full changed pages,
sequentially and without edits, and independently checked the actual
鳴門 headword. Both pages are CLEAN on all three facets; B23-R-01
is resolved. Four unchanged reports are archived and both processes
have exited. The final 60-file cumulative scope preserves all older
nonlink content; the manifest stays `e59e527490d48a92`. Twenty
selected additions remain unauthored.

## Batch 24: script notation, homographic families and custody viewpoints

The batch is 陸隅階隻雇雲零震革順預領額香駐. Its fifteen
kanji and generated stroke files add 38 lexical reading rows; no
source-only qualification is needed. The full-family source packet
contains 57 exact pairs, 58 records and 57 entry families.

Literal candidate lookup is not an absence proof. The raw pinned
JMdict contains 隻せき, even though it was not among the candidate
cache's leading suggestions. It also writes 零ゼロ in katakana,
corresponding to KANJIDIC2's hiragana ぜろ. Keep the character metadata
unchanged and retain the actual lexical-source spelling of the
reading. The verifier normalizes kana script only for sound matching;
it does not rewrite the exact evidence pair or infer an etymology
from the character dictionary's kun-list grouping.

陸ろく has both a legal-document numeral-six family and an unrelated,
usually-kana decent/proper family. Inspection of the first rendered
draft caught the generic first-record selector transferring the
latter's kana flag onto the numeric example. The renderer now accepts
an explicit entry selection for a reading row; the numeral selects
1585310, with the separate 1013290 family still available for the
comparison note. Check the rendered annotation and actual citation,
not merely the correctness of the supplied English gloss.

震う is dated; the renderer does not automatically attach that label,
so it is explicit in both the row and note. 預ける and 預かる are
both transitive, with different conjugation classes and custody
viewpoints. The contrasting 荷物を examples demonstrate the
participants without inventing a transitive/intransitive pair.
Keep 香きょう's shogi identity apart from incense, 領えり from
territory, and 額ひたい from the linked がく article's primary reading.

The new 隻 word article teaches a ship counter rather than a boat
noun, with numeral-counter placement and 一隻いっせき. A
restriction-aware scan of all current article identities against the
pinned dictionary found no other article with a matching ship,
half-pair or bundle counter sense. Actual counter and boat answer
labels were also inspected, including 枚, 軒, 回, 船, 舟 and ボート;
no direct word exclusion was established. Broad object association
alone is not synonymy. The thirteen older two-choice kanji targets
have no newly established synonym in this batch. These checks do
not certify arbitrary future decks or larger quizzes.

All sixteen new pages and the twenty-two old-word component diffs
have been read. The older edits are links only, including 総額;
the helper's actual output, not the preliminary word count, defines
the preservation scope. There are 980 kanji, 3,273 words and 362
selected N2 characters. The cumulative audit covers 360 additions
and 1,060 source-reading rows; five additions remain unauthored.
Validation has zero errors and repeated manifest builds are
byte-identical at `bf113d3993595c44`. Independent review is pending.

Both initial batch-24 reviewers have now exited and their reports
are archived unchanged. GPT established no actionable defect;
Claude uniquely supplied two minor usability recommendations:
register guidance for きざはし and a standard-writing alternative
for 領えり. The author inspected the actual cited Wiktionary
entries and native dictionary/encyclopedia headwords. Preserve
the source distinctions: JMdict does not label きざはし rare,
Wiktionary calls it archaic/literary, and the native dictionaries
recognize it without the same label. Recommend 階段 for ordinary
stairs without declaring きざはし unusable today.

For 領えり, recommend 襟 for standard learner writing and retain
the recognized 領 reading for recognition. A jōyō-table distinction
is not itself a frequency measurement or evidence that a dictionary
entry is wrong. The combined Kotobank エリ page contains both an
unrelated biblical entry and the relevant Nipponica えり section;
cite only what was actually inspected. The optional ゼロ link is
also adopted. Other optional expansion is not necessary for scoped
coverage. The exact three-page correction goes back to the original
reviewers sequentially; their confirmations remain pending.

At correction `ea3744200666795bc56f280dc3a89c9c135d118a`, both
original sessions resumed and independently marked all three
changed pages CLEAN on correctness, scoped coverage and
comprehensibility. Claude resolved F1/F2 and the adopted link;
GPT confirmed the changes without claiming prior discovery.
Both inspected the actual public usage evidence. Their processes
exited sequentially without edits and all four reports are archived.
The final punctuation/source-label preferences remain optional;
no new content was added to prolong the loop. Batch 24 is closed,
with the same manifest version `67808719c130984e`; five additions
remain for batch 25.

## Final batch 25 - 骨麦黄鼻齢

All five final cards use existing supporting word articles. Their
thirteen source-reading rows have twelve lexical examples and one
explicit source-only lookup row, 齢とし. The complete restriction-aware
JMdict scan establishes 22 pairs in 21 complete entry families, but
not that pair. Jitsū lists とし as a character reading; that confirms
the lookup reading without manufacturing a modern lexical example.
Daijisen supplies the actual age-noun construction 齢を重ねる.
Neither its old citations nor its non-jōyō notation is used as a
literary/rare label unsupported by the inspected entry.

Respect sense-local flags: 骨こつ's knack sense is usually written
in kana, but the same entry's bone/remains senses do not carry that
flag. The ほね supporting article is not a link for こつ. 黄金こがね
and 黄金おうごん belong to separate complete families; the obsolete
きがね/くがね flags are retained in the former family's evidence,
not transferred to こがね. 黄こ- is illustrated as a bound reading,
not by a substring match to a コウ compound.

The same よわい age noun also has the recognized spelling 歯.
Do not misclassify that lexical spelling as merely a visual
coincidence or infer that every tooth word is pronounced よわい.
This does not make the displayed tooth answer a meaning of 齢.

麦むぎ is not restricted to wheat: preserve the 小麦/大麦 crop
distinction. 麥/麦, 黃/黄 and 齒/the visible 歯 form have explicit
canonical-radical explanations without speculative historical claims.
The linked 黄色 and 黄色い articles retain their own primary
readings and noun/adjective distinction.

The older 年 target means both year and age. Its two curated wrong
choices would leave a default-quiz fallback slot; the new 齢 answer,
age, would be defensible for 年. Add 牛, cattle/cow, as a third wrong
choice. This is the final batch's only old-kanji metadata edit;
all other 年 metadata and every byte of its teaching text are
preserved. Curating three choices on 齢 alone would not fix the
reverse-direction fallback. The seven old-word changes remain links
only, and the existing 年齢/年 word exclusion is unchanged.

The remaining twelve older two-choice targets are screened against
the new meanings; the result is bounded to the default four-choice
quiz, not a guarantee about larger quizzes. No new word article,
word title, vocabulary JLPT label or exclusion is introduced.
Independent review remains pending.

Both initial final-batch reviewers have exited. GPT marked all
five new cards CLEAN. Claude uniquely identified B25-1: the 黄
note's "another source reading" is opaque learner-facing wording.
Delete that clause while keeping the explicit きいろ pronunciation.
Do not substitute an unverified claim that the dictionary's other
readings are non-everyday. The other suggested compounds, phonetic
history, priority-based frequency ranking and wording preferences
remain optional; no forced expansion is needed.
Both original sessions will confirm this one-page correction
sequentially. Their confirmations remain pending.

Both original sessions subsequently confirmed the committed
one-clause deletion, with GPT exiting before Claude started.
Both marked the complete changed 黄 card CLEAN across the three
facets; Claude explicitly resolved B25-1 and neither established a
regression. All optional suggestions remain optional. Batch 25 is
review-closed, completing review and reconciliation of all 365
additions. The final-batch sample supplied one useful Claude-only
wording catch and no GPT-only finding; it is complementary evidence
for this sample, not a general model ranking or proof of eliminated
bias. Unchanged-card verdicts come from the initial full-batch
reviews, not from the bounded confirmations.

## Completion and bounded model-usefulness summary

All 25 batches are review-closed. The pinned community N2 set has
367 cards: 365 additions plus unchanged 珍 and 短. There are also
63 new supporting word articles. The final source audit matches all
1,073 source-reading rows and all published selected dictionary fields
to the hash-verified inputs. The [completion record](n2-review.md#final-project-verification-and-completion)
details preservation, narrow legacy exceptions and remaining limits.

Using both model families was useful in this work. In the matched,
blind pilot reviews, GPT alone established 仲/中's secondary-meaning
quiz collision, while Claude alone supplied the missing 胡乱 example
for 乱's ロン. In batch 02, GPT alone identified サイン's applicable
secondary sign/indication sense, while Claude alone caught the missing
億万長者 kana. Shared observations also improved spelling
qualifications and context. These comparisons include optional
suggestions and limits as well as labelled findings; a different
severity label does not create a unique discovery.

Later confirmation rounds sometimes caught defects missed by both
initial passes. Those are useful later catches, not blind
initial-review wins. The final batch's Claude-only opaque-wording
finding is a small, independently confirmed contribution, not evidence
that one model is generally superior. The reports also contain
unsupported frequency inferences and optional expansions; adjudicating
against exact dictionary entries was essential. Model agreement did
not replace evidence, and disagreement did not automatically justify
a change.

The archive contains 114 reports, including 50 initial reports with
the same snapshot, scope, rubric and source access within each batch.
Review processes ran sequentially and exited before the next started;
original contexts were resumed for corrections instead of maintaining
a pool of live agents. This respected the memory constraint without
giving either initial reviewer the other's conclusions or the author's
adjudication.

This is qualitative evidence of complementary error detection in this
collection, not a controlled benchmark, a measured learning outcome,
an exhaustive linguistic guarantee or proof that model bias was
eliminated. Retain the sources, preserved reports and dispositions so
future corrections can build on concrete evidence rather than treating
any frozen review as permanent authority.

The later vocabulary phase builds on this completed kanji baseline. The
[whole-project retrospective](n2-vocabulary-notes.md#n2-project-retrospective)
combines the lessons from both phases; reusable checks are consolidated in
the [repository guide](../.github/copilot-instructions.md#large-card-expansions).
