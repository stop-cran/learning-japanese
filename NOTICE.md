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
  The [N4 source snapshot](docs/n4-source-snapshot.json) records inspected versions, hashes and transformations.
  The [new-word pair index](docs/n4-word-sources.tsv) identifies matching JMdict entries for each new article's spelling and reading;
  it is not an assertion that every sense of those entries applies to the article.
- **Canonical radical glyphs for the N4 additions** are mapped from the compatibility decompositions in Unicode 17.0
  [UnicodeData.txt](https://www.unicode.org/Public/17.0.0/ucd/UnicodeData.txt), copyright Unicode, Inc., under the
  [Unicode License V3](docs/UNICODE-LICENSE.txt). Positional component shapes may differ from these canonical glyphs.
- **JLPT levels** follow the community sets mirrored by [kanjiapi.dev](https://kanjiapi.dev), with explicitly sourced exceptions.
  See the [level-source policy](docs/jlpt-levels.md). These are study classifications, not official post-2010 examination lists.

The original articles and cards are licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (see `LICENSE`); `strokes/` stays under CC BY-SA 3.0 as described above.
The Android app that reads this repository is a separate project under Apache-2.0 and does not bundle this content.
