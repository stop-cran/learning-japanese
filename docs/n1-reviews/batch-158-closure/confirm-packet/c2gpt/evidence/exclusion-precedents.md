# Quiz-exclusion precedents in the repository at 348c4f70

Verbatim excerpts, quoted with their file path and line numbers at commit 348c4f70. They are unchanged by batch 158 (the batch base is ad1694c1).

## docs/content-format.md, lines 111-124 and 129

```
111: The meaning quiz displays a kanji and offers other cards' English titles as answers. For new cards, curate **three** semantically
112: distinct wrong options for the default four-choice quiz. Two remain structurally valid for older cards, but the app fills missing
113: choices from other cards, preferring shared tags. Exact-title deduplication alone does not establish semantic uniqueness:
114: different English synonyms can still produce two defensible answers. Keep useful semantic comparisons in the body even when
115: they are unsuitable as wrong answers.
116: 
117: Kanji-exclusion-aware clients ([Android #132](https://github.com/stop-cran/kanji-cards-android/issues/132)) additionally honor
118: `quiz_exclusions`, using exact kanji IDs, not word IDs, readings or titles. A declaration on either card excludes that direct pair
119: both against the target and among chosen distractors, for curated choices and tag/random fallbacks in All, level and custom pools.
120: Exclusions are symmetric but not transitive: A/B and B/C do not exclude A/C. References must resolve in the complete accepted
121: source, not the currently filtered pool. A small pool may yield fewer choices, even only the target; the app never restores an
122: excluded card to fill slots. Exclusions affect meaning choices only, not readings, drawing, membership, ordering or saved progress.
123: 
124: Author a pair only from evidence about the actual displayed labels and ordinary meanings. The observed 剰/冗 fallback ambiguity
129: Editorial review must check the displayed titles against the target's ordinary meanings, not merely look for duplicate strings.
```

## docs/n1-authoring-notes.md, lines 1594 and 1633-1642 (Batch 139)

```
1594: ## Batch 139: published
1633: Two reviewer agents, Claude (claude-opus-5.5) and GPT (gpt-6.1-sol),
1634: reviewed the frozen draft `a47efe9a` one after the other, each without seeing
1635: the other's work. GPT returned NEEDS FIX for one minor defect: 峠 excluded 通
1636: and 経, which share only the English word "pass" with it. Claude passed the
1637: batch with two minor source points: 宣 did not give JMdict's note that
1638: のたまう was originally respectful and is now often used sarcastically, and
1639: 嫁 did not say that JMdict marks its sense "wife" as Kansai dialect. Fix
1640: `3b6f9727` changed four cards and one word article: it removed both 峠
1641: exclusions and added a bullet separating a mountain pass from the verbs 通る
1642: and 経る, added the two notes, and applied three of Claude's optional points:
```

## kanji/峠.md, lines 3, 14 and 49 (after fix 3b6f9727, "Fix batch 139 review findings on 嫁, 宣, 峠, 嬢 and 宴会")

```
3: title: mountain pass; peak; climax
14: quiz_exclusions: [頂, 山, 旬]
49: - A mountain pass is 峠. Passing through a place is a different idea, expressed by verbs such as 通る とおる, to go by or through a place, and 経る へる, for time to pass or to go through a place. English "pass" covers both ideas, so [通](通.md), "pass through; commute," and [経](経.md), "pass through; sutra," remain ordinary wrong options for 峠.
```

## docs/n1-authoring-notes.md, lines 2036 and 2050-2051 (Batch 130)

```
2036: ## Batch 130: local unreviewed authoring candidate
2050: visible. Conservative direct guards are not universal synonymy; shared
2051: topics, materials and English homographs alone do not compel guards.
```

## docs/n2-vocabulary-review.md, line 1753

```
1753: | Claude Limits: 包装/小包 and 法則/支配 | No pair added: wrapping/outer wrapper differs from the parcel itself; rule/law differs from domination/governance. Neither category association nor an English homograph establishes a shared meaning. |
```
