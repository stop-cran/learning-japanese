# Onomatopoeia collection

Phase 1 of [app issue #45](https://github.com/stop-cran/kanji-cards-android/issues/45) is a
content-only thematic selection of 100 word cards and four linked learner guides.
The second content batch expands the collection to **200 tagged cards** and seven guides:
97 new cards plus the enriched existing さっぱり, がっかり, and びっくり cards.
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

The source records enumerate the exact selected forms and inspected dictionary identities:

- [Sensory words](onomatopoeia-sensory-sources.json)
- [Movement, sound, and feeling words](onomatopoeia-feelings-sources.json)
- [Second 100: everyday scenes](onomatopoeia-batch2-sources.json)

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
The second batch also inspects the teacher's entries for
[うきうき](https://mainichi-nonbiri.com/onomatopoeia/ukiuki/) and
[しんみり](https://mainichi-nonbiri.com/onomatopoeia/shinmiri/), whose broad mimetic labels
are editorial classifications rather than inferred JLPT levels.

The second selection uses 100 distinct primary dictionary entries and has no overlap with the starter's IDs.
It preserves reading-restricted senses: the additional ひよひよ movement, ぼたぼた wet-heavy/archaic,
and ぱしゃぱしゃ camera senses are not transferred to ぴよぴよ, ぽたぽた, or ばしゃばしゃ.
Same-sounding words such as ごくごく “extremely,” 続々 “one after another,” and 黙々 “silently”
are distinguished from the selected gulping, shivering, and billowing identities.
The prose and original examples do not claim native-speaker certification or measured frequency.

## Quiz and navigation

Each selected card links to the overview, which links back to all 200 cards. The focused
guides compare patterns, warmth/textures, rain/movement/similar-looking words, eating/drinking,
body sensations/feelings, and motion/voices/everyday sounds.
Confusable pairs are recorded in [the inventory](confusable-words.md).
`quiz_exclusions` protects known overlapping answer labels; it is not appropriate merely
because two forms look alike. Neither a different English gloss nor a generic picture
guarantees that only one choice is semantically defensible.

## Phase boundary

The original content phase was followed by the app's Onomatopoeia stack and a 20-image pilot;
their implementation and limitations are recorded in issue #45. The stack now includes tagged words
regardless of level, including the unlevelled new cards.

The second 100 are another **text-only content batch**. No app code, parser fields, binary assets,
image-generation calls, or scheduling rules change. The 20 existing images are neither expanded nor
re-reviewed here, and no physical-phone delivery or new image-quiz result is implied.
No new JLPT labels are assigned: the reused cards retain N3/N3/N4 respectively.
The exact snapshot and independent two-model review status are recorded in [REVIEW](../REVIEW.md).
