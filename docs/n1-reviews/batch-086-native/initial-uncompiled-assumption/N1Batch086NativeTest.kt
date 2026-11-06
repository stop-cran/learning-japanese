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
import io.github.stopcran.kanji.core.quiz.QuizBuilder
import io.github.stopcran.kanji.core.quiz.QuizCard
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

private fun disposable086() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch086GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun commonplaceLookalikesAndRadicalFallbacksAcrossFourProductionFamilies() {
        disposable086()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("丶 丸 九 使 例 全 几 凡 凹 判 前 号 味 図 地 平 意 明 書 概 注 確 筆 解", "記 認 説 読 論 辞 鍵", "凡 丸 九 凹 几 丶 平凡 凡例 凡そ 凡て")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 086: commonplace / look-alikes / radical fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 31 scoped Han; focused 凡/丸/九/凹, 丶/几. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("丶", "丸", "九", "使", "例", "全", "几", "凡", "凹", "判", "前", "号", "味", "図", "地", "平", "意", "明", "書", "概", "注", "確", "筆", "解", "記", "認", "説", "読", "論", "辞", "鍵")) {
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
            for (word in listOf("平凡", "凡例", "凡そ", "凡て")) {
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
        assertEquals(140, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-086-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-086-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 124).put("wholeWordRasterProbes", 16).put("panels", 3)
            .put("limits", "31 actual scoped Han including exact 丶/几 fallback inspection, four production families, three bounded Compose panels and sixteen whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch086ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineCommonplaceSevenReciprocalPairsTwoOnKeysNoKunDrawingAndSystemBack() {
        disposable086()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-086-${UUID.randomUUID()}", "main")
        val head = "6667318d9d5bdf8ec8c899db64395e2955612432"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-086-6667318d-envelope.zip")
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
        assertEquals(1109, updated.kanji)
        assertEquals(5064, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("86e8cb13aa72ecd0", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(118, n1.size)
        val commonplace = n1.single { it.kanji == "凡" }
        assertEquals(listOf("丸", "九", "凹"), commonplace.distractors.splitSep())
        assertEquals(listOf("ボン", "ハン"), commonplace.onyomi.splitSep())
        assertEquals(listOf("およ.そ", "おうよ.そ", "すべ.て"), commonplace.kunyomi.splitSep())
        assertNotNull(commonplace.quizOnyomi)
        assertNotNull(commonplace.quizKunyomi)
        assertEquals(listOf("ボン", "ハン"), commonplace.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), commonplace.quizKunyomi?.splitSep())
        assertEquals(listOf("ぼん", "はん"), commonplace.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), commonplace.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "凡" to "commonplace; mediocre", "丸" to "round; circle",
            "九" to "nine", "凹" to "concave; sunken",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "凡" }
            assertEquals(listOf("丸", "九", "凹"), target.distractors)
            assertEquals(expectedMeanings, cards.filter { it.kanji in expectedMeanings }.associate { it.kanji to it.title })
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(604))
            assertEquals(4, options.size)
            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("allThreeCuratedAvailable", true).put("defaultFourNoPadding", true))
        }
        val importedLegend = requireNotNull(runBlocking { app.db.content().word(source.id, "凡例") })
        assertEquals(listOf("注", "説明", "解説", "メモ", "筆記", "はじめに", "概論", "鍵"), importedLegend.quizExclusions.splitSep())
        assertEquals("はんれい", importedLegend.reading)
        assertNull(importedLegend.jlpt)
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
                        if (card.kanji == "凡") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "凡" && kind == ReadingKind.On && key in setOf("ぼん", "はん")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "凡", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("directWordGuardCount", importedLegend.quizExclusions.splitSep().size)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(commonplace.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(commonplace.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(commonplace.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(commonplace.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(commonplace.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(commonplace.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 凡 meaning and exactly onぼん/はん due; explicit kun[] gives no questions. Two historical good 凡 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 118 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("凡")
            click("commonplace; mediocre")
            await("凡 — commonplace; mediocre")
            show(articleBullet("Strokes: 3 · Key (radical): 几 (no. 16) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("凡 can express being ordinary or unremarkable, as in 平凡 へいぼん. It also has a broader general or overall association, used in 凡例 はんれい, a book's explanatory conventions or a map's legend. Do not translate every occurrence as \"mediocre.\""), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: imagine the 几-shaped frame with one ordinary dot 丶 inside. This is a memory aid for the current shape, not a historical derivation or a claim about a phonetic component."), "kanji-04")
            section("Readings")
            show(readingExample("ボン"), "kanji-09")
            show(readingExample("平凡 へいぼん — ordinary; unremarkable"), "kanji-11")
            show(readingExample("ハン"), "kanji-12")
            show(readingExample("凡例 はんれい — explanatory notes; legend"), "kanji-14")
            show(readingExample("およ.そ"), "kanji-15")
            show(readingExample("凡そ およそ — approximately; generally; usually written in kana"), "kanji-17")
            show(readingExample("おうよ.そ"), "kanji-18")
            show(readingExample("Preserved exactly from KANJIDIC2; no verified modern word example is supplied here."), "kanji-20")
            show(readingExample("すべ.て"), "kanji-21")
            show(readingExample("凡て すべて — everything; a rare kanji spelling of the word taught under 全て"), "kanji-23")
            show(articleBullet("The two on-readings are selected for reading practice. The native readings remain recognition or lookup information here. In particular, the source-only おうよ.そ is not silently changed to おおよ.そ or treated as a verified word. In 凡そ and 凡て, the final そ and て are written outside the kanji."), "kanji-24")
            section("Common words")
            show(articleBullet("平凡 へいぼん — ordinary; unremarkable"), "kanji-26")
            show(articleBullet("凡例 はんれい — explanatory notes; legend"), "kanji-27")
            show(articleBullet("For recognition, 凡そ corresponds to usually-kana およそ. The rare spelling 凡て corresponds to 全て すべて; the pronunciation and the ordinary kana word are not thereby rare."), "kanji-28")
            section("Notes")
            show(articleBullet("Read 凡例 as はんれい, not ぼんれい. The same pronunciation also belongs to 判例 (はんれい), \"judicial precedent,\" which is a different word."), "kanji-30")
            show(articleBullet("丸 concerns roundness or a circle, and 九 means nine. Compare the position of the dot and the long outer stroke rather than treating these similar shapes as interchangeable."), "kanji-31")
            show(articleBullet("凹 describes a concave or sunken shape, not mediocrity."), "kanji-32")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word pairs: JMdict, entries 1507910, 1523690, 1523450 and 1595730. Reading allocation: Digital Daijisen, 凡."), "kanji-33")
            section("Common words")
            show(articleBullet("平凡 へいぼん — ordinary; unremarkable"), "ordinary-forward")
            inline(await(articleBullet("平凡 へいぼん — ordinary; unremarkable")), "平凡", 0)
            await("Article contents")
            await("平凡 (へいぼん) - ordinary; unremarkable")
            section("How the kanji combine")
            show(articleBullet("平 has an ordinary or level association here; 凡 (ボン) contributes common or ordinary. The overlapping contributions reinforce the idea of not standing out: ヘイ + ボン."), "ordinary-component")
            inline(await(articleBullet("平 has an ordinary or level association here; 凡 (ボン) contributes common or ordinary. The overlapping contributions reinforce the idea of not standing out: ヘイ + ボン.")), "平", 0)
            await("Article contents")
            await("平 — flat; peaceful")
            section("Common words")
            show(articleBullet("平凡 へいぼん — ordinary; unremarkable"), "ordinary-changed-reused")
            inline(await(articleBullet("平凡 へいぼん — ordinary; unremarkable")), "平凡", 0)
            await("Article contents")
            await("平凡 (へいぼん) - ordinary; unremarkable")
            back()
            await(articleBullet("平凡 へいぼん — ordinary; unremarkable")).assertIsDisplayed()
            section("Common words")
            capture("ordinary-back-to-reused-kanji")
            back()
            await(articleBullet("平 has an ordinary or level association here; 凡 (ボン) contributes common or ordinary. The overlapping contributions reinforce the idea of not standing out: ヘイ + ボン.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("ordinary-back-to-word")
            section("How the kanji combine")
            show(articleBullet("平 has an ordinary or level association here; 凡 (ボン) contributes common or ordinary. The overlapping contributions reinforce the idea of not standing out: ヘイ + ボン."), "ordinary-reverse")
            inline(await(articleBullet("平 has an ordinary or level association here; 凡 (ボン) contributes common or ordinary. The overlapping contributions reinforce the idea of not standing out: ヘイ + ボン.")), "凡", 45)
            await("Article contents")
            section("Readings")
            show(readingExample("ボン"), "ordinary-kanji-backlink")
            back()
            await(articleBullet("平 has an ordinary or level association here; 凡 (ボン) contributes common or ordinary. The overlapping contributions reinforce the idea of not standing out: ヘイ + ボン.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("ordinary-system-back-to-word")
            back()
            await(articleBullet("平凡 へいぼん — ordinary; unremarkable")).assertIsDisplayed()
            section("Common words")
            capture("ordinary-system-back-to-kanji")
            section("Common words")
            show(articleBullet("凡例 はんれい — explanatory notes; legend"), "legend-forward")
            inline(await(articleBullet("凡例 はんれい — explanatory notes; legend")), "凡例", 0)
            await("Article contents")
            await("凡例 (はんれい) — explanatory notes; legend")
            await("凡例 (はんれい) — explanatory notes; legend")
            section("Meaning")
            show(articleBullet("凡例 names explanatory conventions or usage notes, often at the beginning of a dictionary or another reference book. It can explain how to read entries, abbreviations or symbols. On a map or diagram, it means the legend explaining the symbols, not a legendary story."), "legend-02")
            show(articleBullet("辞書を使う前に、凡例を読んでください。 (じしょをつかうまえに、はんれいをよんでください。) — Please read the usage notes before using the dictionary."), "legend-03")
            show(articleBullet("地図の凡例で、記号の意味を確認しました。 (ちずのはんれいで、きごうのいみをかくにんしました。) — I checked the meanings of the symbols in the map's legend."), "legend-04")
            show(articleBullet("Both examples use the noun: 凡例を読む (はんれいをよむ), \"read the explanatory notes,\" and 地図の凡例 (ちずのはんれい), \"a map's legend.\""), "legend-05")
            section("How the kanji combine")
            show(articleBullet("凡 contributes a general or overall scope here, not a judgment of mediocrity. 例 contributes conventions or established usage, not only an individual example. Together, they concern the conventions for using or interpreting the material. The on-readings are ハン + レイ: はんれい. This association helps remember the word; it is not a historical derivation."), "legend-07")
            section("Synonyms and antonyms")
            show(articleBullet("説明 (せつめい), \"explanation,\" and 解説 (かいせつ), \"explanation; commentary,\" are broader. 注 (ちゅう) is an annotation that may explain a particular passage. A 凡例 explains conventions for the work or its symbols; it need not be a separate note on each difficult word. There is no useful direct antonym."), "legend-09")
            section("Distinctive meaning")
            show(articleBullet("Do not use 凡例 for every introductory paragraph, example or personal memo. A book's はじめに, \"introduction; preface,\" may discuss its purpose without giving the usage conventions that a 凡例 provides. Context determines whether English \"usage notes,\" \"explanatory notes,\" \"legend\" or \"key\" fits."), "legend-11")
            show(articleBullet("The homophone 判例 (はんれい) means a judicial precedent, not a map legend. Learn the whole spelling and reading rather than choosing ボン merely because it occurs in 平凡 (へいぼん)."), "legend-12")
            show(articleBullet("Dictionary: JMdict, entry 1523690, senses 1–2; Digital Daijisen, 凡例."), "legend-13")
            section("How the kanji combine")
            show(articleBullet("凡 contributes a general or overall scope here, not a judgment of mediocrity. 例 contributes conventions or established usage, not only an individual example. Together, they concern the conventions for using or interpreting the material. The on-readings are ハン + レイ: はんれい. This association helps remember the word; it is not a historical derivation."), "legend-component")
            inline(await(articleBullet("凡 contributes a general or overall scope here, not a judgment of mediocrity. 例 contributes conventions or established usage, not only an individual example. Together, they concern the conventions for using or interpreting the material. The on-readings are ハン + レイ: はんれい. This association helps remember the word; it is not a historical derivation.")), "例", 77)
            await("Article contents")
            await("例 — example; precedent")
            section("Common words")
            show(articleBullet("凡例 はんれい — explanatory notes; legend"), "legend-changed-reused")
            inline(await(articleBullet("凡例 はんれい — explanatory notes; legend")), "凡例", 0)
            await("Article contents")
            await("凡例 (はんれい) — explanatory notes; legend")
            back()
            await(articleBullet("凡例 はんれい — explanatory notes; legend")).assertIsDisplayed()
            section("Common words")
            capture("legend-back-to-reused-kanji")
            back()
            await(articleBullet("凡 contributes a general or overall scope here, not a judgment of mediocrity. 例 contributes conventions or established usage, not only an individual example. Together, they concern the conventions for using or interpreting the material. The on-readings are ハン + レイ: はんれい. This association helps remember the word; it is not a historical derivation.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("legend-back-to-word")
            section("How the kanji combine")
            show(articleBullet("凡 contributes a general or overall scope here, not a judgment of mediocrity. 例 contributes conventions or established usage, not only an individual example. Together, they concern the conventions for using or interpreting the material. The on-readings are ハン + レイ: はんれい. This association helps remember the word; it is not a historical derivation."), "legend-reverse")
            inline(await(articleBullet("凡 contributes a general or overall scope here, not a judgment of mediocrity. 例 contributes conventions or established usage, not only an individual example. Together, they concern the conventions for using or interpreting the material. The on-readings are ハン + レイ: はんれい. This association helps remember the word; it is not a historical derivation.")), "凡", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ボン"), "legend-kanji-backlink")
            back()
            await(articleBullet("凡 contributes a general or overall scope here, not a judgment of mediocrity. 例 contributes conventions or established usage, not only an individual example. Together, they concern the conventions for using or interpreting the material. The on-readings are ハン + レイ: はんれい. This association helps remember the word; it is not a historical derivation.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("legend-system-back-to-word")
            back()
            await(articleBullet("凡例 はんれい — explanatory notes; legend")).assertIsDisplayed()
            section("Common words")
            capture("legend-system-back-to-kanji")
            section("Common words")
            show(articleBullet("For recognition, 凡そ corresponds to usually-kana およそ. The rare spelling 凡て corresponds to 全て すべて; the pronunciation and the ordinary kana word are not thereby rare."), "approximate-forward")
            inline(await(articleBullet("For recognition, 凡そ corresponds to usually-kana およそ. The rare spelling 凡て corresponds to 全て すべて; the pronunciation and the ordinary kana word are not thereby rare.")), "およそ", 48)
            await("Article contents")
            await("およそ - approximately; generally")
            section("How the kanji combine")
            show(articleBullet("The word is usually written in kana. 凡そ is a recognized kanji spelling, but the practical unit to learn is the whole adverb およそ. It is not a loanword or a phrase requiring an extra particle before the number."), "approximate-reverse")
            inline(await(articleBullet("The word is usually written in kana. 凡そ is a recognized kanji spelling, but the practical unit to learn is the whole adverb およそ. It is not a loanword or a phrase requiring an extra particle before the number.")), "凡", 37)
            await("Article contents")
            section("Readings")
            show(readingExample("ボン"), "approximate-kanji-backlink")
            back()
            await(articleBullet("The word is usually written in kana. 凡そ is a recognized kanji spelling, but the practical unit to learn is the whole adverb およそ. It is not a loanword or a phrase requiring an extra particle before the number.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("approximate-system-back-to-word")
            back()
            await(articleBullet("For recognition, 凡そ corresponds to usually-kana およそ. The rare spelling 凡て corresponds to 全て すべて; the pronunciation and the ordinary kana word are not thereby rare.")).assertIsDisplayed()
            section("Common words")
            capture("approximate-system-back-to-kanji")
            section("Common words")
            show(articleBullet("For recognition, 凡そ corresponds to usually-kana およそ. The rare spelling 凡て corresponds to 全て すべて; the pronunciation and the ordinary kana word are not thereby rare."), "everything-forward")
            inline(await(articleBullet("For recognition, 凡そ corresponds to usually-kana およそ. The rare spelling 凡て corresponds to 全て すべて; the pronunciation and the ordinary kana word are not thereby rare.")), "全て", 89)
            await("Article contents")
            await("全て (すべて) - everything; all")
            section("How the kanji combine")
            show(articleBullet("全 contributes wholeness or entirety. It writes the native word すべて with て as okurigana. JMdict marks the word as usually written in kana, so すべて is an important spelling to recognize too."), "everything-component")
            inline(await(articleBullet("全 contributes wholeness or entirety. It writes the native word すべて with て as okurigana. JMdict marks the word as usually written in kana, so すべて is an important spelling to recognize too.")), "全", 0)
            await("Article contents")
            await("全 — whole; complete")
            section("Common words")
            show(articleBullet("全て すべて — everything; usually すべて"), "everything-changed-reused")
            inline(await(articleBullet("全て すべて — everything; usually すべて")), "全て", 0)
            await("Article contents")
            await("全て (すべて) - everything; all")
            back()
            await(articleBullet("全て すべて — everything; usually すべて")).assertIsDisplayed()
            section("Common words")
            capture("everything-back-to-reused-kanji")
            back()
            await(articleBullet("全 contributes wholeness or entirety. It writes the native word すべて with て as okurigana. JMdict marks the word as usually written in kana, so すべて is an important spelling to recognize too.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("everything-back-to-word")
            section("How the kanji combine")
            show(articleBullet("JMdict also records 凡て (すべて) as a rare kanji spelling. That spelling qualification does not make the pronunciation すべて rare."), "everything-reverse")
            inline(await(articleBullet("JMdict also records 凡て (すべて) as a rare kanji spelling. That spelling qualification does not make the pronunciation すべて rare.")), "凡", 20)
            await("Article contents")
            section("Readings")
            show(readingExample("ボン"), "everything-kanji-backlink")
            back()
            await(articleBullet("JMdict also records 凡て (すべて) as a rare kanji spelling. That spelling qualification does not make the pronunciation すべて rare.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("everything-system-back-to-word")
            back()
            await(articleBullet("For recognition, 凡そ corresponds to usually-kana およそ. The rare spelling 凡て corresponds to 全て すべて; the pronunciation and the ordinary kana word are not thereby rare.")).assertIsDisplayed()
            section("Common words")
            capture("everything-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 7).put("directedLinkTransitions", 14)
                .put("completeArticleProjections", 2).put("changedReusedArticles", 6)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("凡", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "凡" to "commonplace; mediocre",
                "丸" to "round; circle",
                "九" to "nine",
                "凹" to "concave; sunken",
            )
            assertEquals(4, meaning.options.size)
            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })
            assertEquals(listOf("丸", "九", "凹"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("exactCuratedChoicesWithoutFallback", true)
            capture("meaning-question")
            click("commonplace; mediocre")
            await("Correct!")
            assertEquals("凡", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("凡", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("ぼん", "はん"))
                assertTrue("Duplicate target reading key", answeredKeys.add(key))
                assertEquals(key, question.question.correctKey)
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-${key}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (question.question.kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${key}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "凡" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("ぼん", "はん"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "凡" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("ぼん", "はん"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })
            capture("curated-two-on-no-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("commonplace; mediocre").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "凡") })
            assertEquals(listOf("丸", "九", "凹"), card.distractors.splitSep())
            assertEquals(listOf("ボン", "ハン"), card.onyomi.splitSep())
            assertEquals(listOf("およ.そ", "おうよ.そ", "すべ.て"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ボン", "ハン"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(3, strokes.length())
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
            rule.onNode(hasContentDescription("3 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "凡" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "凡" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedOnKeysPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-086-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-086-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-086-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
