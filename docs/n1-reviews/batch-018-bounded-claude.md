The supplied offset settles it: Digital Daijisen does have a character entry for 繭, and it lists 繭糸 under ケン. The card's wording is accurate, so my original Daijisen points are withdrawn and all verdicts stay CLEAN.

**Snapshot:** signed commit `39810853a39c033015ec11b9a317484e239eb41e`, unchanged, with no teaching diff, as stated in the task. I did not independently confirm the commit because no shell was available. No uncommitted changes are included.

**Scope:** Claude Opus 5.5, same reviewer and session as the original. This is a dependent confirmation, not a new blind review. I made two serial calls:
- I read my original report, `docs\n1-reviews\batch-018-initial-claude.md`.
- I fetched `https://kotobank.jp/word/%E7%B9%AD-137237` as raw HTML at start_index 64000, max_length 8000.

I did not re-read `kanji\繭.md`; the report already quotes the relevant claim. Everything else is carried forward from the original reads: both teaching files, the metadata, all 44 dictionary families, the comparison kanji and words, the confusable-words search and both earlier Kotobank fetches.

**Source check:** the Digital Daijisen section has the heading **けん【繭】［漢字項目］**. It gives ［常用漢字］, ［音］**ケン**（呉）（漢） and ［訓］**まゆ**. Its two numbered senses read:
- **Sense 1:** 〈ケン〉カイコなどのまゆ。「繭糸／蚕繭・生繭」
- **Sense 2:** 〈まゆ〉「繭玉／初繭・山繭」

The sense numbers are gaiji images (02531, 02532), but the 〈ケン〉 and 〈まゆ〉 labels are plain text. So the card's sentence "Digital Daijisen explicitly gives 繭糸 as an example" for ケン is supported. The entry lists no きぬ reading, which fits the card keeping きぬ as KANJIDIC2-only lookup information. Separately, the けん‐し【繭糸】 headword ("繭からとった糸") supports the card's gloss "thread from cocoons".

**What changes from the original report:**
- **Daijisen attribution (Optional):** withdrawn. The current wording is accurate.
- **"These pages show no Daijisen character entry" (Limits):** withdrawn. My original simplified page extraction left out this entry; it was a tool-access gap, not missing evidence.
- **Adding Daijisen's "cocoons and thread" definition of 繭糸 (Optional):** withdrawn. The card uses 繭糸 only as a recognition example, and its gloss is supported. A second specialist definition doesn't help the goal of recognising the standalone word for cocoon.
- **Citing 字通's 会意 analysis (Optional):** withdrawn. Character history is outside the bounded goal. The card's clearly labelled mnemonic and `structure-unclassified` tag are acceptable as they stand.

**Verdicts** (carried forward from the original reads; the only new evidence is the Daijisen character entry):
- `kanji\繭.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\繭.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:** None.

**Optional:** None.

**Limits:**
- **Process:** my original review broke the one-call rule once by reading the two teaching files in a single parallel call. That stays on record and is not made compliant by this confirmation. This confirmation used two serial calls.
- **Sources:** the sense-number images in the Daijisen entry, the 字通 and 日本国語大辞典 images, and the Britannica and Mypedia bodies remain unread. The dictionary packets are frozen copies, not fresh lookups. Pitch accent was not checked, and `confusable-words.md` was only partly searched.
- **Device testing:** this was a text-only review. Fresh Android, combined-main, CI and public ZIP checks, plus physical-phone and general-release acceptance, are still outstanding.
