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
import io.github.stopcran.kanji.core.words.WordDirection
import io.github.stopcran.kanji.core.words.WordQuizBuilder
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

private fun disposable098() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch098GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun agentLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable098()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("刀 刂 刈 則 削 剛 剤 推 斉 氵 洗 済", "濯 粘 薬 製 調 進 錠", "剤 済 剛 則 斉 刀 刂 氵 洗 洗剤 製剤 推進剤")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 098: agent / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 19 scoped Han; focused 剤/済/剛/則/斉/刀/刂/氵/洗. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("刀", "刂", "刈", "則", "削", "剛", "剤", "推", "斉", "氵", "洗", "済", "濯", "粘", "薬", "製", "調", "進", "錠")) {
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
            for (word in listOf("洗剤", "推進剤")) {
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
        assertEquals(84, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-098-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-098-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 76).put("wholeWordRasterProbes", 8).put("panels", 3)
            .put("limits", "19 actual scoped Han; 刂/氵 absent from all three bundled cmaps requires actual system fallback inspection, four production families, three bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch098ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineAgentReusedSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack() {
        disposable098()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-098-${UUID.randomUUID()}", "main")
        val head = "6cca181b977144603296506cfe0b9ed744e2d193"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-098-6cca181b-envelope.zip")
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
        assertEquals(1121, updated.kanji)
        assertEquals(5073, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("0cbdc2723b0433f2", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(130, n1.size)
        val agent = n1.single { it.kanji == "剤" }
        assertEquals(listOf("済", "剛", "則"), agent.distractors.splitSep())
        assertEquals(listOf("ザイ", "スイ", "セイ"), agent.onyomi.splitSep())
        assertEquals(listOf("かる", "けず.る"), agent.kunyomi.splitSep())
        assertNotNull(agent.quizOnyomi)
        assertNotNull(agent.quizKunyomi)
        assertEquals(listOf("ザイ"), agent.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), agent.quizKunyomi?.splitSep())
        assertEquals(listOf("ざい"), agent.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), agent.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "剤" to "medicinal preparation; chemical agent",
            "済" to "settle; finish",
            "剛" to "sturdy; unyielding strength",
            "則" to "rule; follow a model",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        assertEquals(n1.map { it.kanji }.toSet(),
            all.filter { "jlpt-n1" in it.tags.splitSep() }.map { it.kanji }.toSet())
        val curatedIds = listOf("済", "剛", "則")
        assertEquals(listOf("剛"), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(agent) +
            n1.filter { it.kanji != "剤" }.shuffled(kotlin.random.Random(722)).take(15)
        val checkedPools = JSONArray()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all,
            "boundedCustom" to boundedCustom, "randomN1Subset" to randomSubset)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "剤" }
            assertEquals(curatedIds, target.distractors)
            val available = curatedIds.filter { id -> cards.any { it.kanji == id } }
            val expectedAvailable = when (poolName) {
                "N1" -> 1
                "All", "boundedCustom" -> 3
                else -> curatedIds.count { id -> randomSubset.any { it.kanji == id } }
            }
            assertEquals(expectedAvailable, available.size)
            repeat(16) { seed ->
                val options = QuizBuilder.options(target, cards, kotlin.random.Random(seed))
                assertEquals(4, options.size)
                assertEquals(4, options.map { it.title }.toSet().size)
                assertEquals(1, options.count { it.kanji == target.kanji })
                assertTrue(options.all { option -> cards.any { it.kanji == option.kanji && it.title == option.title } })
                assertTrue(available.all { id -> options.any { it.kanji == id } })
                if (expectedAvailable == 3) assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
                checkedPools.put(JSONObject().put("pool", poolName).put("poolSize", pool.size).put("seed", seed)
                    .put("options", JSONArray().also { rows ->
                        options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                    }).put("availableCuratedCount", available.size)
                    .put("fallbackOptions", options.count { it.kanji != target.kanji && it.kanji !in available }))
            }
        }
        assertEquals(64, checkedPools.length())
        val words = runBlocking { app.db.content().wordsLite(source.id) }.map { it.toCard() }
        val importedAgent = words.single { it.word == "洗剤" }
        assertEquals(listOf("せっけん"), importedAgent.quizExclusions)
        assertEquals("せんざい", importedAgent.reading)
        assertEquals(2, importedAgent.jlpt)
        val directGuardChecks = JSONArray()
        val guardPairs = listOf("洗剤" to "せっけん")
        for ((leftId, rightId) in guardPairs) {
            val left = words.single { it.word == leftId }
            val right = words.single { it.word == rightId }
            assertTrue(right.word in left.quizExclusions)
            for ((target, excluded) in listOf(left to right, right to left)) {
                val custom = listOf(target, excluded) + words.filter {
                    it.word !in setOf(target.word, excluded.word) && it.title !in setOf(target.title, excluded.title) &&
                        it.word !in target.quizExclusions && target.word !in it.quizExclusions
                }.take(12)
                for ((poolName, pool) in listOf("All" to words, "boundedCustom" to custom)) {
                    for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
                        repeat(16) { seed ->
                            val options = WordQuizBuilder.options(target, pool, direction, kotlin.random.Random(seed))
                            assertEquals(4, options.size)
                            assertEquals(1, options.count { it.word == target.word })
                            assertFalse("Direct exclusion leaked", options.any { it.word == excluded.word })
                            directGuardChecks.put(JSONObject().put("target", target.word).put("excluded", excluded.word)
                                .put("pool", poolName).put("direction", direction.name).put("seed", seed)
                                .put("options", JSONArray().also { rows ->
                                    options.forEach { rows.put(JSONObject().put("word", it.word).put("label", it.label)) }
                                }))
                        }
                    }
                }
            }
        }
        assertEquals(128, directGuardChecks.length())
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
                        if (card.kanji == "剤") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "剤" && (kind == ReadingKind.On && key == "ざい")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "剤", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("newDirectWordGuardPairs", 0).put("preservedDirectWordGuardPairs", 1).put("directGuardBuilderChecks", directGuardChecks)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(agent.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(agent.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(agent.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(agent.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(agent.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(agent.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 剤 meaning and onざい due; no kun keys. Full raw readings and explicit curation retained. Two historical good 剤 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 130 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("剤")
            click("medicinal preparation; chemical agent")
            await("剤 — medicinal preparation; chemical agent")
            show(articleBullet("Strokes: 10 · Key (radical): 刀 (no. 18), appearing as 刂 on the right · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("剤 is useful as a compound element for a medicinal preparation or chemical agent. 洗剤 せんざい means detergent or cleaning agent: this use is not limited to medicine that people take. Learn 剤 inside words rather than using it as a general standalone noun for any substance."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Picture the crossed strokes and lower bars of the 斉-shaped left block beside the blade-shaped 刂, as though a preparation were being carefully divided. This invented scene helps remember the modern shape; it is not a historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(readingExample("ザイ"), "kanji-09")
            show(readingExample("洗剤 せんざい — detergent; cleaning agent"), "kanji-11")
            show(readingExample("スイ"), "kanji-12")
            show(readingExample("セイ"), "kanji-15")
            show(readingExample("かる"), "kanji-18")
            show(readingExample("けず.る"), "kanji-21")
            show(articleBullet("Only ザイ is selected for reading questions. The other four readings remain dictionary reference information, not interchangeable pronunciations of 洗剤. Not selecting a word example does not establish that a reading is invalid or obsolete."), "kanji-24")
            show(articleBullet("For ordinary かる, \"mow; trim,\" learn 刈る; for けずる, \"shave; sharpen; reduce,\" learn 削る. Those words do not establish 剤 as an alternative spelling."), "kanji-25")
            section("Common words")
            show(articleBullet("洗剤 せんざい — detergent; cleaning agent"), "kanji-27")
            show(articleBullet("薬剤 やくざい — medicine; chemical agent"), "kanji-28")
            show(articleBullet("錠剤 じょうざい — tablet; pill"), "kanji-29")
            show(articleBullet("調剤 ちょうざい — preparing or dispensing a prescription"), "kanji-30")
            show(articleBullet("These are recognition examples, not instructions about using a product or medicine."), "kanji-31")
            section("Notes")
            show(articleBullet("The indexing radical is 刀, visible here as right-hand 刂. 済, \"settle; finish,\" has a similar 斉-shaped block but adds left-hand 氵 instead. Check the side and shape of the extra strokes, not just the shared block."), "kanji-33")
            show(articleBullet("剛, \"sturdy; unyielding strength,\" and 則, \"rule; follow a model,\" also have right-hand 刂 but different left blocks and meanings."), "kanji-34")
            show(articleBullet("薬 also concerns medicine and chemicals. Its meanings overlap with 剤; do not treat them as mutually exclusive categories or assume that a compound containing either names something safe to ingest."), "kanji-35")
            show(articleBullet("製剤 せいざい, \"pharmaceutical formulation,\" does not demonstrate 剤's セイ: 剤 supplies ざい there. Likewise, in 推進剤 すいしんざい, \"propellant,\" the initial すい belongs to 推, not 剤."), "kanji-36")
            show(articleBullet("JMdict also records the whole word 粘剤 ねり, a material used in making Japanese paper. That whole-word spelling does not establish an independent ねり or り reading for 剤."), "kanji-37")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families: JMdict, entries 1296370, 1390950, 1538220, 1357120, 1429160, 2276330, 2569220 and 2837804. Reading allocation and usage: Digital Daijisen, 剤 and 洗剤."), "kanji-38")
            section("Common words")
            show(articleBullet("洗剤 せんざい — detergent; cleaning agent"), "senzai-forward")
            inline(await(articleBullet("洗剤 せんざい — detergent; cleaning agent")), "洗剤", 0)
            await("Article contents")
            await("洗剤 (せんざい) - detergent; cleaning agent")
            section("How the kanji combine")
            show(articleBullet("洗 contributes washing, and 剤 an agent or preparation. The first character identifies the purpose of the second. The on readings are セン + ザイ."), "zai-reverse")
            inline(await(articleBullet("洗 contributes washing, and 剤 an agent or preparation. The first character identifies the purpose of the second. The on readings are セン + ザイ.")), "剤", 27)
            await("Article contents")
            section("Readings")
            show(readingExample("ザイ"), "zai-kanji-backlink")
            back()
            await(articleBullet("洗 contributes washing, and 剤 an agent or preparation. The first character identifies the purpose of the second. The on readings are セン + ザイ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("zai-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("洗 contributes washing, and 剤 an agent or preparation. The first character identifies the purpose of the second. The on readings are セン + ザイ."), "sen-reverse")
            inline(await(articleBullet("洗 contributes washing, and 剤 an agent or preparation. The first character identifies the purpose of the second. The on readings are セン + ザイ.")), "洗", 0)
            await("Article contents")
            await("洗 — wash")
            section("Common words")
            show(articleBullet("洗剤 せんざい — detergent; cleaning agent"), "sen-forward")
            inline(await(articleBullet("洗剤 せんざい — detergent; cleaning agent")), "洗剤", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("洗 contributes washing, and 剤 an agent or preparation. The first character identifies the purpose of the second. The on readings are セン + ザイ."), "senzai-component-return")
            back()
            await(articleBullet("洗剤 せんざい — detergent; cleaning agent")).assertIsDisplayed()
            section("Common words")
            capture("sen-system-back-to-kanji")
            back()
            await(articleBullet("洗 contributes washing, and 剤 an agent or preparation. The first character identifies the purpose of the second. The on readings are セン + ザイ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("sen-system-back-to-word")
            back()
            await(articleBullet("洗剤 せんざい — detergent; cleaning agent")).assertIsDisplayed()
            section("Common words")
            capture("senzai-system-back-to-zai")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4).put("activatedBaselinePairs", 1)
                .put("completeArticleProjections", 1).put("changedReusedArticles", 2)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("剤", meaning.card.kanji)
            assertEquals(4, meaning.options.size)
            assertEquals(4, meaning.options.map { it.title }.toSet().size)
            assertEquals(1, meaning.options.count { it.kanji == "剤" })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertFalse(meaning.options.any { it.kanji == "済" })
            assertTrue(meaning.options.any { it.kanji == "剛" })
            assertFalse(meaning.options.any { it.kanji == "則" })
            assertEquals("medicinal preparation; chemical agent", meaning.options.single { it.kanji == "剤" }.title)
            assertEquals(listOf("済", "剛", "則"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 1).put("actualN1FallbackOptions", 2)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("medicinal preparation; chemical agent")
            await("Correct!")
            assertEquals("剤", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("剤", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("ざい"))
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "剤" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("ざい"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "剤" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("ざい"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })
            capture("curated-one-on-no-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("medicinal preparation; chemical agent").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "剤") })
            assertEquals(listOf("済", "剛", "則"), card.distractors.splitSep())
            assertEquals(listOf("ザイ", "スイ", "セイ"), card.onyomi.splitSep())
            assertEquals(listOf("かる", "けず.る"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ザイ"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(10, strokes.length())
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
            rule.onNode(hasContentDescription("10 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "剤" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "剤" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("onlyOnZaiNoKunPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-098-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-098-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-098-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
