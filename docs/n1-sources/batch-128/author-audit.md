# B128 author audit: 唇

Base: `bd0f4b842c588e581ccb31ad946eecedb63d32b8`.
Status: local authoring candidate; independent review and publication pending.
This is not a review-closed batch or native/device acceptance.

## Selection and exact changes

Frozen pending row **159**, 唇, was genuinely absent as a card and stroke
file. The admission checks found a clean detached HEAD, the expected origin,
and freshly fetched `origin/main` equal to the base. The one-on/no-kun survey
returned only the already-deferred 伯 (33), 憶 (395), 撲 (461); none was
reclassified as safe or delivered. The earlier packet had identified 唇 as
a possible future candidate, not an accepted member.

The slice adds `kanji/唇.md`, generated `strokes/唇.json`, and exactly one
wrapper in `words/唇.md` at its component introduction. It also removes
exactly the now-false sentence saying no 唇 card exists, using the existing
linkplan `--remarks` interface. All other word prose, identity, primary
reading, N2 level, tags and metadata are byte-preserved after LF normalization.
There is no new word, app/media change, prior-evidence rewrite or easier-deck
rewrite. The manifest is regenerated, not hand-edited.

The all-word metadata scan and frozen candidate inventory both give the
single required pair **唇 / words/唇.md**. The card links to that article and
the article links back. The two incidental occurrences are enumerated in
`support-audit.json`, not silently counted as required support. No arbitrary
constituent reading is assigned to whole-word readings.

## Complete source and reading inspection

`source-receipt.json` binds the frozen community/index bytes, compressed and
decompressed dictionary hashes, exact output hashes and the pinned SVG blob.
`complete-source-verification.json` compares every retained complete record
against its original canonical record. The selected XML is parsed and
reserialized, **not a raw compressed-file slice**. All spellings, priorities,
reading/spelling restrictions, senses, fields, cross-references and flags
remain in the complete XML. Missing priority flags are not rarity evidence.

The 79-record primary selection includes every family containing 唇 or 脣,
plus exact comparison queries; another 24 complete comparison records cover
the finite mouth/side/edge/sound/fear/bloom comparisons. The full primary
inspection and the complete 24-record readback were read. Particular boundaries:

- 1359940 supplies 唇/くちびる, lip/lips, and marks only 脣 as a rare spelling.
- 1276410 supplies 口唇/こうしん, anatomical lips, and separately flags
  口唇/くちびる as a whole-word gikun/jukujikun. This does not allocate
  arbitrary fragments of くちびる to either character.
- 1576940 includes したくちびる and かしん for 下唇. 1580410 includes
  うわくちびる and restricts じょうしん to 上唇; its zoological labrum
  sense is restricted to that latter reading.
- 1359950 is the linguistic labial-consonant family, not a generic sound
  definition of the body part. 2871069 marks 花唇 poetic and 花脣 search-only;
  that whole-compound evidence is distinguished from the independently
  positive standalone poetic-petal sense in the monolingual sources.
- Technical medical, anatomical, botanical and phonetic compounds retain
  all fields. Sensitive/dated medical terms, slang/vulgar fields, whole
  idioms/proverbs and mutual-dependence compounds do not become unqualified
  character meanings or new learner examples.
- 1236690 restricts the surprising/startling 恐ろしい sense to that spelling.
  1593480 instead gives scary/frightening; these are not silently conflated.
- 2842190 gives ほとり with side/edge/bank/shore senses and precise rare,
  search-only and irregular-okurigana flags by spelling. It is not proof
  of ordinary modern 唇=ほとり.

Frozen on/kun metadata remains exactly **[シン] / [くちびる]**, in source
order. There are no nanori in this record. Practice selects only くちびる
with its existing linked word. シン is verified via 口唇/こうしん but is
not selected without a linked compound article; that is not a rarity judgment.

Complete local Kotobank HTML contains the Daijisen, Nikkoku and Jitsu
entries omitted by the simplified fetch output. Both native-word dictionaries
positively record the poetic petal branch. Nikkoku separately has the noun
しん for a lip or labial consonant and tentatively suggests an old くちひる
form. Jitsu's 字訓/訓義 positively gives おどろく; its old-dictionary
ホトリ quotation belongs to **脣**, not an unqualified ordinary 唇 reading.
Kanjipedia has lips in its meaning field and mouth-trembling in a historical
account. The card uses an explicitly non-etymological shape mnemonic rather
than adopting competing historical reconstructions.

`external-source-bindings.json` preserves exact local full-page hashes,
headings, bounded attributable excerpts, source discrepancies, the two
failed guessed-URL lookups and all reading dispositions. Complete external
pages remain local, not wholesale published. Search summaries were not used
to establish dictionary agreement or an unrestricted rim meaning.

