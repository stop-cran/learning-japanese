package io.github.stopcran.kanji.ui

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Typeface
import android.os.Build
import androidx.activity.ComponentActivity
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.mutableStateOf
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
import io.github.stopcran.kanji.core.content.SafeZip
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

/** External content acceptance fixture, not a production app change or public-sync test. */
class N1PilotAcceptanceTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun n1SelectionSessionArticleBackAndDrawing() {
        assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
        assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
        app = InstrumentationRegistry.getInstrumentation().targetContext.applicationContext as KanjiApp
        val assets = InstrumentationRegistry.getInstrumentation().context.assets
        val parsed = assets.open("n1-pilot.zip").use { ContentParser.parse(SafeZip.read(it)) }
        assertTrue(parsed.problems.toString(), parsed.problems.isEmpty())
        assertTrue(parsed.grammarProblems.toString(), parsed.grammarProblems.isEmpty())
        assertEquals(997, parsed.kanji.size)
        assertEquals(17, parsed.kanji.count { it.jlpt == 1 })
        val source = RepoSource("acceptance-fixture", "n1-${UUID.randomUUID()}", "main")
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        val head = "1".repeat(40)
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> assets.open("n1-pilot.zip")
                else -> error("Unexpected fixture request: $url")
            }
            object : ContentResponse {
                override val code = 200
                override val body = input
                override fun header(name: String): String? = null
                override fun close() = input.close()
            }
        }
        val sync = runBlocking { ContentSync(app.db, app.settings.sync, http).sync(source, force = true) }
        assertTrue(sync.toString(), sync is SyncResult.Updated)
        assertTrue((sync as SyncResult.Updated).problems.isEmpty())
        app.settings.sync.lastCheckMs = System.currentTimeMillis()
        app.settings.setStartingGuideVisible(false)
        app.settings.setDailyNewCards(50)
        app.settings.setWeekPlan("FFFFFFF")
        app.settings.setTraceNew(true)
        app.settings.setVaryFonts(true)
        app.settings.setStack("jlpt-n5")
        val now = System.currentTimeMillis()
        runBlocking {
            app.db.withTransaction {
                app.db.content().kanji(source.id).filter { it.jlpt == 1 }.forEach { card ->
                    app.db.reviews().putState(ReviewStateEntity(
                        source.id, "jlpt-n1", card.kanji, StudyMode.Quiz.name, "Review", 30.0, 5.0,
                        if (card.kanji == "莉") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "鷹", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val evidence = JSONObject().put("contentVersion", parsed.manifest.contentVersion)
            .put("transport", "Complete git archive through production ContentSync, synthetic source/HEAD")
            .put("hardware", Build.HARDWARE).put("fingerprint", Build.FINGERPRINT)
            .put("sdk", Build.VERSION.SDK_INT).put("fontScale", app.resources.configuration.fontScale)
            .put("phoneEvidence", false)
            .put("fixture", "Other N1 meanings postponed; 莉 due. Two historical good 鷹 meaning logs unlock drawing. No drawing state seeded.")
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(20_000) { app.settings.stack.value == "jlpt-n1" }
            rule.onNodeWithText("N1 · 17 cards").assertIsDisplayed()
            capture("selection")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(20_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("莉", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("jasmine in compounds")
            await("Correct!")
            val paragraph = rule.onNodeWithText("莉 is a character used", substring = true).performScrollTo()
            val text = paragraph.fetchSemanticsNode().config[SemanticsProperties.Text].joinToString("") { it.text }
            val layouts = mutableListOf<TextLayoutResult>()
            paragraph.performSemanticsAction(SemanticsActions.GetTextLayoutResult) { it(layouts) }
            val offset = text.indexOf("茉莉花")
            assertTrue(offset >= 0)
            paragraph.performTouchInput { click(layouts.single().getBoundingBox(offset).center) }
            await("茉莉花 (まつりか) - Arabian jasmine")
            capture("support-article")
            systemBack()
            await("Correct!")
            assertSame(quiz, model("quiz:"))
            assertEquals("莉", (quiz.ui as QuizUi.Answer).card.kanji)
            evidence.put("articleBackPreservedAnswer", true)
            capture("article-back")
            systemBack()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            rule.onNodeWithText("hawk; falcon").assertIsDisplayed()
            val card = runBlocking { app.db.content().kanji(source.id).single { it.kanji == "鷹" } }
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(24, strokes.length())
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
            rule.onNode(hasContentDescription("24 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            rule.onNodeWithText("Correct strokes").performScrollTo().assertIsDisplayed()
            capture("drawing-feedback")
            click("Next")
            await("Draw the kanji for")
            click("I don't remember")
            await("Here is the kanji")
            capture("drawing-recall-feedback")
            click("Next")
            rule.waitUntil(20_000) {
                runBlocking { app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "鷹" && it.mode == StudyMode.Draw.name } }
            }
            evidence.put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-native-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-native-route-tree.txt").writeText(rule.onRoot().printToString())
            scenario.close()
        }
    }

    private fun model(prefix: String): ViewModel? {
        var result: ViewModel? = null
        scenario.onActivity { activity ->
            result = activity.viewModelStore.keys().lastOrNull { it.startsWith(prefix) }
                ?.let { activity.viewModelStore[it] }
        }
        return result
    }
    private fun await(text: String) {
        rule.waitUntil(30_000) { rule.onAllNodesWithText(text).fetchSemanticsNodes().isNotEmpty() }
    }
    private fun click(text: String) = click(rule.onNodeWithText(text))
    private fun click(node: SemanticsNodeInteraction) {
        rule.waitUntil(30_000) { node.fetchSemanticsNodesSafe() }
        rule.waitUntil(30_000) {
            node.isDisplayed() || node.onAncestors().filter(hasScrollAction()).fetchSemanticsNodes().isNotEmpty()
        }
        val scrollParents = node.onAncestors().filter(hasScrollAction())
        for (index in scrollParents.fetchSemanticsNodes().indices.reversed()) {
            val parent = scrollParents[index]
            if (parent.onAncestors().filter(hasScrollAction()).fetchSemanticsNodes().isNotEmpty()) {
                parent.performScrollTo()
            }
        }
        if (scrollParents.fetchSemanticsNodes().isNotEmpty()) node.performScrollTo()
        node.assertIsDisplayed().assertIsEnabled().performClick()
    }
    private fun SemanticsNodeInteraction.fetchSemanticsNodesSafe() =
        try { fetchSemanticsNode(); true } catch (_: AssertionError) { false }
    private fun systemBack() {
        InstrumentationRegistry.getInstrumentation().uiAutomation.performGlobalAction(
            android.accessibilityservice.AccessibilityService.GLOBAL_ACTION_BACK)
        rule.waitForIdle()
    }
    private fun capture(step: String) {
        rule.waitForIdle()
        val bitmap = requireNotNull(InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot())
        File(app.getExternalFilesDir(null), "n1-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}

class N1FallbackInspectionTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun allFortyFallbacksAndPilotRadicals() {
        assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
        assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val chars = "侑凜勁奎崚彗昴晏晟晨暉栞椰毬洵洸滉漱澪熙燎燿瑶皓眸笙綸綺翔脩茉莉菫詢諄赳迪頌颯黎".map { it.toString() }
        assertEquals(40, chars.size)
        val pages = chars.chunked(8) + listOf(listOf("干", "氏", "手", "凵", "丿", "矛", "鳥", "彐"),
            listOf("水", "木", "艸", "扌", "氵", "艹", "凜凛", "瑶瑤"))
        val page = mutableStateOf(0)
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(20.dp)) {
                    Text("N1 native fallback ${page.value + 1}/${pages.size}")
                    Text("Gothic / Mincho / Textbook / Brush", fontSize = 12.sp)
                    pages[page.value].forEach { char ->
                        Row(Modifier.fillMaxWidth().padding(vertical = 5.dp)) {
                            fonts.forEach { font ->
                                Column(Modifier.weight(1f)) {
                                    Text(char.codePoints().toArray().joinToString("+") { it.toString(16).uppercase() }, fontSize = 10.sp)
                                    Text(char, fontSize = if (char.length == 1) 46.sp else 25.sp,
                                        lineHeight = 52.sp, fontFamily = font.family())
                                }

                            }
                        }
                    }
                }
            }
        }
        val rows = JSONArray()
        val typefaces = listOf(Typeface.DEFAULT,
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_mincho)),
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_textbook)),
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_brush)))
        for ((fontIndex, typeface) in typefaces.withIndex()) {
            val hashes = mutableSetOf<String>()
            for (char in chars) {
                val paint = Paint(Paint.ANTI_ALIAS_FLAG).also {
                    it.typeface = typeface
                    it.textSize = 96f
                    it.textLocale = java.util.Locale.JAPAN
                }
                assertTrue("$char ${fonts[fontIndex]}", paint.hasGlyph(char))
                val image = Bitmap.createBitmap(128, 128, Bitmap.Config.ARGB_8888)
                Canvas(image).drawText(char, 8f, 104f, paint)
                val pixels = IntArray(128 * 128)
                image.getPixels(pixels, 0, 128, 0, 0, 128, 128)
                val bytes = java.nio.ByteBuffer.allocate(pixels.size * 4).also { it.asIntBuffer().put(pixels) }.array()
                val hash = MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it) }
                assertTrue("Duplicate fallback raster $char ${fonts[fontIndex]}", hashes.add(hash))
                rows.put(JSONObject().put("character", char).put("font", fonts[fontIndex].name)
                    .put("hasGlyph", true).put("nativePaintRasterSha256", hash))
                image.recycle()
            }
        }
        pages.indices.forEach { index ->
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            File(context.getExternalFilesDir(null), "n1-font-page-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("limits", "Native Paint probes and Compose screenshots; visual inspection recorded separately. Emulator, not phone.")
            .toString(2))
    }
}
