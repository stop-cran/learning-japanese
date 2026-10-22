**Snapshot:** The corrected commit is 11de9d80c015ed96c5dfa335f909bf605008aeba and the original is 7eedeb1589aedfbf26e84aa3d7a700b5930ebec8 (baseline eece75b4b18bec3bcc6a058670e73947555948d4). I reviewed committed files only. I had file tools but could not run Git, so I could not confirm that the files on disk match that commit, the clean worktree, or the six- and 25-file scopes. I relied on the corrected-snapshot JSON and the supplied patch.

**Scope:** One reviewer, claude-opus-5.5 (Claude family), working read-only and alone. I read:
- my original report;
- the one-file fix patch, which deletes a clause at kanji\黄.md:44;
- all of kanji\黄.md;
- words\黄色.md and words\黄色い.md;
- the 黄 KANJIDIC2 metadata and source row in batch-25.json (lines 60–80 and 159–175), plus the complete record for JMdict 1576760 (lines 1250–1318).

I did not reopen the other four kanji cards, 年.md, the other five correction-scope files, or the stroke files.

**Verdicts:**

| 黄 | Verdict |
|---|---|
| Correctness | CLEAN |
| Scoped coverage | CLEAN |
| Comprehensibility | CLEAN |

- **Correctness:** front matter still matches KANJIDIC2: 11 strokes, radical 黃 no. 201, grade 2, コウ/オウ and き/こ-. The seven JMdict entry IDs match the source row. The remaining sentence "The linked noun article teaches きいろ" is accurate: words\黄色.md has `reading: きいろ` and says "including both adjacent い sounds".
- **Scoped coverage:** all four reading rows still have examples (黄葉 こうよう, 硫黄 いおう, 黄 き, 黄金 こがね). Dropping the clause removes no required content. JMdict 1576760 lists こうしょく and おうしょく without restrictions, but the card never has to name them.
- **Comprehensibility:** the unclear instruction is gone, and the note no longer refers to readings it doesn't name.
- **Unchanged items:** distractors [横, 共, 昔], the links to the word articles, and the mnemonic label are as before. The word articles' links back to the 黄 card are intact.

**Findings:**
- **B25-1: resolved.** I offered deleting the clause as an alternative remedy, and that is what the author did. No unsupported frequency or register claim about こうしょく or おうしょく was added. Confidence: high.
- **No regressions found.** The patch only removes that clause: no new example, reading row, metadata or historical claim.
- **Other cards and author claims:** I found no defects on the other four cards originally and did not reopen them. I could not independently confirm the author's claims that the 22 pairs, 13 reading rows, the 齢 とし note, the strokes, the 年 change and the seven link edits are unchanged. The only support I saw is the corrected-snapshot JSON, which shows 22 pairs, 22 records, 21 entry families, 13 reading rows, 12 lexical rows and 齢 とし as source-only, plus the 黄 links in the two word articles I read.

**Optional:** My earlier optional suggestions were not adopted. They stay optional and are not blockers:
- 黄金 おうごん as the オウ example;
- 黄身 or 黄砂 as more everyday examples;
- rewording 麦.md:42;
- the notes on 齢 よわい and Jitsū (字通).

A small polish, also optional: the remaining sentence at 黄.md:44 repeats the きいろ already shown in Common words.

**Limits:**
- I reviewed only the changed passage in its card context, not the full batch again.
- I did not run Git, the validator, the source audit or the manifest builds. Those results are the author's.
- I did not review stroke paths or test the quiz at runtime, and I re-checked no public sources in this pass.
- I carried over, without re-checking, my original unverified point about the register of 齢 よわい. It lies outside this 黄-only scope.
- This is not native-speaker certification.
