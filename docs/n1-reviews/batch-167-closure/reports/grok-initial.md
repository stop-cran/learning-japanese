Snapshot: a22f26b78ce52a4991391092490dd1a118ea80b6 (snapshot.txt; git not checked). Packet teaching files and changed.txt reviewed as given.
Scope: Comprehensibility (natural examples, contrast, concise phone reading) and scoped coverage. Correctness not assigned. Files: kanji-1..4, words-1..4, changed.txt, comparison-words.txt; evidence primary.xml, sources.json, families-1..7.jsonl, quiz.txt, labels.txt. Model: Grok 4.7 (grok-4.7). No external page, native, or device check.
Verdicts (coverage / comprehensibility):
- kanji/己, 帆, 帝, 帥, 幽, 庶, 庸, 廃: CLEAN / CLEAN
- kanji/幻: CLEAN / NEEDS FIX
- kanji/廉: NEEDS FIX / NEEDS FIX
- words/自己, 帝国, 幻, 幽閉, 庶民, 凡庸, 廃止, 廉価: CLEAN / CLEAN
- words/帆: NEEDS FIX / NEEDS FIX
- words/元帥: CLEAN / NEEDS FIX
- words/安い (comparison-words.txt + diff): NEEDS FIX / NEEDS FIX
- changed 価, 元, 国, 止, 民, 自, 閉 (diff only): CLEAN / CLEAN
- changed 凡 (diff only): CLEAN / NEEDS FIX
Findings:
1. Moderate; comprehensibility and coverage; kanji/廉.md Notes. “嫌疑 (けんぎ) means suspicion; 廉 (かど) can mean grounds for a charge” ties suspicion to 嫌+疑 and drops it from かど. Phone readers can treat 嫌疑 as a 廉 word. Remedy: “廉 (かど), usually kana, means grounds, a charge, or suspicion. 嫌疑 (けんぎ) uses 嫌, not 廉.” Evidence: families-7 2085290; families-2 1257320. Confidence high.
2. Moderate; comprehensibility; changed.txt 凡.md hunk. The new 凡庸 bullet sits directly under the 凡て rare-spelling sentence, before Notes, so it reads as another rare spelling. Remedy: move `- [凡庸](../words/凡庸.md) ぼんよう — mediocre; unremarkable` into the common-word list, not after that warning. Evidence: diff context. Confidence high on local context; full 凡.md was not in the packet.
3. Minor; comprehensibility; kanji/幻.md Meaning. “In 幻の鳥 the image shifts…” is unclear and gives no reading. Remedy: “幻の鳥 (まぼろしのとり) can be a real bird so rarely seen it seems legendary, not something seen only in sleep.” Evidence: wording vs words/幻.md. Confidence high.
4. Minor; coverage and phone reading; words/帆.md How the kanji combine. “its reading is はん” sounds exclusive. Cited 帆船 is はんせん (priority) and ほぶね. Remedy: “Usual reading はんせん (帆 is はん); ほぶね is also recorded. Do not quiz ほぶね.” Evidence: families-6 1583230. Confidence high.
5. Minor; natural examples; words/元帥.md examples. 陸軍元帥 and 海軍元帥 are not in the packet; they are original labels built to force the English split. Partial caveat does not say the titles are unverified. Remedy: use 元帥 alone in the sentences, and state in prose that “field marshal” vs “fleet admiral” is a translation choice, not a fixed 陸軍/海軍 title formula. Evidence: families-2 1260890; sources.json “examples are original.” Unnaturalness itself unverified. Confidence medium.
6. Minor; coverage and comprehensibility; words/安い.md Distinctive meaning. “can also be written 廉い” skips that 廉い has no priority tags and that the calm sense is stagk 安い only. N5 readers may not open 廉.md. Remedy: “Uncommon recorded spelling 廉い, 廉 read やす. Recognize it; do not read 安い as れん, and do not use 廉い for the calm sense.” Evidence: families-1 1153670. Confidence high.
Optional: 自己 vs 事故 (1313850); 廉価 vs 安価, including 安価’s pejorative sense (1153740); one non-quiz note that 大帝 is たいてい (1786140), not a new quiz key; 幽霊; 凡例 vs 判例 (both はんれい); say 大尉 is far below 元帥; compress 幽’s three “do not write” rows; gloss “standard-use table” once. Do not add いさぎよい to the phone quiz.
Limits: Daijisen pages were not opened. Full pre-existing kanji articles were not in the packet. Original example idiomaticity, including 帆は垂れたまま, was not native-checked. Quiz “no errors” is an author-side simulation. Kanjipedia outside readings omitted on 帥, 庶, 庸, and 廃 match the concise-quiz pattern and were not treated as defects.
