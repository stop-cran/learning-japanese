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

private fun disposable053() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch053GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun thirdStemLookalikesAcrossFourProductionFamilies() {
        disposable053()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "丙 内 肉 病"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 053: third rank / heavenly stem / look-alikes")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 28.sp, lineHeight = 40.sp)
                    }
                    Text("Compare 丙 with 内, 肉 and 病. The separate top bar distinguishes 丙 from 内.", fontSize = 18.sp)
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
            for (char in listOf("丙", "内", "肉", "病")) {
                val paint = Paint(Paint.ANTI_ALIAS_FLAG).also {
                    it.typeface = typeface
                    it.textSize = 96f
                    it.textLocale = java.util.Locale.JAPAN
                }
                assertTrue("$char ${fonts[index]}", paint.hasGlyph(char))
                val image = Bitmap.createBitmap(128, 128, Bitmap.Config.ARGB_8888)
                Canvas(image).drawText(char, 8f, 104f, paint)
                val pixels = IntArray(128 * 128)
                image.getPixels(pixels, 0, 128, 0, 0, 128, 128)
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
        }
        rule.waitForIdle()
        rule.onAllNodesWithText(text).assertCountEquals(4)
        for (index in fonts.indices) rule.onAllNodesWithText(text)[index].assertIsDisplayed()
        File(context.getExternalFilesDir(null), "n1-053-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-053-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("limits", "Sixteen native Paint probes and four production Compose rows; visual inspection separate. Emulator, not phone. Cmap presence alone does not certify readability.")
            .toString(2))
    }
}