## Actual baseline scan and both quiz directions

`baseline-gloss-scan.json` contains the actual scan of **all 1,247 baseline
cards**, their titles, complete KANJIDIC2 English meanings and exact matching
tokens. The second actual scan expands it for positive secondary-source
senses and polysemy, including sound/voice, side/shore and margin. It has
**42 matches**. Both outputs are retained; `pair-dispositions.json` is the
separate finite disposition table, not a substitute for scan evidence.

All **45** comparison cards (42 scan matches and three curated choices)
were read as actual baseline cards. Complete character records are retained
in the initial and expanded comparison XML. Every scan pair has explicit
new-prompt/other-label and other-prompt/new-label reasoning.

Fourteen direct guards are declared on the new card:
口・花・震・動・恐・怖・側・辺・際・境・界・岸・畔・音.
Several are deliberately conservative broad-choice guards for unresolved
secondary or historical-variant branches, **not assertions of universal
synonymy**. For example, a petal is not an entire flower, surprise need not
be fear, the historical ホトリ quote does not make everyday 唇 mean
every shore, and a labial sound is not the anatomy that produces it.
Each pair is considered directly, not inherited through earlier exclusions.

Rejected overlaps include blade/cutting edge versus generic side, margin as
a numerical difference, financial bank versus shore, grammatical voice,
counting flowers versus being a petal, blooming versus a petal as a part,
and speaking versus the anatomy or a consonant class. Full comparison
meanings and actual displayed labels, not just titles or shared themes,
determine these dispositions. Unrestricted substitutions are not claimed.

Curated **古 / 右 / 石** have age, rightward-direction and stone labels.
Both label directions and their mutual compatibility were checked. The
historical side gloss does not establish a rightward direction, and a shared
lower box is not a shared meaning. Starter-compatible choices would reduce
some pool dependencies, but 石 is not Starter-tagged; the actual Starter
fallback was checked rather than assumed safe.

## Mechanical evidence and limits

All ten author gates passed in `author-gates-002`: lint, quiz-safety,
linkplan, reading-exposure, validate, manifest, unittest, budget, vocabulary
and manifest-rebuild. Final scoped lint and quiz-safety have zero errors
and zero warnings; 431 host tests passed. Vocabulary remains
**2,122/2,431 reviewed prompts, pilot**, not whole-set closure.

The bounded reading model explicitly supplies おどろく, ほとり, tentative
くちひる, semantic-paraphrase ふるえる and separate-noun しん. The last
two are not promoted to extra frozen readings. Some supplied forms collapse
under the model's existing script/voicing equivalence; the log states the
remaining unlisted keys. There are **zero N1/All production hits, zero
restricted Starter hits and two latent hypothetical-pool collisions**
(ほとり via 辺 and ふるえる via 震). The Starter pool has one open
fallback slot, explicitly analyzed; 100 seeds per named pool were sampled.
This is not arbitrary/custom-pool, multiple-borrow, Kotlin/native/device,
old-APK or whole-set acceptance.

The first author gate attempt failed linkplan because its invocation omitted
the existing exact stale-remark allowance. It also retained one quiz-safety
warning for 口 not repeated in Notes. The original runner, receipts, logs,
failure disposition and subsequent fix remain preserved; no validator was
weakened. The card now repeats the already-justified 口 comparison in Notes.

The pinned converter generated ten strokes from the verified pinned SVG.
Geometry was not edited. All three actual bundled cmaps cover 唇, radical
口, mnemonic 辰 and the curated choices. They all lack **脣 U+8123**,
which remains a variant-recognition/fallback limitation. Cmap evidence is
not actual glyph rendering, native interaction, drawing recognition or phone
acceptance. No app or font files were changed.

Live resource admission requires more than 2 GiB free, with the pinned guard
sampled every 0.25 seconds and interruption below 1 GiB. Child waits are at
most 0.1 seconds; terminate/kill cleanup has bounded deadlines. Gate commands
are serial, and no unrelated process was stopped. Memory receipts describe
the Python process's peak, not unmeasured child peaks.

Baseline preservation binds every candidate manifest-mapped runtime hash,
all unchanged entries and the exact allowed word edit. Runtime text hashes
normalize CRLF to LF; raw source/report hashes do not. Archive entry counts
include directories and packaging files, so they are not manifest-map counts.
The final committed checks/signature/cleanliness will be bound in the scratch
handoff, not falsely embedded as a self-referential committed SHA.

Published accounting remains **257 delivered / 971 undelivered**. This one
local draft is not delivered; 970 other undelivered members remain outside
it. Independent review, reconciliation and any publication belong to the
coordinator. No push or reviewer launch was performed.
