# B133 confirmation — N1-B133-CLAUDE-CONFIRM-003

## Snapshot
Commit: b1acf155fb8c7e1066a5c3baf88ae98ab92c29ac
Model: identity unverified (host reports Claude Opus 5.5; not verifiable from the supplied evidence)

## Scope
Chain: segments 1-34 of n1-b133-claude-confirm-003, each read once in order through END OF CHAIN; no re-views.
Fetches: none.

## Dispositions
- O1 - DECLINE ACCEPTED - The point was optional. The unchanged 鉛 card keeps the title "lead (metal)" and says explicitly that it is not the English verb "lead" (snapshot/kanji/鉛.md:3; snapshot/kanji/鉛.md:23-24). The 率 homograph therefore relies on a visible qualifier, not on the learner guessing.
- O2 - DECLINE ACCEPTED - The point was optional. 字通 analyses 琴 as 形声 with 声符 今 (evidence/external/琴-extract.txt:44-45). The cards keep structure-unclassified and only labelled modern-shape mnemonics (snapshot/kanji/琴.md:29-32; snapshot/kanji/滝.md:30-34), so nothing contradicts that analysis.
- O3 - DECLINE ACCEPTED - Digital Daijisen 滝 sense 2 gives 急流/奔流 with no archaic mark (evidence/external/滝-extract.txt:7). The body still discloses that JMdict marks rapids as archaic (snapshot/kanji/滝.md:23-24), so keeping "waterfall; rapids" is defensible.
- O4 - DECLINE ACCEPTED - The point was optional. ロウ and ソウ are still marked as retained from KANJIDIC2 and not selected for practice (snapshot/kanji/滝.md:40-41). The coordinator's original reason was corrected in evidence/claude-confirm-001-adjudication.json:17. The Joyo row is not in this chain.
- C1 - RESOLVED - 鉛-鉱 is declared (snapshot/kanji/鉛.md:14) and has a qualified Note (snapshot/kanji/鉛.md:57-59). The sources support it: 鉱 is 精錬してない金属 (evidence/external/鉱-extract.txt:8), あらがね is unrefined metal or ore (evidence/external/粗金-extract.txt:7), and 方鉛鉱 is named as a lead ore (evidence/external/鉛-extract.txt:11). JMdict 1736440 鉛鉱 is "lead mine; lead deposits" (snapshot/docs/n1-sources/batch-133-reconciliation/source/jmdict-complete-families.xml:2853-2866), as the Note states.
- C2 - RESOLVED - The 鉛-鉄 distinction is correctly retained. Both senses of 鉄 that name the element mean iron specifically (evidence/external/鉄-extract.txt:6; evidence/external/鉄-extract.txt:14). The generic かね【金・鉄・銀・銅】 metal headword (evidence/external/金-extract.txt:35-37) is covered by the existing 金 guard (snapshot/kanji/鉛.md:14). Neither "iron" nor "lead (metal)" is a defensible answer for the other card.
- C3 - RESOLVED - 滝-速 is declared (snapshot/kanji/滝.md:14) and explained by the fast or surging flow Note (snapshot/kanji/滝.md:62-66). The sources support it: 滝 sense 2 is 急流/奔流 (evidence/external/滝-extract.txt:7), and 速い covers 流れの早い川 (evidence/external/早い-extract.txt:7).

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The cumulative delta from ad047ace only appends 13 direct exclusions to the scoped cards, adds qualified Notes and metadata citations, and corrects one 滝 Meaning sentence; reconciliation-003 changes only 滝.md, and 琴.md and 鉛.md are byte-identical to the earlier confirmed snapshot. Titles, readings, practice selections, distractors, common words and mnemonics are unchanged, and no exclusion overlaps a distractor. The corrected Meaning sentence is now supported: 日国 滝 [2] is 「たきすい（滝水）」の略, with a 1791 洒落本 example, and 日国 たきすい【滝水】 is a sake sold by 四方久兵衛 in 神田和泉町, Edo, while たきみず and ろうすい carry the waterfall-water senses. That supports both the 酒 Note and its qualification that this is not a modern sense of 滝. The amended 液 Note now rests only on supported grounds: 滝 is a flow of water, 字通 gives ひたす/うるおす, the abbreviated sense names a drink, and 液 is a formless flowing substance. I re-verified the 12 other added precautions on the supplied sections. These are 鉱 (unrefined metal), 遅 (おそ【遅／鈍】), 円 (まろ 銭, yen, and JMdict 丸/円 slang money), 速, 声 (inanimate sound and 雨声/水声), 激 (はげしく流れる), 岩 and 険 (the restricted regional タキ cliff sense), 具 (器物/道具), 糸 (koto and shamisen) and 緒 (琴の緒; 和名抄 ことのを). All are worded as guards, not synonymy claims. I judge each of the six retained distinctions as needing no precaution. 鉛-鉄 names two specific metals, and broad metal is guarded by 金. 鉛-似 and 鉛-倣 contrast resemblance or imitation actions (似せる 贋造する; まねる) with 鉛's noun 贋金, and neither displayed title names money. 琴-機 is machine, loom or opportunity. 琴-線 is line, wire or route, and 琴線 belongs to the compound only. 琴-索 is thick rope or search; none of these three names an instrument or instrument string. The 鉛-具 cross-pair stands: 日国 具 ⑥ is a pigment with added 鉛白, and neither displayed title names lead or face powder. All five reconciliation JMdict identities match their headwords. All seven dispositions are accepting, there is no new defect, and no consequential claim remains unresolved.

