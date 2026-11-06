Snapshot: f5b70805d4a4a99d27036c71701277f1b8fc8b00, as supplied. I made no changes. I had no shell, so I couldn't confirm the HEAD commit or that the working tree was clean.

Scope: Claude Opus 5.5 (claude-opus-5.5), one tool call at a time. I read every assigned range in full:
- **Cards and articles:** 典 1-70, 具/曲/共, 文/型/古/辞/百/科/事/香, 香典, 典型, 古典, 百科事典, 辞典, 贈り物, プレゼント, 寄付, お祝い and お見舞い.
- **Sources:** the review JMdict XML 1-3456 (every family, including the 典 のり entry 1438050, 香奠 rare-form flag, 百科辞典 and 事典 ことてん), KANJIDIC2 1-977 (12 records), 典.json and the KanjiVG SVG.
- **Guidance:** copilot-instructions 1-259, content-structure 1-85, content-format 71-177, jlpt-levels 1-23.
- **Extra searches:** line-number checks, `^title:` in `words` and `kanji`, and confusable-words.md.
- **Public sources:** Kotobank 典 (Daijisen; Nikkoku Seisen); Kotobank 香典 (Nikkoku, Nipponica, and the Daijisen body from raw HTML at offset 65000, heading こう‐でん【香典／香×奠】, which defines it as 金品, money or goods).

Verdicts (correctness / coverage / comprehensibility):
- **New 典:** CLEAN / CLEAN / CLEAN.
  - Readings テン, デン, ふみ, のり are in the source order, each has its own row, and quizOnyomi is [テン, デン] with quizKunyomi [].
  - 8 strokes, radical 八 no. 12, grade 4 and N1 match the sources.
  - The mnemonic is labelled as a mnemonic and makes no origin or phonetic claim.
  - Distractors 具/曲/共 don't share any of 典's meanings.
- **New 香典:** CLEAN / CLEAN / CLEAN.
  - The meaning ("usually money" but goods allowed), the readings コウ+デン, the rare-spelling note for 香奠 and the examples are correct.
  - It has no JLPT level.
  - The exclusions 贈り物/プレゼント/寄付 are justified.
  - Leaving お祝い/お見舞い unexcluded is not a defect: they are for happy occasions and illness or misfortune, not funerals.
- **Changed word links**, each CLEAN/CLEAN/CLEAN: 典型:24, 古典:31, 百科事典:29, 辞典:23.
- **Older-kanji links**, each CLEAN/CLEAN/CLEAN: 古:38, 辞:37, 百:22, 科:41, 事:36, 香:42. All line numbers matched.
- **Reciprocal links:** all 12 pairs (24 directions) are present. Word levels N3/N2/N2/N4 are preserved.

Findings: none.

Optional:
1. 典.md:57-59 says "辞典 explains words; 事典 is an encyclopedia". That holds for the standalone words, but in longer titles the spellings vary. JMdict lists 人名辞典 and 人名事典 (1369360) and 用語辞典 and 用語事典 (2841750) as one word each, and 地名辞典 means "gazetteer" (1942370). Adding "usually" would cover this.
2. 典.md:44 says "dictionaries" list 典 read のり. Only JMdict 1438050 shows 典 as a spelling of のり; Daijisen just uses のり to define the word.
3. 香典 could mention 香典返し (JMdict 1820700).

Limits:
- **Wider quiz pools:** large, random or live pools are unverified. Kanji whose titles also mean ceremony or rule (式, 儀, 則, 規, 法) could appear as fallback choices, in either direction. Word titles like 葬式 "funeral" and 土産 "gift brought on a visit" carry the same unverified risk.
- **Not checked by me:** the 事 line-ending changes, 字通 (no definition text came back), whether the bundled fonts have the glyphs 奠/亅/厂/艹, and actual rendering, drawing recognition, native-speaker acceptance and physical-phone acceptance. Compatible Android f9b59a2 or later is needed for the curated reading quiz.
