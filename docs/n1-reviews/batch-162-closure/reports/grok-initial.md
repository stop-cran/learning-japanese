Snapshot: candidate 4dcff959aaa5394e35342e11b9f2c48d846f395e (packet base 2eb37d432a2ecc7d52ad35fcd319ea936b32d505). Packet files only; no worktree check.

Scope: Learner comprehensibility, examples, contrast, and scoped coverage for an English-speaking phone reader. Reviewer: Grok 4.7 (grok-4.7). Read all 19 new cards, reused-word.txt, changed.txt, quiz.txt, related-labels.txt, sources.json, support-families.xml, and the all-families.xml entries cited below. Correctness was not assigned and is not verdicted. Quiz-system safety was not assigned; labels were used only to see which contrasts the reader must make.

Verdicts: Comprehensibility NEEDS FIX. Scoped coverage NEEDS FIX. Most cards are usable: short examples have kana and translations, and 土壌, 塾, 古墳, 開墾 vs 耕す, and 壇’s podium note are clear. Per article (comprehensibility / scoped coverage):

- kanji/塁 NEEDS FIX / NEEDS FIX
- kanji/塑 CLEAN / CLEAN
- kanji/塚 CLEAN / CLEAN
- kanji/塾 CLEAN / CLEAN
- kanji/墜 NEEDS FIX / NEEDS FIX
- kanji/墳 CLEAN / CLEAN
- kanji/墾 CLEAN / CLEAN
- kanji/壇 CLEAN / CLEAN
- kanji/壌 CLEAN / CLEAN
- kanji/壮 CLEAN / CLEAN
- words/一塁 CLEAN / CLEAN
- words/彫塑 NEEDS FIX / NEEDS FIX
- words/塚 NEEDS FIX / NEEDS FIX
- words/塾 CLEAN / CLEAN
- words/古墳 CLEAN / CLEAN
- words/開墾 NEEDS FIX / CLEAN
- words/壇 CLEAN / CLEAN
- words/土壌 CLEAN / CLEAN
- words/壮大 NEEDS FIX / CLEAN
- words/落ちる (full text) CLEAN / CLEAN
- Added gloss lines in kanji/一, 古, 土, 大, 彫, 開: CLEAN / CLEAN for those lines only

Findings:

1. Moderate. Comprehensibility and scoped coverage. kanji-1.txt:32-35, 43 (kanji/塁.md). The fort half of the title is not usable. The table teaches fort only as 塁 とりで and calls that a typical word, adding only that JMdict “also lists” 砦. JMdict 1295240 marks 塁 as a rarely used kanji form; 砦 is the head spelling. The same card cites JMdict 1555910 (all-families.xml:2738), where common 塁 (るい) means baseball base/bag/sack and fortress/stronghold, with no rare tag. A phone reader will produce the rare kun spelling and never learn the on-reading noun. “Not a military base” does not supply a fort example. Remedy: put 塁（るい） on the ルイ row with both glosses; mark とりで/塁 as rare and point to 砦; do not list it under typical words. Confidence: high.

2. Minor. Comprehensibility and scoped coverage. kanji-2.txt:87, 89 (kanji/墜.md). “Highlights the fall” and “not a replacement for 落 in all the verb’s other senses” give no boundary a reader can apply, and line 89 narrows the contrast to an aircraft. JMdict 1548550 lists 墜ちる with no sense restriction; 堕ちる is the spelling that has sense notes. The 落ちる card already says the usable thing: same verb, 墜 writes お, keep 落ちる as the ordinary spelling. Remedy: use that wording; do not state a ban the inspected entry does not support; contrast 堕 and 陥 without making 墜 aircraft-only. Confidence: high.

3. Minor. Comprehensibility and scoped coverage. words-1.txt:100 (words/塚.md). “If you point out a 塚, you are drawing attention to the mound” is too absolute. JMdict 1433620 sense 3, unmarked rare, is standing stone / stone signpost / roadside stone statue. The mound examples are good. Remedy: scope that sentence to the mound uses, and add one clause for the stone-marker sense. Confidence: high.

4. Minor. Comprehensibility. words-1.txt:65 (words/彫塑.md). “Making a model for a sculpture” is not the inspected JMdict 1428070 gloss “clay model,” and no example shows it. The main sculpture examples are usable. Remedy: teach “clay model” in plain words, or quote a Daijisen sense you have actually read, with one example. Confidence: medium.

5. Minor. Comprehensibility. words-2.txt:101 (words/開墾.md). “Reclamation” has no antecedent on the card, so the sea warning does not qualify a claim the reader has seen. The farmland examples and the 耕す contrast are clear. Remedy: “A dictionary gloss is ‘reclamation’; that need not mean land from the sea.” Confidence: high.

6. Minor. Comprehensibility. words-3.txt:86 vs 89 (words/壮大.md). “Use 壮大な before a noun” sits beside 計画は壮大だが. On a phone, that invites the error 壮大なだ. Remedy: “Before a noun, 壮大な; as a predicate, 壮大だ.” Confidence: high.

Optional: name 一塁手 in one position example; one line that 一塁 can mean “one fort” outside baseball; 塑像 (そぞう) as an extra ソ word; 壇’s ceremonial-mound sense and that 壇上 is also glossed “on a stage; on an altar”; do not parse 土壇場 part by part; 塚 “still stands” for 残っている; 壌 “beneath the crops”; readings for 型; drop “source-only” / “metadata” jargon where the next clause already says not to use the reading.

Limits: Daijisen and Kanjipedia pages were not in the packet and were not read. 文壇 (words-3.txt:31) was not found as an entry; the circles sense is in support-families.xml 1419320, the reading ぶんだん was not verified from an entry. 本塁 was not found. Sentence idiomaticity was not corpus-checked. Full text of reused kanji 一, 古, 土, 大, 彫, and 開 was not supplied. Not every one of the 108 families was read. No other reviewer reports.
