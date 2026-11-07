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

private fun disposable091() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch091GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun bladeLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable091()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("丁 丶 乃 傷 先 写 凸 凹 刀 刃 切 包", "日 本 物 白 真 端 縁 見 鋭", "刃 刀 丶 乃 凹 凸 丁 包 先 端 刃物")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 091: blade / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 21 scoped Han; focused 刃/刀/丶/乃/凹/凸 and 先/端. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("丁", "丶", "乃", "傷", "先", "写", "凸", "凹", "刀", "刃", "切", "包", "日", "本", "物", "白", "真", "端", "縁", "見", "鋭")) {
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
            for (word in listOf("刃物")) {
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
        assertEquals(88, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-091-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-091-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 84).put("wholeWordRasterProbes", 4).put("panels", 3)
            .put("limits", "21 actual scoped Han; 丶 absent from all three bundled cmaps requires actual system fallback inspection, four production families, three bounded Compose panels and four whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch091ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineBladeReciprocalPairOneKunNoOnDrawingForefrontAndSystemBack() {
        disposable091()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-091-${UUID.randomUUID()}", "main")
        val head = "f6b2ee397b4e2998abcef6fd747b25d6178b1fa3"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-091-f6b2ee39-envelope.zip")
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
        assertEquals(1114, updated.kanji)
        assertEquals(5070, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("cb3c857f3614485d", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(123, n1.size)
        val blade = n1.single { it.kanji == "刃" }
        assertEquals(listOf("乃", "凹", "凸"), blade.distractors.splitSep())
        assertEquals(listOf("ジン", "ニン"), blade.onyomi.splitSep())
        assertEquals(listOf("は", "やいば", "き.る"), blade.kunyomi.splitSep())
        assertNotNull(blade.quizOnyomi)
        assertNotNull(blade.quizKunyomi)
        assertEquals(emptyList<String>(), blade.quizOnyomi?.splitSep())
        assertEquals(listOf("は"), blade.quizKunyomi?.splitSep())
        assertEquals(emptyList<String>(), blade.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("は"), blade.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "刃" to "blade; cutting edge", "凸" to "convex; protruding",
            "乃" to "thereupon; possessive no", "凹" to "concave; sunken",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "刃" }
            assertEquals(listOf("乃", "凹", "凸"), target.distractors)
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(649))
            assertEquals(4, options.size)
            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            assertEquals(3, cards.count { it.kanji in target.distractors })
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("availableCuratedCount", cards.count { it.kanji in target.distractors })
                .put("fallbackOptions", options.count { it.kanji !in expectedMeanings }))
        }
        val importedBlade = requireNotNull(runBlocking { app.db.content().word(source.id, "刃") })
        assertEquals(listOf("刀", "日本刀", "端", "縁", "先端"), importedBlade.quizExclusions.splitSep())
        assertEquals("は", importedBlade.reading)
        assertNull(importedBlade.jlpt)
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
                        if (card.kanji == "刃") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "刃" && (kind == ReadingKind.Kun && key == "は")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "刃", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("directWordGuardCount", importedBlade.quizExclusions.splitSep().size)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(blade.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(blade.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(blade.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(blade.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(blade.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(blade.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 刃 meaning and kunは due, no on keys. All five raw readings retained. Two historical good 刃 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 123 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("刃")
            click("blade; cutting edge")
            await("刃 — blade; cutting edge")
            show(articleBullet("Strokes: 3 · Key (radical): 刀 (no. 18) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("刃 concerns a blade or cutting edge. The standalone word 刃 は names the cutting part of a knife or sword, not automatically the whole tool. The character also appears in words concerning swords."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Compare 刀, \"sword; blade,\" and notice the extra short inner mark, shaped like 丶. Let that mark remind you of the cutting edge. This is a memory aid for the modern shape, not a historical explanation."), "kanji-04")
            section("Readings")
            show(readingExample("ジン"), "kanji-09")
            show(readingExample("白刃 はくじん — drawn sword; the same word is also read しらは"), "kanji-11")
            show(readingExample("ニン"), "kanji-12")
            show(readingExample("刃傷 にんじょう — injury or bloodshed involving a blade; recognize the whole word"), "kanji-14")
            show(readingExample("は"), "kanji-15")
            show(readingExample("刃 は — blade; cutting edge"), "kanji-17")
            show(readingExample("やいば"), "kanji-18")
            show(readingExample("刃 やいば — blade; sword; a separate documented word reading"), "kanji-20")
            show(readingExample("き.る"), "kanji-21")
            show(readingExample("KANJIDIC2 lists this reading; no independently verified word example is established here"), "kanji-23")
            show(articleBullet("This small lesson practices は. ジン, ニン and やいば remain recognition material here; leaving them out of practice does not make them invalid or uniformly rare. The source-only き.る is not a recommendation to replace the spelling of 切る きる, \"cut,\" with an invented spelling."), "kanji-24")
            section("Common words")
            show(articleBullet("刃 は — blade; cutting edge"), "kanji-26")
            show(articleBullet("刃物 はもの — edged tool; cutting instrument"), "kanji-27")
            section("Notes")
            show(articleBullet("刀 かたな names a sword; 刃 は can name its cutting part. Learn the whole word and context rather than treating the two characters as freely interchangeable."), "kanji-29")
            show(articleBullet("乃, with connecting or particle-related uses, 凹, \"concave; sunken,\" and 凸, \"convex; protruding,\" do not share the blade/cutting-edge meaning."), "kanji-30")
            show(articleBullet("The same spelling 刃 also has the reading やいば. Its dictionary senses are not all automatically senses of the noun は."), "kanji-31")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families: JMdict, entries 1369820, 1369830, 1369840, 1369890 and 1475260. Character and lexical readings: Digital Daijisen and Seisenban Nihon Kokugo Daijiten, 刃."), "kanji-32")
            section("Common words")
            show(articleBullet("刃 は — blade; cutting edge"), "blade-forward")
            inline(await(articleBullet("刃 は — blade; cutting edge")), "刃", 0)
            await("Article contents")
            await("刃 (は) — blade; cutting edge")
            section("Meaning")
            show(articleBullet("刃 is a noun naming the blade or cutting edge of a knife, sword or similar tool. This article teaches the reading は and the physical cutting-part sense."), "blade-02")
            show(articleBullet("この包丁の刃は鋭いです。 (このほうちょうのははするどいです。) — This kitchen knife's blade is sharp."), "blade-03")
            show(articleBullet("写真では、刃がよく見えます。 (しゃしんでは、はがよくみえます。) — The blade is clearly visible in the photograph."), "blade-04")
            show(articleBullet("In 包丁の刃 (ほうちょうのは), \"the blade of a kitchen knife,\" の connects the tool with its cutting part. In 刃が見える (はがみえる), \"the blade is visible,\" が marks what is visible."), "blade-05")
            section("How the kanji combine")
            show(articleBullet("刃 represents the whole native noun は here. There is no compound to split. The same written character also has the separate word reading やいば, \"blade; sword\"; that does not make every sense under やいば a sense of は."), "blade-07")
            section("Synonyms and antonyms")
            show(articleBullet("ナイフ, \"knife,\" and 包丁 ほうちょう, \"kitchen knife,\" name whole tools. 刃 は focuses on the cutting part. Likewise, 刀 かたな and 日本刀 にほんとう name swords rather than just their cutting edges."), "blade-09")
            show(articleBullet("端 はし, \"edge; end; tip,\" and 縁 ふち, \"rim; edge,\" describe boundaries more broadly. Not every edge is a cutting edge. There is no single lexical antonym for 刃."), "blade-10")
            section("Distinctive meaning")
            show(articleBullet("English \"edge\" can mean the edge of a desk or the boundary of an area. 刃 は does not generally replace 端 or 縁 for those spatial meanings. Learn it with a cutting tool and keep the distinction between the tool and its blade."), "blade-12")
            show(articleBullet("For figurative English \"cutting edge\" meaning the forefront of a field, use words such as 先端 せんたん, not 刃 は."), "blade-13")
            show(articleBullet("Dictionary: JMdict, entry 1369820, sense 1; separate やいば family 1369830. Physical は sense: Digital Daijisen and Seisenban Nihon Kokugo Daijiten, 刃."), "blade-14")
            section("How the kanji combine")
            show(articleBullet("刃 represents the whole native noun は here. There is no compound to split. The same written character also has the separate word reading やいば, \"blade; sword\"; that does not make every sense under やいば a sense of は."), "blade-reverse")
            inline(await(articleBullet("刃 represents the whole native noun は here. There is no compound to split. The same written character also has the separate word reading やいば, \"blade; sword\"; that does not make every sense under やいば a sense of は.")), "刃", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("は"), "blade-kanji-backlink")
            back()
            await(articleBullet("刃 represents the whole native noun は here. There is no compound to split. The same written character also has the separate word reading やいば, \"blade; sword\"; that does not make every sense under やいば a sense of は.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("blade-system-back-to-word")
            section("Distinctive meaning")
            show(articleBullet("For figurative English \"cutting edge\" meaning the forefront of a field, use words such as 先端 せんたん, not 刃 は."), "forefront-forward")
            inline(await(articleBullet("For figurative English \"cutting edge\" meaning the forefront of a field, use words such as 先端 せんたん, not 刃 は.")), "先端", 90)
            await("Article contents")
            await("先端 (せんたん) - tip; leading edge")
            capture("forefront-destination")
            back()
            await(articleBullet("For figurative English \"cutting edge\" meaning the forefront of a field, use words such as 先端 せんたん, not 刃 は.")).assertIsDisplayed()
            section("Distinctive meaning")
            capture("forefront-system-back-to-word")
            back()
            await(articleBullet("刃 は — blade; cutting edge")).assertIsDisplayed()
            section("Common words")
            capture("blade-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2).put("extraForefrontTransition", true)
                .put("completeArticleProjections", 2).put("changedReusedArticles", 0)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("刃", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "刃" to "blade; cutting edge",
                "凸" to "convex; protruding",
                "乃" to "thereupon; possessive no",
                "凹" to "concave; sunken",
            )
            assertEquals(4, meaning.options.size)
            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertTrue(meaning.options.any { it.kanji == "凹" })
            assertEquals(0, meaning.options.count { it.kanji !in expectedMeanings })
            assertEquals("blade; cutting edge", meaning.options.single { it.kanji == "刃" }.title)
            assertEquals(listOf("乃", "凹", "凸"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 3).put("actualN1FallbackOptions", 0)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("blade; cutting edge")
            await("Correct!")
            assertEquals("刃", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("刃", question.card.kanji)
                assertEquals(ReadingKind.Kun, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("は"))
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "刃" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("は"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "刃" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("は"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.Kun.mode.name })
            capture("curated-one-kun-no-on-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("blade; cutting edge").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "刃") })
            assertEquals(listOf("乃", "凹", "凸"), card.distractors.splitSep())
            assertEquals(listOf("ジン", "ニン"), card.onyomi.splitSep())
            assertEquals(listOf("は", "やいば", "き.る"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(emptyList<String>(), card.quizOnyomi?.splitSep())
            assertEquals(listOf("は"), card.quizKunyomi?.splitSep())
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
                    it.kanji == "刃" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "刃" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("onlyKunHaNoOnPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-091-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-091-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-091-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
