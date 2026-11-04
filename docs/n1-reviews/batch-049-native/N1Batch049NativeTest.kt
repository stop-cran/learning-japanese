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

private fun disposable049() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch049GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun oxSignLookalikesAndFallbacksAcrossFourProductionFamilies() {
        disposable049()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "丑 五 互 土 宀 氵 牜"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 049: Ox sign / look-alikes / fallback")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 28.sp, lineHeight = 40.sp)
                    }
                    Text("丑: bent top-and-right stroke, inner descending stroke, middle crossbar and bottom bar. Compare 五, 互, 土 and fallback 宀, 氵, 牜.", fontSize = 18.sp)
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
            for (char in listOf("丑", "五", "互", "土", "宀", "氵", "牜")) {
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
        File(context.getExternalFilesDir(null), "n1-049-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-049-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("limits", "Twenty-eight native Paint probes and four production Compose rows; visual inspection separate. Emulator, not phone. Fallback styles may coincide.")
            .toString(2))
    }
}

class N1Batch049ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp

    @Test fun fullSingleImportOfflineOxSignAndBothReusedTigerLinksAndSystemBack() {
        disposable049()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-049-${UUID.randomUUID()}", "main")
        val head = "049c34b2d1527267d567b2f794825cbac1f28f37"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-049-049c34b-envelope.zip")
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
        assertEquals(1061, updated.kanji)
        assertEquals(5019, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("1a13e8e6d637bc5b", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(81, n1.size)
        val ox = n1.single { it.kanji == "丑" }
        assertEquals(listOf("チュウ"), ox.onyomi.splitSep())
        assertEquals(listOf("うし"), ox.kunyomi.splitSep())
        assertNotNull(ox.quizOnyomi)
        assertNotNull(ox.quizKunyomi)
        assertEquals(emptyList<String>(), ox.quizOnyomi?.splitSep())
        assertEquals(listOf("うし"), ox.quizKunyomi?.splitSep())
        assertEquals(emptyList<String>(), ox.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("うし"), ox.toReadingCard().quizKeys(ReadingKind.Kun))
        app.settings.sync.lastCheckMs = System.currentTimeMillis()
        app.settings.setStartingGuideVisible(false)
        app.settings.setStack("jlpt-n5")
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(ox.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(ox.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(ox.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(ox.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("phoneEvidence", false).put("sessionOrDrawingRetest", false).put("passed", false)
        val scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 81 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("丑")
            click("Ox zodiac sign")
            await("Article contents")
            await("no. 1)", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            await("Modern-shape mnemonic", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-mnemonic")
            section("Readings")
            rule.onNodeWithTag("article-body").performScrollToNode(hasText("Only うし is selected", substring = true))
            await("Only うし is selected", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-reading-disposition")
            section("Notes")
            await("modern-shape comparisons", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-lookalikes")
            await("Dictionary hour", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-historical-boundary")
            await("between two branches", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-direction-boundary")
            inline(await("between two branches", substring = true), "寅")
            await("Article contents")
            section("Notes")
            await("between two branches", substring = true).performScrollTo().assertIsDisplayed()
            capture("reused-tiger-kanji-link")
            inline(await("between two branches", substring = true), "丑")
            await("Article contents")
            section("Meaning and origin")
            await("Modern-shape mnemonic", substring = true).performScrollTo().assertIsDisplayed()
            capture("reused-tiger-kanji-target")
            back()
            await("between two branches", substring = true).assertIsDisplayed()
            back()
            await("between two branches", substring = true).assertIsDisplayed()
            section("Common words")
            inline(await("丑 うし — Ox zodiac sign"), "丑")
            await("丑 (うし)", substring = true)
            section("Meaning")
            await("私の干支は丑です", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-sign-example")
            await("十二支の二番目は丑です", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-cycle-example")
            await("The reading かんし", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-calendar-boundary")
            section("How the kanji combine")
            await("writes the whole native sign noun", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-components")
            inline(await("writes the whole native sign noun", substring = true), "丑")
            await("Article contents")
            section("Meaning and origin")
            await("Modern-shape mnemonic", substring = true).performScrollTo().assertIsDisplayed()
            capture("backlink-kanji")
            back()
            await("writes the whole native sign noun", substring = true).assertIsDisplayed()
            capture("system-back-word")
            await("Recognize 丑年", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-compound-reading")
            section("Synonyms and antonyms")
            await("ordinary animal noun", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-animal-comparison")
            section("Distinctive meaning")
            await("Keep the spelling tied", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-sign-boundary")
            await("Older uses of 丑", substring = true).performScrollTo().assertIsDisplayed()
            capture("word-historical-boundary")
            inline(await("Older uses of 丑", substring = true), "寅")
            await("寅 (とら)", substring = true)
            section("Distinctive meaning")
            await("Older uses of 寅", substring = true).performScrollTo().assertIsDisplayed()
            capture("reused-tiger-word-link")
            inline(await("Older uses of 寅", substring = true), "丑")
            await("丑 (うし)", substring = true)
            section("Meaning")
            await("私の干支は丑です", substring = true).performScrollTo().assertIsDisplayed()
            capture("reused-tiger-word-target")
            back()
            await("Older uses of 寅", substring = true).assertIsDisplayed()
            back()
            await("Older uses of 丑", substring = true).assertIsDisplayed()
            back()
            await("Common words")
            back()
            await("Search kanji, meaning or reading")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("reusedTigerKanjiLinkAndSystemBack", true)
                .put("reusedTigerWordLinkAndSystemBack", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-049-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-049-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-049-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
