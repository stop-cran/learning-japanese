# Mechanical checks (automatic output, not a review verdict)

## Content validation

```text
0 error(s)
```

## B157 batch audit

```text
{
  "batch": "157",
  "baseCommit": "e2c25363285fd8fa100d1c4178e7289592562a31",
  "draftKanji": 10,
  "newWords": 10,
  "changedReusedArticles": 7,
  "requiredReciprocalPairs": 10,
  "activatedBaselinePairs": 0,
  "readingDispositions": 17,
  "curatedOfferedKeys": 10,
  "sourceOnlyOfferedKeys": 0,
  "dictionaryFamilies": 26,
  "exactBaseRuntimePreservedOutsideRecordedChanges": true,
  "manifestFresh": true,
  "contentVersion": "b54d817524b0d1ea",
  "limits": "Mechanical draft audit, not lexical-allocation/naturalness verification, independent review, native/phone acceptance or publication."
}
```

## Batch audit tests

```text
......................
----------------------------------------------------------------------
Ran 22 tests in 0.006s
OK
```

## Content validator tests

```text
.......................................................................................
----------------------------------------------------------------------
Ran 87 tests in 6.516s
OK
```

## N1 lint (base warnings and errors disclosed)

```text
kanji checked: 17, words checked: 94
WARN  kanji/作.md: not in the N1 source index; source comparison skipped
WARN  kanji/作.md: no quizOnyomi
WARN  kanji/作.md: no quizKunyomi
WARN  kanji/作.md: no Metadata: line
WARN  kanji/理.md: not in the N1 source index; source comparison skipped
WARN  kanji/理.md: no quizOnyomi
WARN  kanji/理.md: no quizKunyomi
WARN  kanji/理.md: no Metadata: line
WARN  kanji/用.md: not in the N1 source index; source comparison skipped
WARN  kanji/用.md: no quizOnyomi
WARN  kanji/用.md: no quizKunyomi
WARN  kanji/用.md: no Metadata: line
WARN  kanji/補.md: not in the N1 source index; source comparison skipped
WARN  kanji/補.md: no quizOnyomi
WARN  kanji/補.md: no quizKunyomi
WARN  kanji/語.md: not in the N1 source index; source comparison skipped
WARN  kanji/語.md: no quizOnyomi
WARN  kanji/語.md: no quizKunyomi
WARN  kanji/語.md: no Metadata: line
WARN  kanji/諸.md: not in the N1 source index; source comparison skipped
WARN  kanji/諸.md: no quizOnyomi
WARN  kanji/諸.md: no quizKunyomi
WARN  kanji/足.md: not in the N1 source index; source comparison skipped
WARN  kanji/足.md: no quizOnyomi
WARN  kanji/足.md: no quizKunyomi
WARN  kanji/足.md: no Metadata: line
WARN  words/凶作.md: Dictionary: line cites no JMdict entry id
WARN  words/制作.md: Dictionary: line cites no JMdict entry id
WARN  words/創作.md: Dictionary: line cites no JMdict entry id
WARN  words/名作.md: Dictionary: line cites no JMdict entry id
WARN  words/応用.md: Dictionary: line cites no JMdict entry id
WARN  words/日本語.md: no Dictionary: line
WARN  words/理解.md: no Dictionary: line
WARN  words/用事.md: no Dictionary: line
WARN  words/略語.md: Dictionary: line cites no JMdict entry id
WARN  words/英語.md: no Dictionary: line
WARN  words/製作.md: Dictionary: line cites no JMdict entry id
WARN  words/足る.md: Dictionary: line cites no JMdict entry id
WARN  words/足袋.md: Dictionary: line cites no JMdict entry id
WARN  words/通用.md: Dictionary: line cites no JMdict entry id
WARN  words/遠足.md: Dictionary: line cites no JMdict entry id
ERROR kanji/理.md: metadata reading ことわり has no Readings row
ERROR kanji/語.md: unknown keys ['phonetic']
2 error(s), 41 warning(s)
```
