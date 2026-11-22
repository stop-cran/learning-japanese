# Mechanical checks (automatic output, not a review verdict)

Candidate: `f811f8eb13fb9fbea0e19b1e3071d814d3c554b2`
Base: `e2c25363285fd8fa100d1c4178e7289592562a31`

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
  "changedReusedArticles": 8,
  "requiredReciprocalPairs": 10,
  "activatedBaselinePairs": 0,
  "readingDispositions": 17,
  "curatedOfferedKeys": 10,
  "sourceOnlyOfferedKeys": 0,
  "dictionaryFamilies": 27,
  "exactBaseRuntimePreservedOutsideRecordedChanges": true,
  "manifestFresh": true,
  "contentVersion": "3bd1fc240dfdfd08",
  "limits": "Mechanical draft audit, not lexical-allocation/naturalness verification, independent review, native/phone acceptance or publication."
}
```

## Batch audit tests

```text
Ran 22 tests: OK
```

## Content validator tests

```text
Ran 87 tests: OK
```

## N1 lint

Not rerun on this revision. The prior candidate run reported two existing errors in `kanji/理.md` and `kanji/語.md`, plus 41 warnings; this is not a clean lint verdict for the present candidate.
