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

private fun disposable083Corrected() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch083CorrectedGlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun enduranceLookalikesAndRadicalFallbacksAcrossFourProductionFamilies() {
        disposable083Corrected()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("上 作 傑 優 冫 冴 冶 准 凌 前 台 回 売 夌 忍 慢 我 欠 次 行 超 越 追 過", "阝 陵 隹 雨 風 駕", "凌 陵 准 冶 冴 次 冫 夌 阝 隹 凌ぐ 凌駕")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 083: endurance / look-alikes / radical fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 30 scoped Han; focused 凌/陵/准/冶/冴/次, 冫/夌/阝/隹. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("上", "作", "傑", "優", "冫", "冴", "冶", "准", "凌", "前", "台", "回", "売", "夌", "忍", "慢", "我", "欠", "次", "行", "超", "越", "追", "過", "阝", "陵", "隹", "雨", "風", "駕")) {
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
            for (word in listOf("凌ぐ", "凌駕")) {
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
        assertEquals(128, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-083-corrected-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-083-corrected-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 120).put("wholeWordRasterProbes", 8).put("panels", 3)
            .put("limits", "30 actual scoped Han including exact 冫/夌/阝/隹 fallback inspection, four production families, three bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch083CorrectedArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineEnduranceTwoReciprocalPairsCuratedOnAndKunDrawingAndSystemBack() {
        disposable083Corrected()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-083-corrected-${UUID.randomUUID()}", "main")
        val head = "867fe8bef228145ef0a6e48690941b0a0aa50336"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-083-corrected-867fe8be-envelope.zip")
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
        assertEquals(1095, updated.kanji)
        assertEquals(5052, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("6dfe6a1e287ce5df", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(115, n1.size)
        val endurance = n1.single { it.kanji == "凌" }
        assertEquals(listOf("准", "冶", "冴"), endurance.distractors.splitSep())
        assertEquals(listOf("リョウ"), endurance.onyomi.splitSep())
        assertEquals(listOf("しの.ぐ"), endurance.kunyomi.splitSep())
        assertNotNull(endurance.quizOnyomi)
        assertNotNull(endurance.quizKunyomi)
        assertEquals(listOf("リョウ"), endurance.quizOnyomi?.splitSep())
        assertEquals(listOf("しの.ぐ"), endurance.quizKunyomi?.splitSep())
        assertEquals(listOf("りょう"), endurance.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("しのぐ"), endurance.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "凌" to "endure; surpass", "准" to "quasi-; associate rank",
            "冶" to "smelt; work metals", "冴" to "clear; sharp-minded",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "凌" }
            assertEquals(listOf("准", "冶", "冴"), target.distractors)
            assertEquals(expectedMeanings, cards.filter { it.kanji in expectedMeanings }.associate { it.kanji to it.title })
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(577))
            assertEquals(4, options.size)
            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("allThreeCuratedAvailable", true).put("defaultFourNoPadding", true))
        }
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
                        if (card.kanji == "凌") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "凌" && key == (if (kind == ReadingKind.On) "りょう" else "しのぐ")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "凌", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(endurance.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(endurance.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(endurance.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(endurance.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(endurance.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(endurance.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 凌 meaning and curated onりょう/kunしのぐ due. Two historical good 凌 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 115 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("凌")
            click("endure; surpass")
            await("凌 — endure; surpass")
            show(articleBullet("Strokes: 10 · Key (radical): 冫 (the two left-hand strokes, no. 15) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("凌 has two useful branches: enduring or getting through a difficulty, and surpassing something else. In 凌ぐ (しのぐ), the context selects between these branches. 凌駕 (りょうが) concerns surpassing, not sheltering from bad weather."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: imagine the two 冫 marks as drops beside the right-hand 夌 shape, pictured as a barrier. Think of weathering the drops or getting beyond the barrier. This is an invented memory scene, not a historical derivation or a verified explanation of the sound."), "kanji-04")
            section("Readings")
            show(readingExample("リョウ"), "kanji-09")
            show(readingExample("凌駕 りょうが — surpassing; outdoing"), "kanji-11")
            show(readingExample("しの.ぐ"), "kanji-12")
            show(readingExample("凌ぐ しのぐ — endure; surpass"), "kanji-14")
            show(articleBullet("Both readings in the frozen KANJIDIC2 record are selected for practice. Its grade-9/name-use classification does not make these ordinary word readings personal-name readings; names are not taught here."), "kanji-15")
            section("Common words")
            show(articleBullet("凌ぐ しのぐ — endure or pull through; surpass"), "kanji-17")
            show(articleBullet("凌駕 りょうが — surpassing; outdoing, also with する"), "kanji-18")
            section("Notes")
            show(articleBullet("凌ぐ is a ぐ-ending verb: しのぎます, しのいで, しのいだ. Do not confuse it with the separate verb 忍ぶ (しのぶ), which ends in ぶ."), "kanji-20")
            show(articleBullet("陵 (りょう; みささぎ) has 阝 on the left rather than 凌's two 冫 strokes. Recognizing the rarer spelling 陵駕 (りょうが) does not make these characters freely interchangeable in other words."), "kanji-21")
            show(articleBullet("Compare 准, \"quasi-; associate rank,\" with 隹 on the right; 冶, \"smelt; work metals,\" with 台; and 次, \"next,\" with 欠. Similar left-hand marks do not imply the same meaning."), "kanji-22")
            show(articleBullet("Metadata: KANJIDIC2, database 2026-306, 2026-11-02 (EDRDG; CC BY-SA 4.0). Words: JMdict, entries 1554200, 1606270 and 1467450. Usage: Digital Daijisen: 凌ぐ and 凌駕."), "kanji-23")
            section("Common words")
            show(articleBullet("凌ぐ しのぐ — endure or pull through; surpass"), "endure-word-forward-14")
            inline(await(articleBullet("凌ぐ しのぐ — endure or pull through; surpass")), "凌ぐ", 0)
            await("Article contents")
            await("凌ぐ (しのぐ) — endure; surpass")
            section("Meaning")
            show(articleBullet("凌ぐ can mean endure, keep out, or get through something difficult. It can also mean surpass or outdo someone or something in ability, degree or quality. Learn the whole phrase rather than assigning one English equivalent to every occurrence."), "endure-word-02")
            show(articleBullet("風雨を凌ぐ (ふううをしのぐ) — shelter from wind and rain"), "endure-word-03")
            show(articleBullet("前作を凌ぐ傑作 (ぜんさくをしのぐけっさく) — a masterpiece surpassing the previous work"), "endure-word-04")
            show(articleBullet("These short phrases illustrate the two branches. The difficulty faced or the thing surpassed takes を. 凌ぐ is a transitive godan verb ending in ぐ: しのぎます, しのいで, しのいだ, しのがない."), "endure-word-05")
            section("How the kanji combine")
            show(articleBullet("凌 supplies the enduring or surpassing idea. The native verb is しのぐ: ぐ is written as okurigana, while 凌 represents しの-. The same word, not a different reading, has both meaning branches."), "endure-word-07")
            section("Synonyms and antonyms")
            show(articleBullet("こらえる and 我慢 (がまん), with する, overlap in endurance. Their restraint uses do not all transfer to 凌ぐ. 凌駕 (りょうが), with する, overlaps with the surpassing branch, not with sheltering from the weather."), "endure-word-09")
            show(articleBullet("忍ぶ (しのぶ) is a separate verb that can also mean endure. Its ending is ぶ, not 凌ぐ's ぐ: do not confuse しのいで with しのんで."), "endure-word-10")
            section("Distinctive meaning")
            show(articleBullet("Getting through a difficulty does not by itself promise a permanent solution. Conversely, 凌ぐ is not restricted to brief emergencies. In a comparison, it means going above the other thing, not merely matching it. The weather phrase above expresses protection or endurance; the masterpiece phrase expresses comparative quality."), "endure-word-12")
            show(articleBullet("Dictionary: JMdict, entry 1554200, senses 1–3; comparisons 2827352, 1196970, 1606270 and 1467450. Usage and short example phrases: Digital Daijisen: 凌ぐ, senses 2 and 4."), "endure-word-13")
            section("How the kanji combine")
            show(articleBullet("凌 supplies the enduring or surpassing idea. The native verb is しのぐ: ぐ is written as okurigana, while 凌 represents しの-. The same word, not a different reading, has both meaning branches."), "endure-word-reverse-24")
            inline(await(articleBullet("凌 supplies the enduring or surpassing idea. The native verb is しのぐ: ぐ is written as okurigana, while 凌 represents しの-. The same word, not a different reading, has both meaning branches.")), "凌", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("リョウ"), "endure-word-kanji-backlink")
            back()
            await(articleBullet("凌 supplies the enduring or surpassing idea. The native verb is しのぐ: ぐ is written as okurigana, while 凌 represents しの-. The same word, not a different reading, has both meaning branches.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("endure-word-system-back-to-word")
            back()
            await(articleBullet("凌ぐ しのぐ — endure or pull through; surpass")).assertIsDisplayed()
            section("Common words")
            capture("endure-word-system-back-to-kanji")
            section("Common words")
            show(articleBullet("凌駕 りょうが — surpassing; outdoing, also with する"), "surpass-word-forward-25")
            inline(await(articleBullet("凌駕 りょうが — surpassing; outdoing, also with する")), "凌駕", 0)
            await("Article contents")
            await("凌駕 (りょうが) — surpass; outdo")
            section("Meaning")
            show(articleBullet("凌駕 names surpassing or outdoing another thing. It is a noun and a する-verb: 凌駕する, 凌駕します, 凌駕した, 凌駕しない. The thing surpassed takes を."), "surpass-word-02")
            show(articleBullet("前作を凌駕する売れ行き (ぜんさくをりょうがするうれゆき) — sales surpassing those of the previous work"), "surpass-word-03")
            show(articleBullet("Here the comparison concerns sales, not a claim that the new work is artistically better. The context determines the dimension being compared."), "surpass-word-04")
            section("How the kanji combine")
            show(articleBullet("凌 contributes surpassing, read リョウ here. 駕 (ガ) also has a rising-above-others sense, documented with this compound. The two reinforce the surpassing idea; do not force 駕's separate vehicle meaning into a literal story about this word."), "surpass-word-06")
            section("Synonyms and antonyms")
            show(articleBullet("凌ぐ (しのぐ) overlaps in surpassing, but also has endurance and weather-protection uses that 凌駕 does not share. 優れる (すぐれる) describes excellence or superiority; it is an intransitive verb, so its grammar is not 凌駕する's object + を pattern."), "surpass-word-08")
            show(articleBullet("上回る (うわまわる), \"exceed; surpass,\" also suits numerical comparisons. These related words are not unrestricted substitutes in every phrase."), "surpass-word-09")
            section("Distinctive meaning")
            show(articleBullet("凌駕する means going above the comparison target, not simply reaching the same level. Identify what is surpassed and in what respect. It is not a general expression for surviving a hardship."), "surpass-word-11")
            show(articleBullet("陵駕 (りょうが) is also recognized, but JMdict marks that spelling as rarely used. This does not make the pronunciation りょうが rare or make 凌 and 陵 freely interchangeable elsewhere."), "surpass-word-12")
            show(articleBullet("Dictionary: JMdict, entry 1606270; comparisons 1554200, 1539080 and 1352770. Usage and short example phrase: Digital Daijisen: 凌駕. 駕's contribution: Digital Daijisen: 駕, character-entry sense 2."), "surpass-word-13")
            section("How the kanji combine")
            show(articleBullet("凌 contributes surpassing, read リョウ here. 駕 (ガ) also has a rising-above-others sense, documented with this compound. The two reinforce the surpassing idea; do not force 駕's separate vehicle meaning into a literal story about this word."), "surpass-word-reverse-35")
            inline(await(articleBullet("凌 contributes surpassing, read リョウ here. 駕 (ガ) also has a rising-above-others sense, documented with this compound. The two reinforce the surpassing idea; do not force 駕's separate vehicle meaning into a literal story about this word.")), "凌", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("リョウ"), "surpass-word-kanji-backlink")
            back()
            await(articleBullet("凌 contributes surpassing, read リョウ here. 駕 (ガ) also has a rising-above-others sense, documented with this compound. The two reinforce the surpassing idea; do not force 駕's separate vehicle meaning into a literal story about this word.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("surpass-word-system-back-to-word")
            back()
            await(articleBullet("凌駕 りょうが — surpassing; outdoing, also with する")).assertIsDisplayed()
            section("Common words")
            capture("surpass-word-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)
                .put("completeArticleProjections", 3)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("凌", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "凌" to "endure; surpass",
                "准" to "quasi-; associate rank",
                "冶" to "smelt; work metals",
                "冴" to "clear; sharp-minded",
            )
            assertEquals(4, meaning.options.size)
            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })
            assertEquals(listOf("准", "冶", "冴"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("exactCuratedChoicesWithoutFallback", true)
            capture("meaning-question")
            click("endure; surpass")
            await("Correct!")
            assertEquals("凌", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("凌", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "りょう" else "しのぐ"
                assertEquals(key, question.question.correctKey)
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-${question.question.kind}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (question.question.kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${question.question.kind}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "凌" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "凌" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("りょう", "しのぐ"), readingLogs.map { it.reading }.toSet())
            capture("curated-on-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("endure; surpass").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "凌") })
            assertEquals(listOf("准", "冶", "冴"), card.distractors.splitSep())
            assertEquals(listOf("リョウ"), card.onyomi.splitSep())
            assertEquals(listOf("しの.ぐ"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("リョウ"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("しの.ぐ"), card.quizKunyomi?.splitSep())
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
                    it.kanji == "凌" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "凌" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKindsPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-083-corrected-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-083-corrected-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-083-corrected-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
