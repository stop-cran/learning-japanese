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

private fun disposable073() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch073GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun overcomeLookalikesAndIsolatedRadicalAcrossFourProductionFamilies() {
        disposable073()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "人 儿 元 兄 克 制 前 勝 口 古 困 女 己 彼 怖 恐 月 服 朝 決 洋 用 着 紙 解 話 難 克服"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 073: overcome / look-alikes / isolated radical")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect 克/古/兄/元, isolated 儿 and 己/勝/服; all authored Han and 克服. Fallback families may coincide.", fontSize = 18.sp)
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
            for (char in listOf("人", "儿", "元", "兄", "克", "制", "前", "勝", "口", "古", "困", "女", "己", "彼", "怖", "恐", "月", "服", "朝", "決", "洋", "用", "着", "紙", "解", "話", "難")) {
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
            for (word in listOf("克服")) {
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
        assertEquals(112, rows.length())
        rule.waitForIdle()
        rule.onAllNodesWithText(text).assertCountEquals(4)
        for (index in fonts.indices) rule.onAllNodesWithText(text)[index].assertIsDisplayed()
        File(context.getExternalFilesDir(null), "n1-073-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-073-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 108).put("wholeWordRasterProbes", 4)
            .put("limits", "Native Paint probes cover all27 actual authored Han including isolated 儿; four whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")
            .toString(2))
    }
}

