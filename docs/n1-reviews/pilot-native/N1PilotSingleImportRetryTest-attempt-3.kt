package io.github.stopcran.kanji.ui

import android.graphics.Bitmap
import android.net.ConnectivityManager
import android.os.Build
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.semantics.SemanticsActions
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createEmptyComposeRule
import androidx.compose.ui.text.TextLayoutResult
import androidx.lifecycle.ViewModel
import androidx.room.withTransaction
import androidx.test.core.app.ActivityScenario
import androidx.test.platform.app.InstrumentationRegistry
import io.github.stopcran.kanji.KanjiApp
import io.github.stopcran.kanji.MainActivity
import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.content.RepoSource
import io.github.stopcran.kanji.core.reading.ReadingKind
import io.github.stopcran.kanji.core.srs.StudyMode
import io.github.stopcran.kanji.data.*
import kotlinx.coroutines.runBlocking
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import java.io.ByteArrayInputStream
import java.io.File
import java.util.UUID

/** Disposable native acceptance only; the complete archive is parsed once, inside production ContentSync. */
class N1PilotSingleImportRetryTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun completeArchiveN1OfflineMeaningCuratedReadingDrawingArticleAndBack() {
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
        assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val assets = instrumentation.context.assets
        val source = RepoSource("acceptance-fixture", "n1-retry-${UUID.randomUUID()}", "main")
        val head = "79360e975ccf54cb484994ddc2632b2c7dabc6b1"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    assets.open("n1-pilot-single-import-79360e9.zip")
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
        assertEquals(997, updated.kanji)
        assertEquals(4951, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("92c2025be954cf03", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(17, n1.size)
        val rinse = n1.single { it.kanji == "漱" }
        assertEquals("", rinse.quizOnyomi)
        assertEquals("うがい", rinse.quizKunyomi)
        assertEquals(listOf("うがい"), rinse.toReadingCard().quizKeys(ReadingKind.Kun))
        assertTrue(rinse.toReadingCard().quizKeys(ReadingKind.On).isEmpty())
        assertEquals(4, rinse.kunyomi.splitSep().size)
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
                        if (card.kanji == "莉") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "漱" && kind == ReadingKind.Kun && key == "うがい") now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "鷹", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Host must disable disposable emulator Wi-Fi/data before this offline check", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("transport", "Complete git archive through production ContentSync ONCE; synthetic source/HEAD")
            .put("hardware", Build.HARDWARE).put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("phoneEvidence", false).put("offlineActiveNetwork", JSONObject.NULL)
            .put("fixture", "Other N1 meanings/readings postponed; 莉 meaning and 漱/うがい due. Two historical good 鷹 meaning logs unlock drawing. No drawing state seeded.")
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(20_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 17 cards")
            rule.onNodeWithText("N1 · 17 cards").performScrollTo().assertIsDisplayed()
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
            evidence.put("meaningArticleBackPreservedAnswer", true)
            capture("article-back")
            systemBack()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            rule.waitUntil(20_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
            val reading = model("kreading:") as KanjiReadingViewModel
            val question = reading.ui as ReadingUi.Question
            assertEquals("漱", question.card.kanji)
            assertEquals(ReadingKind.Kun, question.question.kind)
            assertEquals("うがい", question.question.correctKey)
            capture("curated-reading-question")
            click(question.question.options.single { it.key == "うがい" }.label)
            await("Correct! — kun'yomi")
            assertTrue((reading.ui as ReadingUi.Answer).correct)
            capture("curated-reading-feedback")
            click("Next")
            rule.waitUntil(20_000) { runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "漱" &&
                    it.mode == StudyMode.KanjiKun.name && it.reading == "うがい" && it.grade == 3 }
            } }
            evidence.put("curatedKunQuestionAndPersistedGrade", true)
            systemBack()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            rule.onNodeWithText("hawk; falcon").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "鷹") })
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
            rule.waitUntil(20_000) { runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "鷹" && it.mode == StudyMode.Draw.name }
            } }
            systemBack()
            await("Meaning quiz")
            assertNull(connectivity.activeNetwork)
            assertEquals("jlpt-n1", app.settings.stack.value)
            evidence.put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-retry-native-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-retry-native-route-tree.txt").writeText(rule.onRoot().printToString())
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
    private fun await(text: String) {
        rule.waitUntil(30_000) { rule.onAllNodesWithText(text).fetchSemanticsNodes().isNotEmpty() }
    }
    private fun click(text: String) = click(rule.onNodeWithText(text))
    private fun click(node: SemanticsNodeInteraction) {
        rule.waitUntil(30_000) { try { node.fetchSemanticsNode(); true } catch (_: AssertionError) { false } }
        rule.waitUntil(30_000) {
            node.isDisplayed() || node.onAncestors().filter(hasScrollAction()).fetchSemanticsNodes().isNotEmpty()
        }
        val parents = node.onAncestors().filter(hasScrollAction())
        for (index in parents.fetchSemanticsNodes().indices.reversed()) {
            val parent = parents[index]
            if (parent.onAncestors().filter(hasScrollAction()).fetchSemanticsNodes().isNotEmpty()) parent.performScrollTo()
        }
        if (parents.fetchSemanticsNodes().isNotEmpty()) node.performScrollTo()
        node.assertIsDisplayed().assertIsEnabled().performClick()
    }
    private fun systemBack() {
        InstrumentationRegistry.getInstrumentation().uiAutomation.performGlobalAction(
            android.accessibilityservice.AccessibilityService.GLOBAL_ACTION_BACK)
        rule.waitForIdle()
    }
    private fun capture(step: String) {
        rule.waitForIdle()
        val bitmap = requireNotNull(InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot())
        File(app.getExternalFilesDir(null), "n1-retry-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
