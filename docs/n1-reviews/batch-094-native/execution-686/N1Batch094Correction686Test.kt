package io.github.stopcran.kanji.ui

import android.os.Build
import androidx.test.platform.app.InstrumentationRegistry
import io.github.stopcran.kanji.KanjiApp
import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.content.RepoSource
import io.github.stopcran.kanji.core.words.WordDirection
import io.github.stopcran.kanji.core.words.WordQuizBuilder
import io.github.stopcran.kanji.data.*
import kotlinx.coroutines.runBlocking
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test
import java.io.ByteArrayInputStream
import java.io.File
import java.util.UUID

class N1Batch094Correction686Test {
    @Test fun correctedArchiveSingleImportAndDirectGuardBothOrientationsDirectionsAndPools() {
        assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
        assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-094-correction-686-${UUID.randomUUID()}", "main")
        val head = "5f0be6677c770b2841073c0864229e49ce1e96bd"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-094-5f0be667-corrected-envelope.zip")
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
        assertEquals("74b7e886a1afbd46", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val kanji = runBlocking { app.db.content().kanjiLite(source.id) }
        assertEquals(1117, kanji.size)
        assertEquals(126, kanji.count { it.jlpt == 1 })
        val words = runBlocking { app.db.content().wordsLite(source.id) }.map { it.toCard() }
        assertEquals(5070, words.size)
        val left = words.single { it.word == "削る" }
        val right = words.single { it.word == "縮める" }
        assertEquals(listOf("切る", "減らす", "省く", "消す", "除く", "外す", "縮める"), left.quizExclusions)
        assertEquals("けずる", left.reading)
        assertEquals("ちぢめる", right.reading)
        assertEquals(2, left.jlpt)
        assertEquals(2, right.jlpt)
        val checks = JSONArray()
        for ((target, excluded) in listOf(left to right, right to left)) {
            val custom = listOf(target, excluded) + words.filter {
                it.word !in setOf(target.word, excluded.word) && it.title !in setOf(target.title, excluded.title) &&
                    it.word !in target.quizExclusions && target.word !in it.quizExclusions
            }.take(12)
            assertEquals(14, custom.size)
            for ((poolName, pool) in listOf("All" to words, "boundedCustom" to custom)) {
                assertTrue(pool.any { it.word == target.word } && pool.any { it.word == excluded.word })
                for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
                    repeat(16) { seed ->
                        val options = WordQuizBuilder.options(target, pool, direction, kotlin.random.Random(seed))
                        assertEquals(4, options.size)
                        assertEquals(4, options.map { it.label }.toSet().size)
                        assertEquals(1, options.count { it.word == target.word })
                        assertTrue(options.all { option -> pool.any { it.word == option.word } })
                        assertFalse("Direct exclusion leaked", options.any { it.word == excluded.word })
                        checks.put(JSONObject().put("target", target.word).put("excluded", excluded.word)
                            .put("pool", poolName).put("poolSize", pool.size).put("direction", direction.name)
                            .put("seed", seed).put("options", JSONArray().also { rows ->
                                options.forEach { rows.put(JSONObject().put("word", it.word).put("label", it.label)) }
                            }))
                    }
                }
            }
        }
        assertEquals(128, checks.length())
        assertEquals(1, archiveRequests)
        File(instrumentation.targetContext.getExternalFilesDir(null), "n1-094-correction-686.json")
            .writeText(JSONObject().put("passed", true).put("contentSnapshot", head)
                .put("contentVersion", meta.contentVersion).put("archiveRequests", archiveRequests)
                .put("importedKanji", updated.kanji).put("importedWords", updated.words)
                .put("n1Cards", kanji.count { it.jlpt == 1 }).put("problems", meta.problems)
                .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
                .put("directGuardBuilderChecks", checks).put("fingerprint", Build.FINGERPRINT)
                .put("limits", "Focused production builder enforcement only; not exhaustive semantic, visual, physical-phone, human-handwriting, MLKit or publication acceptance.")
                .toString(2))
    }
}
