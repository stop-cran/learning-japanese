package io.github.stopcran.kanji.core

import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.quiz.QuizBuilder
import io.github.stopcran.kanji.core.quiz.QuizCard
import io.github.stopcran.kanji.core.quiz.QuizOption
import io.github.stopcran.kanji.core.reading.KanjiReadingQuiz
import io.github.stopcran.kanji.core.reading.ReadingCard
import io.github.stopcran.kanji.core.reading.ReadingKey
import io.github.stopcran.kanji.core.reading.ReadingKind
import io.github.stopcran.kanji.core.words.WordCard
import io.github.stopcran.kanji.core.words.WordDirection
import io.github.stopcran.kanji.core.words.WordQuizBuilder
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import kotlin.random.Random

class Batch103MeaningAcceptance789 {
    @Test
    fun actualPublishedFixtureChoicesGuardsAndSharedStemProjection() {
        val root = File("../../learning-japanese").canonicalFile
        assertEquals(File("C:\\Users\\stop-\\n1-kanji-workspace\\learning-japanese").canonicalFile, root)
        val parsed = ContentParser.parse(PublishableContentFixture.load(root))
        assertTrue(parsed.problems.toString(), parsed.problems.isEmpty())
        assertEquals("38c32a8df5fd6063", parsed.manifest.contentVersion)
        assertEquals(1126, parsed.kanji.size)
        assertEquals(5077, parsed.words.size)
        val all = parsed.kanji.map { QuizCard(it.kanji, it.title, it.tags, it.distractors, it.quizExclusions) }
        val byId = all.associateBy { it.kanji }
        val n1Ids = parsed.kanji.filter { it.jlpt == 1 }.map { it.kanji }.toSet()
        assertEquals(135, n1Ids.size)
        val n1 = all.filter { it.kanji in n1Ids }
        val target = byId.getValue("励")
        val guards = listOf("努", "勉", "勤", "支")
        val curated = listOf("劣", "万", "厚")
        assertEquals(guards, target.quizExclusions)
        assertEquals(curated, target.distractors)
        assertEquals(listOf("劣"), curated.filter { it in n1Ids })
        fun assertPairwiseSafe(options: List<QuizOption>) {
            val cards = options.map { byId.getValue(it.kanji) }
            for (left in cards) for (right in cards.filter { it.kanji != left.kanji }) {
                assertFalse("${left.kanji}/${right.kanji} guarded pair leaked",
                    right.kanji in left.quizExclusions || left.kanji in right.quizExclusions)
            }
        }
        fun optionsJson(options: List<QuizOption>) = JsonArray(options.map { option -> buildJsonObject {
            put("kanji", option.kanji)
            put("title", option.title)
        } })
        val pools = linkedMapOf(
            "N1" to n1, "All" to all,
            "boundedCustom" to all.filter { it.kanji in curated + target.kanji },
            "randomN1Subset789" to listOf(target) + n1.filter { it.kanji != target.kanji }
                .shuffled(Random(789)).take(15),
        )
        val rows = mutableListOf<JsonObject>()
        for ((poolName, pool) in pools) repeat(16) { seed ->
            val options = QuizBuilder.options(target, pool, Random(seed))
            assertEquals(4, options.size)
            assertEquals(4, options.map { it.title }.toSet().size)
            assertEquals(1, options.count { it.kanji == target.kanji })
            assertTrue(options.none { it.kanji in guards })
            assertTrue(curated.filter { id -> pool.any { it.kanji == id } }
                .all { id -> options.any { it.kanji == id } })
            assertTrue(options.all { o -> pool.any { it.kanji == o.kanji && it.title == o.title } })
            assertPairwiseSafe(options)
            if (poolName == "All" || poolName == "boundedCustom") {
                assertEquals((curated + target.kanji).toSet(), options.map { it.kanji }.toSet())
            }
            rows += buildJsonObject {
                put("pool", poolName)
                put("seed", seed)
                put("options", optionsJson(options))
            }
        }
        val guardRows = mutableListOf<JsonObject>()
        for (excludedId in guards) {
            val pair = all.filter { it.kanji in setOf(target.kanji, excludedId) }
            assertEquals(2, pair.size)
            for (quizTarget in pair) repeat(16) { seed ->
                val excluded = pair.single { it.kanji != quizTarget.kanji }
                val sampled = pair + all.filter { it.kanji !in pair.map { p -> p.kanji } }
                    .shuffled(Random(789 + seed)).take(seed)
                val checkedPools = pools + linkedMapOf(
                    "sampledFiltered" to sampled, "pairOnly" to pair,
                    "targetOutsidePool" to sampled.filter { it.kanji != quizTarget.kanji })
                for ((poolName, pool) in checkedPools) {
                    val options = QuizBuilder.options(quizTarget, pool, Random(seed))
                    assertEquals(1, options.count { it.kanji == quizTarget.kanji })
                    assertFalse("$excludedId leaked in $poolName", options.any { it.kanji == excluded.kanji })
                    assertTrue(options.size in 1..4)
                    assertEquals(options.size, options.map { it.title }.toSet().size)
                    assertTrue(options.all { it.kanji == quizTarget.kanji || pool.any { p -> p.kanji == it.kanji } })
                    assertPairwiseSafe(options)
                    if (poolName == "pairOnly") assertEquals(1, options.size)
                    guardRows += buildJsonObject {
                        put("target", quizTarget.kanji)
                        put("excluded", excluded.kanji)
                        put("pool", poolName)
                        put("seed", seed)
                        put("poolMembershipInOrder", JsonArray(pool.map { JsonPrimitive(it.kanji) }))
                        put("options", optionsJson(options))
                    }
                }
            }
        }
        val nontransitiveRows = mutableListOf<JsonObject>()
        val preexistingDirect = mutableSetOf<String>()
        for (left in guards) for (right in guards.filter { it != left }) {
            val pair = all.filter { it.kanji in setOf(left, right) }
            val leftCard = byId.getValue(left)
            val rightCard = byId.getValue(right)
            if (right in leftCard.quizExclusions || left in rightCard.quizExclusions) {
                preexistingDirect += "$left/$right"
                continue
            }
            repeat(16) { seed ->
                val options = QuizBuilder.options(leftCard, pair, Random(seed))
                assertEquals(setOf(left, right), options.map { it.kanji }.toSet())
                nontransitiveRows += buildJsonObject {
                    put("target", left)
                    put("neighbor", right)
                    put("seed", seed)
                    put("options", optionsJson(options))
                }
            }
        }
        val readings = parsed.kanji.map {
            ReadingCard(it.kanji, it.onyomi, it.kunyomi,
                it.quizOnyomi ?: it.onyomi, it.quizKunyomi ?: it.kunyomi, it.distractors)
        }
        val reading = readings.single { it.kanji == "励" }
        assertEquals(listOf("レイ"), reading.on)
        assertEquals(listOf("はげ.む", "はげ.ます"), reading.kun)
        assertEquals(reading.on, reading.askOn)
        assertEquals(reading.kun, reading.askKun)
        assertEquals(listOf("れい"), reading.quizKeys(ReadingKind.On))
        assertEquals(listOf("はげむ"), reading.quizKeys(ReadingKind.Kun))
        assertEquals(ReadingKey.stem("はげ.む"), ReadingKey.stem("はげ.ます"))
        assertTrue("はげます" in KanjiReadingQuiz.excludedKeys(reading))
        val readingRows = mutableListOf<JsonObject>()
        for (kind in ReadingKind.entries) for (key in reading.quizKeys(kind)) repeat(16) { seed ->
            val question = KanjiReadingQuiz.question(reading, kind, readings, Random(seed), reading = key)
            assertNotNull(question)
            question!!
            assertEquals(key, question.correctKey)
            assertEquals(1, question.options.count { it.key == key })
            assertFalse(question.options.any { it.key == "はげます" })
            val wrong = question.options.filter { it.key != key }
            assertTrue(wrong.none { it.key in KanjiReadingQuiz.excludedKeys(reading) })
            readingRows += buildJsonObject {
                put("kind", kind.name)
                put("key", key)
                put("seed", seed)
                put("options", JsonArray(question.options.map { buildJsonObject {
                    put("key", it.key)
                    put("label", it.label)
                } }))
            }
        }
        val words = parsed.words.map {
            WordCard(it.word, it.reading, it.title, it.type, it.kanji, it.tags, it.jlpt,
                it.quizExclusions, it.quizDistractors)
        }.associateBy { it.word }
        val wordGuards = linkedMapOf(
            "激励" to listOf("励ます", "応援", "勧める", "慰める", "支える", "力強い"),
            "励む" to listOf("努める", "努力", "一生懸命", "苦心", "せっせと", "凝らす", "注ぐ", "ねっしん",
                "くるくる", "ばりばり", "もりもり", "勉強", "凝る", "夢中", "熱中", "張り切る"),
            "励ます" to listOf("応援", "勧める", "慰める", "支える", "力強い"),
        )
        assertEquals(27, wordGuards.values.sumOf { it.size })
        val wordRows = mutableListOf<JsonObject>()
        for ((id, excludedIds) in wordGuards) {
            assertEquals(excludedIds, words.getValue(id).quizExclusions)
            assertEquals(null, words.getValue(id).jlpt)
            for (excluded in excludedIds) {
                val pair = listOf(words.getValue(id), words.getValue(excluded))
                for (wordTarget in pair) for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
                    repeat(16) { seed ->
                        val options = WordQuizBuilder.options(wordTarget, pair, direction, Random(seed))
                        assertEquals(listOf(wordTarget.word), options.map { it.word })
                        wordRows += buildJsonObject {
                            put("declaredOn", id)
                            put("excluded", excluded)
                            put("target", wordTarget.word)
                            put("direction", direction.name)
                            put("seed", seed)
                            put("label", options.single().label)
                        }
                    }
                }
            }
        }
        val wordNontransitiveRows = mutableListOf<JsonObject>()
        for (id in listOf("激励", "励ます")) {
            val pair = listOf(words.getValue(id), words.getValue("励む"))
            for (wordTarget in pair) for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
                repeat(16) { seed ->
                    val options = WordQuizBuilder.options(wordTarget, pair, direction, Random(seed))
                    assertEquals(pair.map { it.word }.toSet(), options.map { it.word }.toSet())
                    wordNontransitiveRows += buildJsonObject {
                        put("pair", JsonArray(pair.map { JsonPrimitive(it.word) }))
                        put("target", wordTarget.word)
                        put("direction", direction.name)
                        put("seed", seed)
                    }
                }
            }
        }
        assertEquals(64, rows.size)
        assertEquals(896, guardRows.size)
        assertEquals((12 - preexistingDirect.size) * 16, nontransitiveRows.size)
        assertTrue(nontransitiveRows.isNotEmpty())
        assertEquals(32, readingRows.size)
        assertEquals(1728, wordRows.size)
        assertEquals(128, wordNontransitiveRows.size)
        val destination = File("C:\\Users\\stop-\\n1-kanji-workspace\\control\\logs\\f2b2b1cc-63be-4d81-8a9c-bdb4219c099e")
        for ((name, value) in linkedMapOf(
            "pools" to buildJsonObject { pools.forEach { (name, pool) ->
                put(name, JsonArray(pool.map { JsonPrimitive(it.kanji) }))
            } },
            "choices" to JsonArray(rows), "direct-guards" to JsonArray(guardRows),
            "nontransitive" to JsonArray(nontransitiveRows),
            "preexisting-neighbor-edges" to JsonArray(preexistingDirect.sorted().map { JsonPrimitive(it) }),
            "readings" to JsonArray(readingRows), "word-guards" to JsonArray(wordRows),
            "word-nontransitive" to JsonArray(wordNontransitiveRows))) {
            val file = File(destination, "meaning-789-$name.json")
            check(!file.exists()) { "Do not overwrite acceptance evidence: $file" }
            file.writeText(value.toString() + "\n")
        }
    }
}
