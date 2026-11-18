# B133 confirmation — N1-B133-CLAUDE-CONFIRM-002

## Snapshot
Commit: d7d6cff92afe8220c16a5daa76f1c3f00a2bef30
Model: identity unverified (host reports Claude Opus 5.5; not verifiable from the supplied evidence)

## Scope
Chain: segments 1-29 of n1-b133-claude-confirm-002, each read once in order through END OF CHAIN; no re-views.
Fetches: none.

## Dispositions
- O1 - DECLINE ACCEPTED - The point was optional and already judged harmless. The signed 鉛 card keeps the title "lead (metal)" and says explicitly that it is not the English verb "lead" (snapshot/kanji/鉛.md:3; snapshot/kanji/鉛.md:23-24). 率's sense of commanding has no metal, money, powder or dullness sense, so the qualifier is enough.
- O2 - DECLINE ACCEPTED - The point was optional. 字通 records 琴 as 形声 with 声符 今 (evidence/external/琴-extract.txt:44-45), and 滝 as 形声 with 竜 (evidence/external/滝-extract.txt:69-70). The cards keep structure-unclassified and only labelled modern-shape mnemonics, which contradict neither analysis.
- O3 - DECLINE ACCEPTED - Digital Daijisen 滝 sense 2 gives 急流/奔流 with no archaic mark (evidence/external/滝-extract.txt:7). The card body still discloses that JMdict marks rapids as archaic (snapshot/kanji/滝.md:23-24). The added flow guards (急, 速, 激) are built on the current title, so keeping "waterfall; rapids" is defensible.
- O4 - DECLINE ACCEPTED - The point was optional. The card states that ロウ and ソウ are retained from KANJIDIC2 without a supporting word and are not selected for practice (snapshot/kanji/滝.md:39-40). The coordinator's original reason ("no pinned per-reading Joyo source") was corrected in the CONFIRM-001 adjudication (evidence/claude-confirm-001-adjudication.json:17). The Joyo row itself is not in this chain.
- C1 - RESOLVED - 鉛-鉱 is declared on 鉛 (snapshot/kanji/鉛.md:14) and has a qualified Note (snapshot/kanji/鉛.md:57-59). Daijisen gives 鉱 as 精錬してない金属 (evidence/external/鉱-extract.txt:8), and 粗金/鉱 as unrefined metal or ore (evidence/external/粗金-extract.txt:7). The 日国 鉛 entry names lead ores such as 方鉛鉱 (evidence/external/鉛-extract.txt:20), and JMdict 1736440 鉛鉱 is "lead mine; lead deposits" (snapshot/docs/n1-sources/batch-133-reconciliation/source/jmdict-complete-families.xml:2869-2880). The Note's correction of "lead ore" is accurate.
- C2 - RESOLVED - The 鉛-鉄 distinction is retained, as originally concluded. Daijisen 鉄 sense 1 and the kanji-item sense 1 name the specific element iron (evidence/external/鉄-extract.txt:6; evidence/external/鉄-extract.txt:14). The generic 日国 かね【金・鉄・銀・銅】 "metal" headword is already covered by the 金 guard (evidence/external/金-extract.txt:35-37; snapshot/kanji/鉛.md:57). "iron" is not a defensible answer for 鉛, and "lead (metal)" is not one for 鉄.
- C3 - RESOLVED - 滝-速 is declared on 滝 (snapshot/kanji/滝.md:14) and covered by the Note on fast or surging flow (snapshot/kanji/滝.md:61-65). Daijisen 滝 sense 2 is 急流/奔流 (evidence/external/滝-extract.txt:7), and 速い explicitly covers 流れの早い川 (evidence/external/早い-extract.txt:7).

