**Snapshot:** 159207693284b0451beeb95e8b59dad2e6b5e28f, confirming my residues from e9b5df6bd6c6c9fed4cce91d5ac4c481d208007c. I could not check commit hashes from the packet. This is not a fresh whole-deck, native or device review.

**Scope:** I read these four files once each, one view call per turn.
- `final-diff-1.txt`: hunks for words/回忌, words/弓 and words/弥縫策 only.
- `final-revision-1.txt`: full text of those three cards.
- `final-evidence-diff.txt`: it adds JMdict entry 1002030 (お辞儀) to the pinned extract and selection list.
- `final-evidence.txt`: author dispositions.

I compared these against my earlier notes on the same packet (JMdict extract, quiz and labels). I did not re-read the unchanged cards. I rely on the diff showing no other card changed, which is an author-supplied claim. `[S]` marks a source fact in the packet. `[A]` marks an author statement I cannot verify.

**Residue dispositions**

| Residue | Status | Basis |
|---|---|---|
| R1: word 弓 did not exclude word 礼 ("thanks; bow") | **Resolved** | `quiz_exclusions: [お辞儀, 礼]`. The note says both "can also be glossed 'bow' but mean bowing the head". `[S]` お辞儀 1002030 is glossed "bow; bowing". The 礼 gloss rests on the words/礼.md title `[A]`, which matches what I saw earlier. |
| R2: 回忌 Dictionary line missed the numbered-form entries | **Resolved** | The line now lists 1161330, 1814080 and 1319250. `[S]` These are 一回忌 "first anniversary, usu. 一周忌", 三回忌 "second anniversary" and 七回忌 "sixth anniversary". The citation now matches what the text says "JMdict glosses". |
| Cosmetic: stray space in the 弥縫策 example 1 reading | **Resolved** | ただの is dropped. The reading is now contiguous: ねあげをさきにのばすのは、びほうさくにすぎない。 |
| Optional: cite 1214130 and 1769460 on 弦楽 | **Still optional** | Not changed, and no defect. |

**Regression check on the changed passages (none found)**
- **回忌 rule:** "三回忌 is two years after the death… from 三回忌 on the number is the years since the death plus one" holds for 三回忌 (2+1) and 七回忌 (6+1). It agrees with both examples ("second", "sixth"). The "usually 一周忌 / 一回忌 recorded" wording matches the JMdict usage note. "One year after the death" is a plain restatement of "first anniversary". The Daijisen 満1年目 quote behind it is `[A]`.
- **弥縫策 example 1:** "…のは、弥縫策にすぎない" is grammatical. The reading is correct. The translation "nothing more than" is carried by にすぎない, so dropping ただの loses no meaning.
- **弓 note:** "For traditional Japanese archery, use 弓道 (きゅうどう)" is accurate. It is more precise than the earlier "usual word", and it does not contradict the Meaning line, which keeps the JMdict "archery" sense. The 弓 front matter is consistent with the new exclusion.

**Remaining actionable issues:** None in my facet. Correctness and scoped coverage are CLEAN for the three changed cards.

**Optional, low confidence**
- **Duplicated rule:** The 回忌 counting rule now appears twice, in "How the kanji combine" and "Distinctive meaning". You could keep one.
- **Missing citation:** The 弓 Dictionary line cites only 1228490. The お辞儀 contrast cites no entry, and 弓道 (1228540) is cited only on the kanji card. You could mirror the 回忌 treatment and add 1002030 and 1228540. The author says 1002030 is "cited by the note", but the card shows no id.
- **Quiz wording:** "The quiz keeps 弓 apart from…" describes quiz mechanics rather than meaning. A direct contrast, as in the kanji 弓 note, would read more naturally. I do not know the project's convention, so this is not a defect.
- **Earlier optionals:** The 表彰 active example, 色彩 and 弔問 exclusions, 法廷 polish, Kanjipedia-only 弥 readings and the 弥 ビ exception are unchanged and still for the adjudicator.

**Limits**
- The pinned お辞儀 entry cannot be diffed against live JMdict. No 礼 entry is in the extract.
- Exclusion symmetry, the Daijisen and Kotobank quotes and KanjiVG remain author claims.
- Mechanical checks are author-reported (validate 0 errors, quiz_safety 0/0, 100 families). I cannot interpret the "6 latent" reading-exposure figure, so it is outside this confirmation.
