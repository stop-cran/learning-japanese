Snapshot: cbf5c2c5ca52758812aff3e61ae421e72fadd9e7, based on ac5304bac6a9352c7e6d98526e932875e6445edf (snapshot.txt). Packet extract only; git not checked.

Scope: Comprehensibility and scoped coverage, including natural examples, contrast, and concise phone reading. Reviewer: Grok 4.7 (grok-4.7), one pass. Read in full: kanji-1..4.txt (10 new kanji), words-1..4.txt (10 new words), changed.txt (10 diffs), comparison-words.txt (克服, 支配, 裁判, 対策, 葬式, 見舞い). Evidence used: sources.json, primary.xml, families-1..7.jsonl, quiz.txt, labels.txt. Correctness and quiz safety were not assigned.

Verdicts: correctness not assigned on every card. Scoped coverage / comprehensibility:
- 廷, 弊, 弓, 弔, 弥, 弦, 彩, 彰, 征, 忌: CLEAN / CLEAN
- 法廷, 弊害, 弓, 弔問, 弥縫策, 色彩, 表彰, 征服: CLEAN / CLEAN
- 弦楽: CLEAN / NEEDS FIX
- 回忌: NEEDS FIX / NEEDS FIX
- Diffs only (問, 回, 害, 服, 楽, 法, 策, 縫, 色, 表): CLEAN / CLEAN

Findings:
1. Moderate; scoped coverage and comprehensibility; words/回忌.md (words-4.txt:15, 17–18, 22, 26, 30). The meaning calls 回忌 a "yearly anniversary," and both examples are 三回忌 translated as the second anniversary. The off-by-one rule appears only later, and 一回忌 is presented as equal to 一周忌. A phone reader can treat 三回忌 as a one-off translation quirk and still miscount other anniversaries, or produce 一回忌 as the normal first anniversary. Remedy: define it as a numbered death anniversary (abbr. of 年回忌), not a yearly event. Replace one repeated 三回忌 sentence with a contrast next to the rule: 一周忌 is the usual first anniversary, one year later (一回忌 is also recorded, usually not the form used); 三回忌 is the second anniversary, two years later; from 三回忌 on, the number is years plus one. Do not add a full memorial calendar. Evidence: JMdict 1199390; 1161330 s_inf "usu. 一周忌"; 1163200; 1814080 "second anniversary." Confidence: high.

2. Moderate; comprehensibility (contrast); words/弦楽.md (words-2.txt:97). The card says an オーケストラ "adds wind and percussion" and that "its kanji word is 管弦楽." Packet JMdict glosses 管弦楽 only as orchestral music, while the card has just said 弦楽 names music, not an instrument or group. The equation undoes that distinction. Remedy: keep オーケストラ as the ensemble loanword; say 管弦楽 (かんげんがく) is orchestral music. Do not call it the kanji word for オーケストラ unless a sourced entry equates them. Evidence: 1263050; 1214130 gloss "orchestral music" only; 1769460 is the quartet, not this equation. Confidence: high on the packet mismatch.

Optional:
- words/弓.md (words-1.txt:88): 弓を習う in a school club is an original example used to force the archery sense. Sense 2 of 1228490 is real; the collocation is not in the packet. 弓道 (1228540) is the sourced activity name. Qualify the sentence, or do not use an unattested club collocation as the proof of the sense.
- words/弥縫策.md (words-2.txt:53): `ただのびほうさく` can be read as のび. Bound びほうさく with a space or dot in that reading only. The isolated びほうさく note can stay.
- kanji/弥.md Notes: move the joyo-only や / ビ-outside-table caveat beside the ビ row. Wording is already careful.
- kanji/弦.md つる row: pot-handle sense is esp. 鉉 (1578400). Add that qualifier.
- 弔問 and 表彰 second examples are long but readings match. Shortening is polish.
- 色彩 example 2 (赤や黄色の色彩) is slightly tautological. Not a meaning error.
- 征服 vs 克服 overlap is already qualified and matches both JMdict glosses. A sharper illness/fear note is optional, not required.

Limits: Daijisen bodies, the joyo PDF, and Kanjipedia pages were not in the packet; sources.json only records heading checks. No native, device, or external-page verification. Examples are original. 法廷 "usually inside a courthouse" and 色彩's figurative 保守的色彩が強い are Daijisen-attributed and unverified here; the taught senses are in JMdict, so those cards are not failed. labels.txt has no rows for 裁判, 支配, 対策, オーケストラ, 見舞い, 損害, or 公害; those contrasts were checked against comparison articles and families. Changed kanji were reviewed from diffs only. Example kana was checked against the Japanese sentences; that is not a correctness review.
