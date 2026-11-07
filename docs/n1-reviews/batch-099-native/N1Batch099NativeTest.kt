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

private fun disposable099() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch099GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun surplusLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable099()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("乗 余 刀 刂 則 剣 剩 剰 去 字 通 過", "剰 剩 乗 余 剣 則 刀 刂 過 過剰 剰え")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 099: surplus / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 12 scoped Han; focused 剰/剩/乗/余/剣/則/刀/刂/過. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("乗", "余", "刀", "刂", "則", "剣", "剩", "剰", "去", "字", "通", "過")) {
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
            for (word in listOf("過剰", "剰え")) {
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
        assertEquals(56, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-099-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-099-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 48).put("wholeWordRasterProbes", 8).put("panels", 2)
            .put("limits", "12 actual scoped Han; 刂/older剩 absent from all three bundled cmaps requires actual system fallback inspection, four production families, two bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch099ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineSurplusReusedSupportTwoReciprocalPairsOneOnNoKunElevenStrokesAndSystemBack() {
        disposable099()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-099-${UUID.randomUUID()}", "main")
        val head = "17a4bbb997c1940dc802cf4e97599c560009e4a7"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-099-17a4bbb9-envelope.zip")
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
        assertEquals(1122, updated.kanji)
        assertEquals(5073, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("5408632b5aa1382c", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(131, n1.size)
        val surplus = n1.single { it.kanji == "剰" }
        assertEquals(listOf("乗", "剣", "則"), surplus.distractors.splitSep())
        assertEquals(listOf("ジョウ"), surplus.onyomi.splitSep())
        assertEquals(listOf("あまつさえ", "あま.り", "あま.る"), surplus.kunyomi.splitSep())
        assertNotNull(surplus.quizOnyomi)
        assertNotNull(surplus.quizKunyomi)
        assertEquals(listOf("ジョウ"), surplus.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), surplus.quizKunyomi?.splitSep())
        assertEquals(listOf("じょう"), surplus.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), surplus.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "剰" to "remainder; surplus amount",
            "乗" to "ride; board",
            "剣" to "sword; double-edged blade",
            "則" to "rule; follow a model",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        assertEquals(n1.map { it.kanji }.toSet(),
            all.filter { "jlpt-n1" in it.tags.splitSep() }.map { it.kanji }.toSet())
        val curatedIds = listOf("乗", "剣", "則")
        assertEquals(listOf("剣"), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(surplus) +
            n1.filter { it.kanji != "剰" }.shuffled(kotlin.random.Random(732)).take(15)
        val checkedPools = JSONArray()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all,
            "boundedCustom" to boundedCustom, "randomN1Subset" to randomSubset)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "剰" }
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
        val importedSurplus = words.single { it.word == "過剰" }
        assertEquals(listOf("余分", "超過", "オーバー", "あまり", "あんまり", "余る", "余裕"), importedSurplus.quizExclusions)
        assertEquals("かじょう", importedSurplus.reading)
        assertEquals(2, importedSurplus.jlpt)
        val directGuardChecks = JSONArray()
        val guardPairs = importedSurplus.quizExclusions.map { "過剰" to it }
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
        assertEquals(896, directGuardChecks.length())
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
                        if (card.kanji == "剰") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "剰" && (kind == ReadingKind.On && key == "じょう")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "剰", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("newDirectWordGuardPairs", 0).put("preservedDirectWordGuardPairs", 7).put("directGuardBuilderChecks", directGuardChecks)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(surplus.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(surplus.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(surplus.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(surplus.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(surplus.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(surplus.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 剰 meaning and onじょう due; no kun keys. Full raw readings and explicit curation retained. Two historical good 剰 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 131 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("剰")
            click("remainder; surplus amount")
            await("剰 — remainder; surplus amount")
            show(articleBullet("Strokes: 11 · Key (radical): 刀 (no. 18), appearing as 刂 on the right · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("剰 concerns a surplus or remainder. 過剰 かじょう means excess: more than is needed or appropriate, not simply a large amount. Learn 剰 through compounds rather than treating it as an everyday standalone noun."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Picture a compressed 乗-like block beside the blade-shaped 刂, as though cutting off a surplus. This invented scene is a memory aid for the modern shape, not a historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(readingExample("ジョウ"), "kanji-09")
            show(readingExample("過剰 かじょう — excess; too much"), "kanji-11")
            show(readingExample("あまつさえ"), "kanji-12")
            show(readingExample("剰え あまつさえ — besides; to make matters worse. A rare kanji spelling of a dated adverb, usually written in kana and usually adding something negative. Recognition only."), "kanji-14")
            show(readingExample("あま.り"), "kanji-15")
            show(readingExample("KANJIDIC2 source-only lookup reading. JMdict lists 剰り あまり as a search-only spelling for lookup, not a recommended normal spelling; the noun means a remainder or surplus."), "kanji-17")
            show(readingExample("あま.る"), "kanji-18")
            show(readingExample("KANJIDIC2 source-only lookup reading. The character dictionary also lists あまる, but the ordinary verb taught here is 余る あまる — be left over; its spelling does not establish a modern 剰る example."), "kanji-20")
            show(articleBullet("Only ジョウ is selected for reading questions. The other readings remain reference information, not alternative pronunciations of 過剰. Their exclusion does not mean that ordinary あまり or あまる is rare or invalid."), "kanji-21")
            show(articleBullet("The source lists あまつさえ without an okurigana dot, but the rare lexical spelling above writes a final え. For the noun \"remainder,\" learn 余り あまり or kana あまり, not the search-only spelling 剰り. This noun sense is read あまり, not あんまり; the related adverbial uses are a separate learning point."), "kanji-22")
            section("Common words")
            show(articleBullet("過剰 かじょう — excess; too much"), "kanji-24")
            show(articleBullet("余剰 よじょう — surplus; remainder"), "kanji-25")
            show(articleBullet("剰余 じょうよ — surplus; remainder, including a mathematical remainder"), "kanji-26")
            section("Notes")
            show(articleBullet("The indexing radical is 刀, visible here as right-hand 刂. 乗, \"ride; board,\" has a similar dense block without that extra right-hand blade. 剣, \"sword; double-edged blade,\" and 則, \"rule; follow a model,\" share 刂 but have different left blocks."), "kanji-28")
            show(articleBullet("余 also means surplus. The two characters' meanings overlap; do not invent a strict division between them. The useful distinction here is learning actual words and spellings."), "kanji-29")
            show(articleBullet("The older form 剩 has 12 strokes; this card teaches the modern 11-stroke 剰. Recognizing the older form does not change this card's drawing target."), "kanji-30")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families and spelling restrictions: JMdict, entries 1196170, 1355690, 1544260, 1580500, 1584930 and 1543910. Reading allocation and usage: Digital Daijisen, 剰 and 過剰; the separately headed 字通 entry on the 剰 page records the older form and its stroke count."), "kanji-31")
            section("Common words")
            show(articleBullet("過剰 かじょう — excess; too much"), "kajo-forward")
            inline(await(articleBullet("過剰 かじょう — excess; too much")), "過剰", 0)
            await("Article contents")
            await("過剰 (かじょう) - excess; too much")
            section("How the kanji combine")
            show(articleBullet("過 contributes going beyond; 剰 contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ."), "jo-reverse")
            inline(await(articleBullet("過 contributes going beyond; 剰 contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ.")), "剰", 28)
            await("Article contents")
            section("Readings")
            show(readingExample("ジョウ"), "jo-kanji-backlink")
            back()
            await(articleBullet("過 contributes going beyond; 剰 contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("jo-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("過 contributes going beyond; 剰 contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ."), "ka-reverse")
            inline(await(articleBullet("過 contributes going beyond; 剰 contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ.")), "過", 0)
            await("Article contents")
            await("過 — exceed; go beyond")
            section("Common words")
            show(articleBullet("過剰 かじょう — excess; too much"), "ka-forward")
            inline(await(articleBullet("過剰 かじょう — excess; too much")), "過剰", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("過 contributes going beyond; 剰 contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ."), "kajo-component-return")
            back()
            await(articleBullet("過剰 かじょう — excess; too much")).assertIsDisplayed()
            section("Common words")
            capture("ka-system-back-to-kanji")
            back()
            await(articleBullet("過 contributes going beyond; 剰 contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("ka-system-back-to-word")
            back()
            await(articleBullet("過剰 かじょう — excess; too much")).assertIsDisplayed()
            section("Common words")
            capture("kajo-system-back-to-jo")
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
            assertEquals("剰", meaning.card.kanji)
            assertEquals(4, meaning.options.size)
            assertEquals(4, meaning.options.map { it.title }.toSet().size)
            assertEquals(1, meaning.options.count { it.kanji == "剰" })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertFalse(meaning.options.any { it.kanji == "乗" })
            assertTrue(meaning.options.any { it.kanji == "剣" })
            assertFalse(meaning.options.any { it.kanji == "則" })
            assertEquals("remainder; surplus amount", meaning.options.single { it.kanji == "剰" }.title)
            assertEquals(listOf("乗", "剣", "則"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 1).put("actualN1FallbackOptions", 2)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("remainder; surplus amount")
            await("Correct!")
            assertEquals("剰", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("剰", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("じょう"))
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "剰" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("じょう"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "剰" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("じょう"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })
            capture("curated-one-on-no-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("remainder; surplus amount").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "剰") })
            assertEquals(listOf("乗", "剣", "則"), card.distractors.splitSep())
            assertEquals(listOf("ジョウ"), card.onyomi.splitSep())
            assertEquals(listOf("あまつさえ", "あま.り", "あま.る"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ジョウ"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(11, strokes.length())
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
            rule.onNode(hasContentDescription("11 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "剰" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "剰" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("onlyOnJouNoKunPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-099-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-099-article-tree.txt").writeText(rule.onRoot().printToString())
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

    private fun show(matcher: SemanticsMatcher, step: String, occurrence: Int = 0, expectedCount: Int = 1) {
        val body = rule.onNodeWithTag("article-body")
        body.performScrollToNode(matcher)
        rule.onAllNodes(matcher).assertCountEquals(expectedCount)
        val target = rule.onAllNodes(matcher)[occurrence]
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
        File(app.getExternalFilesDir(null), "n1-099-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
