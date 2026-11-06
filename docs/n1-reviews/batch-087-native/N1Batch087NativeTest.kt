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

private fun disposable087() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch087GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun calmSeaLookalikesAndRadicalFallbacksAcrossFourProductionFamilies() {
        disposable087()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("今 冷 几 凡 凪 凹 化 和 夕 心 方 日 時 朝 止 海 着 穏 落 静 風", "凪 風 止 几 凡 凹 凪ぐ 朝凪 夕凪")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 087: calm seas / look-alikes / radical fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 21 scoped Han; focused 凪/風/止/凡/凹, 几. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("今", "冷", "几", "凡", "凪", "凹", "化", "和", "夕", "心", "方", "日", "時", "朝", "止", "海", "着", "穏", "落", "静", "風")) {
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
            for (word in listOf("凪", "凪ぐ")) {
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
        assertEquals(92, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-087-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-087-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 84).put("wholeWordRasterProbes", 8).put("panels", 2)
            .put("limits", "21 actual scoped Han including exact 几 fallback inspection, four production families, two bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch087ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineCalmSeaTwoReciprocalPairsTwoKunKeysNoOnDrawingAndSystemBack() {
        disposable087()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-087-${UUID.randomUUID()}", "main")
        val head = "404f507d5f9d3abe4e8bdc5e72bd41ea5607c521"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-087-404f507d-envelope.zip")
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
        assertEquals(1110, updated.kanji)
        assertEquals(5066, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("eb3a9413cccd4f57", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(119, n1.size)
        val calmSea = n1.single { it.kanji == "凪" }
        assertEquals(listOf("風", "凡", "凹"), calmSea.distractors.splitSep())
        assertEquals(emptyList<String>(), calmSea.onyomi.splitSep())
        assertEquals(listOf("なぎ", "な.ぐ"), calmSea.kunyomi.splitSep())
        assertNotNull(calmSea.quizOnyomi)
        assertNotNull(calmSea.quizKunyomi)
        assertEquals(emptyList<String>(), calmSea.quizOnyomi?.splitSep())
        assertEquals(listOf("なぎ", "な.ぐ"), calmSea.quizKunyomi?.splitSep())
        assertEquals(emptyList<String>(), calmSea.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("なぎ", "なぐ"), calmSea.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "凪" to "calm seas; lull", "風" to "wind; style",
            "凡" to "commonplace; mediocre", "凹" to "concave; sunken",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "凪" }
            assertEquals(listOf("風", "凡", "凹"), target.distractors)
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(613))
            assertEquals(4, options.size)
            if (poolName == "All") {
                assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            } else {
                assertEquals(setOf("凪", "凡", "凹"), cards.filter { it.kanji in expectedMeanings }.map { it.kanji }.toSet())
                assertTrue(options.any { it.kanji == "凹" })
                assertEquals(1, options.count { it.kanji !in expectedMeanings })
            }
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("availableCuratedCount", cards.count { it.kanji in target.distractors })
                .put("fallbackOptions", options.count { it.kanji !in expectedMeanings }))
        }
        val importedNoun = requireNotNull(runBlocking { app.db.content().word(source.id, "凪") })
        val importedVerb = requireNotNull(runBlocking { app.db.content().word(source.id, "凪ぐ") })
        assertEquals(listOf("穏やか", "静か"), importedNoun.quizExclusions.splitSep())
        assertEquals(listOf("静まる", "止む", "落ち着く", "穏やか", "静か"), importedVerb.quizExclusions.splitSep())
        assertEquals("なぎ", importedNoun.reading)
        assertEquals("なぐ", importedVerb.reading)
        assertNull(importedNoun.jlpt)
        assertNull(importedVerb.jlpt)
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
                        if (card.kanji == "凪") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "凪" && kind == ReadingKind.Kun && key in setOf("なぎ", "なぐ")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "凪", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("directWordGuardCount", importedNoun.quizExclusions.splitSep().size + importedVerb.quizExclusions.splitSep().size)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(calmSea.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(calmSea.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(calmSea.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(calmSea.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(calmSea.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(calmSea.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 凪 meaning and exactly kunなぎ/なぐ due; explicit on[] gives no questions. Two historical good 凪 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 119 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("凪")
            click("calm seas; lull")
            await("凪 — calm seas; lull")
            show(articleBullet("Strokes: 6 · Key (radical): 几 (no. 16) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("凪 concerns a lull in the wind and calm conditions at sea. The noun 凪 なぎ names the calm; the verb 凪ぐ なぐ describes the wind or sea becoming calm. This is not a general translation of every English use of \"calm.\""), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: picture the outer frame of 風, \"wind,\" with 止, \"stop,\" inside: the wind has stopped. The indexing radical is 几, the frame, not the whole character 風."), "kanji-04")
            show(articleBullet("Digital Daijisen identifies 凪 as a kokuji, a character created in Japan. The mnemonic above is a memory aid for its modern shape, not a detailed historical derivation."), "kanji-05")
            section("Readings")
            show(readingExample("なぎ"), "kanji-10")
            show(readingExample("凪 なぎ — calm at sea; lull"), "kanji-12")
            show(readingExample("な.ぐ"), "kanji-13")
            show(readingExample("凪ぐ なぐ — become calm (wind/sea)"), "kanji-15")
            show(articleBullet("Both native readings are selected for practice. In 凪ぐ, 凪 writes な and the ending ぐ stays outside the kanji. No on-reading is supplied in the source metadata."), "kanji-16")
            section("Common words")
            show(articleBullet("凪 なぎ — calm at sea; lull"), "kanji-18")
            show(articleBullet("凪ぐ なぐ — become calm (wind/sea)"), "kanji-19")
            show(articleBullet("For recognition, 朝凪 (あさなぎ) is the morning calm over the sea, and 夕凪 (ゆうなぎ) is the evening calm. These are whole-word readings."), "kanji-20")
            section("Notes")
            show(articleBullet("Distinguish the noun なぎ from the dictionary-form verb なぐ: 凪です (なぎです), \"it is calm at sea,\" versus 風が凪ぐ (かぜがなぐ), \"the wind dies down.\""), "kanji-22")
            show(articleBullet("風 concerns wind or style, not the lull itself. 凡 has a dot inside its frame and concerns the ordinary or general; 凹 describes a concave or sunken shape."), "kanji-23")
            show(articleBullet("Grade 9 is the source's name-use classification, not a claim that 凪 occurs only in names. The weather noun and verb above are not names."), "kanji-24")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word pairs: JMdict, entries 1459650, 1459660, 1696000 and 1739920. Usage: Digital Daijisen, 凪 and 凪ぐ."), "kanji-25")
            section("Common words")
            show(articleBullet("凪 なぎ — calm at sea; lull"), "noun-forward")
            inline(await(articleBullet("凪 なぎ — calm at sea; lull")), "凪", 0)
            await("Article contents")
            await("凪 (なぎ) — calm at sea; lull")
            section("Meaning")
            show(articleBullet("凪 is a noun for a lull in the wind, especially the calm conditions at sea when the wind has died down. It names a weather condition, not a person's composure."), "noun-02")
            show(articleBullet("今日は凪です。 (きょうはなぎです。) — It is calm at sea today."), "noun-03")
            show(articleBullet("夕凪の海は静かだった。 (ゆうなぎのうみはしずかだった。) — The sea was still in the evening calm."), "noun-04")
            show(articleBullet("朝凪 (あさなぎ) means the morning calm over the sea; 夕凪 (ゆうなぎ) means the evening calm. A lull can be temporary; the word does not promise that the sea will remain calm all day."), "noun-05")
            section("How the kanji combine")
            show(articleBullet("This is one native word written with 凪, not a multi-kanji compound. The whole character writes なぎ. Compare the related verb 凪ぐ (なぐ), \"become calm (wind/sea).\""), "noun-07")
            section("Synonyms and antonyms")
            show(articleBullet("穏やか (おだやか) and 静か (しずか) can describe calm sea conditions, but they are な-adjectives with broader uses. 凪 is a noun: 凪です (なぎです), rather than treating it as a な-adjective. 時化 (しけ), \"stormy weather at sea,\" is a contrasting noun; JMdict marks that word as usually written in kana."), "noun-09")
            section("Distinctive meaning")
            show(articleBullet("For a person's cool-headedness, 冷静 (れいせい) is more appropriate than using 凪 as a general equivalent of English \"calm.\" 凪 focuses here on wind and sea conditions. To describe the change into those conditions, use 凪ぐ, not the noun alone as a verb."), "noun-11")
            show(articleBullet("Dictionary: JMdict, entries 1459650, 1696000, 1739920 and 1816340. Usage: Digital Daijisen and Nipponica, 凪."), "noun-12")
            section("How the kanji combine")
            show(articleBullet("This is one native word written with 凪, not a multi-kanji compound. The whole character writes なぎ. Compare the related verb 凪ぐ (なぐ), \"become calm (wind/sea).\""), "noun-reverse")
            inline(await(articleBullet("This is one native word written with 凪, not a multi-kanji compound. The whole character writes なぎ. Compare the related verb 凪ぐ (なぐ), \"become calm (wind/sea).\"")), "凪", 37)
            await("Article contents")
            section("Readings")
            show(readingExample("なぎ"), "noun-kanji-backlink")
            back()
            await(articleBullet("This is one native word written with 凪, not a multi-kanji compound. The whole character writes なぎ. Compare the related verb 凪ぐ (なぐ), \"become calm (wind/sea).\"")).assertIsDisplayed()
            section("How the kanji combine")
            capture("noun-system-back-to-word")
            back()
            await(articleBullet("凪 なぎ — calm at sea; lull")).assertIsDisplayed()
            section("Common words")
            capture("noun-system-back-to-kanji")
            section("Common words")
            show(articleBullet("凪ぐ なぐ — become calm (wind/sea)"), "verb-forward")
            inline(await(articleBullet("凪ぐ なぐ — become calm (wind/sea)")), "凪ぐ", 0)
            await("Article contents")
            await("凪ぐ (なぐ) — become calm (wind/sea)")
            section("Meaning")
            show(articleBullet("凪ぐ is an intransitive godan verb: the wind dies down or the sea becomes calm. The wind or sea is the subject, marked with が; this is not a verb for someone actively calming another person."), "verb-02")
            show(articleBullet("夕方、風が凪いだ。 (ゆうがた、かぜがないだ。) — The wind died down in the evening."), "verb-03")
            show(articleBullet("凪いだ海は静かだった。 (ないだうみはしずかだった。) — The sea was still after it had calmed."), "verb-04")
            show(articleBullet("The ぐ ending changes as in other gu-ending godan verbs: 凪ぎます (なぎます), 凪がない (ながない), 凪いで (ないで), and 凪いだ (ないだ). In 凪いだ海 (ないだうみ), the past form describes the sea that has become calm."), "verb-05")
            section("How the kanji combine")
            show(articleBullet("凪 supplies the calm-wind/sea association and writes な; ぐ is written outside the kanji. This is one native verb, not a multi-kanji compound. The related noun 凪 is read なぎ: 凪です (なぎです), \"it is calm at sea.\""), "verb-07")
            section("Synonyms and antonyms")
            show(articleBullet("止む (やむ), \"cease; let up,\" can also describe wind stopping. 静まる (しずまる), \"quiet down; subside,\" is broader than this weather verb. Neither is an unrestricted replacement in every sentence. The noun 時化 (しけ), \"stormy weather at sea,\" provides a contrasting condition, not an opposite verb with the same conjugation."), "verb-09")
            section("Distinctive meaning")
            show(articleBullet("This article teaches the modern weather verb 凪ぐ. Dictionaries distinguish 和ぐ (なぐ), for a mind or feelings becoming calm; do not transfer the example 心が和ぐ (こころがなぐ), \"one's heart becomes calm,\" to the ordinary weather spelling taught here. For regaining personal composure, 落ち着く (おちつく) is a useful broader comparison."), "verb-11")
            show(articleBullet("Dictionary: JMdict, entries 1459660, 1459650, 1310640, 1594270, 1816340 and 2859999. Usage: Digital Daijisen, 凪ぐ／和ぐ, modern godan senses; the separate classical conjugation is not taught here."), "verb-12")
            section("How the kanji combine")
            show(articleBullet("凪 supplies the calm-wind/sea association and writes な; ぐ is written outside the kanji. This is one native verb, not a multi-kanji compound. The related noun 凪 is read なぎ: 凪です (なぎです), \"it is calm at sea.\""), "verb-reverse")
            inline(await(articleBullet("凪 supplies the calm-wind/sea association and writes な; ぐ is written outside the kanji. This is one native verb, not a multi-kanji compound. The related noun 凪 is read なぎ: 凪です (なぎです), \"it is calm at sea.\"")), "凪", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("なぎ"), "verb-kanji-backlink")
            back()
            await(articleBullet("凪 supplies the calm-wind/sea association and writes な; ぐ is written outside the kanji. This is one native verb, not a multi-kanji compound. The related noun 凪 is read なぎ: 凪です (なぎです), \"it is calm at sea.\"")).assertIsDisplayed()
            section("How the kanji combine")
            capture("verb-system-back-to-word")
            back()
            await(articleBullet("凪ぐ なぐ — become calm (wind/sea)")).assertIsDisplayed()
            section("Common words")
            capture("verb-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)
                .put("completeArticleProjections", 3).put("changedReusedArticles", 0)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("凪", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "凪" to "calm seas; lull",
                "風" to "wind; style",
                "凡" to "commonplace; mediocre",
                "凹" to "concave; sunken",
            )
            assertEquals(4, meaning.options.size)
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertTrue(meaning.options.any { it.kanji == "凹" })
            assertEquals(1, meaning.options.count { it.kanji !in expectedMeanings })
            assertEquals("calm seas; lull", meaning.options.single { it.kanji == "凪" }.title)
            assertEquals(listOf("風", "凡", "凹"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 2).put("actualN1FallbackOptions", 1)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("calm seas; lull")
            await("Correct!")
            assertEquals("凪", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("凪", question.card.kanji)
                assertEquals(ReadingKind.Kun, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("なぎ", "なぐ"))
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "凪" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("なぎ", "なぐ"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "凪" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("なぎ", "なぐ"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.Kun.mode.name })
            capture("curated-two-kun-no-on-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("calm seas; lull").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "凪") })
            assertEquals(listOf("風", "凡", "凹"), card.distractors.splitSep())
            assertEquals(emptyList<String>(), card.onyomi.splitSep())
            assertEquals(listOf("なぎ", "な.ぐ"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(emptyList<String>(), card.quizOnyomi?.splitSep())
            assertEquals(listOf("なぎ", "な.ぐ"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(6, strokes.length())
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
            rule.onNode(hasContentDescription("6 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "凪" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "凪" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKunKeysPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-087-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-087-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-087-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
