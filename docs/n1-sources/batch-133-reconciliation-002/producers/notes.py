PARENT = "110b4ffb6af078eb2adb00645db4c9e0bd6db188"
REL = "docs/n1-sources/batch-133-reconciliation-002"
OLD_EXCLUSIONS = "quiz_exclusions: [川, 急, 水, 河, 注, 流, 湿, 落, 降, 雨, 音, 響, 騒, 鳴, 速, 声, 激, 岩, 険]"
NOTES = (
    "- [液](液.md) receives a qualified precaution for the broad liquid/fluid\n"
    "  label. 日本国語大辞典 records 滝 as short for 滝水, water from a\n"
    "  waterfall; 字通 also records soaking/moistening. デジタル大辞泉\n"
    "  defines 液 as a formless flowing substance such as water or oil.\n"
    "  Not every liquid is a waterfall, and 滝 is not taught as meaning\n"
    "  liquid generally.\n"
)
ANCHOR = "- 世界大百科事典's folklore section records that from the Chugoku\n"
OLD_CITATION = "[岩](https://kotobank.jp/word/岩) and [険](https://kotobank.jp/word/険).\n"
NEW_CITATION = "[岩](https://kotobank.jp/word/岩), [険](https://kotobank.jp/word/険) and [液](https://kotobank.jp/word/液).\n"


def expected_after(before):
    assert before.count(OLD_EXCLUSIONS) == before.count(ANCHOR) == before.count(OLD_CITATION) == 1
    return before.replace(OLD_EXCLUSIONS, OLD_EXCLUSIONS[:-1] + ", 液]").replace(
        ANCHOR, NOTES + ANCHOR).replace(OLD_CITATION, NEW_CITATION)
