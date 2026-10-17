# Grammar authoring sources

Use this contributor guide to start a search, not as a whitelist that makes every claim on a site authoritative.
The sources below helped with earlier batches; their usefulness depends on the particular construction and claim.
Follow the [grammar exercise contract](content-format.md#grammar-exercises) and
[writing and review rules](../.github/copilot-instructions.md).

## Search order

1. Search the existing `docs/grammar-*-sources.json` records for the construction and its closest alternatives.
   Reuse their inspected URLs and read their scope and caveats before searching afresh.
2. Choose sources by the question: teaching references for whole patterns, dictionaries for exact senses and spellings,
   and contextual explanations for register or speaker intention. The table provides concrete starting pages.
3. Inspect the actual passage, including its publisher, heading, reading, sense or section, and examples.
   A search summary, guessed URL or successful fetch of the wrong entry is not evidence.
   Cross-check consequential restrictions and competing constructions; resolve disagreements by the exact claim, not a vote.
4. Author original scenarios and screen the full linked article inventory. Sources support patterns, not automatically the
   naturalness or unique answer of a new sentence. Keep genuine equivalents together or make a defensible task restriction
   visible before answering, as required by the exercise contract, and retain editorial review.

## Starting points by purpose

Links in the first column are previously inspected seed pages, not an exhaustive bibliography or a blanket endorsement.
The batch records contain the exact sections and qualifications used.

| Sources and inspected seed pages | Useful starting point for | Existing batch records |
| --- | --- | --- |
| [Japan Foundation: こと](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/grammar/201112.html) / [TUFS: とき](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/093.html) | Teaching explanations, attachment, event order and relative tense. Institutional authorship does not make every teaching shortcut universal. | [Actions](grammar-actions-sources.json), [before/after](grammar-before-after-sources.json), [time](grammar-time-sources.json) |
| [Daijisen: 末](https://kotobank.jp/word/末-136437) / [Nihon Kokugo Daijiten: 代り](https://kotobank.jp/word/代り-468939), via Kotobank | Exact senses, readings, classification and distinctions lost in simplified glosses. Match the dictionary, not just the hosting site. | [Outcomes](grammar-expectations-sources.json), [causes/alternatives](grammar-causes-sources.json) |
| [Bunpro: たほうがいい](https://bunpro.jp/grammar_points/たほうがいい) | Broad construction discovery, structure tables, related patterns and example leads. Cross-check categorical restrictions rather than adopting them wholesale. | [Comparison/advice](grammar-comparisons-sources.json), [conditions](grammar-conditions-sources.json) |
| [Maggie Sensei: ばかり](https://maggiesensei.com/2013/07/02/%E3%81%B0%E3%81%8B%E3%82%8A-bakari/) / [Tofugu: つもり](https://www.tofugu.com/japanese-grammar/tsumori/) | Communicative context, register, speaker intention and contrasting formulations. Separate a scenario's nuance from a universal rule. | [Particle neighbors](grammar-particles-sources.json), [intention/inference](grammar-intent-sources.json) |
| [Tae Kim: amounts](https://guidetojapanese.org/learn/grammar/amount) / [IMABI: after](https://imabi.org/after-i-%e3%81%82%e3%81%a8-%e3%81%ae%e3%81%a1-%ef%bd%9e%e3%81%a6%e3%81%8b%e3%82%89/) | Syntax, negation, tense and more detailed explanations. Account for differences in grammatical frameworks and scope. | [Degree/extent](grammar-degree-extent-sources.json), [before/after](grammar-before-after-sources.json) |
| [JMdict through Jisho: だけ](https://jisho.org/api/v1/search/words?keyword=だけ) | Lexical identity, readings, sense restrictions and accepted spellings. Recognition is not evidence of frequency or idiomaticity in an invented sentence. | [Particle neighbors](grammar-particles-sources.json), [degree/extent](grammar-degree-extent-sources.json) |

Other sources can be useful when they address the exact question. Do not stop searching merely because a claim appears
on a listed site, or reject a relevant source merely because it is absent here.

## Retrieval pitfalls already encountered

- **Bunpro:** simplified extraction can return a forum comment instead of the grammar explanation. Inspect the actual
  Structure, About and relevant Related sections; community discussion is not interchangeable with the main lesson.
  The [comparison/advice record](grammar-comparisons-sources.json) documents this for たほうがいい.
- **Kotobank:** extraction can omit the modern Daijisen entry and expose another dictionary or reading. Check the actual
  entry heading and sense, not merely a matching character. The [outcome record](grammar-expectations-sources.json)
  documents the 末 and 癖に cases.
- **Weblio:** isolate the named dictionary from adjacent expression dictionaries and automatically generated examples.
  The [あげく record](grammar-expectations-sources.json) uses Daijisen's spelling heading; it does not establish equal
  frequency for the accepted spellings.
- **Tae Kim:** inline Japanese can disappear in simplified extraction. Inspect the actual HTML/body text before evaluating
  an incomplete example; see the [degree/extent record](grammar-degree-extent-sources.json).

If the relevant passage remains unavailable, record the limitation instead of reconstructing it from a summary.

## Keep provenance in the batch record

Continue recording the exact URL, retrieval date, publisher, inspected heading/sense/section, supported construction IDs,
and important qualifications or claims not adopted in each batch's source JSON. Do not replace those records with a link
to this guide, duplicate their full bibliographies here, or change an old retrieval date merely because its URL was reused.

These notes are contributor-only: `docs/` is not imported by the app. Learner articles should cite the relevant external
sources directly rather than use relative links into this directory.
