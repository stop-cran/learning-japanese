# Onomatopoeia starter collection

Phase 1 of [app issue #45](https://github.com/stop-cran/kanji-cards-android/issues/45) is a
content-only thematic selection of 100 word cards and four linked learner guides.
The learner-facing entry point is [Japanese onomatopoeia](../articles/japanese-onomatopoeia.md).

## Selection and identity

The set covers warmth, textures, cooking, weather, movement, voices, feelings, and several
non-repeated forms. It is a practical editorial selection, not an independently measured
top-100 frequency list, a comprehensive taxonomy, or an official JLPT list.

Existing cards are enriched in place. Their stable written-form IDs, dictionary identities,
and independently sourced JLPT labels are retained. Hiragana/katakana variants do not create
separate cards just for typography. No level is inferred for a new kana-only word.

`onomatopoeia` is the common tag. Broad `giongo`, `giseigo`, and `gitaigo` tags describe
applicable uses, not mutually exclusive parts of speech. More detailed treatments may separate
motion and feeling words into other classes. Form tags describe visible patterns, not
productive rules for inventing new meanings or attaching する to every word.

## Dictionary evidence and examples

The two source records enumerate the exact selected forms and inspected dictionary identities:

- [Sensory words](onomatopoeia-sensory-sources.json)
- [Movement, sound, and feeling words](onomatopoeia-feelings-sources.json)

They identify the inspected local JMdict snapshot by file hashes. Its upstream release date
has not been established; it is not asserted to be the same snapshot as the earlier
[N3 vocabulary work](n3-vocabulary-snapshot.json).
Dictionary-derived information is attributed and licensed as stated in [NOTICE](../NOTICE.md).
The source records and individual cards should be read together: an entry may contain
additional senses not taught by the starter card.

Examples are original teaching sentences selected for ordinary usage, with English translations
and kana support. They are not quotations or claims of attestation in a particular manga,
news report, recipe, or corpus. Dictionary recognition is not proof of relative frequency.
The guides additionally consult [Tofugu's introductory treatment](https://www.tofugu.com/japanese/japanese-onomatopoeia/)
for taxonomy and pattern terminology, while explicitly qualifying broad sound-symbolic tendencies.

## Quiz and navigation

Each selected card links to the overview, which links back to all 100 cards. The focused
guides compare patterns, warmth/textures, and rain/movement/similar-looking words.
Confusable pairs are recorded in [the inventory](confusable-words.md).
`quiz_exclusions` protects known overlapping answer labels; it is not appropriate merely
because two forms look alike. Neither a different English gloss nor a generic picture
guarantees that only one choice is semantically defensible.

## Phase boundary

No app code, parser fields, binary assets, image-generation calls, or scheduling rules change.
These are ordinary word cards. The current app has no dedicated onomatopoeia tag filter;
unlevelled kana-only cards may require the All word stack.

Later phases still need the reviewed design decisions in issue #45: a studyable section's
state ownership, image schema/storage/sync, raw-byte binary hashes, archive budgets, and
image-specific option eligibility. The proposed AI image-review pilot is not part of this
content delivery.
