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

private fun disposable094() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch094GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun shavingLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable094()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("一 不 中 予 余 刀 刂 切 刑 判 削 前", "加 取 外 掃 文 斫 日 曜 止 氵 消 添", "減 省 筆 算 肖 行 複 要 追 都 重 鉛", "阜 阝 降 院 除", "削 消 肖 刀 刂 斫 氵 阜 阝 前 判 刑 削る 削除 削ぐ")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 094: shaving / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 41 scoped Han; focused 削/消/肖/刀/刂/斫/氵/阜/阝/前/判/刑. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("一", "不", "中", "予", "余", "刀", "刂", "切", "刑", "判", "削", "前", "加", "取", "外", "掃", "文", "斫", "日", "曜", "止", "氵", "消", "添", "減", "省", "筆", "算", "肖", "行", "複", "要", "追", "都", "重", "鉛", "阜", "阝", "降", "院", "除")) {
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
            for (word in listOf("削る", "削除", "削ぐ")) {
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
        assertEquals(176, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-094-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-094-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 164).put("wholeWordRasterProbes", 12).put("panels", 5)
            .put("limits", "41 actual scoped Han; 刂/斫/氵/阝 absent from all three bundled cmaps requires actual system fallback inspection, four production families, five bounded Compose panels and twelve whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch094ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineShavingTwoReusedN2ThreeReciprocalPairsBothReadingsNineStrokesAndSystemBack() {
        disposable094()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-094-${UUID.randomUUID()}", "main")
        val head = "18ad4bed3264a7c30e04cd60edbd85264a5b39d8"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-094-18ad4bed-envelope.zip")
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
        assertEquals(1117, updated.kanji)
        assertEquals(5070, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("eeae47753a460f72", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(126, n1.size)
        val shaving = n1.single { it.kanji == "削" }
        assertEquals(listOf("前", "判", "刑"), shaving.distractors.splitSep())
        assertEquals(listOf("サク"), shaving.onyomi.splitSep())
        assertEquals(listOf("けず.る", "はつ.る", "そ.ぐ"), shaving.kunyomi.splitSep())
        assertNotNull(shaving.quizOnyomi)
        assertNotNull(shaving.quizKunyomi)
        assertEquals(listOf("サク"), shaving.quizOnyomi?.splitSep())
        assertEquals(listOf("けず.る"), shaving.quizKunyomi?.splitSep())
        assertEquals(listOf("さく"), shaving.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("けずる"), shaving.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "削" to "shave; sharpen; pare", "刑" to "criminal punishment",
            "前" to "front, before", "判" to "judge; seal",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        assertEquals(n1.map { it.kanji }.toSet(),
            all.filter { "jlpt-n1" in it.tags.splitSep() }.map { it.kanji }.toSet())
        val curatedIds = listOf("前", "判", "刑")
        assertEquals(listOf("刑"), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(shaving, n1.single { it.kanji == "刑" }) +
            n1.filter { it.kanji !in setOf("削", "刑") }.shuffled(kotlin.random.Random(681)).take(12)
        val checkedPools = JSONArray()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all,
            "boundedCustom" to boundedCustom, "randomN1Subset" to randomSubset)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "削" }
            assertEquals(curatedIds, target.distractors)
            val available = curatedIds.filter { id -> cards.any { it.kanji == id } }
            val expectedAvailable = if (poolName == "N1" || poolName == "randomN1Subset") 1 else 3
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
        val importedShave = words.single { it.word == "削る" }
        val importedDeletion = words.single { it.word == "削除" }
        assertEquals(listOf("切る", "減らす", "省く", "消す", "除く", "外す"), importedShave.quizExclusions)
        assertEquals(listOf("消す", "除く", "外す", "取る", "削る", "省く"), importedDeletion.quizExclusions)
        assertEquals("けずる", importedShave.reading)
        assertEquals("さくじょ", importedDeletion.reading)
        assertEquals(2, importedShave.jlpt)
        assertEquals(2, importedDeletion.jlpt)
        val directGuardChecks = JSONArray()
        val guardPairs = listOf("削る" to "除く", "削る" to "外す", "削除" to "省く")
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
                        if (card.kanji == "削") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "削" && ((kind == ReadingKind.On && key == "さく") || (kind == ReadingKind.Kun && key == "けずる"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "削", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
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
            .put("fullOnyomi", JSONArray(shaving.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(shaving.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(shaving.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(shaving.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(shaving.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(shaving.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 削 meaning and onさく/kunけずる due. Full raw readings and explicit curation retained. Two historical good 削 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 126 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("削")
            click("shave; sharpen; pare")
            await("削 — shave; sharpen; pare")
            show(articleBullet("Strokes: 9 · Key (radical): 刀 (no. 18), appearing as 刂 on the right · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("削 concerns shaving or cutting material away. 削る けずる can mean sharpening a pencil by shaving it, reducing an amount, or deleting part of a text. In 削除 さくじょ, the focus is deletion or erasure, not necessarily a physical cut."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Picture the 肖-shaped left part as a block with small marks above it, being shaved by the blade radical 刂 on the right. This invented scene is a memory aid, not a historical explanation or a verified phonetic analysis."), "kanji-04")
            section("Readings")
            show(readingExample("サク"), "kanji-09")
            show(readingExample("削除 さくじょ — deletion; erasure"), "kanji-11")
            show(readingExample("けず.る"), "kanji-12")
            show(readingExample("削る けずる — shave; sharpen; pare; cut down"), "kanji-14")
            show(readingExample("はつ.る"), "kanji-15")
            show(readingExample("削る はつる — shave off, especially concrete; usually written はつる; also written 斫る in construction"), "kanji-17")
            show(readingExample("そ.ぐ"), "kanji-18")
            show(readingExample("削ぐ そぐ — chip, shave or slice off"), "kanji-20")
            show(articleBullet("This card selects サク and けず.る for reading questions. The other two readings remain useful recognition information, not invalid or obsolete pronunciations. The dots mark the written ending: 削る has る outside the kanji, while 削ぐ has ぐ."), "kanji-21")
            section("Common words")
            show(articleBullet("削る けずる — shave; sharpen; cut down"), "kanji-23")
            show(articleBullet("削除 さくじょ — deletion; erasure"), "kanji-24")
            show(articleBullet("削減 さくげん — reduction; cut"), "kanji-25")
            show(articleBullet("添削 てんさく — correction of writing"), "kanji-26")
            show(articleBullet("Two practical uses of けずる are 鉛筆を削る (えんぴつをけずる), \"sharpen a pencil,\" and 予算を削る (よさんをけずる), \"cut the budget.\""), "kanji-27")
            section("Notes")
            show(articleBullet("The indexing radical is 刀; its visible form here is 刂. 消 also has a 肖-shaped part, but its left side is 氵 rather than the right-side 刂 of 削. Erasing and deleting meanings can overlap; these shapes do not create an absolute semantic boundary."), "kanji-29")
            show(articleBullet("The spelling 削る can represent the separate verb はつる as well as けずる. The linked word article teaches けずる. JMdict's \"take a percentage\" sense belongs to its separate はつる entry, not the けずる lesson."), "kanji-30")
            show(articleBullet("削ぐ そぐ is another verb, not a different spelling of けずる. It also has figurative weakening or dampening uses; JMdict marks those senses as usually written in kana, not every physical use of 削ぐ."), "kanji-31")
            show(articleBullet("Compare the right-side 刂 in 前, 判 and 刑. Their meanings are not shaving or sharpening; a shared radical does not make the words interchangeable."), "kanji-32")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families: JMdict, entries 1298040, 1298090, 1298100, 1298110, 1298120, 1440850 and 1915010. Reading allocation and usage: Digital Daijisen, 削, 削る and 削除."), "kanji-33")
            section("Common words")
            show(articleBullet("削る けずる — shave; sharpen; cut down"), "kezuru-forward")
            inline(await(articleBullet("削る けずる — shave; sharpen; cut down")), "削る", 0)
            await("Article contents")
            await("削る (けずる) - shave; pare; cut down")
            section("Meaning")
            show(articleBullet("削る means shaving or scraping material away, including sharpening a pencil. It also means cutting down an amount, such as a budget, expenses, or time. This is a transitive godan verb: 削ります, 削って, 削らない."), "kezuru-02")
            show(articleBullet("ナイフで鉛筆を削ります。 (ナイフでえんぴつをけずります。) - I sharpen a pencil with a knife."), "kezuru-03")
            show(articleBullet("予算を削りました。 (よさんをけずりました。) - We cut the budget."), "kezuru-04")
            show(articleBullet("A further use is deleting or striking out part of a text: 不要な一文を削りました。 (ふようないちぶんをけずりました。) - I deleted an unnecessary sentence. This deletion use is additional teaching, not a separate N2 assignment."), "kezuru-05")
            section("How the kanji combine")
            show(articleBullet("削 contributes cutting away or shaving. The native reading is けず.る: the kanji supplies けず, and る is the written ending. This is one native verb, not a combination of on readings."), "kezuru-07")
            section("Synonyms and antonyms")
            show(articleBullet("減らす (へらす) more generally means reducing an amount. 省く (はぶく) overlaps in omission or cutting down; 消す (けす) overlaps in erasing. 切る (きる) has broader cutting uses, including reductions."), "kezuru-09")
            section("Distinctive meaning")
            show(articleBullet("削る need not mean removing a large piece in one cut; shaving a surface is a central use. Nor does every use require repeated tiny reductions. The source list's \"take a percentage\" belongs to the separate reading はつる in JMdict, not this けずる entry. Do not learn it here as a general expression for charging commission."), "kezuru-11")
            show(articleBullet("Dictionary: JMdict, entry 1298090, selected senses 1-2 and additional sense 3; separate はつる entry 1298100, sense 2. Usage check: Daijisen, hosted by Weblio, separate けずる, はつる, and へずる entries."), "kezuru-12")
            section("How the kanji combine")
            show(articleBullet("削 contributes cutting away or shaving. The native reading is けず.る: the kanji supplies けず, and る is the written ending. This is one native verb, not a combination of on readings."), "kezuru-reverse")
            inline(await(articleBullet("削 contributes cutting away or shaving. The native reading is けず.る: the kanji supplies けず, and る is the written ending. This is one native verb, not a combination of on readings.")), "削", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("けず.る"), "kezuru-kanji-backlink")
            back()
            await(articleBullet("削 contributes cutting away or shaving. The native reading is けず.る: the kanji supplies けず, and る is the written ending. This is one native verb, not a combination of on readings.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("kezuru-system-back-to-word")
            back()
            await(articleBullet("削る けずる — shave; sharpen; cut down")).assertIsDisplayed()
            section("Common words")
            capture("kezuru-system-back-to-kanji")
            section("Common words")
            show(articleBullet("削除 さくじょ — deletion; erasure"), "sakujo-forward")
            inline(await(articleBullet("削除 さくじょ — deletion; erasure")), "削除", 0)
            await("Article contents")
            await("削除 (さくじょ) - deletion; erasure")
            section("Meaning")
            show(articleBullet("削除 is deletion or elimination, especially removing writing, entries, or data. 削除する is transitive: the item removed takes を."), "sakujo-02")
            show(articleBullet("重複した行を削除しました。 (ちょうふくしたぎょうをさくじょしました。) - I deleted the duplicate line."), "sakujo-03")
            show(articleBullet("このファイルを削除してもいいですか。 (このファイルをさくじょしてもいいですか。) - May I delete this file?"), "sakujo-04")
            show(articleBullet("削除されたファイル (さくじょされたファイル) is \"a deleted file\"; された is passive."), "sakujo-05")
            section("How the kanji combine")
            show(articleBullet("削 contributes shaving or cutting away, and 除 contributes removal or exclusion. The related meanings reinforce taking something out. The on readings are サク + ジョ, with a small ょ. Deleting a line is not a claim that paper was physically shaved."), "sakujo-07")
            section("Synonyms and antonyms")
            show(articleBullet("消す (けす) also covers erasing or deleting, as well as turning off lights. 除く (のぞく) is broader removal or exclusion. 追加 (ついか), \"addition,\" supplies a practical contrast when editing a list."), "sakujo-09")
            section("Distinctive meaning")
            show(articleBullet("The legacy source's \"cancellation\" should not make 削除する a general verb for canceling an event. 中止 (ちゅうし) concerns calling off or discontinuing an activity. Deleting a calendar entry and canceling the event itself are different actions. The word alone also does not promise that deleted data can be recovered."), "sakujo-11")
            show(articleBullet("Dictionary: JMdict, entry 1298120, sense 1. Usage: Digital Daijisen."), "sakujo-12")
            section("How the kanji combine")
            show(articleBullet("削 contributes shaving or cutting away, and 除 contributes removal or exclusion. The related meanings reinforce taking something out. The on readings are サク + ジョ, with a small ょ. Deleting a line is not a claim that paper was physically shaved."), "sakujo-saku-reverse")
            inline(await(articleBullet("削 contributes shaving or cutting away, and 除 contributes removal or exclusion. The related meanings reinforce taking something out. The on readings are サク + ジョ, with a small ょ. Deleting a line is not a claim that paper was physically shaved.")), "削", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("サク"), "saku-kanji-backlink")
            back()
            await(articleBullet("削 contributes shaving or cutting away, and 除 contributes removal or exclusion. The related meanings reinforce taking something out. The on readings are サク + ジョ, with a small ょ. Deleting a line is not a claim that paper was physically shaved.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("saku-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("削 contributes shaving or cutting away, and 除 contributes removal or exclusion. The related meanings reinforce taking something out. The on readings are サク + ジョ, with a small ょ. Deleting a line is not a claim that paper was physically shaved."), "sakujo-jo-reverse")
            inline(await(articleBullet("削 contributes shaving or cutting away, and 除 contributes removal or exclusion. The related meanings reinforce taking something out. The on readings are サク + ジョ, with a small ょ. Deleting a line is not a claim that paper was physically shaved.")), "除", 43)
            await("Article contents")
            await("除 — remove; exclude")
            show(articleBullet("Strokes: 10 · Key (radical): 阜 (as left-hand 阝, no. 170) · JLPT: N3 (community list)"), "jo-01")
            section("Meaning and origin")
            show(articleBullet("除 concerns taking something away or leaving it out. 除く のぞく can describe physical removal, but also an exception: 日曜日を除く (にちようびをのぞく), \"excluding Sundays.\""), "jo-03")
            show(articleBullet("Modern-shape mnemonic: imagine clearing the 余-shaped piece away from the left-hand 阝. This is a visual reminder of removal, not an etymology."), "jo-04")
            section("Readings")
            show(articleBullet("The table selects useful readings; the metadata preserves the complete source reading list."), "jo-06")
            show(readingExample("のぞ.く"), "jo-10")
            show(readingExample("除く のぞく — remove; exclude"), "jo-12")
            show(readingExample("ジョ"), "jo-13")
            show(readingExample("除外 じょがい — exclusion"), "jo-15")
            show(readingExample("ジ"), "jo-16")
            show(readingExample("掃除 そうじ — cleaning"), "jo-18")
            section("Common words")
            show(articleBullet("除く のぞく — remove; exclude"), "jo-20")
            show(articleBullet("除外 じょがい — exclusion"), "jo-21")
            show(articleBullet("掃除 そうじ — cleaning"), "jo-22")
            show(articleBullet("削除 さくじょ — deletion; erasure"), "jo-23")
            section("Notes")
            show(articleBullet("掃除 uses ジ, not ジョ; learn its whole reading そうじ. Excluding a day from a schedule does not remove that day from the calendar: the scope of the statement changes. 降 shares left-hand 阝 but not the 余 on its right."), "jo-25")
            show(articleBullet("Metadata: KANJIDIC2. Dictionary: JMdict, entries 1345640, 1345650, 1399790."), "jo-26")
            section("Common words")
            show(articleBullet("削除 さくじょ — deletion; erasure"), "jo-sakujo-forward")
            inline(await(articleBullet("削除 さくじょ — deletion; erasure")), "削除", 0)
            await("Article contents")
            section("Meaning")
            capture("jo-sakujo-backlink")
            back()
            await(articleBullet("削除 さくじょ — deletion; erasure")).assertIsDisplayed()
            section("Common words")
            capture("jo-system-back-to-kanji")
            back()
            await(articleBullet("削 contributes shaving or cutting away, and 除 contributes removal or exclusion. The related meanings reinforce taking something out. The on readings are サク + ジョ, with a small ょ. Deleting a line is not a claim that paper was physically shaved.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("jo-system-back-to-word")
            back()
            await(articleBullet("削除 さくじょ — deletion; erasure")).assertIsDisplayed()
            section("Common words")
            capture("sakujo-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 3).put("directedLinkTransitions", 6).put("activatedBaselinePairs", 2)
                .put("completeArticleProjections", 4).put("changedReusedArticles", 3)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("削", meaning.card.kanji)
            assertEquals(4, meaning.options.size)
            assertEquals(4, meaning.options.map { it.title }.toSet().size)
            assertEquals(1, meaning.options.count { it.kanji == "削" })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertEquals("criminal punishment", meaning.options.single { it.kanji == "刑" }.title)
            assertFalse(meaning.options.any { it.kanji in setOf("前", "判") })
            assertEquals("shave; sharpen; pare", meaning.options.single { it.kanji == "削" }.title)
            assertEquals(listOf("前", "判", "刑"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 1).put("actualN1FallbackOptions", 2)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("shave; sharpen; pare")
            await("Correct!")
            assertEquals("削", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("削", question.card.kanji)
                val key = question.question.correctKey
                assertTrue(key in setOf("さく", "けずる"))
                assertTrue("Duplicate target reading key", answeredKeys.add(key))
                assertEquals(if (key == "さく") ReadingKind.On else ReadingKind.Kun, question.question.kind)
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-${key}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (question.question.kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${key}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "削" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("さく", "けずる"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "削" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("さく", "けずる"), readingLogs.map { it.reading }.toSet())
            assertEquals(setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name), readingLogs.map { it.mode }.toSet())
            capture("curated-one-on-one-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("shave; sharpen; pare").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "削") })
            assertEquals(listOf("前", "判", "刑"), card.distractors.splitSep())
            assertEquals(listOf("サク"), card.onyomi.splitSep())
            assertEquals(listOf("けず.る", "はつ.る", "そ.ぐ"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("サク"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("けず.る"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(9, strokes.length())
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
            rule.onNode(hasContentDescription("9 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "削" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "削" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("onlySakuAndKezuruBothKindsPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-094-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-094-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-094-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
