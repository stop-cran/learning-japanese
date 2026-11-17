# B133 confirmation — N1-B133-CLAUDE-CONFIRM-001

## Snapshot
Commit: 110b4ffb6af078eb2adb00645db4c9e0bd6db188
Model: identity unverified (host reports Claude Opus 5.5; not verifiable from the supplied evidence)

## Scope
Chain: segments 1-17 of n1-b133-claude-confirm-001, each read once in order through END OF CHAIN; no re-views.
Fetches: none.

## Dispositions
- O1 - DECLINE ACCEPTED - My original O1 was optional and already judged 率/鉛 harmless. The revised 鉛 card still carries the "(metal)" title qualifier and states that it is not the verb "lead" (snapshot/kanji/鉛.md:3, snapshot/kanji/鉛.md:23-24), so declining the extra guard is sound.
- O2 - DECLINE ACCEPTED - The 字通 形声 analysis remains source-attested (evidence/external/琴-extract.txt:44-45). The cards keep structure-unclassified and do not contradict it, and the rubric permits that tag when no analysis is established. My point was optional.
- O3 - DECLINE ACCEPTED - The coordinator's reason is verified: Digital Daijisen 滝 sense 2 gives 急流/奔流 with a Man'yōshū example and no archaic mark (evidence/external/滝-extract.txt:7). The card body still records the JMdict archaic label, so keeping "waterfall; rapids" is defensible.
- O4 - DECLINE ACCEPTED - My point was optional. The card still marks ロウ and ソウ as retained from KANJIDIC2 and not practised (snapshot/kanji/滝.md:38-39). The decline reason says there is no pinned per-reading Joyo source, but the original packet did supply evidence/joyo-rows.json showing only たき for 滝. That inaccuracy in the reason is noted, but declining an optional clarity point remains acceptable.
- C1 - RESOLVED - 鉛-鉱 is now declared on 鉛 with a qualified Note (snapshot/kanji/鉛.md:13; snapshot/kanji/鉛.md:57-59). The supplied sources support it: あらがね/鉱 means unrefined metal or ore (evidence/external/鉱-extract.txt:8; evidence/external/粗金-extract.txt:7-8), and 鉛鉱 means lead mine or deposits (evidence/jmdict-families.xml:3). The Note correctly fixes my original description of 鉛鉱 as "lead ore". As a broad-label guard, not a synonymy claim, the precaution is consistent with the existing 金/素 guards.
- C2 - RESOLVED - The 鉛-鉄 distinction is retained, as I originally concluded. 鉄's senses are iron, weapons, hardness/strength, railway and iron colour (evidence/external/鉄-extract.txt:7-11). The generic かね【金・鉄・銀・銅】 "metal" word is unresolved per spelling, and the broad metal label is already guarded by 金 (evidence/external/金-extract.txt:42-43). "iron" and "lead (metal)" name different specific metals, so neither is a defensible answer for the other card.
- C3 - RESOLVED - 滝-速 is now declared on 滝 with the Note "including fast or surging flow" (snapshot/kanji/滝.md:13; snapshot/kanji/滝.md:60-63). The sources support it: Daijisen 滝 2 is 急流/奔流 (evidence/external/滝-extract.txt:7), and 速い explicitly covers 流れの速い川 (evidence/external/早い-extract.txt:5). The guard is conservative and consistent with the existing 急 precaution.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The complete teaching delta (diffs/fix.patch) only appends 11 direct exclusions to the three scoped cards and adds qualified Notes. The Notes do not overlap any distractor, change no title, reading, practice selection or mnemonic, and each one checked is supported by the supplied sources: 鉱/粗金 unrefined metal; 円 まろ 銭 and the JMdict 丸/円 slang-money sense; 遅 おそ【遅／鈍】 dull; 速い fast flow; 激 はげしく流れる; 声 inanimate sound; the 世界大百科事典 regional タキ cliff sense with its stated restriction (岩, 険 steep place); 具 器物/道具; 糸 for koto/shamisen; and 緒 琴の緒 with 和名抄 ことのを. All are framed as precautions, not synonymy. The 鉛-具 cross-pair distinction is accepted: 日国 具 ⑥ is pigment with added 鉛白, which names neither lead nor face powder in either displayed title. The revision proof confirms that only the three cards changed. All seven dispositions are accepting, there is no new defect and no consequential claim remains unresolved.

## Findings
None.

## Optional
None.

## Limits
- L1: My model identity is unverified; the host-reported Claude Opus 5.5 cannot be confirmed from the evidence.
- L2: The six retained distinctions 鉛-似, 鉛-倣, 琴-機, 琴-線, 琴-索 and 滝-液 are outside this confirmation. Their sections and counterpart cards were not supplied, and I did not judge them.
- L3: New metadata JMdict citations 1396980, 1404975, 1380440, 1244950 and 1343610 were not supplied as families. Only 1216250 and 1736440 were read, so those citation identities are unverified.
- L4: Kotobank evidence consisted of named publisher-section extracts, not whole pages, layout or images. There was no fresh KANJIDIC2 or whole-JMdict read and no web access.
- L5: The committed gates are listed in evidence/revision-proof.json, but their fresh logs were not in this chain and I did not re-run them. Runtime exposure is not independently re-modelled. Exclusions only remove choices; the curated distractors are unchanged and no added exclusion overlaps one.
- L6: Host models and mechanical proofs do not establish caller-built or multi-borrow pools, Kotlin execution, native/device acceptance, compatibility with the older installed APK, rendering or publication.
- L7: The precautions for 遅, 円, 岩, 険, 具 and 緒 rest on qualified, secondary, regional or historical senses. I judged them as conservative guards against unresolved labels, not as established ordinary overlaps; over-exclusion only reduces options.
