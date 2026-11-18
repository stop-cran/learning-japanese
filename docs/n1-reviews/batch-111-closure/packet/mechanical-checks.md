# Mechanical checks (automatic output, not a review verdict)

## lint

```text
kanji checked: 17, words checked: 69
WARN  words/女房.md: Dictionary: line cites no JMdict entry id
WARN  words/授業.md: no Dictionary: line
WARN  words/標本.md: Dictionary: line cites no JMdict entry id
WARN  words/標準.md: Dictionary: line cites no JMdict entry id
WARN  words/標識.md: Dictionary: line cites no JMdict entry id
WARN  words/独り言.md: Dictionary: line cites no JMdict entry id
WARN  words/眼鏡.md: no Dictionary: line
WARN  words/能率.md: Dictionary: line cites no JMdict entry id
WARN  words/製作.md: Dictionary: line cites no JMdict entry id
WARN  words/評論.md: Dictionary: line cites no JMdict entry id
WARN  words/調節.md: Dictionary: line cites no JMdict entry id
WARN  words/鏡.md: no Dictionary: line
WARN  words/風呂敷.md: Dictionary: line cites no JMdict entry id
0 error(s), 13 warning(s)
```

## unit tests

```text
----------------------------------------------------------------------
Ran 431 tests in 72.385s
OK
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8578, 'entries': 8593, 'retainedBytes': 45305197, 'inflatedBytes': 45576507, 'localZipBytes': 30635382, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot
```

## manifest

```text
manifest.json: 8571 files incl. 400 images, 202 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 3f255571cd82aa08
warning: in the working copy of 'manifest.json', LF will be replaced by CRLF the next time Git touches it
```

## android JVM content tests

```text
Not run at this freeze commit. No Android JVM test result exists for this candidate.
```

## quiz safety simulation

```text
修 (repair; amend; cultivate)  options: autumn | state; province | circumference; circuit
    reading シュウ    (on): wrong options from distractors 1/3 (rest filled from other cards)
句 (phrase; verse)  options: wrap; enclose | a long time | bitter; suffering
    reading ク      (on): wrong options from distractors 2/3 (rest filled from other cards)
房 (room; tassel; bunch)  options: return; revert | defend; ward off | busy
    reading ボウ     (on): wrong options from distractors 2/3 (rest filled from other cards)
授 (grant; impart; teach)  options: throw | tree; establish | push
    reading ジュ     (on): wrong options from distractors 2/3 (rest filled from other cards)
敷 (spread; lay out)  options: release | respect; honor | failure; defeat
    reading し.く    (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading -し.き   (kun): wrong options from distractors 3/3 (rest filled from other cards)
旬 (ten days; peak season)  options: pure; genuine | order; sequence | former; old
    reading ジュン    (on): wrong options from distractors 1/3 (rest filled from other cards)
標 (mark; signpost; goal)  options: soldier; troops | ice; freeze | second as a time unit
    reading ヒョウ    (on): wrong options from distractors 1/3 (rest filled from other cards)
独 (alone; sole; Germany (abbreviation))  options: poison; venom | read | cat
    reading ドク     (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading ひと.り   (kun): wrong options from distractors 2/3 (rest filled from other cards)
率 (rate; lead; frank)  options: graduate; finish | law; rhythm | chestnut
    reading ソツ     (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading リツ     (on): wrong options from distractors 1/3 (rest filled from other cards)
節 (joint; season; restraint)  options: snow | kill | laugh
    reading セツ     (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading ふし     (kun): wrong options from distractors 3/3 (rest filled from other cards)
義 (righteousness; duty; meaning)  options: deliberate; debate | doubt; suspect | skill; technique
    reading ギ      (on): wrong options from distractors 0/3 (rest filled from other cards)
製 (manufacture; made of)  options: world, generation | voice | bag; sack; pouch
    reading セイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
評 (appraise; reputation)  options: flat; peaceful | ice; freeze | surface; chart
    reading ヒョウ    (on): wrong options from distractors 1/3 (rest filled from other cards)
養 (nourish; raise; adopt)  options: ocean; Western style | manner; honorific suffix | leaf
    reading ヨウ     (on): wrong options from distractors 1/3 (rest filled from other cards)
鏡 (mirror; lens)  options: boundary; border | silver | dull; blunt
    reading キョウ    (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading かがみ    (kun): wrong options from distractors 3/3 (rest filled from other cards)
existing cards that fall back to tag-similar options: 11
    人 (person) curated slots used 2/3
    休 (rest) curated slots used 2/3
    何 (what) curated slots used 2/3
    入 (enter, put in) curated slots used 2/3
    出 (go out, exit) curated slots used 2/3
    口 (mouth) curated slots used 2/3
    女 (woman, female) curated slots used 2/3
    日 (sun, day) curated slots used 2/3
    月 (moon, month) curated slots used 2/3
    男 (man, male) curated slots used 2/3
    買 (buy) curated slots used 2/3
0 error(s), 0 warning(s)
```
