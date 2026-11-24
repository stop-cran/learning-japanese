Snapshot: b89b7a459db5f06a35fd690a7a5f535a5fdeb4dd, based on 364937d3a3c4b4f162f11c23c2d5f411d78d0a2e. Packet only; old-article edits from changed.txt. No uncommitted tree was reviewed.

Scope: 10 new kanji, 9 new words, reused 一, 8 diffs. Facets: scoped coverage, comprehensibility, natural examples, contrast, concise phone reading. Not correctness or quiz-safety. Reviewer: Grok 4.7 (grok-4.7), one blind pass.

Verdicts:
- kanji/壱: coverage CLEAN; comprehensibility CLEAN; examples CLEAN; contrast CLEAN; phone reading CLEAN
- kanji/奈: coverage NEEDS FIX; comprehensibility NEEDS FIX; examples CLEAN; contrast NEEDS FIX; phone reading NEEDS FIX
- kanji/奉: coverage CLEAN; comprehensibility CLEAN; examples CLEAN; contrast CLEAN; phone reading CLEAN
- kanji/奔: all five CLEAN
- kanji/奮: all five CLEAN
- kanji/奴: coverage CLEAN; comprehensibility NEEDS FIX; examples CLEAN; contrast CLEAN; phone reading NEEDS FIX
- kanji/如: coverage CLEAN; comprehensibility CLEAN; examples CLEAN; contrast NEEDS FIX; phone reading CLEAN
- kanji/妃: coverage CLEAN; comprehensibility NEEDS FIX; examples CLEAN; contrast NEEDS FIX; phone reading CLEAN
- kanji/妄: all five CLEAN
- kanji/妊: all five CLEAN
- words/奈良, 奔走, 奮う, 欠如, 王妃, 妄想, 妊婦: all five CLEAN
- words/奉仕: coverage NEEDS FIX; comprehensibility NEEDS FIX; examples UNVERIFIED; contrast NEEDS FIX; phone reading CLEAN
- words/奴: coverage CLEAN; comprehensibility NEEDS FIX; examples CLEAN; contrast CLEAN; phone reading CLEAN
- Diffs 仕, 婦, 想, 欠, 王, 良, 走, 一: hunks CLEAN on these facets

Findings:

1. Consequential. Comprehensibility, scoped coverage, contrast, phone label. kanji-1.txt:52, :66, :72, :83, :92, :94 (kanji/奈). The phone title is "na in names; how", but the body warns against everyday "what", the note teaches formal 奈辺 (なへん, "where"), and the rare spelling 奈何 is いかん ("how"). Impact: the quiz label memorizes a rare sense and leaves what/how/where unmapped; it also collides with 如's 如何 (いかが, "how"). Exclusion of 何 does not fix the label. Remedy: title and heading "na in names" only. In the body, map three sourced uses in one place: 奈良 (なら) is the name; formal 奈辺 (なへん, also 那辺) means "where"; rare 奈何 is a spelling of いかん ("how/what"), not everyday いかが, and must not split 奈良. Evidence: families 2827768, 1457680, 1582850, 2845606; KANJIDIC meanings "Nara", "what?". Confidence: high.

2. Minor. Phone reading, comprehensibility. kanji-2.txt:127–128; words-2.txt:50. The やっこ row says it is outside-table and "distinct from やつ", but Kanjipedia marks やつ outside-table too. The word card says やつ is "often" written in kana; entry 1445640 senses 1–2 say usually kana. Impact: 奴 looks like the ordinary spelling to produce. Remedy: on the やつ row, say Kanjipedia marks this kun outside the table and the word is usually kana; keep it as the useful quiz reading. Change "often" to "usually". Evidence: sources.json outside ["ヌ","やっこ","やつ"]; families-3 1445640. Confidence: high.

3. Minor. Comprehensibility, contrast. kanji-3.txt:72, :89. The opening says "consort or princess", but the only princess word learners get is the warning not to equate 王女 with 王妃. Entry 1956860 is the suffix 妃 (ひ), "princess, consort", not a free word for a king's daughter. Impact: "princess" is read as 王女. Remedy: "妃 is a consort. As a suffix read ひ it can mark a princely consort; that is not 王女 (おうじょ), a king's daughter." Evidence: families-5 1956860; families-1 1181560; families-2 1345020. Confidence: high.

4. Minor. Comprehensibility, coverage, contrast. words-1.txt:53, :61, :65. 「特価でご奉仕」 is translated "Special prices for our customers," so ご奉仕 has no English counterpart. Cited sense 2 is reduced price or a free service; the card gives "offered free" to サービス and only the discount half to 奉仕. Impact: learners cannot see the target word, and the サービス contrast is skewed. Remedy: translate so ご奉仕 remains, e.g. "Special prices, at your service." Add that sales 奉仕 can be a discount or a free offering, which is the overlap with サービス; community 奉仕 is the dedication sense. Evidence: families-4 1515950 sense 2; families-5 1946830, 2145970; families-1 1055000. Confidence: high on the gloss gap; the exact sign string is not in the packet.

5. Minor. Contrast. kanji-3.txt:42. "Compare 似 (resemble)" does not show the difference. The likeness question is otherwise well bounded by 如し and the 欠如 warning. Remedy: one clause that 似 is the ordinary "resemble" character, 如し (ごとし) is the classical "like / as if", and 如 in 欠如 is neither. Evidence: card text; 似's family entry is not in this packet, so do not treat a reading as verified here. Confidence: high that the contrast is missing; medium on the wording of the fix.

Optional: Rewrite 奉's "frozen source" (kanji-1.txt:134) as "listed under kun readings, though it starts with ほう." Align 壱's title "formal" with the legal-document note already in changed.txt:116 if the phone label should match JMdict, not KANJIDIC's broader "in documents." On 奴, one clause that やつ can also mean he/she in the same rough tone (cited sense 3). On 妄想, one clause that 空想 is a daydream and need not be wild. 惑 is only a pointer. "Does not add a zero" on 壱 is clear enough beside 10,000 yen. Undefined "source-only" is house jargon; the learner instruction in the same cell is what matters. 妊娠, the adverb 奮って, and 援助 are not required for the stated questions.

Limits: Daijisen/Weblio and live Kanjipedia pages were not opened. Example sentences are not corpus-attested here; sense alignment was checked against pinned JMdict. Example-internal words such as 気力 and 肖像画 were not separate family rows. Kanjipedia-only readings いかんぞ, なんぞ, うけたまわる, ヌ, しく, ゆく, もし are absent from the tables; treated as out of the KANJIDIC inventory, not defects. labels.txt has no kanji/奈 or kanji/如 row; titles were taken from the articles and quiz.txt, not treated as a runtime gap. Full text of the eight old articles was not in the packet. No native, device, or external-page verification. This is not a three-family publication review.
