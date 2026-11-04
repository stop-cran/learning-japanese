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
import androidx.test.core.app.ActivityScenario
import androidx.test.platform.app.InstrumentationRegistry
import io.github.stopcran.kanji.KanjiApp
import io.github.stopcran.kanji.MainActivity
import io.github.stopcran.kanji.R
import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.content.RepoSource
import io.github.stopcran.kanji.core.reading.ReadingKind
import io.github.stopcran.kanji.core.srs.KanjiFont
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

private fun disposable048() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch048GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun tigerSignRadicalAndFallbacksAcrossFourProductionFamilies() {
        disposable048()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "寅 演 黄 申 宀 氵 虍 黃"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 048: Tiger sign / radical / fallback")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 28.sp, lineHeight = 40.sp)
                    }
                    Text("寅: roof 宀, radical 40. 演 adds 氵; 黄 has a different top; 申 has no roof. Compare fallback 虍 and 黃.", fontSize = 18.sp)
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
            for (char in listOf("寅", "演", "黄", "申", "宀", "氵", "虍", "黃")) {
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
        File(context.getExternalFilesDir(null), "n1-048-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-048-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("limits", "Thirty-two native Paint probes and four production Compose rows; visual inspection separate. Emulator, not phone. Fallback styles may coincide.")
            .toString(2))
    }
}

class N1Batch048ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp

    @Test fun fullSingleImportOfflineTigerSignArticleAndSystemBack() {
        disposable048()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-048-${UUID.randomUUID()}", "main")
        val head = "66211c0f70abdc92f565bebb095e6c18344bde52"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-048-66211c0-envelope.zip")
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
        assertEquals(1060, updated.kanji)
        assertEquals(5018, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("019d8515d222414a", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(80, n1.size)
        val tiger = n1.single { it.kanji == "寅" }
        assertEquals(listOf("イン"), tiger.onyomi.splitSep())
        assertEquals(listOf("とら"), tiger.kunyomi.splitSep())
        assertNotNull(tiger.quizOnyomi)
        assertNotNull(tiger.quizKunyomi)
        assertEquals(emptyList<String>(), tiger.quizOnyomi?.splitSep())
        assertEquals(listOf("とら"), tiger.quizKunyomi?.splitSep())
        assertEquals(emptyList<String>(), tiger.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("とら"), tiger.toReadingCard().quizKeys(ReadingKind.Kun))
        app.settings.sync.lastCheckMs = System.currentTimeMillis()
        app.settings.setStartingGuideVisible(false)
        app.settings.setStack("jlpt-n5")
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(tiger.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(tiger.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(tiger.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(tiger.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("phoneEvidence", false).put("sessionOrDrawingRetest", false).put("passed", false)
        val scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 80 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("寅")
            click("Tiger zodiac sign")
            await("Article contents")
            await("no. 40", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            await("Modern-shape mnemonic", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-mnemonic")
            section("Readings")
            rule.onNodeWithTag("article-body").performScrollToNode(hasText("Only とら is selected", substring = true))
            await("Only とら is selected", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-reading-disposition")
            section("Notes")
            await("modern-shape comparisons", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-lookalikes")
            inline(await("modern-shape comparisons", substring = true), "演")
            await("Article contents")
            section("Meaning and origin")
            await("covered stage", substring = true).performScrollTo().assertIsDisplayed()
            capture("reused-en-mnemonic")
            inline(await("covered stage", substring = true), "寅")
            await("Article contents")
            section("Meaning and origin")
            await("Modern-shape mnemonic", substring = true).performScrollTo().assertIsDisplayed()
            capture("reused-en-link-target")
            back()
            await("covered stage", substring = true).assertIsDisplayed()
            back()
            await("modern-shape comparisons", substring = true).assertIsDisplayed()
            await("Dictionary hour", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-historical-boundary")
            await("between two branches", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-direction-boundary")
            section("Common words")
            inline(await("寅 とら — Tiger zodiac sign"), "寅")
            await("寅 (とら)", substring = true)
            section("Meaning")
            await("私の干支は寅です", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-sign-example")
            await("十二支の三番目は寅です", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-cycle-example")
            await("The reading かんし", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-calendar-boundary")
            section("How the kanji combine")
            await("writes the whole native sign noun", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-components")
            inline(await("writes the whole native sign noun", substring = true), "寅")
            await("Article contents")
            section("Meaning and origin")
            await("Modern-shape mnemonic", substring = true).performScrollTo().assertIsDisplayed()
            capture("backlink-kanji")
            back()
            await("writes the whole native sign noun", substring = true).assertIsDisplayed()
            capture("system-back-word")
            await("Recognize 寅年", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-compound-reading")
            section("Synonyms and antonyms")
            await("ordinary animal noun", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-animal-comparison")
            section("Distinctive meaning")
            await("Keep the spelling tied", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-sign-boundary")
            await("Older uses of 寅", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-historical-boundary")
            back()
            await("Common words")
            back()
            await("Search kanji, meaning or reading")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            evidence.put("reciprocalLinkAndSystemBack", true).put("reusedEnLinkAndSystemBack", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-048-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-048-article-tree.txt").writeText(rule.onRoot().printToString())
            scenario.close()
        }
    }

    private fun await(text: String, substring: Boolean = false): SemanticsNodeInteraction {
        rule.waitUntil(30_000) { rule.onAllNodesWithText(text, substring = substring).fetchSemanticsNodes().isNotEmpty() }
        return rule.onNodeWithText(text, substring = substring)
    }

    private fun click(text: String) {
        val node = await(text)
        if (node.onAncestors().filter(hasScrollAction()).fetchSemanticsNodes().isNotEmpty()) node.performScrollTo()
        node.assertIsDisplayed().assertIsEnabled().performClick()
    }

    private fun section(title: String) {
        rule.onNodeWithTag("article-body").performScrollToIndex(0)
        click("Article contents")
        rule.onNode(hasText(title, substring = true) and hasClickAction()).performScrollTo().performClick()
        rule.waitForIdle()
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
        val bitmap = requireNotNull(automation.takeScreenshot())
        File(app.getExternalFilesDir(null), "n1-048-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
