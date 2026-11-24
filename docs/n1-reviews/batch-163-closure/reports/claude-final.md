**Snapshot:** afad8a17 → 7d8e559e. This is a changed-passage confirmation covering only the 奈 hunks. It is not a second blind review.

**Inspected:** `last.diff`, `last-card.txt`, `last-families.xml` and `collocation-check.txt`. I did not reread the rest of the batch.

**Dispositions**
- **N1 (如何/奈何/いかん/いかが, 奈 Notes and Readings table): resolved.** I found no regression in the changed passages.
  - **Two shared readings of 如何:** The Notes say 如何 can be いかん or いかが. This matches JMdict 1582850 (如何 with いかん) and 2845606 (如何 with いかが).
  - **Rare spelling:** The Readings row and the Notes call 奈何 a rare spelling of the いかん word. This matches 1582850, where 奈何 carries "rarely used kanji form". The "belongs to the whole word" wording fits the jukujikun/gikun tag on both entries.
  - **Gloss:** "depending on how or what" matches sense 1 of 1582850. The table and Notes now give the same gloss, so the earlier inconsistency is gone. "How; how about" for いかが matches 2845606.
  - **Kana guidance:** "The second is usually written いかが" matches the "usually written using kana alone" tag on 2845606. The earlier false spelling-to-reading split is gone.
  - **Metadata:** Entries 1582850 and 2845606 were already cited.
- **F7 (奮う, 気力を奮って): resolved on the supplied excerpt only; non-blocking.**
  - The excerpt in `collocation-check.txt` is the fragment 気力を―・って under the heading ふる・う【奮う】. It supports the 気力を奮って collocation under the named headword. I checked this author-supplied text, not the website.
  - The author states that only the collocation is verified, not a whole Daijisen sentence. I make the same distinction. The fragment does not confirm any complete example sentence or the card's gloss wording.

**Optional (not blocking)**
- The gloss "depending on how or what" covers only the after-noun-+-の sense. The sentence-end sense ("what is…?") is omitted, which is acceptable for this scope. You could add "after a noun + の" if you want it precise.
- "The second is usually written いかが" could say "in kana" to avoid any reading as a kanji spelling.

**Limits**
- I did not open Daijisen, Kanjipedia, KANJIDIC2 or full JMdict, so the Daijisen result is not independently confirmed.
- The JMdict checks use only the supplied XML. The batch audit figures are the author's.
- I did no link, native or device checks.