## Verdicts
Correctness: UNVERIFIED
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: UNVERIFIED
Basis: The cumulative delta (diffs/fix.patch; diffs/reconciliation-002.patch) only appends 12 direct exclusions to the three scoped cards, adds qualified Notes and adds metadata citations; no title, reading, practice selection, distractor, common word or mnemonic changes, and no added exclusion overlaps a distractor. On the supplied sections I confirm the added precautions: 鉱 (unrefined metal or ore), 遅 (おそ【遅／鈍】 dull), 円 (まろ【円・丸】 銭, yen, and the JMdict 丸/円 slang money sense), 速 (fast flow), 声 (inanimate sound), 激 (はげしく流れる), 岩 and 険 (the restricted regional タキ cliff sense), 具 (器物/道具), 糸 (koto and shamisen) and 緒 (琴の緒, with 和名抄 ことのを). I also confirm the 滝-液 precaution decision: 滝 [2] is an abbreviation of 滝水, 字通 gives ひたす/うるおす, and 液 is a formless flowing substance. I judge each of the six retained distinctions as needing no precaution. 鉛-鉄 contrasts two specific metals, and broad metal is guarded by 金. 鉛-似 and 鉛-倣 contrast an imitation action with 鉛's noun 贋金. 琴-機 (machine, loom, opportunity), 琴-線 (line, wire, route; 琴線 is a compound only) and 琴-索 (thick rope, search) name no instrument or instrument string. The 鉛-具 cross-pair also stands: 日国 具 ⑥ is a pigment containing 鉛白, and neither displayed title names lead or face powder. The five new JMdict identities match their cited headwords. However, the new 液 Note teaches 滝水 as "water from a waterfall," and the supplied 日国 section only says that 滝 is short for 「たきすい（滝水）」 with an Edo sharebon example; it does not define 滝水. That learner-facing gloss therefore remains a consequential unverified meaning claim, though the precaution is sound under any liquid reading.

## Findings
None.

## Optional
### O1: Source or remove the 滝水 gloss
- Facet: Correctness
- Severity: optional
- Confidence: medium
- Citations: snapshot/kanji/滝.md:72-77; snapshot/kanji/滝.md:26-27; evidence/external/滝-extract.txt:33-34; evidence/external/液-extract.txt:12-13
- Evidence: Both the new 液 Note and the unchanged Meaning section gloss 滝水 as "water from a waterfall." The cited 日国 section gives only 「たきすい（滝水）」の略 and the example 「たきがあらばちっとわってくんねへ」. No supplied section defines 滝水 or its reading たきすい, so the gloss cannot be confirmed or refuted here. The 液 precaution is safe whatever liquid 滝水 denotes.
- Suggestion: Cite the 日国 headword たきすい【滝水】 for the gloss. Alternatively, reword both places to say only that 日本国語大辞典 records 滝 as an abbreviation of 滝水 (たきすい), and keep the precaution.

## Limits
- L1: My model identity is unverified; the host-reported Claude Opus 5.5 cannot be confirmed from the supplied evidence.
- L2: The meaning of 滝水 (たきすい) is not defined in any supplied source, so the gloss "water from a waterfall" is unverified (see Optional O1); I did not fetch or infer it.
- L3: The Kotobank evidence consisted of complete named publisher sections, not whole pages, layout or images. I did no fresh KANJIDIC2 or whole-JMdict read and had no web access. I verified the five new JMdict identities against the reconciliation family file: 1244950 具 (lines 1057-1082), 1343610 緒 (1541-1563), 1380440 声 (1623-1676), 1396980 粗金/鉱 (1819-1840) and 1404975 早い/速い (1841-1931). Earlier card citations are outside this delta.
- L4: evidence/joyo-rows.json and the original packet are not in this chain, so the O4 Joyo basis rests on the card text and the adjudication record.
- L5: The committed gates are listed in evidence/revision-proof.json and evidence/revision-proof-002.json, but I did not read or re-run their logs. These are mechanical boundary proofs, not semantic acceptance, and one latent reading collision is reported. Runtime exposure is not re-modelled: exclusions only remove choices, and no added exclusion overlaps a curated distractor.
- L6: Host models and mechanical proofs do not establish caller-built or multi-borrow pools, Kotlin execution, native or device acceptance, compatibility with the older installed APK, rendering or publication.
- L7: The precautions for 遅, 円, 岩, 険, 激, 具, 緒 and 液 rest on qualified, secondary, regional or historical senses. I judged them as conservative quiz guards, not synonymy claims. The retained-distinction judgments depend partly on how learners read English labels.
- L8: The coordinator's line pointers in evidence/coordinator-dispositions-002.json for 液 (:12 and :17) are offset by one line from the definitions at evidence/external/液-extract.txt:13 and :18. This affects only the record, not the card.