## Findings
None.

## Optional
None.

## Limits
- L1: My model identity is unverified; the host-reported Claude Opus 5.5 cannot be confirmed from the supplied evidence.
- L2: Prior CONFIRM-002 observations are reassessed as follows. Its optional point O1 and limit L2 on the 滝水 gloss are resolved. The gloss is corrected at snapshot/kanji/滝.md:26-28 and snapshot/kanji/滝.md:73-78, with the 酒 Note at snapshot/kanji/滝.md:79-84 and the citation at snapshot/kanji/滝.md:109-110. All of this is supported by evidence/external/takisui-sections.txt:4-9 and evidence/external/滝-extract.txt:33-34. Its L8 was my error: the 液 pointers :12 and :17 correctly locate the definitions (evidence/external/液-extract.txt:12; evidence/external/液-extract.txt:17), so that observation is withdrawn. Its C1 citation of family-file lines 2869-2880 for JMdict 1736440 was also wrong; the entry is at lines 2853-2866. Its other observations still apply unchanged.
- L3: The たきすい definition ends with 「滝の水。」 after the sake definition and has no separate numbered sense (evidence/external/takisui-sections.txt:5). I read that phrase as part of the single sake sense. The card makes no claim that depends on it, and the 液 and 酒 precautions hold either way.
- L4: "Edo-period" for the abbreviation rests on the 1791 example and the Edo sake, not on an explicit period label in 日国 (evidence/external/滝-extract.txt:33-34).
- L5: I verified the five reconciliation JMdict identities in the signed family file: 1244950 具 (lines 1057-1082), 1343610 緒 (1541-1563), 1380440 声 (1623-1676), 1396980 粗金/鉱 (1819-1840) and 1404975 早い/速い (1841-1931). Earlier unchanged citations are outside this audit.
- L6: The Kotobank evidence consisted of complete selected publisher sections, not whole pages, HTML, layout or images. I did no fresh KANJIDIC2 or whole-JMdict read and had no web access. evidence/joyo-rows.json and the original packet were not in this chain.
- L7: The committed gates are listed in evidence/revision-proof-003.json, but I did not read or re-run their logs. These mechanical proofs are not semantic acceptance, and one latent reading collision is reported. Runtime exposure is not re-modelled; exclusions only remove choices.
- L8: Host models and mechanical proofs do not establish caller-built or multi-borrow pools, Kotlin execution, native or device acceptance, compatibility with the older installed APK, rendering or publication.
- L9: The precautions for 遅, 円, 岩, 険, 激, 具, 緒, 液 and 酒 rest on qualified, secondary, regional or historical senses. I judged them as conservative quiz guards; the retained-distinction judgments depend partly on how learners read English labels.
