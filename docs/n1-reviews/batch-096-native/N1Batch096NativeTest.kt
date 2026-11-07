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

private fun disposable096() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch096GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun strengthLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable096()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("丈 体 健 元 冂 刀 刂 則 削 剖 剛 力", "勉 勤 夫 実 山 岡 康 弱 強 性 毛 気", "活 生 質 風", "剛 削 剖 則 岡 冂 山 刀 刂 剛健 剛性 剛毛")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 096: strength / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 28 scoped Han; focused 剛/削/剖/則/岡/冂/山/刀/刂. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("丈", "体", "健", "元", "冂", "刀", "刂", "則", "削", "剖", "剛", "力", "勉", "勤", "夫", "実", "山", "岡", "康", "弱", "強", "性", "毛", "気", "活", "生", "質", "風")) {
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
            for (word in listOf("剛健", "質実剛健")) {
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
        assertEquals(120, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-096-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-096-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 112).put("wholeWordRasterProbes", 8).put("panels", 4)
            .put("limits", "28 actual scoped Han; 冂/刂 absent from all three bundled cmaps requires actual system fallback inspection, four production families, four bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch096ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineStrengthOneSupportOneReciprocalPairOneOnNoKunTenStrokesAndSystemBack() {
        disposable096()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-096-${UUID.randomUUID()}", "main")
        val head = "58129f197c1f88a59ebb82c02cea9e9a0220377e"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-096-58129f19-envelope.zip")
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
        assertEquals(1119, updated.kanji)
        assertEquals(5072, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("54645b95fe8e939c", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(128, n1.size)
        val strength = n1.single { it.kanji == "剛" }
        assertEquals(listOf("削", "剖", "則"), strength.distractors.splitSep())
        assertEquals(listOf("ゴウ"), strength.onyomi.splitSep())
        assertEquals(emptyList<String>(), strength.kunyomi.splitSep())
        assertNotNull(strength.quizOnyomi)
        assertNotNull(strength.quizKunyomi)
        assertEquals(listOf("ゴウ"), strength.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), strength.quizKunyomi?.splitSep())
        assertEquals(listOf("ごう"), strength.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), strength.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "剛" to "sturdy; unyielding strength",
            "削" to "shave; sharpen; pare",
            "剖" to "dissect; split open",
            "則" to "rule; follow a model",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        assertEquals(n1.map { it.kanji }.toSet(),
            all.filter { "jlpt-n1" in it.tags.splitSep() }.map { it.kanji }.toSet())
        val curatedIds = listOf("削", "剖", "則")
        assertEquals(listOf("削", "剖"), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(strength) +
            n1.filter { it.kanji != "剛" }.shuffled(kotlin.random.Random(704)).take(15)
        val checkedPools = JSONArray()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all,
            "boundedCustom" to boundedCustom, "randomN1Subset" to randomSubset)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "剛" }
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
        val importedStrength = words.single { it.word == "剛健" }
        assertEquals(listOf("丈夫", "健康", "元気", "強い", "強力", "体力", "力", "活気", "もりもり", "生き生き", "ぴんぴん", "活力"), importedStrength.quizExclusions)
        assertEquals("ごうけん", importedStrength.reading)
        assertNull(importedStrength.jlpt)
        val directGuardChecks = JSONArray()
        val guardPairs = listOf("剛健" to "丈夫", "剛健" to "健康", "剛健" to "元気", "剛健" to "強い", "剛健" to "強力", "剛健" to "体力", "剛健" to "力", "剛健" to "活気", "剛健" to "もりもり", "剛健" to "生き生き", "剛健" to "ぴんぴん", "剛健" to "活力")
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
        assertEquals(1536, directGuardChecks.length())
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
                        if (card.kanji == "剛") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "剛" && (kind == ReadingKind.On && key == "ごう")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "剛", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("newDirectWordGuardPairs", 12).put("directGuardBuilderChecks", directGuardChecks)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(strength.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(strength.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(strength.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(strength.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(strength.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(strength.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 剛 meaning and onごう due; no kun keys. Full raw readings and explicit curation retained. Two historical good 剛 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 128 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("剛")
            click("sturdy; unyielding strength")
            await("剛 — sturdy; unyielding strength")
            show(articleBullet("Strokes: 10 · Key (radical): 刀 (no. 18), appearing as 刂 on the right · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("剛 concerns strength, sturdiness or an unyielding quality, physically or in character. 剛健 ごうけん describes robust bodily or mental vigor; 剛性 ごうせい means stiffness or rigidity."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Picture the 岡-shaped left block, with an enclosing 冂 and a 山-shaped part inside, holding firm beside the blade-shaped 刂 on the right. This invented scene is a memory aid, not a historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(readingExample("ゴウ"), "kanji-09")
            show(readingExample("剛健 ごうけん — robust; vigorous"), "kanji-11")
            show(articleBullet("This card selects ゴウ for reading questions. The frozen KANJIDIC2 record has no kunyomi. Other dictionaries also record コウ; that is additional source coverage, not an invalid reading or another question on this card. Personal-name readings are outside this lesson."), "kanji-12")
            section("Common words")
            show(articleBullet("剛健 ごうけん — robust; vigorous"), "kanji-14")
            show(articleBullet("剛性 ごうせい — stiffness; rigidity"), "kanji-15")
            show(articleBullet("剛毛 ごうもう — stiff or coarse hair; bristles"), "kanji-16")
            show(articleBullet("These are recognition examples, not a claim that every compound is everyday vocabulary."), "kanji-17")
            section("Notes")
            show(articleBullet("The indexing radical is 刀; its visible form here is 刂. 削, \"shave; sharpen; pare,\" 剖, \"dissect; split open,\" and 則, \"rule; follow a model,\" share right-hand 刂 but have different left blocks and meanings."), "kanji-19")
            show(articleBullet("強 also concerns strength, and 力 power. Their meanings overlap with 剛; they are not mutually exclusive categories. For the everyday adjective \"strong,\" learn 強い つよい rather than treating 剛 as a general standalone replacement."), "kanji-20")
            show(articleBullet("JMdict indexes 剛い under つよい as a search-only spelling. That is not a recommendation to write the ordinary adjective that way."), "kanji-21")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families: JMdict, entries 1236070, 1284120, 1284130 and 1284160. Reading allocation and usage: Digital Daijisen, 剛 and 剛健."), "kanji-22")
            section("Common words")
            show(articleBullet("剛健 ごうけん — robust; vigorous"), "gouken-forward")
            inline(await(articleBullet("剛健 ごうけん — robust; vigorous")), "剛健", 0)
            await("Article contents")
            await("剛健 (ごうけん) — robust; vigorous")
            section("Meaning")
            show(articleBullet("剛健 describes being robust and strong in body or spirit. It is a noun and a na-adjective: 剛健な + noun, or 剛健です as a polite predicate."), "gouken-02")
            show(articleBullet("Digital Daijisen gives the phrase 勤勉で剛健な気風 (きんべんでごうけんなきふう), \"a hardworking and robust spirit.\" Here 気風 means a characteristic spirit or ethos, and な connects 剛健 to that noun."), "gouken-03")
            show(articleBullet("The expression 質実剛健 (しつじつごうけん) combines being plain and sincere with fortitude and vigor. It does not simply mean being cheerful or busy."), "gouken-04")
            section("How the kanji combine")
            show(articleBullet("剛 contributes strength or sturdiness, and 健 contributes health or strength. The related meanings reinforce the idea of robust vigor. The on readings here are ゴウ + ケン. This is a meaning aid, not a reconstruction of the word's history."), "gouken-06")
            section("Synonyms and antonyms")
            show(articleBullet("丈夫 じょうぶ can describe a robust constitution and also durable objects. 健康 けんこう concerns health; 元気 げんき can emphasize being well or energetic. These meanings overlap, but 剛健 emphasizes robust strength rather than just a momentary lively mood."), "gouken-08")
            show(articleBullet("強い つよい is a broader adjective for strength or intensity. 弱い よわい, \"weak,\" gives a contextual contrast, not a judgment of a person's worth. There is no single opposite covering every bodily and mental use."), "gouken-09")
            section("Distinctive meaning")
            show(articleBullet("Japanese dictionaries describe a traditional masculine association in 剛健. That association is part of its connotation, not a grammatical restriction to male subjects or a rule about who can be strong."), "gouken-11")
            show(articleBullet("Learn 剛健 as an adjective/noun, not as an i-adjective or an automatic する verb. It describes a robust quality; it is not the general word for every vigorous activity or every English use of \"strong.\""), "gouken-12")
            show(articleBullet("Dictionary: JMdict, entries 1284120 and 1320700; Digital Daijisen and Seisenban Nihon Kokugo Daijiten, 剛健, including the attributed short phrase."), "gouken-13")
            section("How the kanji combine")
            show(articleBullet("剛 contributes strength or sturdiness, and 健 contributes health or strength. The related meanings reinforce the idea of robust vigor. The on readings here are ゴウ + ケン. This is a meaning aid, not a reconstruction of the word's history."), "gou-reverse")
            inline(await(articleBullet("剛 contributes strength or sturdiness, and 健 contributes health or strength. The related meanings reinforce the idea of robust vigor. The on readings here are ゴウ + ケン. This is a meaning aid, not a reconstruction of the word's history.")), "剛", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ゴウ"), "gou-kanji-backlink")
            back()
            await(articleBullet("剛 contributes strength or sturdiness, and 健 contributes health or strength. The related meanings reinforce the idea of robust vigor. The on readings here are ゴウ + ケン. This is a meaning aid, not a reconstruction of the word's history.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("gou-system-back-to-word")
            back()
            await(articleBullet("剛健 ごうけん — robust; vigorous")).assertIsDisplayed()
            section("Common words")
            capture("gouken-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2).put("activatedBaselinePairs", 0)
                .put("completeArticleProjections", 2).put("changedReusedArticles", 0)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("剛", meaning.card.kanji)
            assertEquals(4, meaning.options.size)
            assertEquals(4, meaning.options.map { it.title }.toSet().size)
            assertEquals(1, meaning.options.count { it.kanji == "剛" })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertTrue(meaning.options.any { it.kanji == "削" })
            assertTrue(meaning.options.any { it.kanji == "剖" })
            assertFalse(meaning.options.any { it.kanji == "則" })
            assertEquals("sturdy; unyielding strength", meaning.options.single { it.kanji == "剛" }.title)
            assertEquals(listOf("削", "剖", "則"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 2).put("actualN1FallbackOptions", 1)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("sturdy; unyielding strength")
            await("Correct!")
            assertEquals("剛", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("剛", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("ごう"))
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "剛" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("ごう"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "剛" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("ごう"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })
            capture("curated-one-on-no-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("sturdy; unyielding strength").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "剛") })
            assertEquals(listOf("削", "剖", "則"), card.distractors.splitSep())
            assertEquals(listOf("ゴウ"), card.onyomi.splitSep())
            assertEquals(emptyList<String>(), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ゴウ"), card.quizOnyomi?.splitSep())
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
                    it.kanji == "剛" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "剛" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("onlyOnGouNoKunPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-096-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-096-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-096-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
