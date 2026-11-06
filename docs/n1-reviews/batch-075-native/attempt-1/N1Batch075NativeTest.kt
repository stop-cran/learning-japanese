package io.github.stopcran.kanji.ui

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Typeface
import android.net.ConnectivityManager
import android.os.Build
import androidx.activity.ComponentActivity
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.asAndroidBitmap
import androidx.compose.ui.semantics.SemanticsActions
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.junit4.createEmptyComposeRule
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.res.ResourcesCompat
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.room.withTransaction
import androidx.test.core.app.ActivityScenario
import androidx.test.platform.app.InstrumentationRegistry
import io.github.stopcran.kanji.KanjiApp
import io.github.stopcran.kanji.MainActivity
import io.github.stopcran.kanji.R
import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.content.RepoSource
import io.github.stopcran.kanji.core.reading.ReadingKind
import io.github.stopcran.kanji.core.srs.KanjiFont
import io.github.stopcran.kanji.core.srs.StudyMode
import io.github.stopcran.kanji.data.*
import kotlinx.coroutines.runBlocking
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import java.io.ByteArrayInputStream
import java.io.File
import java.security.MessageDigest
import java.util.UUID

private fun disposable075() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch075GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun referenceTextsLookalikesAndFourFallbacksAcrossFourProductionFamilies() {
        disposable075()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("一 七 三 上 中 九 亅 事 二 五 人 仕 付 代 件 任 使 例 借 儀 八 六 共 具", "典 円 力 化 十 千 厂 取 口 古 右 味 和 四 図 国 地 型 外 大 失 奠 好 季", "学 家 寄 山 年 店 建 式 意 授 故 敗 文 斗 料 新 方 日 春 曲 書 本 業 水", "済 渡 火 物 現 理 用 白 百 的 知 石 祝 禾 私 秋 科 種 立 築 米 経 考 舌", "艹 花 苦 英 葉 言 話 語 読 調 貨 贈 車 辛 辞 道 雪 類 食 館 香", "典 具 曲 共 奠 亅 厂 艹 八 典型 古典 百科事典 辞典 香典 香奠")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 075: reference texts / look-alikes / fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 117 scoped Han; focused 奠/亅/厂/艹 and 典/具/曲/共. Fallback families may coincide.", fontSize = 16.sp)
                }
            }
        }
        val typefaces = listOf(Typeface.DEFAULT,
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_mincho)),
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_textbook)),
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_brush)))
        val rows = JSONArray()
        for ((index, typeface) in typefaces.withIndex()) {
            val hashes = mutableSetOf<String>()
            for (char in listOf("一", "七", "三", "上", "中", "九", "亅", "事", "二", "五", "人", "仕", "付", "代", "件", "任", "使", "例", "借", "儀", "八", "六", "共", "具", "典", "円", "力", "化", "十", "千", "厂", "取", "口", "古", "右", "味", "和", "四", "図", "国", "地", "型", "外", "大", "失", "奠", "好", "季", "学", "家", "寄", "山", "年", "店", "建", "式", "意", "授", "故", "敗", "文", "斗", "料", "新", "方", "日", "春", "曲", "書", "本", "業", "水", "済", "渡", "火", "物", "現", "理", "用", "白", "百", "的", "知", "石", "祝", "禾", "私", "秋", "科", "種", "立", "築", "米", "経", "考", "舌", "艹", "花", "苦", "英", "葉", "言", "話", "語", "読", "調", "貨", "贈", "車", "辛", "辞", "道", "雪", "類", "食", "館", "香")) {
                val paint = Paint(Paint.ANTI_ALIAS_FLAG).also {
                    it.typeface = typeface
                    it.textSize = 96f
                    it.textLocale = java.util.Locale.JAPAN
                }
                assertTrue("$char ${fonts[index]}", paint.hasGlyph(char))
                val image = Bitmap.createBitmap(if (char.length > 1) 256 else 128, 128, Bitmap.Config.ARGB_8888)
                Canvas(image).drawText(char, 8f, 104f, paint)
                val pixels = IntArray(image.width * image.height)
                image.getPixels(pixels, 0, image.width, 0, 0, image.width, image.height)
                assertTrue(pixels.any { it != 0 })
                val bytes = java.nio.ByteBuffer.allocate(pixels.size * 4)
                    .also { it.asIntBuffer().put(pixels) }.array()
                val hash = MessageDigest.getInstance("SHA-256").digest(bytes)
                    .joinToString("") { "%02x".format(it) }
                assertTrue("Indistinguishable raster ${fonts[index]}", hashes.add(hash))
                rows.put(JSONObject().put("character", char).put("font", fonts[index].name)
                    .put("hasGlyph", true).put("nativePaintRasterSha256", hash))
                image.recycle()
            }
            for (word in listOf("典型", "古典", "百科事典", "辞典", "香典", "香奠")) {
                val paint = Paint(Paint.ANTI_ALIAS_FLAG).also {
                    it.typeface = typeface
                    it.textSize = 96f
                    it.textLocale = java.util.Locale.JAPAN
                }
                // hasGlyph tests multi-character ligatures, not ordinary word coverage.
                val image = Bitmap.createBitmap(kotlin.math.ceil(paint.measureText(word)).toInt() + 16, 128, Bitmap.Config.ARGB_8888)
                Canvas(image).drawText(word, 8f, 104f, paint)
                val pixels = IntArray(image.width * image.height)
                image.getPixels(pixels, 0, image.width, 0, 0, image.width, image.height)
                for (position in word.indices) {
                    val left = (8f + paint.measureText(word, 0, position)).toInt()
                    val right = kotlin.math.ceil(8f + paint.measureText(word, 0, position + 1)).toInt()
                    assertTrue("Word raster bounds $word ${fonts[index]}", left >= 0 && right <= image.width && left < right)
                    assertTrue("Blank word character ${word[position]} ${fonts[index]}",
                        (0 until image.height).any { y -> (left until right).any { x -> pixels[y * image.width + x] != 0 } })
                }
                val bytes = java.nio.ByteBuffer.allocate(pixels.size * 4)
                    .also { it.asIntBuffer().put(pixels) }.array()
                val hash = MessageDigest.getInstance("SHA-256").digest(bytes)
                    .joinToString("") { "%02x".format(it) }
                rows.put(JSONObject().put("word", word).put("font", fonts[index].name)
                    .put("renderedCharactersNonblank", word.length).put("nativePaintRasterSha256", hash))
                image.recycle()
            }
        }
        assertEquals(492, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-075-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-075-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 468).put("wholeWordRasterProbes", 24).put("panels", 6)
            .put("limits", "117 scoped authored Han including 奠/亅/厂/艹, four production families, six bounded Compose panels and 24 whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch075ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineReferenceTextsTwelveReciprocalPairsTwoOnReadingsDrawingAndSystemBack() {
        disposable075()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-075-${UUID.randomUUID()}", "main")
        val head = "fba1a8868b82cd93d7bfaeae1080f5642bd92730"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-075-fba1a886-envelope.zip")
                }
                else -> error("Unexpected fixture request: $url")
            }
            object : ContentResponse {
                override val code = 200
                override val body = input
                override fun header(name: String): String? = null
                override fun close() = input.close()
            }
        }
        val result = runBlocking { ContentSync(app.db, app.settings.sync, http).sync(source, force = true) }
        assertTrue(result.toString(), result is SyncResult.Updated)
        val updated = result as SyncResult.Updated
        assertEquals(1, archiveRequests)
        assertEquals(1087, updated.kanji)
        assertEquals(5044, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("2759d7b13c89eb8f", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(107, n1.size)
        val referenceTexts = n1.single { it.kanji == "典" }
        assertEquals(listOf("テン", "デン"), referenceTexts.onyomi.splitSep())
        assertEquals(listOf("ふみ", "のり"), referenceTexts.kunyomi.splitSep())
        assertNotNull(referenceTexts.quizOnyomi)
        assertNotNull(referenceTexts.quizKunyomi)
        assertEquals(listOf("テン", "デン"), referenceTexts.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), referenceTexts.quizKunyomi?.splitSep())
        assertEquals(listOf("てん", "でん"), referenceTexts.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), referenceTexts.toReadingCard().quizKeys(ReadingKind.Kun))
        val now = System.currentTimeMillis()
        app.settings.sync.lastCheckMs = now
        app.settings.setStartingGuideVisible(false)
        app.settings.setDailyNewCards(50)
        app.settings.setWeekPlan("FFFFFFF")
        app.settings.setTraceNew(true)
        app.settings.setVaryFonts(true)
        app.settings.setStack("jlpt-n5")
        runBlocking {
            app.db.withTransaction {
                n1.forEach { card ->
                    app.db.reviews().putState(ReviewStateEntity(
                        source.id, "jlpt-n1", card.kanji, StudyMode.Quiz.name, "Review", 30.0, 5.0,
                        if (card.kanji == "典") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "典" && (kind == ReadingKind.On && key in setOf("てん", "でん"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "典", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(referenceTexts.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(referenceTexts.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(referenceTexts.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(referenceTexts.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(referenceTexts.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(referenceTexts.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 典 meaning and two curated on keys due; raw source-only ふみ/のり retained but no kun keys. Two historical good 典 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 107 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("典")
            click("reference texts; rules; ceremony")
            await("典 — reference texts; rules; ceremony")
            show(articleBullet("Strokes: 8 · Key (radical): 八 (the spreading bottom strokes, no. 12) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("典 appears in words for reference texts and established standards: 辞典 じてん is a dictionary, 古典 こてん a classic work, and 典型 てんけい a typical example or model. It also has a ceremony branch, as in 式典 (しきてん), \"ceremony.\" These are related uses, not one English translation that fits every compound."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: picture a reference text in the upper divided enclosure, resting on two spreading supports below. This remembers the modern outline; it does not establish a historical origin or phonetic component."), "kanji-04")
            section("Readings")
            show(readingExample("テン"), "kanji-09")
            show(readingExample("辞典 じてん — dictionary; 典型 てんけい — typical example; 古典 こてん — classic work"), "kanji-11")
            show(readingExample("デン"), "kanji-12")
            show(readingExample("香典 こうでん — condolence money; funeral gift"), "kanji-14")
            show(readingExample("ふみ"), "kanji-15")
            show(readingExample("source-only lookup information in this lesson; retained from KANJIDIC2 without a verified word example spelled 典 for practice here"), "kanji-17")
            show(readingExample("のり"), "kanji-18")
            show(readingExample("source-only in this lesson; dictionaries recognize 典 のり among spellings for a rule or law, but no linked practice word is selected here"), "kanji-20")
            show(articleBullet("Practise テン and デン in the linked whole words. The two kun readings remain available for lookup, not as alternative pronunciations to try in 辞典 or 香典. Their nonselection does not mean they are incorrect or restricted to names."), "kanji-21")
            section("Common words")
            show(articleBullet("辞典 じてん — dictionary; lexicon"), "kanji-23")
            show(articleBullet("典型 てんけい — typical example; model"), "kanji-24")
            show(articleBullet("古典 こてん — classic work; the classics"), "kanji-25")
            show(articleBullet("百科事典 ひゃっかじてん — encyclopedia"), "kanji-26")
            show(articleBullet("香典 こうでん — condolence money; funeral gift"), "kanji-27")
            section("Notes")
            show(articleBullet("辞典 (じてん) explains words; 事典 (also じてん) is an encyclopedia or subject reference. The complete word 百科事典 can also be spelled 百科辞典 without becoming merely a language dictionary."), "kanji-29")
            show(articleBullet("Learn デン in 香典 as part of こうでん. This example does not give a rule that changes every テン to デン after another kanji."), "kanji-30")
            show(articleBullet("Compare 具, which has a taller stacked box, and 曲, which has a divided enclosure but no spreading feet. 共 has spreading lower strokes without 典's enclosed upper part."), "kanji-31")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word pairs: JMdict, entries 1265860, 1283090, 1314210, 1319100, 1438050, 1438080, 1595270 and 1602190. Meaning branches: Digital Daijisen and Nihon Kokugo Daijiten, 典."), "kanji-32")
            section("Common words")
            show(articleBullet("典型 てんけい — typical example; model"), "典型-forward-21")
            inline(await(articleBullet("典型 てんけい — typical example; model")), "典型", 0)
            await("Article contents")
            await("典型 (てんけい) - typical example; model")
            section("How the kanji combine")
            show(articleBullet("典 contributes a standard or model, and 型 contributes a form or pattern. Their related meanings combine to identify a model of a type. The on readings are テン + ケイ."), "典型-07")
            section("How the kanji combine")
            show(articleBullet("典 contributes a standard or model, and 型 contributes a form or pattern. Their related meanings combine to identify a model of a type. The on readings are テン + ケイ."), "典型-reverse-23")
            inline(await(articleBullet("典 contributes a standard or model, and 型 contributes a form or pattern. Their related meanings combine to identify a model of a type. The on readings are テン + ケイ.")), "典", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("デン"), "典型-kanji-backlink")
            back()
            await(articleBullet("典 contributes a standard or model, and 型 contributes a form or pattern. Their related meanings combine to identify a model of a type. The on readings are テン + ケイ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("典型-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("典 contributes a standard or model, and 型 contributes a form or pattern. Their related meanings combine to identify a model of a type. The on readings are テン + ケイ."), "典型-型-24")
            inline(await(articleBullet("典 contributes a standard or model, and 型 contributes a form or pattern. Their related meanings combine to identify a model of a type. The on readings are テン + ケイ.")), "型", 39)
            await("Article contents")
            section("Common words")
            show(articleBullet("典型 てんけい - typical example; model"), "型-counterpart-25")
            inline(await(articleBullet("典型 てんけい - typical example; model")), "典型", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("典 contributes a standard or model, and 型 contributes a form or pattern. Their related meanings combine to identify a model of a type. The on readings are テン + ケイ."), "典型-型-component-backlink")
            back()
            await(articleBullet("典型 てんけい - typical example; model")).assertIsDisplayed()
            section("Common words")
            capture("典型-型-system-back-to-component")
            back()
            await(articleBullet("典 contributes a standard or model, and 型 contributes a form or pattern. Their related meanings combine to identify a model of a type. The on readings are テン + ケイ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("典型-型-system-back-from-component")
            back()
            await(articleBullet("典型 てんけい — typical example; model")).assertIsDisplayed()
            section("Common words")
            capture("典型-system-back-to-kanji")
            section("Common words")
            show(articleBullet("古典 こてん — classic work; the classics"), "古典-forward-26")
            inline(await(articleBullet("古典 こてん — classic work; the classics")), "古典", 0)
            await("Article contents")
            await("古典 (こてん) - classic work; the classics")
            section("How the kanji combine")
            show(articleBullet("古 contributes old or ancient. 典 contributes a book, canon, or established standard. Their modifier-and-head relationship helps recall an old or established classic work. The on readings are コ + テン. This does not mean that any worn-out book is a 古典."), "古典-07")
            section("How the kanji combine")
            show(articleBullet("古 contributes old or ancient. 典 contributes a book, canon, or established standard. Their modifier-and-head relationship helps recall an old or established classic work. The on readings are コ + テン. This does not mean that any worn-out book is a 古典."), "古典-reverse-28")
            inline(await(articleBullet("古 contributes old or ancient. 典 contributes a book, canon, or established standard. Their modifier-and-head relationship helps recall an old or established classic work. The on readings are コ + テン. This does not mean that any worn-out book is a 古典.")), "典", 30)
            await("Article contents")
            section("Readings")
            show(readingExample("デン"), "古典-kanji-backlink")
            back()
            await(articleBullet("古 contributes old or ancient. 典 contributes a book, canon, or established standard. Their modifier-and-head relationship helps recall an old or established classic work. The on readings are コ + テン. This does not mean that any worn-out book is a 古典.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("古典-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("古 contributes old or ancient. 典 contributes a book, canon, or established standard. Their modifier-and-head relationship helps recall an old or established classic work. The on readings are コ + テン. This does not mean that any worn-out book is a 古典."), "古典-古-29")
            inline(await(articleBullet("古 contributes old or ancient. 典 contributes a book, canon, or established standard. Their modifier-and-head relationship helps recall an old or established classic work. The on readings are コ + テン. This does not mean that any worn-out book is a 古典.")), "古", 0)
            await("Article contents")
            section("Common words")
            show(articleBullet("古典 こてん — classic work; the classics"), "古-counterpart-30")
            inline(await(articleBullet("古典 こてん — classic work; the classics")), "古典", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("古 contributes old or ancient. 典 contributes a book, canon, or established standard. Their modifier-and-head relationship helps recall an old or established classic work. The on readings are コ + テン. This does not mean that any worn-out book is a 古典."), "古典-古-component-backlink")
            back()
            await(articleBullet("古典 こてん — classic work; the classics")).assertIsDisplayed()
            section("Common words")
            capture("古典-古-system-back-to-component")
            back()
            await(articleBullet("古 contributes old or ancient. 典 contributes a book, canon, or established standard. Their modifier-and-head relationship helps recall an old or established classic work. The on readings are コ + テン. This does not mean that any worn-out book is a 古典.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("古典-古-system-back-from-component")
            back()
            await(articleBullet("古典 こてん — classic work; the classics")).assertIsDisplayed()
            section("Common words")
            capture("古典-system-back-to-kanji")
            section("Common words")
            show(articleBullet("百科事典 ひゃっかじてん — encyclopedia"), "百科事典-forward-31")
            inline(await(articleBullet("百科事典 ひゃっかじてん — encyclopedia")), "百科事典", 0)
            await("Article contents")
            await("百科事典 (ひゃっかじてん) - encyclopedia")
            section("How the kanji combine")
            show(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning."), "百科事典-07")
            section("How the kanji combine")
            show(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning."), "百科事典-reverse-33")
            inline(await(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning.")), "典", 121)
            await("Article contents")
            section("Readings")
            show(readingExample("デン"), "百科事典-kanji-backlink")
            back()
            await(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("百科事典-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning."), "百科事典-百-34")
            inline(await(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning.")), "百", 0)
            await("Article contents")
            section("Meaning and origin")
            show(articleBullet("百 is commonly explained as 一 over 白 (white), where 白 gives the sound (Old Chinese pronunciations of the two are similar; modern Japanese on readings ハク and ヒャク still resemble each other) and 一 marks the number. Some sources analyse the shape differently, so the story of \"one white = hundred\" is only a mnemonic. It means \"100\" and, figuratively, \"many\" (百科事典 ひゃっかじてん, encyclopedia; 百貨店 ひゃっかてん, department store)."), "百-counterpart-35")
            inline(await(articleBullet("百 is commonly explained as 一 over 白 (white), where 白 gives the sound (Old Chinese pronunciations of the two are similar; modern Japanese on readings ハク and ヒャク still resemble each other) and 一 marks the number. Some sources analyse the shape differently, so the story of \"one white = hundred\" is only a mnemonic. It means \"100\" and, figuratively, \"many\" (百科事典 ひゃっかじてん, encyclopedia; 百貨店 ひゃっかてん, department store).")), "百科事典", 355)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning."), "百科事典-百-component-backlink")
            back()
            await(articleBullet("百 is commonly explained as 一 over 白 (white), where 白 gives the sound (Old Chinese pronunciations of the two are similar; modern Japanese on readings ハク and ヒャク still resemble each other) and 一 marks the number. Some sources analyse the shape differently, so the story of \"one white = hundred\" is only a mnemonic. It means \"100\" and, figuratively, \"many\" (百科事典 ひゃっかじてん, encyclopedia; 百貨店 ひゃっかてん, department store).")).assertIsDisplayed()
            section("Meaning and origin")
            capture("百科事典-百-system-back-to-component")
            back()
            await(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("百科事典-百-system-back-from-component")
            section("How the kanji combine")
            show(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning."), "百科事典-科-36")
            inline(await(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning.")), "科", 26)
            await("Article contents")
            section("Common words")
            show(articleBullet("百科事典 ひゃっかじてん — encyclopedia"), "科-counterpart-37")
            inline(await(articleBullet("百科事典 ひゃっかじてん — encyclopedia")), "百科事典", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning."), "百科事典-科-component-backlink")
            back()
            await(articleBullet("百科事典 ひゃっかじてん — encyclopedia")).assertIsDisplayed()
            section("Common words")
            capture("百科事典-科-system-back-to-component")
            back()
            await(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("百科事典-科-system-back-from-component")
            section("How the kanji combine")
            show(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning."), "百科事典-事-38")
            inline(await(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning.")), "事", 82)
            await("Article contents")
            section("Common words")
            show(articleBullet("百科事典 ひゃっかじてん — encyclopedia"), "事-counterpart-39")
            inline(await(articleBullet("百科事典 ひゃっかじてん — encyclopedia")), "百科事典", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning."), "百科事典-事-component-backlink")
            back()
            await(articleBullet("百科事典 ひゃっかじてん — encyclopedia")).assertIsDisplayed()
            section("Common words")
            capture("百科事典-事-system-back-to-component")
            back()
            await(articleBullet("百, hundred, combines with 科, fields or branches, in 百科, many fields of knowledge. 事 contributes matters or subjects, and 典 a reference text in 事典, encyclopedia. 百科 modifies 事典. Learn ひゃっか + じてん, with small っ, rather than saying ひゃくか. In 百科辞典, 辞 replaces 事 in the spelling, without changing the whole word's encyclopedia meaning.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("百科事典-事-system-back-from-component")
            back()
            await(articleBullet("百科事典 ひゃっかじてん — encyclopedia")).assertIsDisplayed()
            section("Common words")
            capture("百科事典-system-back-to-kanji")
            section("Common words")
            show(articleBullet("辞典 じてん — dictionary; lexicon"), "辞典-forward-40")
            inline(await(articleBullet("辞典 じてん — dictionary; lexicon")), "辞典", 0)
            await("Article contents")
            await("辞典 (じてん) — dictionary; lexicon")
            section("How the kanji combine")
            show(articleBullet("辞 contributes words or language, and 典 contributes a reference work or authoritative text. The on readings ジ + テン give じてん."), "辞典-06")
            section("How the kanji combine")
            show(articleBullet("辞 contributes words or language, and 典 contributes a reference work or authoritative text. The on readings ジ + テン give じてん."), "辞典-reverse-42")
            inline(await(articleBullet("辞 contributes words or language, and 典 contributes a reference work or authoritative text. The on readings ジ + テン give じてん.")), "典", 37)
            await("Article contents")
            section("Readings")
            show(readingExample("デン"), "辞典-kanji-backlink")
            back()
            await(articleBullet("辞 contributes words or language, and 典 contributes a reference work or authoritative text. The on readings ジ + テン give じてん.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("辞典-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("辞 contributes words or language, and 典 contributes a reference work or authoritative text. The on readings ジ + テン give じてん."), "辞典-辞-43")
            inline(await(articleBullet("辞 contributes words or language, and 典 contributes a reference work or authoritative text. The on readings ジ + テン give じてん.")), "辞", 0)
            await("Article contents")
            section("Common words")
            show(articleBullet("辞典 じてん — dictionary; lexicon"), "辞-counterpart-44")
            inline(await(articleBullet("辞典 じてん — dictionary; lexicon")), "辞典", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("辞 contributes words or language, and 典 contributes a reference work or authoritative text. The on readings ジ + テン give じてん."), "辞典-辞-component-backlink")
            back()
            await(articleBullet("辞典 じてん — dictionary; lexicon")).assertIsDisplayed()
            section("Common words")
            capture("辞典-辞-system-back-to-component")
            back()
            await(articleBullet("辞 contributes words or language, and 典 contributes a reference work or authoritative text. The on readings ジ + テン give じてん.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("辞典-辞-system-back-from-component")
            back()
            await(articleBullet("辞典 じてん — dictionary; lexicon")).assertIsDisplayed()
            section("Common words")
            capture("辞典-system-back-to-kanji")
            section("Common words")
            show(articleBullet("香典 こうでん — condolence money; funeral gift"), "香典-forward-45")
            inline(await(articleBullet("香典 こうでん — condolence money; funeral gift")), "香典", 0)
            await("Article contents")
            await("香典 (こうでん) — condolence money; funeral gift")
            section("Meaning")
            show(articleBullet("香典 is a condolence gift offered in connection with a funeral, usually money. It names the offering, not the funeral ceremony or incense itself. The dictionary definition also allows goods; \"money\" is a practical translation, not an absolute restriction."), "香典-02")
            show(articleBullet("香典を用意しました。 (こうでんをよういしました。) — I prepared condolence money."), "香典-03")
            show(articleBullet("香典を渡しました。 (こうでんをわたしました。) — I handed over the condolence money."), "香典-04")
            show(articleBullet("In both examples, を marks the gift as the object. 用意する (よういする) means \"prepare\"; 渡す (わたす) means \"hand over.\""), "香典-05")
            section("How the kanji combine")
            show(articleBullet("香 supplies the incense connection; 典 also occurs in ceremonial vocabulary. Learn this as an established funeral-offering compound, not a freely productive formula: 典 alone does not mean \"money.\" The on readings コウ + デン give こうでん."), "香典-07")
            show(articleBullet("The same word is also written 香奠 (こうでん). JMdict marks that alternate spelling as rare; the flag does not make the pronunciation こうでん rare."), "香典-08")
            section("Synonyms and antonyms")
            show(articleBullet("贈り物 (おくりもの) and プレゼント mean a gift more generally, without specifying a funeral. 寄付 (きふ) is a donation or contribution, not specifically a funeral condolence gift. お祝い (おいわい), a celebration or congratulatory gift, concerns a happy occasion instead. There is no single useful lexical opposite."), "香典-10")
            section("Distinctive meaning")
            show(articleBullet("Use the whole word for the funeral-related offering. Do not translate it as an ordinary birthday present, the funeral itself, or a stick of incense. The word does not tell you an appropriate amount or every community's customs; this is vocabulary guidance, not an etiquette prescription."), "香典-12")
            show(articleBullet("Dictionary: JMdict, entry 1283090, sense 1; comparisons 1116840, 1589030, 1591400 and 1612770. Money-or-goods definition: Digital Daijisen, 香典."), "香典-13")
            section("How the kanji combine")
            show(articleBullet("香 supplies the incense connection; 典 also occurs in ceremonial vocabulary. Learn this as an established funeral-offering compound, not a freely productive formula: 典 alone does not mean \"money.\" The on readings コウ + デン give こうでん."), "香典-reverse-55")
            inline(await(articleBullet("香 supplies the incense connection; 典 also occurs in ceremonial vocabulary. Learn this as an established funeral-offering compound, not a freely productive formula: 典 alone does not mean \"money.\" The on readings コウ + デン give こうでん.")), "典", 35)
            await("Article contents")
            section("Readings")
            show(readingExample("デン"), "香典-kanji-backlink")
            back()
            await(articleBullet("香 supplies the incense connection; 典 also occurs in ceremonial vocabulary. Learn this as an established funeral-offering compound, not a freely productive formula: 典 alone does not mean \"money.\" The on readings コウ + デン give こうでん.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("香典-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("香 supplies the incense connection; 典 also occurs in ceremonial vocabulary. Learn this as an established funeral-offering compound, not a freely productive formula: 典 alone does not mean \"money.\" The on readings コウ + デン give こうでん."), "香典-香-56")
            inline(await(articleBullet("香 supplies the incense connection; 典 also occurs in ceremonial vocabulary. Learn this as an established funeral-offering compound, not a freely productive formula: 典 alone does not mean \"money.\" The on readings コウ + デン give こうでん.")), "香", 0)
            await("Article contents")
            section("Common words")
            show(articleBullet("香典 こうでん - condolence money; funeral gift"), "香-counterpart-57")
            inline(await(articleBullet("香典 こうでん - condolence money; funeral gift")), "香典", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("香 supplies the incense connection; 典 also occurs in ceremonial vocabulary. Learn this as an established funeral-offering compound, not a freely productive formula: 典 alone does not mean \"money.\" The on readings コウ + デン give こうでん."), "香典-香-component-backlink")
            back()
            await(articleBullet("香典 こうでん - condolence money; funeral gift")).assertIsDisplayed()
            section("Common words")
            capture("香典-香-system-back-to-component")
            back()
            await(articleBullet("香 supplies the incense connection; 典 also occurs in ceremonial vocabulary. Learn this as an established funeral-offering compound, not a freely productive formula: 典 alone does not mean \"money.\" The on readings コウ + デン give こうでん.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("香典-香-system-back-from-component")
            back()
            await(articleBullet("香典 こうでん — condolence money; funeral gift")).assertIsDisplayed()
            section("Common words")
            capture("香典-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 12).put("directedLinkTransitions", 24)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("典", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("reference texts; rules; ceremony")
            await("Correct!")
            assertEquals("典", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("典", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue("Unexpected offered key $key", key in setOf("てん", "でん"))
                assertTrue("Duplicate target key $key", answeredKeys.add(key))
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-$key-question")
                click(question.question.options.single { it.key == key }.label)
                await("Correct! — on'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-$key-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "典" &&
                        log.mode == ReadingKind.On.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("てん", "でん"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "典" && it.mode == ReadingKind.Kun.mode.name }
            })
            capture("curated-two-on-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("reference texts; rules; ceremony").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "典") })
            assertEquals(listOf("テン", "デン"), card.onyomi.splitSep())
            assertEquals(listOf("ふみ", "のり"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("テン", "デン"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(8, strokes.length())
            capture("drawing-trace")
            val pad = rule.onNode(hasContentDescription("Drawing area for the kanji", substring = true))
            pad.performScrollTo()
            for (index in 0 until strokes.length()) {
                val points = strokes.getJSONObject(index).getJSONArray("points")
                pad.performTouchInput {
                    fun point(i: Int): Offset {
                        val pair = points.getJSONArray(i)
                        return Offset(pair.getDouble(0).toFloat() * width / 109f,
                            pair.getDouble(1).toFloat() * height / 109f)
                    }
                    down(point(0))
                    for (i in 1 until points.length()) moveTo(point(i), delayMillis = 16)
                    up()
                }
            }
            rule.onNode(hasContentDescription("8 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "典" && it.mode == StudyMode.Draw.name }
            })
            await("Correct strokes").performScrollTo().assertIsDisplayed()
            capture("drawing-feedback")
            click("Next")
            await("Draw the kanji for")
            click("I don't remember")
            await("Here is the kanji")
            capture("drawing-recall-feedback")
            click("Next")
            rule.waitUntil(30_000) { runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "典" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedOnKeysPersistedGoodNoKunAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-075-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-075-article-tree.txt").writeText(rule.onRoot().printToString())
            scenario.close()
        }
    }

    private fun model(prefix: String): ViewModel? {
        var result: ViewModel? = null
        scenario.onActivity { activity ->
            result = activity.viewModelStore.keys().lastOrNull { it.startsWith(prefix) }?.let { activity.viewModelStore[it] }
        }
        return result
    }

    private fun await(text: String, substring: Boolean = false): SemanticsNodeInteraction {
        return await(hasText(text, substring = substring))
    }

    private fun await(matcher: SemanticsMatcher): SemanticsNodeInteraction {
        rule.waitUntil(30_000) { rule.onAllNodes(matcher).fetchSemanticsNodes().isNotEmpty() }
        rule.onAllNodes(matcher).assertCountEquals(1)
        return rule.onNode(matcher)
    }

    private fun readingExample(text: String): SemanticsMatcher {
        return hasText(text) and hasAnyAncestor(hasTestTag("article-body")) and
            hasAnyAncestor(SemanticsMatcher.keyIsDefined(SemanticsProperties.HorizontalScrollAxisRange))
    }

    private fun articleBullet(text: String): SemanticsMatcher {
        return hasText(text) and hasAnyAncestor(hasTestTag("article-body")) and
            !hasAnyAncestor(SemanticsMatcher.keyIsDefined(SemanticsProperties.HorizontalScrollAxisRange))
    }

    private fun click(text: String) = click(await(text))

    private fun click(node: SemanticsNodeInteraction) {
        rule.waitUntil(30_000) { !node.fetchSemanticsNode().config.contains(SemanticsProperties.Disabled) }
        if (node.onAncestors().filter(hasScrollAction()).fetchSemanticsNodes().isNotEmpty()) node.performScrollTo()
        node.assertIsDisplayed().assertIsEnabled().performClick()
    }

    private fun section(title: String) {
        rule.onNodeWithTag("article-body").performScrollToIndex(0)
        click("Article contents")
        rule.onNode(hasText(title, substring = true) and hasClickAction()).performScrollTo().performClick()
        rule.waitForIdle()
    }

    private fun show(selector: String, step: String) {
        show(hasText(selector, substring = true), step)
    }

    private fun show(matcher: SemanticsMatcher, step: String) {
        val body = rule.onNodeWithTag("article-body")
        body.performScrollToNode(matcher)
        val target = await(matcher)
        target.performScrollTo()
        val viewport = body.fetchSemanticsNode()
        val cell = target.fetchSemanticsNode()
        val top = viewport.positionInRoot.y
        val bottom = top + viewport.size.height
        if (cell.positionInRoot.y < top || cell.positionInRoot.y + cell.size.height > bottom) {
            body.performSemanticsAction(SemanticsActions.ScrollBy) {
                it(0f, cell.positionInRoot.y - top - 16f)
            }
            rule.waitForIdle()
        }
        target.assertIsDisplayed()
        capture(step)
    }

    private fun inline(node: SemanticsNodeInteraction, label: String, offset: Int) {
        node.performScrollTo().assertIsDisplayed()
        val text = node.fetchSemanticsNode().config[SemanticsProperties.Text].joinToString("") { it.text }
        val layouts = mutableListOf<TextLayoutResult>()
        node.performSemanticsAction(SemanticsActions.GetTextLayoutResult) { it(layouts) }
        assertTrue("Wrong linked offset $offset for $label in $text", offset >= 0 && text.substring(offset).startsWith(label))
        node.performTouchInput { click(layouts.single().getBoundingBox(offset).center) }
    }

    private fun back() {
        InstrumentationRegistry.getInstrumentation().uiAutomation.performGlobalAction(
            android.accessibilityservice.AccessibilityService.GLOBAL_ACTION_BACK)
        rule.waitForIdle()
    }

    private fun capture(step: String) {
        rule.waitForIdle()
        val automation = InstrumentationRegistry.getInstrumentation().uiAutomation
        automation.waitForIdle(500, 5_000)
        android.os.SystemClock.sleep(1_000)
        rule.waitForIdle()
        val bitmap = requireNotNull(automation.takeScreenshot())
        File(app.getExternalFilesDir(null), "n1-075-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
