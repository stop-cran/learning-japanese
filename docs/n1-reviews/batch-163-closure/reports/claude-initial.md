**Snapshot:** b89b7a459db5f06a35fd690a7a5f535a5fdeb4dd (base 364937d3…), packet files only. For the 7 changed kanji articles and the changed 一 word card I saw only the `changed.txt` hunks. I did not read the full 仕, 婦, 想, 欠, 王, 良 or 走 articles. No uncommitted changes were identified.

**Scope:** Blind, read-only review by one reviewer, Claude Sonnet 5.5 (model ID claude-sonnet-5.5, self-reported). Facets: correctness (readings, restricted senses, grammar, translations) and scoped coverage. Comprehensibility was not assigned, so it is UNVERIFIED for every article and only noted incidentally.

I read these in full, one view at a time: `rubric.txt`, `snapshot.txt`, `changed.txt`, `reused-word.txt`, `kanji-1` to `kanji-4`, `words-1` to `words-3`, `sources.json`, all 309 lines of `primary.xml`, `families-1` to `families-5`, `quiz.txt` and `labels.txt`. The view tool returned no line numbers, so findings cite the file and section.

**Verdicts** (correctness / scoped coverage)
- **New kanji:**
  - CLEAN / CLEAN: 壱, 奈, 奉, 奔, 奮, 如, 妃, 妄, 妊.
  - 奴: NEEDS FIX (F1) / CLEAN.
- **New words:**
  - CLEAN / CLEAN: 奈良, 奔走, 王妃, 妊婦.
  - 奉仕: NEEDS FIX (F5) / CLEAN.
  - 奮う: UNVERIFIED (F7) / CLEAN.
  - 奴: CLEAN / NEEDS FIX (F3).
  - 欠如: NEEDS FIX (F2) / CLEAN.
  - 妄想: NEEDS FIX (F4) / CLEAN.
- **Changed articles:**
  - CLEAN / CLEAN: 仕, 婦, 想, 欠, 王, 走. The added bullets and entry IDs match JMdict.
  - 良: CLEAN / UNVERIFIED (F8).
  - 一: NEEDS FIX (F6, provenance only) / CLEAN.

No blocking defect was found. Every finding below is minor.

**Findings (actionable)**

- **F1 — minor, correctness, `kanji-2` 奴 Readings table.** The やっこ row says "outside-table reading distinct from やつ", which implies やつ is in the table. `sources.json` lists やつ, やっこ and ヌ all as Kanjipedia "outside". Remedy:
  - Mark the やつ row as outside-table too.
  - Say it is taught because of the word 奴, which JMdict 1445640 marks usually-kana.
  - Reword the やっこ row as a different word (JMdict 1445630).
  - Confidence: high.
- **F2 — minor, correctness, `words-2` 欠如 "How the kanji combine".** "[如] … helps form a word for a state" is not supported by the packet, which gives only glosses. Remedy: cite a source, or replace it with "如 has no separate 'like' meaning here; learn 欠如 as a whole word". Confidence: medium.
- **F3 — minor, coverage, `words-2` 奴.** The card cites JMdict senses 1–3 but teaches only person and thing. Sense 3 is the pronoun use ("he/she", derogatory or familiar). Remedy: add one clause on sense 3, or narrow the citation to senses 1–2 and clarify the title's "that one". Confidence: medium.
- **F4 — minor, translation, `words-3` 妄想 example 2.** 旅行の話 means "talk or idea of a trip", but the translation reads "That trip…". Remedy: "The idea of a trip is still just a fantasy of mine." Confidence: medium.
- **F5 — minor, provenance, `words-1` 奉仕 (and 奉 metadata).** The card uses 奉仕活動 and ご奉仕品, but cites only entry 1515950. `families-5` has 2145970 (奉仕活動) and 1946830 (奉仕品). JMdict attests 奉仕品, not ご奉仕品 or the sign text. Remedy: cite both entries and mark the sign as illustrative ad copy. Confidence: high for the omission, medium for attestation.
- **F6 — minor, provenance, `changed.txt` 一.** The new "壱万円 and 一万円 both mean 10,000 yen" is supported by JMdict 2138590, which the Source line doesn't cite. Remedy: add that entry. Confidence: high.
- **F7 — minor, UNVERIFIED, `words-2` 奮う.** "気力を奮って" is an invented collocation with no corpus evidence in the packet. JMdict's sense 1 gloss gives only "muster (e.g. one's courage)", so the title's "or energy" is extra. Remedy: replace it with a courage example, or verify via the Daijisen entry or a corpus. Confidence: low to medium.
- **F8 — minor, UNVERIFIED, `changed.txt` 良.** The diff adds 奈良 なら to the common words but shows no note that ら is name-only, not a reading of 良. The full 良.md was not in the packet. Remedy: add a one-line note, or confirm one exists. Confidence: medium.

**Optional**
- 奮 Notes: "long う" is ambiguous. Say "the う after る (ふるう, not ふる)".
- 奮う:
  - 振るう (a homophone) and the adverb 奮って (JMdict 1504710, a separate entry) are unmentioned. 振るう is from my background knowledge and is not in the packet.
  - The intransitive sense has no example.
- 奔: JMdict's "occ. 奔る" note is attached only to sense 5 (run away, elope). The card's "run or rush" is broader.
- 奈: いかん is labelled kun, but JMdict marks 奈何 as gikun/jukujikun (a whole-word reading).
- 如: ごとし is probably literary. The packet carries no register tag, so I could not verify this.
- 欠如: 欠如 vs 不足, the actual quiz partner, is not contrasted. This would be a tendency only.
- 奉仕: explain the prefix ご, and state the discount sense in "Meaning".
- Quiz-safety observations from `labels.txt` (outside my facet; hypotheses only):
  - 奮 "rouse…" and 鼓 "drum; rouse" are not excluded in either direction.
  - 奔走 is close to せっせと and 苦心.
  - 奮う is close to 勇気.
  - 奉仕 may overlap 勤め "religious service" (JMdict 奉仕 sense 1 includes "ministry; church work").

**Limits**
- I did not open Kanjipedia, weblio Daijisen, KANJIDIC2, JMdict beyond the packet, or any link target (県, 市, サービス, 走る, 后, 献 and others).
- I did not check JLPT tags, device rendering or native usage.
- I did not read the full text of 婦.md, so whether it documents the ぷ in にんぷ is unverified.
- Quiz generation behaviour is unknown.
- Kanjipedia-only readings (奴 ヌ, 奉 うけたまわ.る, 如 し.く/ゆ.く/も.し, 奈 いかん.ぞ/なん.ぞ) are omitted from the cards. I treated that as acceptable because the metadata follows KANJIDIC2.
- All other kanji reading rows, grade, stroke and radical values, the kana readings in the examples, and the JMdict glosses cited in the cards matched `sources.json`, `primary.xml` and the families files.
