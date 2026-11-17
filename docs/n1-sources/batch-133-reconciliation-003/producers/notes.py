PARENT = "d7d6cff92afe8220c16a5daa76f1c3f00a2bef30"
REL = "docs/n1-sources/batch-133-reconciliation-003"
OLD_EXCLUSIONS = "quiz_exclusions: [川, 急, 水, 河, 注, 流, 湿, 落, 降, 雨, 音, 響, 騒, 鳴, 速, 声, 激, 岩, 険, 液]"
OLD_MEANING = (
    "waterfall focus. 日本国語大辞典 additionally records an abbreviation\n"
    "of 滝水, water from a waterfall.\n"
)
NEW_MEANING = (
    "waterfall focus. 日本国語大辞典 additionally records 滝 as an\n"
    "Edo-period abbreviation of 滝水 たきすい, the name of a sake sold\n"
    "in Edo; that historical sense is not taught here.\n"
)
OLD_NOTE = (
    "- [液](液.md) receives a qualified precaution for the broad liquid/fluid\n"
    "  label. 日本国語大辞典 records 滝 as short for 滝水, water from a\n"
    "  waterfall; 字通 also records soaking/moistening. デジタル大辞泉\n"
    "  defines 液 as a formless flowing substance such as water or oil.\n"
    "  Not every liquid is a waterfall, and 滝 is not taught as meaning\n"
    "  liquid generally.\n"
)
NEW_NOTES = (
    "- [液](液.md) receives a qualified precaution for the broad liquid/fluid\n"
    "  label: 滝 is a flow of water, 字通 also records soaking/moistening,\n"
    "  and 日本国語大辞典's abbreviated sense names a drink.\n"
    "  デジタル大辞泉 defines 液 as a formless flowing substance such as\n"
    "  water or oil. Not every liquid is a waterfall, and 滝 is not taught\n"
    "  as meaning liquid generally.\n"
    "- [酒](酒.md) receives a qualified precaution for its alcohol/sake\n"
    "  label. 日本国語大辞典 records 滝 as short for 滝水 たきすい,\n"
    "  a named sake sold by a shop in Edo's Kanda; the waterfall-water\n"
    "  words 滝水 たきみず and ろうすい are separate readings. This\n"
    "  historical abbreviation is not a modern sense of 滝, and 滝 is\n"
    "  not taught as meaning alcohol.\n"
)
SOURCE_LINE = (
    "Abbreviated sense: 日本国語大辞典's\n"
    "[滝水](https://kotobank.jp/word/滝水), たきすい.\n"
)


def expected_after(before):
    assert before.endswith("\n") and "https://kotobank.jp/word/滝水" not in before
    for old in (OLD_EXCLUSIONS, OLD_MEANING, OLD_NOTE):
        assert before.count(old) == 1
    return before.replace(OLD_EXCLUSIONS, OLD_EXCLUSIONS[:-1] + ", 酒]").replace(
        OLD_MEANING, NEW_MEANING).replace(OLD_NOTE, NEW_NOTES) + SOURCE_LINE