class N1Batch073ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineOvercomeTwoReciprocalPairsOnOnlyDrawingAndSystemBack() {
        disposable073()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-073-${UUID.randomUUID()}", "main")
        val head = "5d322346c0c8bccdc36769d85f3fb23f4b5cbbee"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-073-5d322346-envelope.zip")
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
        assertEquals(1085, updated.kanji)
        assertEquals(5042, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("1d8a4ee1a97c6bb5", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(105, n1.size)
        val overcome = n1.single { it.kanji == "克" }
        assertEquals(listOf("コク"), overcome.onyomi.splitSep())
        assertEquals(listOf("か.つ"), overcome.kunyomi.splitSep())
        assertNotNull(overcome.quizOnyomi)
        assertNotNull(overcome.quizKunyomi)
        assertEquals(listOf("コク"), overcome.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), overcome.quizKunyomi?.splitSep())
        assertEquals(listOf("こく"), overcome.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), overcome.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "克") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "克" && (kind == ReadingKind.On && key == "こく")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "克", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(overcome.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(overcome.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(overcome.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(overcome.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(overcome.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(overcome.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 克 meaning and sole curated on key due; raw か.つ retained but explicit empty quiz kun. Two historical good 克 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 105 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("克")
            click("overcome")
            await("克 — overcome")
            show(articleBullet("Strokes: 7 · Key (radical): 儿 (no. 10) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("克 expresses overcoming or mastering something. In 克服 こくふく, the challenge can be a difficulty, illness, fear, or weakness."), "kanji-03")
            show(articleBullet("The modern shape has a 古-like top above the two leg-like strokes 儿, the indexing radical. Modern-shape mnemonic: picture that top standing firmly on two legs to overcome a difficulty. This is a memory aid, not a historical derivation or a phonetic analysis."), "kanji-04")
            section("Readings")
            show(readingExample("コク"), "kanji-09")
            show(readingExample("克服 こくふく — overcoming; surmounting"), "kanji-11")
            show(readingExample("か.つ"), "kanji-12")
            show(readingExample("source-only for this quiz: 克つ かつ — overcome; prevail; rare spelling of the かつ verb; 己に克つ おのれにかつ — control oneself"), "kanji-14")
            show(articleBullet("Both sourced readings remain in the metadata. Reading questions select コク only. The rarity label concerns the standalone spelling 克つ, not the pronunciation かつ. The self-control expression 己に克つ illustrates the native reading without making every use of 勝つ interchangeable with 克つ."), "kanji-15")
            section("Common words")
            show(articleBullet("克服 こくふく — overcoming; surmounting a difficulty"), "kanji-17")
            section("Notes")
            show(articleBullet("古 lacks the lower legs; 兄 has 口 above its legs, while 元 has two horizontal lines above them."), "kanji-19")
            show(articleBullet("勝 also concerns prevailing. Learn 勝つ かつ for winning a contest. 克つ appears in self-control uses such as 己に克つ; this is a useful spelling association, not an absolute division of every meaning between 克 and 勝."), "kanji-20")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Words: JMdict, entries 1285790, 1346150 and 1852770. Meaning and spelling: Daijisen, 克; Nikkoku, 勝つ・克つ."), "kanji-21")
            section("Common words")
            inline(await(articleBullet("克服 こくふく — overcoming; surmounting a difficulty")), "克服", 0)
            await("克服 (こくふく) - overcoming; surmounting")
            section("How the kanji combine")
            show(articleBullet("克 contributes overcoming or mastering, and 服 contributes submission or bringing under control here. The related ideas reinforce the meaning in コク + フク. 服 is not \"clothes\" in this compound."), "word-reused-07")
            section("How the kanji combine")
            inline(await(articleBullet("克 contributes overcoming or mastering, and 服 contributes submission or bringing under control here. The related ideas reinforce the meaning in コク + フク. 服 is not \"clothes\" in this compound.")), "克", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("克服 こくふく — overcoming; surmounting"), "word-kanji-backlink")
            back()
            await(articleBullet("克 contributes overcoming or mastering, and 服 contributes submission or bringing under control here. The related ideas reinforce the meaning in コク + フク. 服 is not \"clothes\" in this compound.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-word-kanji")
            section("How the kanji combine")
            inline(await(articleBullet("克 contributes overcoming or mastering, and 服 contributes submission or bringing under control here. The related ideas reinforce the meaning in コク + フク. 服 is not \"clothes\" in this compound.")), "服", 43)
            await("服 — clothing")
            section("Meaning and origin")
            show(articleBullet("服 is central to words for clothes. In other vocabulary it also relates to taking medicine or obeying; do not translate it as \"clothing\" in every compound. In 克服 こくふく, \"overcoming; surmounting,\" it contributes bringing under control, not clothes."), "clothing-reused-03")
            section("Meaning and origin")
            inline(await(articleBullet("服 is central to words for clothes. In other vocabulary it also relates to taking medicine or obeying; do not translate it as \"clothing\" in every compound. In 克服 こくふく, \"overcoming; surmounting,\" it contributes bringing under control, not clothes.")), "克服", 158)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("克 contributes overcoming or mastering, and 服 contributes submission or bringing under control here. The related ideas reinforce the meaning in コク + フク. 服 is not \"clothes\" in this compound."), "clothing-word-backlink")
            back()
            await(articleBullet("服 is central to words for clothes. In other vocabulary it also relates to taking medicine or obeying; do not translate it as \"clothing\" in every compound. In 克服 こくふく, \"overcoming; surmounting,\" it contributes bringing under control, not clothes.")).assertIsDisplayed()
            section("Meaning and origin")
            capture("system-back-clothing-word")
            back()
            await(articleBullet("克 contributes overcoming or mastering, and 服 contributes submission or bringing under control here. The related ideas reinforce the meaning in コク + フク. 服 is not \"clothes\" in this compound.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-word-clothing")
            back()
            await(articleBullet("克服 こくふく — overcoming; surmounting a difficulty")).assertIsDisplayed()
            section("Common words")
            capture("system-back-kanji-word")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("克", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("overcome")
            await("Correct!")
            assertEquals("克", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("克", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                assertEquals(ReadingKind.On, question.question.kind)
                val key = "こく"
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(key, question.question.correctKey)
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-${question.question.kind}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (question.question.kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${question.question.kind}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "克" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "克" && it.mode == ReadingKind.Kun.mode.name }
            })
            capture("curated-on-only-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("overcome").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "克") })
            assertEquals(listOf("コク"), card.onyomi.splitSep())
            assertEquals(listOf("か.つ"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("コク"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(7, strokes.length())
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
            rule.onNode(hasContentDescription("7 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "克" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "克" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("soleCuratedOnPersistedGoodNoKunAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-073-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-073-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-073-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
