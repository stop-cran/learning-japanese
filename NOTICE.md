# Notices and data sources

This repository contains original notes plus data derived from open dictionary projects.

- **Stroke data** (`strokes/*.json`) is derived from [KanjiVG](https://kanjivg.tagaini.net) (© Ulrich Apel and contributors),
  licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). The paths were converted to resampled polylines; the
  files remain under CC BY-SA 3.0 and name the source revision.
- **Readings, stroke counts and radicals** use [KANJIDIC2](https://www.edrdg.org/wiki/index.php/KANJIDIC_Project);
  word spellings, readings and senses are checked against [JMdict](https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project).
  Copyright James William Breen and the [Electronic Dictionary Research and Development Group](https://www.edrdg.org).
  Dictionary-derived data is used under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), following the
  [EDRDG terms](https://www.edrdg.org/edrdg/licence.html). Explanations and examples are original teaching text.
  The [N4](docs/n4-source-snapshot.json) and [N3](docs/n3-source-snapshot.json) source snapshots record inspected versions,
  hashes and transformations. N3 reuses the 2026-10-08 dictionary snapshot; its community kanji list was retrieved on 2026-10-09.
  The [N4 word-pair index](docs/n4-word-sources.tsv) and [N3 primary-word index](docs/n3-word-sources.tsv) identify matching
  JMdict entries for the selected spellings and readings; not every sense of those entries applies to an article.
  The N3 index identifies a non-exhaustive selection of primary teaching senses and distinguishes new articles from two reused ones.
  Individual pages may explain and cite additional applicable senses; the index is not a complete inventory of those explanations.
  The [N5/N4 vocabulary snapshot](docs/n5-n4-vocabulary-snapshot.json) and
  [source-row index](docs/n5-n4-vocabulary-sources.tsv) reuse the same dictionary snapshot and distinguish supplied source IDs
  from corrected lexical identities. Selected sense indices are one-based within that inspected dictionary version, not stable
  identifiers for every future JMdict revision.
  The separate [N3 vocabulary snapshot](docs/n3-vocabulary-snapshot.json) and
  [source-row index](docs/n3-vocabulary-sources.tsv) use that same dictionary version for the later vocabulary expansion.
  They preserve original source fields, selected teaching identities, spelling-sensitive coverage and retained source-intent uncertainty.
  The [article-subject snapshot](docs/article-subjects-source-snapshot.json) uses dictionaries retrieved on 2026-10-10
  and records six added kanji, 17 new word articles, and the reused 訳 article. It distinguishes rare character-dictionary
  readings from verified ordinary word spellings. The rare 奇しい/あやしい spelling is supported by the cited
  *Seisenban Nihon Kokugo Daijiten* entry rather than claimed as a spelling in JMdict.
- **Canonical radical glyphs for the N4 and N3 additions** are mapped from the compatibility decompositions in Unicode 17.0
  [UnicodeData.txt](https://www.unicode.org/Public/17.0.0/ucd/UnicodeData.txt), copyright Unicode, Inc., under the
  [Unicode License V3](docs/UNICODE-LICENSE.txt). Positional component shapes may differ from these canonical glyphs.
- **Kanji JLPT levels** follow the community sets mirrored by [kanjiapi.dev](https://kanjiapi.dev), with explicitly sourced exceptions.
- **Vocabulary membership** derives from [Stephen Kraus's Yomitan JLPT vocabulary data](https://github.com/stephenmk/yomitan-jlpt-vocab),
  revision `b062d4e38c4bdd0950ae1d4ec55f04b176182e03`, using `original_data/n5.csv`, `original_data/n4.csv` and `original_data/n3.csv`.
  Selected article-subject additions also use `n1.csv`, `n2.csv`, and `n3.csv` at that revision; their source record
  preserves the chosen rows and explains why ambiguous homographs or absent levels were not inferred.
  Credit Stephen Kraus, Jonathan Waller (the underlying [Tanos community lists](https://www.tanos.co.uk/jlpt/)), and EDRDG for
  the dictionary data. Kraus's distribution is explicitly
  [CC BY-SA 4.0](https://github.com/stephenmk/yomitan-jlpt-vocab/blob/b062d4e38c4bdd0950ae1d4ec55f04b176182e03/yomitan-jlpt-vocab/index.json#L10-L12).
  Waller's [archived sharing notice](https://web.archive.org/web/20240223231910id_/http://www.tanos.co.uk/jlpt/sharing/) permits reuse
  with attribution under CC BY but does not name a license version. This repository uses the pinned Kraus distribution under
  CC BY-SA 4.0; that does not re-label Waller's original notice as a version it did not state.
  Transformations include documented spelling normalization, reuse of existing articles, grouping some readings on one page,
  and correction of mistaken homograph IDs. Teaching explanations and examples are newly authored.
  See the [level-source policy](docs/jlpt-levels.md). Both kanji and vocabulary levels are community study classifications,
  not official post-2010 examination lists.

The original articles and cards are licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (see `LICENSE`); `strokes/` stays under CC BY-SA 3.0 as described above.
The Android app that reads this repository is a separate project under Apache-2.0 and does not bundle this content.
