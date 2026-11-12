# N5 reading pilot: Momotaro

This is the authoring record for `reading/momotaro-n5.json`. It is not runtime clearance,
an official JLPT certification, or a claim that every traditional version uses these causes.

## Publication

`tools/build_manifest.py` omits `reading` and `readingImages` unless `publish_reading=True`.
Do not enable that flag until the Android renderer accepts the package. The current app at
`10d98d0` does not list `reading/` in `SafeZip.allowedFolders`, so a source ZIP that contains
the file does not import it. Validation still checks the file and rejects CR. `.gitattributes` keeps `reading/*.json` as LF
because Windows `autocrlf` would otherwise break that check. Do not put it in `manifest.files`.

Empty `distribution.reviewed` means no jurisdiction has been reviewed. It is not worldwide permission.

## Package

- Schema 1, id `momotaro-n5`, integer JLPT 5.
- Eight sections, 581 Unicode code points. The N5 band is 400-1000, with a target of 480-800.
- Seven questions: two tier 1, two tier 2, two tier 3, one tier 4.
- No question images.
- Teaching-language fields are English. Japanese fields are the title, provenance title, section text,
  and span text/reading/headword.
- Each quiz may be open-book or closed-book. Prompts include any Japanese quote they test.
  Cause questions ask about a reason the passage states with から. Evidence is feedback, not a required hint.
- Unlock thresholds and progression sharing are not content fields.

## Wording and rights

The passage is original wording. It was not copied from Kusuyama Masao, Akutagawa Ryunosuke, or
Ishizuka Hiroyuki. Aozora card 18376 (楠山正雄, 桃太郎) was consulted on 2026-11-12 as a plot check only.
That card records his death as 1950-11-26. [Aozora card 56878](https://www.aozora.gr.jp/cards/001813/card56878.html) is marked 著作権存続 and was not used.
The millet-dumpling name is omitted; the passage says だんご.

The oni's weakness is an authored cause in this wording so the tier-3 question has an explicit から.
It is not a claim about the motive in every traditional telling. There is no battle sentence.

`いいももです` is a simplified learner evaluation, not a claim that the collocation is a literary idiom.
He leaves home with the dumplings. The animals meet him on the road to the island, and the party reaches the island once. 途中 is N4, so the road is 道. The naming sentence uses 「この子供の名前は桃太郎です」 rather than XをYと呼ぶ, because the 呼ぶ card
teaches calling a name aloud or summoning, not that naming construction. The return names the three
animals instead of introducing unexplained 友達.

## Level exceptions

Linked cards at N5 are not listed. These are the exceptions:

| Surface | Card | Level evidence | Why it remains |
| --- | --- | --- | --- |
| 桃 inside 桃太郎 | kanji `桃` | `kanji/桃.md` has `jlpt: 1` | The personal name needs the character. The fruit is written もも. |
| もも | word `桃` | `words/桃.md` has no `jlpt` field | Kana fruit still links to the peach card. Absence of a word level is not an N5 label. |
| 鬼 | word `鬼` | `words/鬼.md` `jlpt: 3` | The plot needs the oni. The gloss says oni; ogre. |
| さる | word `猿` | `words/猿.md` `jlpt: 3` | The monkey is written in kana and linked to the kanji card. |
| 宝 | word `宝` | `words/宝.md` `jlpt: 3` | The ending needs the treasure. |
| 島 | word `島` | `words/島.md` `jlpt: 4` | The destination is an island. |
| むかし | word `昔` | `words/昔.md` `jlpt: 4` | The opening is kana; the link is the N4 card. |
| だんご, きじ, 桃太郎 | none | no `words/<id>.md` | Gloss and reading still appear. No card reference is invented. |

## Quiz scope

Tier 1 asks where the peach was seen and what came out of it. Tier 2 asks event order and what
「これを持ってください」 refers to. Tier 3 asks the two stated から causes. Tier 4 asks which
summary matches the journey. Distractors are not supported by the passage. They do not depend on outside plot knowledge. One tier-3 option, that the old man ordered the animals to go, is unstated rather than directly contradicted.
