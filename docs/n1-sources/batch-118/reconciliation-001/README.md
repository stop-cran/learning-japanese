# B118 reconciliation 001

The comparison records in `kanjidic2-records.xml` were streamed from the
pinned KANJIDIC2 input identified in `source-extraction.json`. The complete
parsed records are reserialized, not original byte slices. The extraction
receipt also identifies exact comparison-card blobs at candidate
`dc2ee12623b36eb059d147ece2f2cfa3f87dfad7`; use those cards for the
displayed titles and teaching, not as independent dictionary evidence.
Existing B118 source and selection receipts remain unchanged.

The accepted direct separation guards are 析/別 and 析/離: 析's
KANJIDIC2 record gives "divide" and its separately captured Digital
Daijisen entry gives こまかく分かつ; 別 and 離 display "separate".
The existing seven guards remain. 刻 is also guarded directly because
KANJIDIC2 gives both 析 and 刻 "chop", and 刻's card teaches chopping
finely. This is not a blanket rule for the cutting family. 盤, like 板,
is guarded as a precaution because its displayed title includes "board"
and a separate historical-terminology entry defines へぎ as a thin split
board. The historical noun does not establish a general modern board sense.
None of these guards asserts that the characters' words are interchangeable.

The Weblio response and complete source-specific slices are preserved in
the B118 external evidence handoff, including the Digital Daijisen and
historical-terminology sections, with offsets and SHA-256 hashes. The
pair-by-pair dispositions and responses are in the reconciliation handoff;
they are bounded judgments, not a whole-corpus safety certification.
