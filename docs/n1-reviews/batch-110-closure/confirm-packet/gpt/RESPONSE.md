# Author's statement for the reviewer of `reports-110-gpt\initial-gpt.md`

This statement answers only the points in YOUR initial report. Your report numbers its findings 1 to 5; the author's
labels are: Finding 1 = **#1**; Finding 2 = **#2**; the two bullets of Finding 3 = **#3a** (嫌/怪) and **#3b** (素/料); the
two bullets of Finding 4 = **#4a** (応/募) and **#4b** (級/校); Finding 5 = **#5**. The two points of your Optional paragraph
are **OA** (the other cards: word inventories and boilerplate) and **OB** (the 激 cue). The first and second bullets under
Limits are **L1** (fallback reading options) and **L2** (no quiz implementation); the fourth bullet (Joyo) is **L3**; the
remaining Limits bullets (the third, fifth and sixth) are **L4**. The statement is the author's claim about what changed
and why. Verify each claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources;
do not rely on this text as evidence. Line numbers refer to the revised cards in this packet (and to
`snapshot\words\応援.md`). All 15 cards are in `snapshot\kanji\`, and all 15 changed, because every long paragraph was split
(see `CHANGES.md`). Give a disposition for each of #1, #2, #3a, #3b, #4a, #4b, #5, OA, OB and L1-L3; L4 needs none.

## Findings

### #1 (minor): 価 says it supplies both か of かかく

Author action: **changed.**

- `価.md:37`: "In 価格, 価 is read か and 格 supplies カク." The clause "so 価 is か in both syllables of かかく" is gone. The
  wording is not your suggested sentence, but it gives the same split as `snapshot\words\価格.md:25` in the original packet
  ("カ + カク gives かかく"), which is unchanged.

To verify: that the split is now stated correctly, and that nothing else in `価.md:37-41` misaligns a character and a reading.

### #2 (minor): 応援 still says neither character has a kanji card

Author action: **changed.**

- `snapshot\words\応援.md:32-33`: "オウ + エン. Both written characters belong in the word, though 援 does not have a kanji
  card here." The old clause was "even though neither currently has a kanji card here". These two lines are the only change
  to the article in this revision. 援 has no card (it is not in the original packet's `titles\kanji-titles.tsv`); 応 has
  one, and the link at `応援.md:30` goes to it.

To verify: that the sentence is now true and that no other line of `応援.md` contradicts it.

### #3 (minor): two direct pairs were not protected

Author action: **changed, once per pair, on one card only, no group made a clique.** `evidence\QuizBuilder.kt` treats an
exclusion as symmetric (`excluded(a, b)` is true if either card lists the other), so one declaration protects both
directions; the repository lists each pair once. The validator rule that an exclusion may not also be a distractor of the
same card passes.

| ID | Pair | Where the exclusion is listed | New explanatory text |
| --- | --- | --- | --- |
| #3a | 嫌/怪 | `嫌.md:14` `[憎, 疑, 怪]` | `嫌.md:58`: 憎 shares the KANJIDIC2 glosses "hate" and "detest"; 疑, "doubt; suspect," and 怪, "suspicious; uncanny," overlap the Daijisen sense of suspecting and the title word "suspicion"; all three are kept out of the quiz options. |
| #3b | 素/料 | `素.md:14` `[原, 単, 純, 具, 材, 料, 要, 元, 本]` | `素.md:61`: 料, "materials, fee," is added to the ingredient and material overlap. |

`怪.md` and `料.md` are unchanged (originals in the original packet's `repo\kanji\`). The options now shown for 嫌 and 素 are
on their lines of `checks\quiz-safety.txt`. Your point that these pairs were not options actually shown in the old
simulation is accepted; the exclusions guard the fallback pool.

To verify: that each pair is justified by the cited evidence and not over-broad, and that neither exclusion leaves the
card without defensible wrong options (see `checks\quiz-safety.txt`).

### #4 (minor): two exclusions justified as overlaps

Author action: **changed, both exclusions removed; both pairs are now described as contrasts.**

| ID | Pair | Exclusion | New text |
| --- | --- | --- | --- |
| #4a | 応/募 | 募 is no longer in `応.md:14` (`[答, 承, 受, 適, 対]`); the overlap bullet `応.md:60` no longer lists it | `応.md:61`: 募, "recruit; solicit," is a contrast, not an overlap: in 応募 おうぼ, 募 is the recruiting side and 応 the responding side, and JMdict lists "to apply (in response to recruitment)" among the senses of 応じる; applying is a response to a recruitment, not the same act, so 募 is not kept out of the quiz options. |
| #4b | 級/校 | 校 is no longer in `級.md:14` (`[位, 格, 段, 等, 階, 組]`); the overlap bullet `級.md:55` no longer lists it | `級.md:56`: 校, "school," belongs to the same setting but is a contrast, not an overlap: 学校 がっこう is the school itself, while a 学級 がっきゅう is one class within it; a school and a school class are different things, so 校 is not kept out of the quiz options. |

The author checked every card in `kanji\`: no card lists 募 or 校 any more, and neither `募.md` nor `校.md` has any
`quiz_exclusions`, so both pairs are now unexcluded in both directions.

To verify: that the two new bullets describe the distinctions correctly (including the JMdict 応じる sense in #4a), that no
overlap claim remains in either card, and that the options now shown for 応 and 級 (`checks\quiz-safety.txt`) are
defensibly wrong.

### #5 (minor): 基 and 素 are walls of text

Author action: **changed.**

- `基.md:23` is now 37 words: 基 as a foundation, 基礎 and 基本, and "The other common words are listed below." Every word
  link removed from it (基準, 基地, 基盤, 基 もと, 基づく) is still in the Readings table (`基.md:33-34`) and in Common words.
  The old 264-word reading paragraph is six short paragraphs: `基.md:37` (compound breakdowns), `:39` (the counter き and the
  chemical term), `:41` (the Joyo table), `:43` (the もと spellings and the senses restricted to 元 and 本), `:45` (practice
  selection and もとい) and `:47` (基督). Longest paragraph of the card: 88 words (`基.md:25`).
- `素.md:23` is now 36 words in the same way: 素 as the plain state and its basic element, 素質 and 要素, and "The other
  common words are listed below." Every word link removed from it (酸素, 水素, 素直, 素 もと, 素人) is still in Common words.
  The old 244-word reading paragraph is five paragraphs: `素.md:37` (breakdowns), `:39` (new, see below), `:41` (the Joyo
  table and 素人), `:43` (practice selection and もと) and `:45` (もとより and 素 そ). Longest paragraph: 82 words
  (`素.md:25`).
- No reading, qualification or citation was deleted from either card; the wording removed is the opening word inventory of
  each card. (A word-by-word comparison with the reviewed card shows no other deletion, apart from one "and" that moved
  within the Notes of 素 when 料 was added, and the punctuation of the Metadata list of JMdict ids of 素, to which two ids
  were added.)
- `素.md:39` is new and does not come from your report: it explains 素敵 すてき and 素晴らしい すばらしい (unlinked, no
  word article, no quiz item) and says that JMdict marks both spellings as ateji, so they help you recognise 素 but do not
  show its meaning. JMdict entries 1397350 and 1397300 are added to the Metadata line (`素.md:63`). Please review it like
  any other changed hunk.
- All 15 cards: 45 prose paragraphs became 93, and the longest paragraph went from 264 to 99 words (table in `CHANGES.md`).

To verify: that the two cards are now easy to read on a phone screen, and that no coverage was lost.

## Optional points

| ID | Author action | Where | Change |
| --- | --- | --- | --- |
| OA | **partly adopted** | all 15 cards; `基.md:23`, `素.md:23` | The word inventories were shortened only in the openings of 基 and 素 (#5), the two cards where they were longest. On the other 13 cards the opening word lists were left as they were (38 to 99 words per opening paragraph, longest `暖.md:23`), the same pattern as the cards published earlier (for example `促.md:23`, `撮.md:23` and `勧.md:23` in the original packet's `repo\kanji\`). Every prose paragraph of the Meaning and Readings sections of every card is now at most 99 words. No vocabulary coverage was added or removed by this point. |
| OB | **changed** | `激.md:27` | "find 氵, "water," at the left, [白](白.md), "white," above [方](方.md), "direction, method," in the middle, and 攵 standing at the far right; 方 and 攵 together make [放](放.md), "release."" KanjiVG record: `evidence\kanjivg\06fc0.svg` (stroke coordinates: 氵 at x 10-26; in the left column of the right part, x 25-62, 白 at y 14-53 above 方 at y 54-94; 攵 at x 57-94 on the right; the record marks 放 as part 1 (方) and part 2 (攵)). |

## Limits

### L1: fallback reading options (UNVERIFIED in your report)

Your first Limits bullet could not name the fallback options of 23 of the 32 reading prompts. `checks\reading-options.txt` is
the author's audit of every reading prompt of the 15 cards (26 prompts with a reading to ask; the six on or kun kinds
without a prompt are marked "no reading prompts"). For each prompt it prints the excluded readings, what each curated
option card offers, the fallback candidates by closeness tier and a simulation of 200 seeded draws, and it checks whether a
reading that is attested for the card but absent from its metadata (KANJIDIC2 name readings, or readings given in the card
text: for example 張 わり, 素 もとより, 応 いらえる, 縮 ちり, 騒 さい) can be offered as a wrong option. Its result is "0
problem(s)". Three "note" lines and one informational case are explained in `CHANGES.md`. Caveats: the audit pool is every
card in `kanji\` (the app draws from the cards the learner has studied), fallback options are random within closeness
tiers, and the audit's random generator is not the app's, so it reports candidate sets rather than exact draws.
`evidence\KanjiReadings.kt` and `evidence\Words.kt` are the app sources it follows (`KanjiReadingQuiz.question`,
`excludedKeys`, `closeness`, `ReadingOptions.mutations`); `evidence\README.md` says where they come from.

To verify and answer: whether any wrong option for any reading prompt of these cards could be a valid reading of the card;
what the audit still cannot show; and a disposition for L1 itself: `RESOLVED` (nothing remains open), or a statement of
what remains.

### L2: no quiz implementation (author's answer)

Your second Limits bullet says no quiz implementation was available. `evidence\QuizBuilder.kt` (meaning quiz) and
`evidence\KanjiReadings.kt` and `evidence\Words.kt` (reading quiz) are now in the packet, taken from the Android checkout at
commit `10d98d0`. No APK and no running phone UI is supplied, and none is needed for the claims above. One compatibility
fact: `quiz_exclusions` are honoured only by app builds from the commit "Honor explicit kanji meaning pair exclusions"
(`2edbf36`) onward; the phone build most recently delivered for testing was made before that commit (its installation was
not verified), so no claim is made about what any installed build does.

To verify and answer: whether the supplied sources settle your limit about the exclusion-aware client behaviour, and a
disposition for L2 itself: `RESOLVED`, or a statement of what remains.

### L3: Joyo claims compared only with text extracts (author's answer)

Your fourth Limits bullet says the Joyo PDF pages were not inspected visually. `evidence\joyo\p<N>.txt` are the text
extracts of the pages used (the header of each gives the page, the source URL and the expected kanji), and
`evidence\README.md` gives the PDF's SHA-256 and the URL; public web sources are allowed, so you can open the page at
`...joyokanjihyo_20101130.pdf#page=N` yourself. This revision changes no Joyo claim except one new paragraph, `器.md:27`
(the table prints an older form of 器 in round brackets), for which the packet also holds two images:
`evidence\joyo-p33-utsuwa.png` (crop of the 器 entry on page 33) and `evidence\joyo-p33-utsuwa-pair.png` (the two glyphs
enlarged side by side). In `evidence\joyo\p33.txt` the bracketed older form is printed as the compatibility ideograph
U+FA38, which Unicode normalisation maps to the standard 器 (U+5668); depending on the font or viewer the two can look
alike, so use the images or the PDF to compare the shapes.

To verify and answer: the new 器 claim, and a disposition for L3 itself: `RESOLVED`, or a statement of what remains.

### L4: other limits in your report

Public dictionary checks (third bullet), the 93 word articles reviewed for their changes only (fifth), the meaning of CLEAN
(sixth), and the second sentence of the fourth bullet (KanjiVG comparisons without animation or handwriting tests): no
action is claimed and no disposition is needed. The changes that do not answer a point
in your report (the 器 mnemonic and Joyo paragraph, the 応用 sentence, the 応 まさに row, the 嫌 wording, the 縮 and 騒 notes,
the 素敵 paragraph) are listed in `CHANGES.md`; please check them as new hunks.
