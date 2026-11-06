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

private fun disposable076() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch076GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun concurrentRolesLookalikesAndPersonFallbackAcrossFourProductionFamilies() {
        disposable076()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("事 人 亻 仕 件 任 会 住 体 八 具 典 兼 務 勤 同 困 外 女 室 寝 専 就 屋", "彼 意 所 故 曲 条 無 理 相 社 答 責 部 長 難 題 首", "兼 典 具 曲 八 人 亻 兼任 兼ねる")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 076: concurrent roles / look-alikes / fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 41 scoped Han; focused 兼/典/具/曲/八 and 人/亻. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("事", "人", "亻", "仕", "件", "任", "会", "住", "体", "八", "具", "典", "兼", "務", "勤", "同", "困", "外", "女", "室", "寝", "専", "就", "屋", "彼", "意", "所", "故", "曲", "条", "無", "理", "相", "社", "答", "責", "部", "長", "難", "題", "首")) {
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
            for (word in listOf("兼任", "兼ねる")) {
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
        assertEquals(172, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-076-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-076-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 164).put("wholeWordRasterProbes", 8).put("panels", 3)
            .put("limits", "41 scoped authored Han including pre-existing 亻, four production families, three bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch076ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineConcurrentRolesThreeReciprocalPairsBothReadingsDrawingAndSystemBack() {
        disposable076()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-076-${UUID.randomUUID()}", "main")
        val head = "b89b333682fa5bfb4123ea8f4a74c2cc59935a7c"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-076-b89b3336-envelope.zip")
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
        assertEquals(1088, updated.kanji)
        assertEquals(5045, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("8bd0a375668bee11", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(108, n1.size)
        val concurrentRoles = n1.single { it.kanji == "兼" }
        assertEquals(listOf("ケン"), concurrentRoles.onyomi.splitSep())
        assertEquals(listOf("か.ねる", "-か.ねる"), concurrentRoles.kunyomi.splitSep())
        assertNotNull(concurrentRoles.quizOnyomi)
        assertNotNull(concurrentRoles.quizKunyomi)
        assertEquals(listOf("ケン"), concurrentRoles.quizOnyomi?.splitSep())
        assertEquals(listOf("か.ねる"), concurrentRoles.quizKunyomi?.splitSep())
        assertEquals(listOf("けん"), concurrentRoles.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("かねる"), concurrentRoles.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "兼") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "兼" && ((kind == ReadingKind.On && key == "けん") || (kind == ReadingKind.Kun && key == "かねる"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "兼", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(concurrentRoles.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(concurrentRoles.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(concurrentRoles.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(concurrentRoles.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(concurrentRoles.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(concurrentRoles.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 兼 meaning and curated on/kun due; valid suffix -か.ねる retained but not selected separately; one かねる key. Two historical good 兼 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 108 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("兼")
            click("combine; concurrent roles")
            await("兼 — combine; concurrent roles")
            show(articleBullet("Strokes: 10 · Key (radical): 八 (a variant in the two top strokes, no. 12) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("兼 brings two or more functions or posts together. 兼ねる かねる can describe a room serving two purposes or a person holding two posts. 兼任 けんにん specifically concerns holding concurrent posts. Concurrent roles need not involve performing two actions at exactly the same moment."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: picture two upright posts joined by several crossbars, sharing one frame. This recalls the modern shape, not the character's historical origin or a verified phonetic component. The indexing 八 appears as the paired strokes at the top, rather than as the spreading bottom strokes seen in 典."), "kanji-04")
            section("Readings")
            show(readingExample("ケン"), "kanji-09")
            show(readingExample("兼任 けんにん — holding concurrent posts"), "kanji-11")
            show(readingExample("か.ねる"), "kanji-12")
            show(readingExample("兼ねる かねる — combine functions; hold two or more posts"), "kanji-14")
            show(readingExample("-か.ねる"), "kanji-15")
            show(readingExample("～かねる, usually written in kana after a verb's masu stem: 同意しかねる (どういしかねる) — cannot agree; a difficulty/inability construction, not literal combining"), "kanji-17")
            show(articleBullet("The two kun entries share the pronunciation かねる but describe different constructions. Practise one reading key, not two independent readings. For the suffix, 同意する becomes 同意し + かねる; do not attach it to the dictionary form or the て-form. It is negative in meaning without ない. The separate ～かねない pattern means \"might,\" not simply \"can.\" The linked article explains both uses and their examples."), "kanji-18")
            section("Common words")
            show(articleBullet("兼ねる かねる — combine functions; serve in more than one capacity"), "kanji-20")
            show(articleBullet("兼任 けんにん — holding concurrent posts"), "kanji-21")
            section("Notes")
            show(articleBullet("Between role or function names, 兼 (けん) can mean \"also serving as\": 首相兼外相 (しゅしょうけんがいしょう) is a prime minister also serving as foreign minister. It is not a general replacement for と or English \"and.\""), "kanji-23")
            show(articleBullet("Dictionaries also record a separate \"beforehand\" branch, as in 兼題 (けんだい), a poetry topic announced before the meeting. Do not force the concurrent-role translation onto every compound."), "kanji-24")
            show(articleBullet("Compare 典 and 具, which have spreading feet below their upper boxes. 曲 has a divided enclosure, without 兼's long central vertical strokes and spreading lower strokes."), "kanji-25")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word pairs: JMdict, entries 1256490, 1256520, 1256660, 1256670, 1329310 and 1922120. Meaning branches: Digital Daijisen, 兼. Constructions: Digital Daijisen and Seisenban Nihon Kokugo Daijiten, 兼ねる."), "kanji-26")
            section("Common words")
            show(articleBullet("兼ねる かねる — combine functions; serve in more than one capacity"), "兼ねる-forward-16")
            inline(await(articleBullet("兼ねる かねる — combine functions; serve in more than one capacity")), "兼ねる", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("兼 concerns combining or serving in more than one capacity; ねる completes the native verb. The ordinary combined-role verb is written 兼ねる. The difficulty suffix is usually written in kana as ～かねる; its meaning is not obtained by translating the kanji literally."), "兼ねる-08")
            section("Synonyms and antonyms")
            show(articleBullet("兼任する (けんにんする) describes holding concurrent posts. 勤める (つとめる) means to work for or be employed, not specifically to combine positions. ～できない also expresses inability, but ～かねる is useful for difficulty or reluctance in formal responses; it is not a universal replacement in every inability sentence."), "兼ねる-10")
            section("How the kanji combine")
            show(articleBullet("兼 concerns combining or serving in more than one capacity; ねる completes the native verb. The ordinary combined-role verb is written 兼ねる. The difficulty suffix is usually written in kana as ～かねる; its meaning is not obtained by translating the kanji literally."), "兼ねる-reverse-19")
            inline(await(articleBullet("兼 concerns combining or serving in more than one capacity; ねる completes the native verb. The ordinary combined-role verb is written 兼ねる. The difficulty suffix is usually written in kana as ～かねる; its meaning is not obtained by translating the kanji literally.")), "兼", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ケン"), "兼ねる-kanji-backlink")
            back()
            await(articleBullet("兼 concerns combining or serving in more than one capacity; ねる completes the native verb. The ordinary combined-role verb is written 兼ねる. The difficulty suffix is usually written in kana as ～かねる; its meaning is not obtained by translating the kanji literally.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("兼ねる-system-back-to-word")
            back()
            await(articleBullet("兼ねる かねる — combine functions; serve in more than one capacity")).assertIsDisplayed()
            section("Common words")
            capture("兼ねる-system-back-to-kanji")
            section("Common words")
            show(articleBullet("兼任 けんにん — holding concurrent posts"), "兼任-forward-20")
            inline(await(articleBullet("兼任 けんにん — holding concurrent posts")), "兼任", 0)
            await("Article contents")
            await("兼任 (けんにん) — holding concurrent posts")
            section("Meaning")
            show(articleBullet("兼任 means one person holding two or more posts or duties concurrently. Use 兼任する as a verb, marking the post or posts with を: an additional post, or two posts joined with と."), "兼任-02")
            show(articleBullet("首相が外相を兼任しています。 (しゅしょうががいしょうをけんにんしています。) — The prime minister also serves as foreign minister."), "兼任-03")
            show(articleBullet("彼女は社長と会長を兼任しています。 (かのじょはしゃちょうとかいちょうをけんにんしています。) — She holds both the president's and the chairperson's positions."), "兼任-04")
            show(articleBullet("These are overlapping appointments, not necessarily two tasks performed at the same instant."), "兼任-05")
            section("How the kanji combine")
            show(articleBullet("兼 contributes combining or serving concurrently; 任 contributes a post or duty. The modifier 兼 describes how the posts are held. The on readings are ケン + ニン. This explains the compound's meaning, not the historical origin of either character."), "兼任-07")
            section("Synonyms and antonyms")
            show(articleBullet("兼ねる (かねる) also describes combining posts, but extends to combined functions, such as a room serving two purposes. 兼務 (けんむ) is a close synonym for carrying out concurrent duties. 専任 (せんにん), dedicated service in a particular post or duty, is the contrast."), "兼任-09")
            show(articleBullet("就任 (しゅうにん) means taking office. It marks entry into a post, not the continued holding of two posts. Compare the particles: 社長に就任する (しゃちょうにしゅうにんする), \"take office as president,\" but 外相を兼任する (がいしょうをけんにんする), \"also serve as foreign minister.\""), "兼任-10")
            section("Distinctive meaning")
            show(articleBullet("The point is that one person has multiple roles. Two colleagues sharing one job do not establish 兼任 merely by sharing it. Nor does ordinary employment by itself imply concurrent posts: 勤める (つとめる) can simply mean working for an employer."), "兼任-12")
            show(articleBullet("Dictionary: JMdict, entry 1256670; comparisons 1256520, 1256710, 1331780 and 1389840. Usage: Digital Daijisen, 兼任."), "兼任-13")
            section("How the kanji combine")
            show(articleBullet("兼 contributes combining or serving concurrently; 任 contributes a post or duty. The modifier 兼 describes how the posts are held. The on readings are ケン + ニン. This explains the compound's meaning, not the historical origin of either character."), "兼任-reverse-30")
            inline(await(articleBullet("兼 contributes combining or serving concurrently; 任 contributes a post or duty. The modifier 兼 describes how the posts are held. The on readings are ケン + ニン. This explains the compound's meaning, not the historical origin of either character.")), "兼", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ケン"), "兼任-kanji-backlink")
            back()
            await(articleBullet("兼 contributes combining or serving concurrently; 任 contributes a post or duty. The modifier 兼 describes how the posts are held. The on readings are ケン + ニン. This explains the compound's meaning, not the historical origin of either character.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("兼任-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("兼 contributes combining or serving concurrently; 任 contributes a post or duty. The modifier 兼 describes how the posts are held. The on readings are ケン + ニン. This explains the compound's meaning, not the historical origin of either character."), "兼任-任-31")
            inline(await(articleBullet("兼 contributes combining or serving concurrently; 任 contributes a post or duty. The modifier 兼 describes how the posts are held. The on readings are ケン + ニン. This explains the compound's meaning, not the historical origin of either character.")), "任", 49)
            await("Article contents")
            show(articleBullet("Strokes: 6 · Key (radical): 人 (as 亻, no. 9) · JLPT: N3 (community list)"), "任-fallback-01")
            section("Common words")
            show(articleBullet("兼任 けんにん — holding concurrent posts"), "任-counterpart-33")
            inline(await(articleBullet("兼任 けんにん — holding concurrent posts")), "兼任", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("兼 contributes combining or serving concurrently; 任 contributes a post or duty. The modifier 兼 describes how the posts are held. The on readings are ケン + ニン. This explains the compound's meaning, not the historical origin of either character."), "兼任-任-component-backlink")
            back()
            await(articleBullet("兼任 けんにん — holding concurrent posts")).assertIsDisplayed()
            section("Common words")
            capture("兼任-任-system-back-to-component")
            back()
            await(articleBullet("兼 contributes combining or serving concurrently; 任 contributes a post or duty. The modifier 兼 describes how the posts are held. The on readings are ケン + ニン. This explains the compound's meaning, not the historical origin of either character.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("兼任-任-system-back-from-component")
            back()
            await(articleBullet("兼任 けんにん — holding concurrent posts")).assertIsDisplayed()
            section("Common words")
            capture("兼任-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 3).put("directedLinkTransitions", 6)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("兼", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("combine; concurrent roles")
            await("Correct!")
            assertEquals("兼", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("兼", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "けん" else "かねる"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "兼" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "兼" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("けん", "かねる"), readingLogs.map { it.reading }.toSet())
            capture("curated-both-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("combine; concurrent roles").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "兼") })
            assertEquals(listOf("ケン"), card.onyomi.splitSep())
            assertEquals(listOf("か.ねる", "-か.ねる"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ケン"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("か.ねる"), card.quizKunyomi?.splitSep())
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
                    it.kanji == "兼" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "兼" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKindsPersistedGoodNoDuplicateSuffixAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-076-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-076-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-076-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
