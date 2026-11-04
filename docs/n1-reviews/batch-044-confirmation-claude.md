The confirmation is done: the revision fixes my original finding, and no consequential regression remains in the changed passage. All three verdicts for `words/亥.md` are now CLEAN.

```text
Snapshot:
- Initial df413408aa3ef0edd09fbc0dd47756594bd79709; revised d99792c48abc5de957c3834c4d627a2be39f486d, said to be normally signed; no uncommitted teaching.
- The commits, the signature, the clean working tree, the regenerated manifest and the claim that nothing else changed are all taken from the task. I had no shell, so I could not check any of them.

Scope:
- Claude Opus 5.5 (claude-opus-5.5), the same session as my initial review; read-only; a bounded confirmation, not a new blind review.
- Reads:
  - My own preserved report, docs/n1-reviews/batch-044-initial-claude.md, in full. It matches the report I returned.
  - The current words/亥.md and words/猪.md in full.
  - docs/content-format.md lines 128-148.
  - The supplied artifacts batch-044-idoshi.html (1810-1855) and batch-044-kanjipedia-i-word.html (45-99).
  - batch-044-jmdict.xml lines 260-295, which include the complete 2845246 and 2853749 entries.
  - Two fresh lookups on the dictionary site; both failed (see Limits).
- I did not reread kanji/亥.md, the metadata or the comparison cards. My claim that they are unchanged rests on the supplied diff.
- The current words/亥.md matches the supplied diff exactly: line 8 now reads `quiz_exclusions: [猪]`, and three new lines (38-40) follow the Daijisen sentence on line 37.

Verdicts (words/亥.md as changed):
- Correctness: CLEAN.
- Scoped coverage: CLEAN (was NEEDS FIX).
- Comprehensibility: CLEAN.
- No consequential regression remains in the changed passage.

Findings:
1. Original finding, sign named by its animal (いのしし年): resolved.
   - Lines 38-40 say the year can also be called いのしし年 and that zodiac expressions can name a sign by its associated animal. They keep the boundary that い is not a general word for a living wild boar.
   - Each part is supported:
     - Daijisen 亥年 (い‐どし〔ゐ‐〕) ends "その年に生まれた人。いのしし年。"
     - Kanjipedia い sense ① reads "十二支の一二番目。イノシシ。"
     - JMdict 2853749 gives 亥の年 the readings いのとし and いのししのとし, cross-referenced to 亥年.
   - These support recognising the animal as a name for the sign. They do not support swapping the sign noun and the live-animal noun freely, and the note does not claim that. The 猪 article still teaches the live wild boar.
   - The selected reading い, the title, the raw kun metadata and the quiz curation are unchanged according to the diff. No いのしし kun reading was added to 亥.
2. Original quiz-guard suggestion (medium confidence): resolved.
   - 亥 now excludes 猪. The displayed labels are "Boar zodiac sign" and "wild boar". Given いのしし年, a learner shown "Boar zodiac sign" in an English-to-Japanese question could reasonably accept 猪, so the guard is justified under content-format.md.
   - The guard only stops the two words appearing together in one question. It does not make them synonyms or change 猪's identity.
   - content-format.md says one declaration covers both directions. words/猪.md is unchanged (`[動物]`), and that is sufficient.
   - Exclusions do not chain, so 猪/動物 does not extend to 亥/動物. No 豚 guard is added. JMdict's "the Pig" for 亥 is only an English label for the sign, so I agree that none is needed.

Optional:
- New, not a defect: the kana reading いのししどし in line 38 has no source in the evidence I read.
  - Daijisen writes いのしし年 without kana. JMdict 2853749 gives いのししのとし, not いのししどし.
  - The voiced どし follows the same compound pattern as Daijisen's い‐どし, so I see it as plausible and low-impact.
  - Possible polish: cite a source for the reading, or show only the spelling いのしし年.
- Still optional, unchanged: showing 亥の日 (いのひ, JMdict 2845246), and the "Likewise" wording on line 50. Neither is a defect.

Limits:
- Process breach: I made one parallel batch of five read-only views (words/猪.md, content-format.md 128-148, the idoshi and Kanjipedia artifacts, and jmdict 260-295). That broke the one-tool-per-response rule. All five returned their full assigned ranges without truncation; every other call was serial.
- Both fresh lookups failed. https://www.weblio.jp/content/いのしし年 and https://www.weblio.jp/content/いのししどし returned only the site header, with no dictionary entry. I could not independently verify the いのししどし reading.
- All other dictionary evidence comes from the supplied artifacts and frozen JMdict, not fresh retrieval from the original sites.
- Quiz reasoning rests on the documentation in content-format.md, not the app's code.
- Text-only review: no native, viewport, Android, phone or publication checks, and no fresh check of the whole source set.
```
