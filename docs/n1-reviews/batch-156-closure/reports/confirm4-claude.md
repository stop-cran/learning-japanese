Snapshot: commit ba44b2809e6f46a6532ad58a016cb9d639ad2afc; reviewer model: Claude (Anthropic), running as a GitHub Copilot sub-agent. The exact model version string is not visible to me.

Scope:
- This packet: INSTRUCTIONS.md, CHANGES.md and RESPONSE.md in full; diffs\fix.patch in full; snapshot\kanji\乙.md in full; snapshot\kanji\伯.md lines 20-45; checks\link-targets.tsv in full.
- Evidence read in full: evidence\README.md, selection-evidence.md, candidates.md, link-scan.txt, kanjipedia-乙.txt, and weblio-乙.txt, weblio-乙種.txt, weblio-乙種合格.txt and weblio-種.txt.
- Evidence read in part:
  - evidence\jmdict-cited-entries.xml: grep of every keb, reb, pri, misc, restr, xref and gloss line for all 21 entries.
  - evidence\joyo\*.txt: grep for 乙, 仙, 伯, おじ, おば, 付表 and おとめ across p3, p19, p94, p97, p126 and p162.
  - evidence\word-quiz.txt: lines 1-90, lines 2540-2600 and the last lines.
- Compared with the earlier confirmation packet (confirm3-156-claude):
  - checks\quiz-safety.txt, reading-exposure.txt and reading-options.txt: sha256 of both copies, then a line diff of the two files that differ.
  - evidence\word-quiz.txt: a line diff, with every changed line that does not contain 甲乙 or 乙種 listed.
- Original packet: evidence\kanjipedia-senses.txt lines 18-50.
- Web: the live Weblio/Digital Daijisen page for 乙種. Online JMdictDB is password-gated, and a jisho.org fetch returned no entry text.
- Not reopened: evidence\QuizBuilder.kt. No kanji card's quiz metadata changed, and checks\quiz-safety.txt is byte-identical to the copy I reviewed last round.

Dispositions:
- P1 - RESOLVED - checks\quiz-safety.txt has the same sha256 in both packets (7F50B517E13E286C…). checks\reading-exposure.txt and checks\reading-options.txt each differ from the earlier copies on line 1 only, the "Command (at …)" line, which now names fix-otsushu ba44b280 instead of a7cc61e2. The arguments on that line are identical. CHANGES.md now describes all three files correctly.
- A1 - RESOLVED - The patch changes only 乙.md lines 23, 31 and 38, adds words\乙種.md (41 lines) and deletes words\甲乙.md, as CHANGES.md says. Every fact in A1 checks out against the evidence:
  - 甲乙 carries news2 and spec2 only, and 甲 has no card.
  - 早乙女 (news1) is an appendix whole-word reading (p.162; p.97 under 早; p.3 note 13), and Daijisen lists it under 乙's ［難読］.
  - 乙女 (2855480) is untagged and is also an appendix word.
  - The 乙/おと collision through 2837087 is real: that entry has keb 乙 with reb おと.
  - 乙種 (1862630) has no tag and no mark, and its only reading おつしゅ uses オツ.
  - 乙種 is the first Joyo example for 乙 (p.19), Daijisen's example for 〈オツ〉 sense 2 "順位で、第二位", and Kanjipedia's example for meaning ②.

  The justification for using an untagged word is sound, and I would not choose another word. The new text is correct:
  - JMdict glosses: 1862630 "B-grade; second-class" with an xref to 甲乙丙; 1280150 "A-grade; first-class"; 1907280 "third grade; third class; C-grade"; 1280090 "A, B and C; first, second and third".
  - The Daijisen statements on 乙種 (第2種; sense 2 as an abbreviation of 乙種合格) and on 乙種合格 (the pass rank after 甲種 in the 徴兵検査) match the evidence and the live 乙種 page.
  - The two links resolve with titles that equal the quoted glosses: 丙 "third rank; class C" and 級 "class; rank; level".
  - Quiz options: the distractor 丙 is not excluded, and the four exclusions (位, 級, 段, 次ぐ) are real near-meaning words. The resulting options 丙, 一種 and 種類 are all clearly wrong for "B grade; second class". The reading look-alikes are not JMdict readings, and the audit reports 0 problems.
  - The link scan shows no link to 甲乙.md, plain or percent-encoded, and no exclusion list naming 甲乙.
- A2 - DECLINE ACCEPTED - The facts check out:
  - The only listed-tag candidate is 仙台 (spec1), whose only sense is "Sendai (city in Miyagi)".
  - 水仙 is marked "usually written using kana alone".
  - 仙人 is the second of the three examples in the Joyo table (p.94: 仙骨, 仙人, 酒仙) and Kanjipedia's example for ① (line 24).

  The rule says "the tags guide the choice", so a place name that shows none of 仙's meanings does not have to beat 仙人, which shows the main meaning. 仙人 has no mark and uses セン.
- A3 - DECLINE ACCEPTED - The facts check out:
  - 伯父 and 伯母 carry tags only on おじ/おば, the appendix readings (p.162; p.126). はくふ and はくぼ are restricted to those spellings and untagged.
  - 伯爵 needs 爵, which has no card.
  - 伯楽 carries a "sensitive" mark, and えおじ is archaic.
  - The Joyo table gives 伯仲 and then 画伯 (p.126).
  - Kanjipedia gives 画伯 for ④ and 伯兄, not 伯仲, for ②. RESPONSE does not claim otherwise.

  Neither 伯仲 nor 画伯 shows main meaning ①. The rule does not rank untagged candidates by transparency, and both meet the hard requirements. Keeping the table's first example, which already has an article, is defensible. 画伯 would also be acceptable (see Optional), but this is not grounds to reject.

Verdicts:
- Correctness: CLEAN
- Scoped coverage: CLEAN
- Consistency and quiz safety: CLEAN
- Comprehensibility: CLEAN

Confirmation: CONFIRMED

Findings: none

Optional:
1. A3: the RESPONSE does not mention the JMdict nf ranks. They slightly favour 画伯, which is nf26, over 伯仲, which is nf31; the tags are not frequency evidence. 画伯 also shows a 伯 meaning (④) directly. If the 伯 row is ever revisited, this is a reason to prefer 画伯. It does not require a change now.

Limits:
- I could not query live JMdict online: JMdictDB is password-gated, and jisho.org returned no entry text. JMdict facts rest on the pinned extract evidence\jmdict-cited-entries.xml.
- I did not open the official Joyo PDF. The Joyo lines are from the pdfplumber extracts.
- I did not check live Kanjipedia or live Daijisen pages other than 乙種. evidence\kanjipedia-乙.txt is dated 2026-11-22, which is consistent with JST at review time.
- The completeness of candidates.md (every tagged JMdict form containing 乙, 仙 or 伯) depends on the author's script and was not independently re-derived, because corpus scans are not allowed.
- I did not re-read QuizBuilder.kt, since no card's quiz metadata changed, and no JVM tests were run.
- RESPONSE's line reference for 仙 card line 23 was not opened.
- Every response made exactly one tool call; there were no parallel calls, helper files or sub-agents. Two calls ran a single pipeline (Compare-Object over two Get-Content reads, and Get-FileHash over six paths). I treated each as one command.
