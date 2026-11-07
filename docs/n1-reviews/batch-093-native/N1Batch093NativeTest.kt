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

private fun disposable093() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch093GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun punishmentLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable093()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("一 乃 亅 事 仕 件 偵 典 凸 凹 刀 刂", "刑 判 力 土 型 大 好 官 家 察 巡 彡", "形 探 撃 故 来 査 民 法 火 物 百 目", "省 科 罰 者 聞 裁 話 警 部 食", "刑 形 型 刀 刂 彡 土 事 亅 乃 凹 凸 刑事 刑罰 刑法")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 093: punishment / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 46 scoped Han; focused 刑/形/型/刀/刂/彡/事/亅/乃/凹/凸. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("一", "乃", "亅", "事", "仕", "件", "偵", "典", "凸", "凹", "刀", "刂", "刑", "判", "力", "土", "型", "大", "好", "官", "家", "察", "巡", "彡", "形", "探", "撃", "故", "来", "査", "民", "法", "火", "物", "百", "目", "省", "科", "罰", "者", "聞", "裁", "話", "警", "部", "食")) {
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
            for (word in listOf("刑事", "刑罰", "刑法")) {
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
        assertEquals(196, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-093-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-093-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 184).put("wholeWordRasterProbes", 12).put("panels", 5)
            .put("limits", "46 actual scoped Han; 亅/刂/彡 absent from all three bundled cmaps requires actual system fallback inspection, four production families, five bounded Compose panels and twelve whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch093ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflinePunishmentReusedN3TwoReciprocalPairsOneOnNoKunSixStrokesAndSystemBack() {
        disposable093()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-093-${UUID.randomUUID()}", "main")
        val head = "324b0bd95ba8c255d7f0bead0b3f7ba771fccacc"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-093-324b0bd9-envelope.zip")
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
        assertEquals(1116, updated.kanji)
        assertEquals(5070, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("bf4cc85592bb9727", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(125, n1.size)
        val punishment = n1.single { it.kanji == "刑" }
        assertEquals(listOf("乃", "凹", "凸"), punishment.distractors.splitSep())
        assertEquals(listOf("ケイ"), punishment.onyomi.splitSep())
        assertEquals(emptyList<String>(), punishment.kunyomi.splitSep())
        assertNotNull(punishment.quizOnyomi)
        assertNotNull(punishment.quizKunyomi)
        assertEquals(listOf("ケイ"), punishment.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), punishment.quizKunyomi?.splitSep())
        assertEquals(listOf("けい"), punishment.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), punishment.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "刑" to "criminal punishment", "凸" to "convex; protruding",
            "乃" to "thereupon; possessive no", "凹" to "concave; sunken",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "刑" }
            assertEquals(listOf("乃", "凹", "凸"), target.distractors)
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(671))
            assertEquals(4, options.size)
            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            assertEquals(3, cards.count { it.kanji in target.distractors })
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("availableCuratedCount", cards.count { it.kanji in target.distractors })
                .put("fallbackOptions", options.count { it.kanji !in expectedMeanings }))
        }
        val importedDetective = requireNotNull(runBlocking { app.db.content().word(source.id, "刑事") })
        assertEquals(listOf("警官", "警察", "巡査", "おまわりさん"), importedDetective.quizExclusions.splitSep())
        assertEquals("けいじ", importedDetective.reading)
        assertEquals(3, importedDetective.jlpt)
        assertEquals("police detective; criminal matters", importedDetective.title)
        val detective = requireNotNull(runBlocking { app.db.content().word(source.id, "探偵") })
        assertTrue("Existing inbound detective guard", "刑事" in detective.quizExclusions.splitSep())
        val policeGuards = JSONArray()
        for (id in importedDetective.quizExclusions.splitSep()) {
            val guard = requireNotNull(runBlocking { app.db.content().word(source.id, id) })
            assertNotEquals("Unusable direct guard", guard.word, importedDetective.word)
            policeGuards.put(JSONObject().put("word", guard.word).put("title", guard.title))
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
                        if (card.kanji == "刑") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "刑" && (kind == ReadingKind.On && key == "けい")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "刑", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("directWordGuardCount", importedDetective.quizExclusions.splitSep().size)
            .put("directPoliceLabelGuards", policeGuards).put("inboundTanteiGuardPreserved", true)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(punishment.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(punishment.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(punishment.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(punishment.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(punishment.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(punishment.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 刑 meaning and onけい due, no kun keys. Full raw ケイ/emptykun and explicit curation retained. Two historical good 刑 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 125 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("刑")
            click("criminal punishment")
            await("刑 — criminal punishment")
            show(articleBullet("Strokes: 6 · Key (radical): 刀 (no. 18), appearing as 刂 on the right · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("刑 concerns criminal punishment or a legal sentence. Here \"sentence\" means a penalty imposed for an offense, not a grammatical sentence. In 刑事 けいじ, it contributes the criminal-law association: the whole word can name a police detective or concern criminal matters."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Picture the squared-off left part as a rule board beside the blade radical 刂, a reminder of a legal penalty. This invented association does not establish the character's history or a phonetic component."), "kanji-04")
            section("Readings")
            show(readingExample("ケイ"), "kanji-09")
            show(readingExample("刑事 けいじ — police detective; criminal matters; 刑罰 けいばつ — criminal punishment; penalty"), "kanji-11")
            show(articleBullet("The frozen KANJIDIC2 metadata lists ケイ and no kun readings. Other dictionaries have broader reading coverage: Digital Daijisen also records ギョウ, as in the historical ministry name 刑部省 ぎょうぶしょう. That does not change the reading of 刑事 to ぎょうじ."), "kanji-12")
            section("Common words")
            show(articleBullet("刑事 けいじ — police detective; criminal matters"), "kanji-14")
            show(articleBullet("刑 けい — penalty; sentence"), "kanji-15")
            show(articleBullet("刑罰 けいばつ — criminal punishment; penalty"), "kanji-16")
            show(articleBullet("刑法 けいほう — criminal law; penal code"), "kanji-17")
            section("Notes")
            show(articleBullet("刀 is the dictionary radical; its visible right-side form here is 刂. Compare 形, with three slanting strokes 彡 on the right, and 型, with 土 underneath the 刑-shaped upper part."), "kanji-19")
            show(articleBullet("The main lesson here is punishment. Dictionaries also record older model/form-related senses of 刑; the shape comparisons above are not a claim that 刑, 型 and 形 have never overlapped in meaning."), "kanji-20")
            show(articleBullet("刑事 also has the slang whole-word reading でか. Learn it as a separate reading of the whole word, not as a kun reading of 刑 alone. The linked article's primary reading remains けいじ."), "kanji-21")
            show(articleBullet("In legal expressions, 刑事 does not mean \"criminal\" as a noun naming an offender. Use the surrounding noun and sentence role to distinguish criminal matters from the detective."), "kanji-22")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families: JMdict, entries 1249610, 1249660, 1249780, 1249790, 1008360 and 2256510. Character readings and wider senses: Digital Daijisen, 刑; compound senses: 刑事."), "kanji-23")
            section("Common words")
            show(articleBullet("刑事 けいじ — police detective; criminal matters"), "keiji-forward")
            inline(await(articleBullet("刑事 けいじ — police detective; criminal matters")), "刑事", 0)
            await("Article contents")
            await("刑事 (けいじ) - police detective; criminal matters")
            section("Meaning")
            show(articleBullet("刑事 has two related uses: a noun for a police detective, and \"criminal\" in legal expressions concerning criminal matters."), "keiji-02")
            show(articleBullet("刑事が目撃者に話を聞いています。 (けいじがもくげきしゃにはなしをきいています。) - A detective is talking to a witness."), "keiji-03")
            show(articleBullet("これは刑事事件です。 (これはけいじじけんです。) - This is a criminal case."), "keiji-04")
            show(articleBullet("In the first example, 刑事 is a person. In 刑事事件, it qualifies 事件 (じけん), \"case/incident\"; it does not mean \"a detective's incident.\" Another useful combination is 刑事裁判 (けいじさいばん), \"criminal trial.\""), "keiji-05")
            section("How the kanji combine")
            show(articleBullet("刑 contributes criminal punishment, and 事 contributes a matter or affair. The legal meaning is therefore a helpful guide to the compound. The on readings are ケイ + ジ."), "keiji-07")
            section("Synonyms and antonyms")
            show(articleBullet("警官 (けいかん) means a police officer, a broader role than detective. 探偵 (たんてい) can refer to a detective such as a private investigator. For legal matters, 民事 (みんじ), \"civil,\" contrasts with 刑事; it is not an opposite kind of police officer."), "keiji-09")
            section("Distinctive meaning")
            show(articleBullet("Use the surrounding noun and sentence role to separate the two senses. 刑事が来た (けいじがきた) means a detective came. 刑事事件 concerns criminal law. Neither use means \"criminal\" as a noun naming the person who committed an offense."), "keiji-11")
            show(articleBullet("Dictionary: JMdict, entry 1249660, senses 1-2."), "keiji-12")
            section("How the kanji combine")
            show(articleBullet("刑 contributes criminal punishment, and 事 contributes a matter or affair. The legal meaning is therefore a helpful guide to the compound. The on readings are ケイ + ジ."), "keiji-kei-reverse")
            inline(await(articleBullet("刑 contributes criminal punishment, and 事 contributes a matter or affair. The legal meaning is therefore a helpful guide to the compound. The on readings are ケイ + ジ.")), "刑", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ケイ"), "kei-kanji-backlink")
            back()
            await(articleBullet("刑 contributes criminal punishment, and 事 contributes a matter or affair. The legal meaning is therefore a helpful guide to the compound. The on readings are ケイ + ジ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("kei-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("刑 contributes criminal punishment, and 事 contributes a matter or affair. The legal meaning is therefore a helpful guide to the compound. The on readings are ケイ + ジ."), "keiji-ji-reverse")
            inline(await(articleBullet("刑 contributes criminal punishment, and 事 contributes a matter or affair. The legal meaning is therefore a helpful guide to the compound. The on readings are ケイ + ジ.")), "事", 39)
            await("Article contents")
            await("事 — matter, affair")
            show(articleBullet("Strokes: 8 · Key (radical): 亅 (no. 6) · JLPT: N4 (community list)"), "ji-01")
            section("Meaning and origin")
            show(articleBullet("事 means \"matter, affair, thing to be done\", and from there \"business\", \"incident\" and \"fact\". The early form is usually explained as a hand holding a tool or a pennant-like object, in the sense of \"to serve, to do a task\", but scholars disagree on the details, so treat the picture as uncertain. It is filed under 亅 (the hook stroke) only for dictionary purposes; the hook does not carry the meaning."), "ji-03")
            section("Readings")
            show(readingExample("ジ"), "ji-08")
            show(readingExample("食事 しょくじ, 大事 だいじ, 火事 かじ, 事故 じこ, 事件 じけん"), "ji-10")
            show(readingExample("ズ"), "ji-11")
            show(readingExample("rare, e.g. 好事家 こうずか (a dilettante, an enthusiast)"), "ji-13")
            show(readingExample("こと"), "ji-14")
            show(readingExample("事 こと (a matter), 大事なこと (an important matter), 仕事 しごと (voiced: ごと)"), "ji-16")
            section("Common words")
            show(articleBullet("食事 しょくじ — a meal"), "ji-18")
            show(articleBullet("仕事 しごと — work, job"), "ji-19")
            show(articleBullet("火事 かじ — fire (a blaze)"), "ji-20")
            show(articleBullet("百科事典 ひゃっかじてん — encyclopedia"), "ji-21")
            show(articleBullet("刑事 けいじ — police detective; criminal matters"), "ji-22")
            section("Notes")
            show(articleBullet("事 (こと) is an abstract matter or an act, while 物 (もの) is a concrete thing. 事 also serves as a formal noun (the こと-nominalizer) but is usually written in kana in that role; see the koto and wake article."), "ji-24")
            show(articleBullet("仕事 しごと is read with the kun reading (voiced ごと), while 食事 and 火事 use ジ."), "ji-25")
            show(articleBullet("Look-alikes: 事 has a vertical stroke with a hook running through the whole character, with 一 and a box-like part above it; compare 力 and 話, which are not related in shape."), "ji-26")
            section("Common words")
            show(articleBullet("刑事 けいじ — police detective; criminal matters"), "ji-keiji-forward")
            inline(await(articleBullet("刑事 けいじ — police detective; criminal matters")), "刑事", 0)
            await("Article contents")
            section("Meaning")
            capture("ji-keiji-backlink")
            back()
            await(articleBullet("刑事 けいじ — police detective; criminal matters")).assertIsDisplayed()
            section("Common words")
            capture("ji-system-back-to-kanji")
            back()
            await(articleBullet("刑 contributes criminal punishment, and 事 contributes a matter or affair. The legal meaning is therefore a helpful guide to the compound. The on readings are ケイ + ジ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("ji-system-back-to-word")
            back()
            await(articleBullet("刑事 けいじ — police detective; criminal matters")).assertIsDisplayed()
            section("Common words")
            capture("keiji-system-back-to-kei")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4).put("activatedBaselinePairs", 1)
                .put("completeArticleProjections", 3).put("changedReusedArticles", 2)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("刑", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "刑" to "criminal punishment",
                "凸" to "convex; protruding",
                "乃" to "thereupon; possessive no",
                "凹" to "concave; sunken",
            )
            assertEquals(4, meaning.options.size)
            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertTrue(meaning.options.any { it.kanji == "凹" })
            assertEquals(0, meaning.options.count { it.kanji !in expectedMeanings })
            assertEquals("criminal punishment", meaning.options.single { it.kanji == "刑" }.title)
            assertEquals(listOf("乃", "凹", "凸"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 3).put("actualN1FallbackOptions", 0)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("criminal punishment")
            await("Correct!")
            assertEquals("刑", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("刑", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("けい"))
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "刑" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("けい"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "刑" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("けい"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })
            capture("curated-one-on-no-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("criminal punishment").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "刑") })
            assertEquals(listOf("乃", "凹", "凸"), card.distractors.splitSep())
            assertEquals(listOf("ケイ"), card.onyomi.splitSep())
            assertEquals(emptyList<String>(), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ケイ"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(6, strokes.length())
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
            rule.onNode(hasContentDescription("6 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "刑" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "刑" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("onlyOnKeiNoKunPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-093-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-093-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-093-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
