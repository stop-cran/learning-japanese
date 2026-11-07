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

private fun disposable097() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch097GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun swordLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable097()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("丁 写 刀 刂 刃 則 剖 剛 剣 包 博 口", "古 日 本 物 真 見 道 館", "剣 剛 剖 則 刀 刂 刃 口 真 真剣 剣道")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 097: sword / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 20 scoped Han; focused 剣/剛/剖/則/刀/刂/刃/口/真. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("丁", "写", "刀", "刂", "刃", "則", "剖", "剛", "剣", "包", "博", "口", "古", "日", "本", "物", "真", "見", "道", "館")) {
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
            for (word in listOf("真剣", "剣道")) {
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
            File(context.getExternalFilesDir(null), "n1-097-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-097-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 80).put("wholeWordRasterProbes", 8).put("panels", 3)
            .put("limits", "20 actual scoped Han; 刂 absent from all three bundled cmaps requires actual system fallback inspection, four production families, three bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch097ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineSwordOneSupportThreeReciprocalPairsBothReadingsTenStrokesAndSystemBack() {
        disposable097()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-097-${UUID.randomUUID()}", "main")
        val head = "83e5c0901a2d080e33b3583da7e0271a6aa329a0"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-097-83e5c090-envelope.zip")
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
        assertEquals(1120, updated.kanji)
        assertEquals(5073, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("a066afceaf1f447a", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(129, n1.size)
        val sword = n1.single { it.kanji == "剣" }
        assertEquals(listOf("剛", "剖", "則"), sword.distractors.splitSep())
        assertEquals(listOf("ケン"), sword.onyomi.splitSep())
        assertEquals(listOf("つるぎ"), sword.kunyomi.splitSep())
        assertNotNull(sword.quizOnyomi)
        assertNotNull(sword.quizKunyomi)
        assertEquals(listOf("ケン"), sword.quizOnyomi?.splitSep())
        assertEquals(listOf("つるぎ"), sword.quizKunyomi?.splitSep())
        assertEquals(listOf("けん"), sword.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("つるぎ"), sword.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "剣" to "sword; double-edged blade",
            "剛" to "sturdy; unyielding strength",
            "剖" to "dissect; split open",
            "則" to "rule; follow a model",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        assertEquals(n1.map { it.kanji }.toSet(),
            all.filter { "jlpt-n1" in it.tags.splitSep() }.map { it.kanji }.toSet())
        val curatedIds = listOf("剛", "剖", "則")
        assertEquals(listOf("剛", "剖"), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(sword) +
            n1.filter { it.kanji != "剣" }.shuffled(kotlin.random.Random(713)).take(15)
        val checkedPools = JSONArray()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all,
            "boundedCustom" to boundedCustom, "randomN1Subset" to randomSubset)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "剣" }
            assertEquals(curatedIds, target.distractors)
            val available = curatedIds.filter { id -> cards.any { it.kanji == id } }
            val expectedAvailable = when (poolName) {
                "N1" -> 2
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
        val importedSword = words.single { it.word == "剣" }
        assertEquals(listOf("刀", "日本刀", "刃", "真剣"), importedSword.quizExclusions)
        assertEquals("つるぎ", importedSword.reading)
        assertNull(importedSword.jlpt)
        val directGuardChecks = JSONArray()
        val guardPairs = listOf("剣" to "刀", "剣" to "日本刀", "剣" to "刃", "剣" to "真剣")
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
        assertEquals(512, directGuardChecks.length())
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
                        if (card.kanji == "剣") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "剣" && ((kind == ReadingKind.On && key == "けん") || (kind == ReadingKind.Kun && key == "つるぎ"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "剣", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("newDirectWordGuardPairs", 4).put("directGuardBuilderChecks", directGuardChecks)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(sword.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(sword.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(sword.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(sword.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(sword.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(sword.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 剣 meaning and onけん/kunつるぎ due. Full raw readings and explicit curation retained. Two historical good 剣 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 129 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("剣")
            click("sword; double-edged blade")
            await("剣 — sword; double-edged blade")
            show(articleBullet("Strokes: 10 · Key (radical): 刀 (no. 18), appearing as 刂 on the right · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("剣 concerns a sword or blade, especially a double-edged sword. The word 剣 つるぎ can also name swords more broadly; do not treat \"double-edged\" as an exceptionless definition."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Picture a sword beside a pointed roof, a horizontal line and a 口-shaped box, with spreading strokes below. The sword-shaped part is the right-hand 刂. This invented scene helps distinguish the modern shape; it is not a historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(readingExample("ケン"), "kanji-09")
            show(readingExample("真剣 しんけん — serious; earnest; also a real sword"), "kanji-11")
            show(readingExample("つるぎ"), "kanji-12")
            show(readingExample("剣 つるぎ — sword; especially a double-edged blade"), "kanji-14")
            show(articleBullet("Both source readings are selected for reading questions. The standalone noun 剣 can also be read けん; that does not make every dictionary sense interchangeable between the two pronunciations."), "kanji-15")
            section("Common words")
            show(articleBullet("剣 つるぎ — sword; especially a double-edged blade"), "kanji-17")
            show(articleBullet("真剣 しんけん — serious; earnest; also a real sword rather than a wooden practice weapon"), "kanji-18")
            show(articleBullet("剣道 けんどう — kendo, the martial art using bamboo swords"), "kanji-19")
            section("Notes")
            show(articleBullet("The indexing radical is 刀, visible here as 刂. 剛, \"sturdy; unyielding strength,\" 剖, \"dissect; split open,\" and 則, \"rule; follow a model,\" share right-hand 刂 but have different left blocks and meanings."), "kanji-21")
            show(articleBullet("刀 かたな especially suggests a Japanese single-edged sword; 剣 especially suggests a double-edged one. Broader sword uses overlap, so this is not a strict division of all swords."), "kanji-22")
            show(articleBullet("刃 は focuses on the blade or cutting edge, rather than naming the whole sword."), "kanji-23")
            show(articleBullet("真剣 usually describes earnest engagement in the examples on its word card. Do not translate every occurrence literally as a weapon, or use it for every English sense of \"serious.\""), "kanji-24")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families: JMdict, entries 1256750, 1256910 and 1363650. Reading allocation and usage: Digital Daijisen, 剣 and 真剣."), "kanji-25")
            section("Common words")
            show(articleBullet("剣 つるぎ — sword; especially a double-edged blade"), "tsurugi-forward")
            inline(await(articleBullet("剣 つるぎ — sword; especially a double-edged blade")), "剣", 0)
            await("Article contents")
            await("剣 (つるぎ) — sword; double-edged blade")
            section("Meaning")
            show(articleBullet("剣 is a noun for a sword, especially a double-edged one. This article teaches つるぎ. Dictionaries also recognize broader sword usage, so the double-edged association is not an absolute restriction."), "tsurugi-02")
            show(articleBullet("博物館で古い剣を見ました。 (はくぶつかんでふるいつるぎをみました。) — I saw an old sword at the museum."), "tsurugi-03")
            show(articleBullet("これは剣の写真です。 (これはつるぎのしゃしんです。) — This is a photograph of a sword."), "tsurugi-04")
            show(articleBullet("In 剣を見る (つるぎをみる), \"look at a sword,\" を marks the object. 剣の写真 uses の to connect the sword with its photograph."), "tsurugi-05")
            section("How the kanji combine")
            show(articleBullet("剣 represents the whole native noun つるぎ here. There is no compound to split. The same spelling also has the word reading けん; this is another valid pronunciation, not a correction of つるぎ."), "tsurugi-07")
            section("Synonyms and antonyms")
            show(articleBullet("刀 かたな especially suggests a Japanese single-edged sword, while 剣 つるぎ especially suggests a double-edged one. These associations do not partition every broader use of \"sword.\" 日本刀 にほんとう identifies the Japanese sword tradition."), "tsurugi-09")
            show(articleBullet("刃 は, \"blade; cutting edge,\" focuses on a cutting part. ナイフ, \"knife,\" and 包丁 ほうちょう, \"kitchen knife,\" name different kinds of tools, not general translations of つるぎ. There is no natural lexical antonym."), "tsurugi-10")
            section("Distinctive meaning")
            show(articleBullet("真剣 しんけん has a literal noun sense \"real sword,\" contrasting with a wooden practice weapon, as well as its familiar \"serious; earnest\" adjective sense. Do not infer the meaning of the whole compound just by translating 剣."), "tsurugi-12")
            show(articleBullet("JMdict restricts its separate bayonet, swordsmanship and zoological senses to the reading けん. Those are not additional senses to memorize for this つるぎ article."), "tsurugi-13")
            show(articleBullet("Dictionary: JMdict, entry 1256750, sense 1; reading restrictions in senses 2-4. Usage: Digital Daijisen, つるぎ【剣】 and けん【剣】."), "tsurugi-14")
            section("How the kanji combine")
            show(articleBullet("剣 represents the whole native noun つるぎ here. There is no compound to split. The same spelling also has the word reading けん; this is another valid pronunciation, not a correction of つるぎ."), "tsurugi-reverse")
            inline(await(articleBullet("剣 represents the whole native noun つるぎ here. There is no compound to split. The same spelling also has the word reading けん; this is another valid pronunciation, not a correction of つるぎ.")), "剣", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("つるぎ"), "tsurugi-kanji-backlink")
            back()
            await(articleBullet("剣 represents the whole native noun つるぎ here. There is no compound to split. The same spelling also has the word reading けん; this is another valid pronunciation, not a correction of つるぎ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("tsurugi-system-back-to-word")
            back()
            await(articleBullet("剣 つるぎ — sword; especially a double-edged blade")).assertIsDisplayed()
            section("Common words")
            capture("tsurugi-system-back-to-kanji")
            section("Common words")
            show(articleBullet("真剣 しんけん — serious; earnest; also a real sword rather than a wooden practice weapon"), "shinken-forward")
            inline(await(articleBullet("真剣 しんけん — serious; earnest; also a real sword rather than a wooden practice weapon")), "真剣", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("真 contributes \"true; real,\" and 剣 means \"sword.\" The compound also has the literal noun sense \"a real sword,\" as opposed to a wooden practice weapon. That literal contrast is a useful association, not a reason to translate a serious discussion as a weapon."), "shinken-reverse")
            inline(await(articleBullet("真 contributes \"true; real,\" and 剣 means \"sword.\" The compound also has the literal noun sense \"a real sword,\" as opposed to a wooden practice weapon. That literal contrast is a useful association, not a reason to translate a serious discussion as a weapon.")), "剣", 32)
            await("Article contents")
            section("Readings")
            show(readingExample("ケン"), "shinken-kanji-backlink")
            back()
            await(articleBullet("真 contributes \"true; real,\" and 剣 means \"sword.\" The compound also has the literal noun sense \"a real sword,\" as opposed to a wooden practice weapon. That literal contrast is a useful association, not a reason to translate a serious discussion as a weapon.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("shinken-system-back-from-ken")
            section("How the kanji combine")
            show(articleBullet("真 contributes \"true; real,\" and 剣 means \"sword.\" The compound also has the literal noun sense \"a real sword,\" as opposed to a wooden practice weapon. That literal contrast is a useful association, not a reason to translate a serious discussion as a weapon."), "shin-reverse")
            inline(await(articleBullet("真 contributes \"true; real,\" and 剣 means \"sword.\" The compound also has the literal noun sense \"a real sword,\" as opposed to a wooden practice weapon. That literal contrast is a useful association, not a reason to translate a serious discussion as a weapon.")), "真", 0)
            await("Article contents")
            section("Common words")
            show(articleBullet("真剣 しんけん — serious; earnest; also a real sword"), "shin-forward")
            inline(await(articleBullet("真剣 しんけん — serious; earnest; also a real sword")), "真剣", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("真 contributes \"true; real,\" and 剣 means \"sword.\" The compound also has the literal noun sense \"a real sword,\" as opposed to a wooden practice weapon. That literal contrast is a useful association, not a reason to translate a serious discussion as a weapon."), "shinken-component-return")
            back()
            await(articleBullet("真剣 しんけん — serious; earnest; also a real sword")).assertIsDisplayed()
            section("Common words")
            capture("shin-system-back-to-kanji")
            back()
            await(articleBullet("真 contributes \"true; real,\" and 剣 means \"sword.\" The compound also has the literal noun sense \"a real sword,\" as opposed to a wooden practice weapon. That literal contrast is a useful association, not a reason to translate a serious discussion as a weapon.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("shin-system-back-to-word")
            back()
            await(articleBullet("真剣 しんけん — serious; earnest; also a real sword rather than a wooden practice weapon")).assertIsDisplayed()
            section("Common words")
            capture("shinken-system-back-to-ken")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 3).put("directedLinkTransitions", 6).put("activatedBaselinePairs", 1)
                .put("completeArticleProjections", 2).put("changedReusedArticles", 2)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("剣", meaning.card.kanji)
            assertEquals(4, meaning.options.size)
            assertEquals(4, meaning.options.map { it.title }.toSet().size)
            assertEquals(1, meaning.options.count { it.kanji == "剣" })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertTrue(meaning.options.any { it.kanji == "剛" })
            assertTrue(meaning.options.any { it.kanji == "剖" })
            assertFalse(meaning.options.any { it.kanji == "則" })
            assertEquals("sword; double-edged blade", meaning.options.single { it.kanji == "剣" }.title)
            assertEquals(listOf("剛", "剖", "則"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 2).put("actualN1FallbackOptions", 1)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("sword; double-edged blade")
            await("Correct!")
            assertEquals("剣", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("剣", question.card.kanji)
                val key = if (question.question.kind == ReadingKind.On) "けん" else "つるぎ"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "剣" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("けん", "つるぎ"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "剣" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("けん", "つるぎ"), readingLogs.map { it.reading }.toSet())
            assertEquals(setOf(ReadingKind.On.mode.name to "けん", ReadingKind.Kun.mode.name to "つるぎ"),
                readingLogs.map { it.mode to it.reading }.toSet())
            capture("curated-on-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("sword; double-edged blade").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "剣") })
            assertEquals(listOf("剛", "剖", "則"), card.distractors.splitSep())
            assertEquals(listOf("ケン"), card.onyomi.splitSep())
            assertEquals(listOf("つるぎ"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ケン"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("つるぎ"), card.quizKunyomi?.splitSep())
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
                    it.kanji == "剣" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "剣" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothKenAndTsurugiPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-097-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-097-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-097-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
