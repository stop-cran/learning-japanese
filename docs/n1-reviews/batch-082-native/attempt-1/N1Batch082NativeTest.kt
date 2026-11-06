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

private fun disposable082() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch082GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun associateRankLookalikesAndRadicalFallbacksAcrossFourProductionFamilies() {
        disposable082()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("中 事 備 先 典 冫 准 助 十 基 大 女 学 彼 手 批 授 教 木 氵 準 生 田 義", "聞 講 辶 進 隹 集 難", "准 準 集 進 難 冫 氵 辶 隹 准教授")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 082: associate rank / look-alikes / radical fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 31 scoped Han; focused 准/準/集/進/難, 冫/氵/辶/隹. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("中", "事", "備", "先", "典", "冫", "准", "助", "十", "基", "大", "女", "学", "彼", "手", "批", "授", "教", "木", "氵", "準", "生", "田", "義", "聞", "講", "辶", "進", "隹", "集", "難")) {
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
            for (word in listOf("准教授")) {
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
            File(context.getExternalFilesDir(null), "n1-082-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-082-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 124).put("wholeWordRasterProbes", 4).put("panels", 3)
            .put("limits", "31 actual scoped Han including exact 冫/氵/辶/隹 fallback inspection, four production families, three bounded Compose panels and four whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch082ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineAssociateRankReciprocalAndComparisonLinksCuratedOnDrawingAndSystemBack() {
        disposable082()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-082-${UUID.randomUUID()}", "main")
        val head = "4f5812bc7f33e7996214661e7dbf5f8e765df849"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-082-4f5812bc-envelope.zip")
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
        assertEquals(1094, updated.kanji)
        assertEquals(5050, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("0739a82c9699f031", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(114, n1.size)
        val associateRank = n1.single { it.kanji == "准" }
        assertEquals(listOf("ジュン"), associateRank.onyomi.splitSep())
        assertEquals(emptyList<String>(), associateRank.kunyomi.splitSep())
        assertNotNull(associateRank.quizOnyomi)
        assertNotNull(associateRank.quizKunyomi)
        assertEquals(listOf("ジュン"), associateRank.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), associateRank.quizKunyomi?.splitSep())
        assertEquals(listOf("じゅん"), associateRank.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), associateRank.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "准") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "准" && kind == ReadingKind.On && key == "じゅん") now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "准", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(associateRank.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(associateRank.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(associateRank.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(associateRank.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(associateRank.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(associateRank.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 准 meaning and sole curated on key じゅん due. Source and quiz kun lists empty. Two historical good 准 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 114 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("准")
            click("quasi-; associate rank")
            await("准 — quasi-; associate rank")
            show(articleBullet("Strokes: 10 · Key (radical): 冫 (no. 15) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("准 can mark a status corresponding to, but not fully the same as, a named rank. In 准教授 じゅんきょうじゅ, it helps name the established rank associate professor. Do not interpret it as a literal half-professor or a trainee awaiting automatic promotion."), "kanji-03")
            show(articleBullet("Another branch concerns approval: 批准 ひじゅん means ratification. Not every compound containing 准 is an associate rank."), "kanji-04")
            show(articleBullet("Modern-shape mnemonic, not etymology: picture the bird-shaped 隹 beside the two marks of 冫 as a bird standing beside a rank sign. This is an invented memory scene, not an explanation of the character's historical formation."), "kanji-05")
            section("Readings")
            show(readingExample("ジュン"), "kanji-10")
            show(readingExample("准教授 じゅんきょうじゅ — associate professor"), "kanji-12")
            show(articleBullet("This table covers the sole on-reading in the frozen KANJIDIC2 record; that record lists no kun-readings. Readings supplied by other dictionaries do not change this card's source metadata."), "kanji-13")
            section("Common words")
            show(articleBullet("准教授 じゅんきょうじゅ — associate professor"), "kanji-15")
            show(articleBullet("批准 ひじゅん — ratification"), "kanji-16")
            section("Notes")
            show(articleBullet("準 shares ジュン and has related meanings, but its shape has 氵 at the upper left and 十 below. 准 has two left-hand 冫 marks and no lower 十."), "kanji-18")
            show(articleBullet("The spellings are not freely interchangeable in modern words: learn 準備 じゅんび (preparation), 基準 きじゅん (standard), and 批准 ひじゅん (ratification) as written. JMdict also recognizes 準教授 じゅんきょうじゅ; the current Japanese university title taught here is 准教授."), "kanji-19")
            show(articleBullet("For look-alikes, 集 has 木 below 隹, 進 has 辶, and 難 has a different, dense left-hand block. Their meanings are not associate rank or approval."), "kanji-20")
            show(articleBullet("Metadata: KANJIDIC2, database 2026-306, 2026-11-02 (EDRDG; CC BY-SA 4.0). Words: JMdict, entries 2178020, 1483390, 1341670 and 1591210. Character senses: Digital Daijisen: 准. Rank usage: Nipponica and 大学事典: 准教授."), "kanji-21")
            section("Common words")
            show(articleBullet("准教授 じゅんきょうじゅ — associate professor"), "word-forward-13")
            inline(await(articleBullet("准教授 じゅんきょうじゅ — associate professor")), "准教授", 0)
            await("Article contents")
            await("准教授 (じゅんきょうじゅ) — associate professor")
            section("Meaning")
            show(articleBullet("准教授 names an associate professor. In the Japanese university system, this is an established academic rank below 教授 きょうじゅ (professor), with teaching and research responsibilities. It does not mean a professor's personal helper."), "word-02")
            show(articleBullet("彼女は大学の准教授です。 (かのじょはだいがくのじゅんきょうじゅです。) — She is an associate professor at a university."), "word-03")
            show(articleBullet("田中准教授の講義を聞きました。 (たなかじゅんきょうじゅのこうぎをききました。) — I listened to Associate Professor Tanaka's lecture."), "word-04")
            show(articleBullet("The second example places the rank after a name. For respectful direct address, 田中先生 (たなかせんせい) can be appropriate; 先生 is not itself a statement of this particular academic rank."), "word-05")
            section("How the kanji combine")
            show(articleBullet("准 modifies the rank head 教授, marking the associate rank. Within 教授, 教 contributes teaching and 授 contributes imparting knowledge. The on-readings are ジュン + キョウ + ジュ. Learn the whole institutional title rather than translating it as \"half a professor.\""), "word-07")
            section("Synonyms and antonyms")
            show(articleBullet("助教授 じょきょうじゅ is the former Japanese title replaced by 准教授 in April 2007. It remains relevant when reading older documents."), "word-09")
            show(articleBullet("助教 じょきょう, often translated \"assistant professor,\" is a separate rank, not an abbreviation of 准教授."), "word-10")
            show(articleBullet("助手 じょしゅ means assistant and has its own academic uses. It does not by itself identify someone as a 准教授."), "word-11")
            show(articleBullet("教授 きょうじゅ names the professor rank; 先生 せんせい is a broader designation or respectful form of address."), "word-12")
            show(articleBullet("These are role and title comparisons, not strict antonyms."), "word-13")
            section("Distinctive meaning")
            show(articleBullet("准教授 is a rank noun, not a verb meaning \"work as an associate professor.\" Use 准教授です (じゅんきょうじゅです) to state the role. The separate teaching/instruction sense of 教授する does not license 准教授する for having this job."), "word-15")
            show(articleBullet("The English label \"associate professor\" is useful, but rank systems and employment conditions differ between countries and institutions. Do not assume an exact international equivalence or an automatic future promotion. JMdict also lists the spelling 準教授 with the same reading; 准教授 is the current Japanese university title used here."), "word-16")
            show(articleBullet("Dictionary: JMdict, entry 2178020; comparisons 1237160, 1344540, 1344550, 1344650 and 1387990. Japanese rank and April 2007 reform: Nipponica and 大学事典: 准教授."), "word-17")
            section("How the kanji combine")
            show(articleBullet("准 modifies the rank head 教授, marking the associate rank. Within 教授, 教 contributes teaching and 授 contributes imparting knowledge. The on-readings are ジュン + キョウ + ジュ. Learn the whole institutional title rather than translating it as \"half a professor.\""), "word-reverse-27")
            inline(await(articleBullet("准 modifies the rank head 教授, marking the associate rank. Within 教授, 教 contributes teaching and 授 contributes imparting knowledge. The on-readings are ジュン + キョウ + ジュ. Learn the whole institutional title rather than translating it as \"half a professor.\"")), "准", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ジュン"), "kanji-backlink")
            back()
            await(articleBullet("准 modifies the rank head 教授, marking the associate rank. Within 教授, 教 contributes teaching and 授 contributes imparting knowledge. The on-readings are ジュン + キョウ + ジュ. Learn the whole institutional title rather than translating it as \"half a professor.\"")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("准 modifies the rank head 教授, marking the associate rank. Within 教授, 教 contributes teaching and 授 contributes imparting knowledge. The on-readings are ジュン + キョウ + ジュ. Learn the whole institutional title rather than translating it as \"half a professor.\""), "teach-forward-28")
            inline(await(articleBullet("准 modifies the rank head 教授, marking the associate rank. Within 教授, 教 contributes teaching and 授 contributes imparting knowledge. The on-readings are ジュン + キョウ + ジュ. Learn the whole institutional title rather than translating it as \"half a professor.\"")), "教", 68)
            await("Article contents")
            await("教 — teach, instruct")
            section("Common words")
            show(articleBullet("准教授 じゅんきょうじゅ — associate professor"), "teach-reverse-29")
            inline(await(articleBullet("准教授 じゅんきょうじゅ — associate professor")), "准教授", 0)
            await("Article contents")
            await("准教授 (じゅんきょうじゅ) — associate professor")
            back()
            await(articleBullet("准教授 じゅんきょうじゅ — associate professor")).assertIsDisplayed()
            section("Common words")
            capture("system-back-to-teach")
            back()
            await(articleBullet("准 modifies the rank head 教授, marking the associate rank. Within 教授, 教 contributes teaching and 授 contributes imparting knowledge. The on-readings are ジュン + キョウ + ジュ. Learn the whole institutional title rather than translating it as \"half a professor.\"")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-to-word-from-teach")
            section("Synonyms and antonyms")
            show(articleBullet("助教授 じょきょうじゅ is the former Japanese title replaced by 准教授 in April 2007. It remains relevant when reading older documents."), "former-forward-30")
            inline(await(articleBullet("助教授 じょきょうじゅ is the former Japanese title replaced by 准教授 in April 2007. It remains relevant when reading older documents.")), "助教授", 0)
            await("Article contents")
            await("助教授 (じょきょうじゅ) - associate professor (former Japanese title)")
            section("Meaning")
            show(articleBullet("助教授 names a former Japanese university or college rank below 教授, professor. The Japanese rank was renamed 准教授 (じゅんきょうじゅ), associate professor, in April 2007. Read 助教授 in its historical or institutional context."), "successor-reverse-31")
            inline(await(articleBullet("助教授 names a former Japanese university or college rank below 教授, professor. The Japanese rank was renamed 准教授 (じゅんきょうじゅ), associate professor, in April 2007. Read 助教授 in its historical or institutional context.")), "准教授", 106)
            await("Article contents")
            await("准教授 (じゅんきょうじゅ) — associate professor")
            back()
            await(articleBullet("助教授 names a former Japanese university or college rank below 教授, professor. The Japanese rank was renamed 准教授 (じゅんきょうじゅ), associate professor, in April 2007. Read 助教授 in its historical or institutional context.")).assertIsDisplayed()
            section("Meaning")
            capture("system-back-to-former-title")
            back()
            await(articleBullet("助教授 じょきょうじゅ is the former Japanese title replaced by 准教授 in April 2007. It remains relevant when reading older documents.")).assertIsDisplayed()
            section("Synonyms and antonyms")
            capture("system-back-to-current-title")
            back()
            await(articleBullet("准教授 じゅんきょうじゅ — associate professor")).assertIsDisplayed()
            section("Common words")
            capture("system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)
                .put("comparisonPairs", 1).put("comparisonLinkTransitions", 2)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("准", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("quasi-; associate rank")
            await("Correct!")
            assertEquals("准", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("准", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                assertEquals(ReadingKind.On, question.question.kind)
                val key = "じゅん"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "准" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "准" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("じゅん"), readingLogs.map { it.reading }.toSet())
            capture("curated-on-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("quasi-; associate rank").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "准") })
            assertEquals(listOf("ジュン"), card.onyomi.splitSep())
            assertEquals(emptyList<String>(), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ジュン"), card.quizOnyomi?.splitSep())
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
                    it.kanji == "准" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "准" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("soleCuratedOnPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-082-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-082-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-082-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
