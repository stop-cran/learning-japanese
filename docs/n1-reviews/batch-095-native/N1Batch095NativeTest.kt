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

private fun disposable095() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch095GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun dissectionLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable095()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("事 亻 件 体 倍 刀 刂 分 剖 副 医 口", "問 学 料 析 査 検 構 牛 物 特 理 生", "立 角 解 誤 造 部 阝 題", "剖 部 倍 副 立 口 刀 刂 亻 阝 解 解剖 解剖学")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 095: dissection / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 32 scoped Han; focused 剖/部/倍/副/立/口/刀/刂/亻/阝/解. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("事", "亻", "件", "体", "倍", "刀", "刂", "分", "剖", "副", "医", "口", "問", "学", "料", "析", "査", "検", "構", "牛", "物", "特", "理", "生", "立", "角", "解", "誤", "造", "部", "阝", "題")) {
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
            for (word in listOf("解剖", "解剖学")) {
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
        assertEquals(136, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-095-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-095-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 128).put("wholeWordRasterProbes", 8).put("panels", 4)
            .put("limits", "32 actual scoped Han; 亻/刂/阝 absent from all three bundled cmaps requires actual system fallback inspection, four production families, four bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch095ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineDissectionOneNewSupportTwoReciprocalPairsOneOnNoKunTenStrokesAndSystemBack() {
        disposable095()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-095-${UUID.randomUUID()}", "main")
        val head = "cc74834756847ad23fad6a721bb0a02ca859fa99"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-095-cc748347-envelope.zip")
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
        assertEquals(1118, updated.kanji)
        assertEquals(5071, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("463619d79972e9f2", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(127, n1.size)
        val dissection = n1.single { it.kanji == "剖" }
        assertEquals(listOf("部", "倍", "副"), dissection.distractors.splitSep())
        assertEquals(listOf("ボウ"), dissection.onyomi.splitSep())
        assertEquals(emptyList<String>(), dissection.kunyomi.splitSep())
        assertNotNull(dissection.quizOnyomi)
        assertNotNull(dissection.quizKunyomi)
        assertEquals(listOf("ボウ"), dissection.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), dissection.quizKunyomi?.splitSep())
        assertEquals(listOf("ぼう"), dissection.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), dissection.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "剖" to "dissect; split open", "副" to "vice-; secondary",
            "部" to "section; department", "倍" to "multiple; double",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        assertEquals(n1.map { it.kanji }.toSet(),
            all.filter { "jlpt-n1" in it.tags.splitSep() }.map { it.kanji }.toSet())
        val curatedIds = listOf("部", "倍", "副")
        assertEquals(emptyList<String>(), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(dissection) +
            n1.filter { it.kanji != "剖" }.shuffled(kotlin.random.Random(693)).take(15)
        val checkedPools = JSONArray()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all,
            "boundedCustom" to boundedCustom, "randomN1Subset" to randomSubset)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "剖" }
            assertEquals(curatedIds, target.distractors)
            val available = curatedIds.filter { id -> cards.any { it.kanji == id } }
            val expectedAvailable = if (poolName == "N1" || poolName == "randomN1Subset") 0 else 3
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
        val importedDissection = words.single { it.word == "解剖" }
        assertEquals(listOf("分析", "分解", "検査"), importedDissection.quizExclusions)
        assertEquals("かいぼう", importedDissection.reading)
        assertNull(importedDissection.jlpt)
        val directGuardChecks = JSONArray()
        val guardPairs = listOf("解剖" to "分析", "解剖" to "分解", "解剖" to "検査")
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
        assertEquals(384, directGuardChecks.length())
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
                        if (card.kanji == "剖") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "剖" && (kind == ReadingKind.On && key == "ぼう")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "剖", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("newDirectWordGuardPairs", 3).put("directGuardBuilderChecks", directGuardChecks)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(dissection.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(dissection.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(dissection.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(dissection.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(dissection.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(dissection.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 剖 meaning and onぼう due; no kun keys. Full raw readings and explicit curation retained. Two historical good 剖 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 127 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("剖")
            click("dissect; split open")
            await("剖 — dissect; split open")
            show(articleBullet("Strokes: 10 · Key (radical): 刀 (no. 18), appearing as 刂 on the right · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("剖 concerns cutting something open or separating it to examine it. In 解剖 かいぼう, it contributes the idea of dissecting; the whole word also has a figurative \"analysis\" sense. Do not use 剖 as a standalone replacement for the general verb 分ける わける, \"divide; separate.\""), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Picture the stacked 立-over-口 shape on the left as something opened by the blade-shaped 刂 on the right. This invented scene helps distinguish the modern shape; it is not a historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(readingExample("ボウ"), "kanji-09")
            show(readingExample("解剖 かいぼう — dissection; autopsy; figurative analysis"), "kanji-11")
            show(articleBullet("This card selects ボウ for reading questions. The frozen KANJIDIC2 record has no kunyomi. Other dictionaries also record ホウ; that does not make it an invalid reading, but it is outside this card's source reading list."), "kanji-12")
            section("Common words")
            show(articleBullet("解剖 かいぼう — dissection; autopsy; analysis"), "kanji-14")
            show(articleBullet("解剖学 かいぼうがく — anatomy, the field of study"), "kanji-15")
            section("Notes")
            show(articleBullet("The indexing radical is 刀; its right-hand form here is 刂."), "kanji-17")
            show(articleBullet("部, \"section; department,\" has the same stacked left shape but right-hand 阝 instead of 刂. 倍, \"multiple; double,\" has left-hand 亻 beside the stacked shape. 副, \"vice-; secondary,\" shares the right-hand 刂 but has a different left block."), "kanji-18")
            show(articleBullet("分 and 解 also have separating or dividing associations. Those related meanings do not make all their words interchangeable."), "kanji-19")
            show(articleBullet("解剖 is not limited to investigating a cause of death: it can concern learning a body's structure, and it can figuratively analyze a case."), "kanji-20")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families: JMdict, entries 1199270 and 1199280. Reading allocation and usage: Digital Daijisen, 剖 and 解剖."), "kanji-21")
            section("Common words")
            show(articleBullet("解剖 かいぼう — dissection; autopsy; analysis"), "kaibou-forward")
            inline(await(articleBullet("解剖 かいぼう — dissection; autopsy; analysis")), "解剖", 0)
            await("Article contents")
            await("解剖 (かいぼう) — dissection; autopsy; analysis")
            section("Meaning")
            show(articleBullet("解剖 means dissection: cutting open a body to examine its internal structure. Depending on the purpose and context, it can mean an autopsy or postmortem examination. It is not limited to finding a cause of death."), "kaibou-02")
            show(articleBullet("医学生は解剖で体の構造を学びます。 (いがくせいはかいぼうでからだのこうぞうをまなびます。) — Medical students learn the body's structure through dissection."), "kaibou-03")
            show(articleBullet("It also means analyzing something in detail to clarify its structure or causal relationships. Digital Daijisen gives the figurative example 事件を解剖する (じけんをかいぼうする), \"analyze a case.\""), "kaibou-04")
            show(articleBullet("解剖 is a noun and a transitive する verb: Nを解剖する means to dissect or analyze N. The object and context distinguish physical dissection from figurative analysis."), "kaibou-05")
            section("How the kanji combine")
            show(articleBullet("解 contributes undoing or separating, and 剖 contributes splitting open or dissecting. The related actions combine in the idea of opening something up to examine it. This is a meaning aid, not a reconstruction of the word's history. The on readings are カイ + ボウ."), "kaibou-07")
            section("Synonyms and antonyms")
            show(articleBullet("分析 ぶんせき is analysis and does not imply a physical cut. It overlaps the figurative sense of 解剖. 分解 ぶんかい means taking apart or breaking down into components and also has an analysis sense."), "kaibou-09")
            show(articleBullet("検査 けんさ is inspection, examination or testing more generally. A medical test is not automatically 解剖: 解剖 specifically brings in dissection in its physical sense. There is no single everyday opposite covering both the physical and figurative senses."), "kaibou-10")
            section("Distinctive meaning")
            show(articleBullet("In medical or biological contexts, 解剖 identifies dissection or an autopsy, not every examination of a patient. In figurative use, it presents detailed analysis as opening something up to understand how it works."), "kaibou-12")
            show(articleBullet("Distinguish 解剖学 (かいぼうがく), \"anatomy,\" the field of study, from a particular dissection or autopsy."), "kaibou-13")
            show(articleBullet("Dictionary: JMdict, entry 1199270, senses 1–2, and entry 1199280; Digital Daijisen, 解剖, including the attributed figurative example. The medical-student sentence is an original illustration, not a quotation."), "kaibou-14")
            section("How the kanji combine")
            show(articleBullet("解 contributes undoing or separating, and 剖 contributes splitting open or dissecting. The related actions combine in the idea of opening something up to examine it. This is a meaning aid, not a reconstruction of the word's history. The on readings are カイ + ボウ."), "bou-reverse")
            inline(await(articleBullet("解 contributes undoing or separating, and 剖 contributes splitting open or dissecting. The related actions combine in the idea of opening something up to examine it. This is a meaning aid, not a reconstruction of the word's history. The on readings are カイ + ボウ.")), "剖", 41)
            await("Article contents")
            section("Readings")
            show(readingExample("ボウ"), "bou-kanji-backlink")
            back()
            await(articleBullet("解 contributes undoing or separating, and 剖 contributes splitting open or dissecting. The related actions combine in the idea of opening something up to examine it. This is a meaning aid, not a reconstruction of the word's history. The on readings are カイ + ボウ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("bou-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("解 contributes undoing or separating, and 剖 contributes splitting open or dissecting. The related actions combine in the idea of opening something up to examine it. This is a meaning aid, not a reconstruction of the word's history. The on readings are カイ + ボウ."), "kai-reverse")
            inline(await(articleBullet("解 contributes undoing or separating, and 剖 contributes splitting open or dissecting. The related actions combine in the idea of opening something up to examine it. This is a meaning aid, not a reconstruction of the word's history. The on readings are カイ + ボウ.")), "解", 0)
            await("Article contents")
            await("解 — unravel; solve")
            show(articleBullet("Strokes: 13 · Key (radical): 角 (no. 148) · JLPT: N3 (community list)"), "kai-01")
            section("Meaning and origin")
            show(articleBullet("解 spans undoing a tangle and working something out. 理解 りかい concerns comprehension; 解く とく can mean untying something or solving a problem. This gives a useful learning connection between releasing a knot and resolving a difficulty, without making a historical claim."), "kai-03")
            show(articleBullet("Modern-shape mnemonic: locate 角 on the left, with 刀 above 牛 on the right. Imagine taking a complicated arrangement apart. This is a modern memory scene, not verified etymology."), "kai-04")
            section("Readings")
            show(readingExample("カイ"), "kai-09")
            show(readingExample("理解 りかい — understanding; 誤解 ごかい — misunderstanding"), "kai-11")
            show(readingExample("と.く"), "kai-12")
            show(readingExample("解く とく — untie; solve"), "kai-14")
            section("Common words")
            show(articleBullet("理解 りかい — comprehension"), "kai-16")
            show(articleBullet("解く とく — untie; solve"), "kai-17")
            show(articleBullet("誤解 ごかい — misunderstanding"), "kai-18")
            show(articleBullet("解剖 かいぼう — dissection; autopsy; figurative analysis"), "kai-19")
            section("Notes")
            show(articleBullet("問題を解く (もんだいをとく) means \"solve a problem.\" Understanding a problem and solving it are related but not identical tasks. 物 and 特 put their cattle component on the left, unlike the lower-right 牛 here. 料 is only a looser dense-stroke contrast; it has neither the same left part nor the same layout."), "kai-21")
            show(articleBullet("Metadata: KANJIDIC2."), "kai-22")
            show(articleBullet("Vocabulary: JMdict, entries 1549910, 1198890, 1271310."), "kai-23")
            section("Common words")
            show(articleBullet("解剖 かいぼう — dissection; autopsy; figurative analysis"), "kai-kaibou-forward")
            inline(await(articleBullet("解剖 かいぼう — dissection; autopsy; figurative analysis")), "解剖", 0)
            await("Article contents")
            section("Meaning")
            capture("kai-kaibou-backlink")
            back()
            await(articleBullet("解剖 かいぼう — dissection; autopsy; figurative analysis")).assertIsDisplayed()
            section("Common words")
            capture("kai-system-back-to-kanji")
            back()
            await(articleBullet("解 contributes undoing or separating, and 剖 contributes splitting open or dissecting. The related actions combine in the idea of opening something up to examine it. This is a meaning aid, not a reconstruction of the word's history. The on readings are カイ + ボウ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("kai-system-back-to-word")
            back()
            await(articleBullet("解剖 かいぼう — dissection; autopsy; analysis")).assertIsDisplayed()
            section("Common words")
            capture("kaibou-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4).put("activatedBaselinePairs", 0)
                .put("completeArticleProjections", 3).put("changedReusedArticles", 1)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("剖", meaning.card.kanji)
            assertEquals(4, meaning.options.size)
            assertEquals(4, meaning.options.map { it.title }.toSet().size)
            assertEquals(1, meaning.options.count { it.kanji == "剖" })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertFalse(meaning.options.any { it.kanji in setOf("部", "倍", "副") })
            assertEquals("dissect; split open", meaning.options.single { it.kanji == "剖" }.title)
            assertEquals(listOf("部", "倍", "副"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 0).put("actualN1FallbackOptions", 3)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("dissect; split open")
            await("Correct!")
            assertEquals("剖", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("剖", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("ぼう"))
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "剖" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("ぼう"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "剖" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("ぼう"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })
            capture("curated-one-on-no-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("dissect; split open").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "剖") })
            assertEquals(listOf("部", "倍", "副"), card.distractors.splitSep())
            assertEquals(listOf("ボウ"), card.onyomi.splitSep())
            assertEquals(emptyList<String>(), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ボウ"), card.quizOnyomi?.splitSep())
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
                    it.kanji == "剖" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "剖" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("onlyOnBouNoKunPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-095-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-095-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-095-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