class N1Batch053ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineThirdStemArticlesBothReadingsDrawingAndSystemBack() {
        disposable053()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-053-${UUID.randomUUID()}", "main")
        val head = "93c55a2c17bd61123e2a5bacf1ff47a5c2ad48cf"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-053-93c55a2c-envelope.zip")
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
        assertEquals(1065, updated.kanji)
        assertEquals(5023, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("ba2d74eac9ea12e1", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(85, n1.size)
        val thirdStem = n1.single { it.kanji == "丙" }
        assertEquals(listOf("ヘイ"), thirdStem.onyomi.splitSep())
        assertEquals(listOf("ひのえ"), thirdStem.kunyomi.splitSep())
        assertNotNull(thirdStem.quizOnyomi)
        assertNotNull(thirdStem.quizKunyomi)
        assertEquals(listOf("ヘイ"), thirdStem.quizOnyomi?.splitSep())
        assertEquals(listOf("ひのえ"), thirdStem.quizKunyomi?.splitSep())
        assertEquals(listOf("へい"), thirdStem.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("ひのえ"), thirdStem.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "丙") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "丙") now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "丙", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(thirdStem.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(thirdStem.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(thirdStem.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(thirdStem.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 丙 meaning and both へい/ひのえ keys due. Both kinds must execute in one session, without assuming shuffled order. Two historical good 丙 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 85 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("丙")
            click("third rank; third heavenly stem")
            await("Article contents")
            await("no. 1)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("Modern-shape mnemonic", "kanji-mnemonic")
            show("Historical explanations differ", "kanji-origin-boundary")
            section("Readings")
            show("third rank; class C", "kanji-on-reading")
            show("a calendar term combining", "kanji-kun-reading")
            show("The stem can also be called", "kanji-alternate-reading")
            section("Notes")
            show("modern-shape comparisons", "kanji-lookalikes")
            show("Not the numeral three", "kanji-quantity-boundary")
            show("Pairing the two sequences", "kanji-calendar-cycle")
            section("Common words")
            inline(await("へい — the third rank or class", substring = true), "丙")
            await("丙 (へい)", substring = true)
            section("Meaning")
            show("この表では", "word-rank-example")
            section("How the kanji combine")
            show("The single character", "word-rank-component")
            inline(await("The single character", substring = true), "丙")
            await("Article contents")
            section("Meaning and origin")
            show("Modern-shape mnemonic", "backlink-kanji")
            back()
            await("The single character", substring = true).assertIsDisplayed()
            capture("system-back-rank-word")
            section("Distinctive meaning")
            show("In ranked evaluation", "word-rank-nuance")
            show("Do not read the rank-label examples", "word-rank-reading-boundary")
            back()
            await("Common words")
            inline(await("ひのえうま — Fire Horse, term 43", substring = true), "丙午")
            await("丙午 (ひのえうま)", substring = true)
            section("Meaning")
            show("2026年は丙午です", "word-calendar-example")
            show("not instructions for converting", "word-calendar-date-boundary")
            section("Synonyms and antonyms")
            show("another documented reading", "word-calendar-alternate")
            show("It is broader than", "word-calendar-horse-boundary")
            section("Distinctive meaning")
            show("does not predict", "word-calendar-prediction-boundary")
            section("How the kanji combine")
            show("associated with fire", "word-calendar-components")
            inline(await("associated with fire", substring = true), "丙")
            await("Article contents")
            section("Meaning and origin")
            show("Modern-shape mnemonic", "calendar-backlink-kanji")
            back()
            await("associated with fire", substring = true).assertIsDisplayed()
            capture("system-back-calendar-word")
            inline(await("associated with fire", substring = true), "午")
            await("Article contents")
            await("午 — noon", substring = true).assertIsDisplayed()
            capture("existing-horse-component")
            back()
            await("associated with fire", substring = true).assertIsDisplayed()
            back()
            await("Common words")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("丙", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("third rank; third heavenly stem")
            await("Correct!")
            assertEquals("丙", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
            val reading = model("kreading:") as KanjiReadingViewModel
            val exercisedKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { reading.ui is ReadingUi.Question }
                val question = reading.ui as ReadingUi.Question
                val kind = question.question.kind
                val key = if (kind == ReadingKind.On) "へい" else "ひのえ"
                assertTrue("Duplicate reading kind", exercisedKinds.add(kind))
                assertEquals("丙", question.card.kanji)
                assertEquals(key, question.question.correctKey)
                val otherKey = if (kind == ReadingKind.On) "ひのえ" else "へい"
                assertFalse(question.question.options.any { it.key == otherKey })
                capture("curated-${kind.name.lowercase()}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${kind.name.lowercase()}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "丙" &&
                        it.mode == kind.mode.name && it.reading == key && it.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), exercisedKinds)
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("third rank; third heavenly stem").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "丙") })
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(5, strokes.length())
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
            rule.onNode(hasContentDescription("5 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            await("Correct strokes").performScrollTo().assertIsDisplayed()
            capture("drawing-feedback")
            click("Next")
            await("Draw the kanji for")
            click("I don't remember")
            await("Here is the kanji")
            capture("drawing-recall-feedback")
            click("Next")
            rule.waitUntil(30_000) { runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "丙" && it.mode == StudyMode.Draw.name }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKindsAndPersistedGrades", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-053-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-053-article-tree.txt").writeText(rule.onRoot().printToString())
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
        rule.waitUntil(30_000) { rule.onAllNodesWithText(text, substring = substring).fetchSemanticsNodes().isNotEmpty() }
        return rule.onNodeWithText(text, substring = substring)
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
        val body = rule.onNodeWithTag("article-body")
        body.performScrollToNode(hasText(selector, substring = true))
        val target = await(selector, substring = true)
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

    private fun inline(node: SemanticsNodeInteraction, label: String) {
        node.performScrollTo().assertIsDisplayed()
        val text = node.fetchSemanticsNode().config[SemanticsProperties.Text].joinToString("") { it.text }
        val layouts = mutableListOf<TextLayoutResult>()
        node.performSemanticsAction(SemanticsActions.GetTextLayoutResult) { it(layouts) }
        val offset = text.indexOf(label)
        assertTrue("Missing $label in $text", offset >= 0)
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
        File(app.getExternalFilesDir(null), "n1-053-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
