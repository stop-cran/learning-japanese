package io.github.stopcran.kanji.core

import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.quiz.QuizBuilder
import io.github.stopcran.kanji.core.quiz.QuizCard
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import kotlin.random.Random

class Batch101MeaningAcceptance766 {
    @Test
    fun actualPublishedFixtureChoicesDirectSymmetricAndNontransitiveGuards() {
        val root = File("../../learning-japanese").canonicalFile
        assertEquals(File("C:\\Users\\stop-\\n1-kanji-workspace\\learning-japanese").canonicalFile, root)
        val parsed = ContentParser.parse(PublishableContentFixture.load(root))
        assertTrue(parsed.problems.toString(), parsed.problems.isEmpty())
        assertEquals("6e9b74967e21fc3c", parsed.manifest.contentVersion)
        assertEquals(1124, parsed.kanji.size)
        assertEquals(5073, parsed.words.size)
        val all = parsed.kanji.map { QuizCard(it.kanji, it.title, it.tags, it.distractors, it.quizExclusions) }
        val n1Ids = parsed.kanji.filter { it.jlpt == 1 }.map { it.kanji }.toSet()
        assertEquals(133, n1Ids.size)
        val n1 = all.filter { it.kanji in n1Ids }
        val target = all.single { it.kanji == "功" }
        val guards = listOf("績", "効", "果", "成", "達", "勝", "凱", "栄", "敬", "働", "業", "技", "工")
        val curated = listOf("加", "幼", "刀")
        assertEquals(guards, target.quizExclusions)
        assertEquals(curated, target.distractors)
        assertEquals(listOf("刀"), curated.filter { it in n1Ids })
        val custom = all.filter { it.kanji in curated + target.kanji }
        val randomSubset = listOf(target) + n1.filter { it.kanji != target.kanji }
            .shuffled(Random(766)).take(15)
        val rows = mutableListOf<kotlinx.serialization.json.JsonObject>()
        val pools = linkedMapOf("N1" to n1, "All" to all, "boundedCustom" to custom,
            "randomN1Subset766" to randomSubset)
        for ((poolName, pool) in pools) repeat(16) { seed ->
            val options = QuizBuilder.options(target, pool, Random(seed))
            assertEquals(4, options.size)
            assertEquals(4, options.map { it.title }.toSet().size)
            assertEquals(1, options.count { it.kanji == target.kanji })
            assertTrue(options.none { it.kanji in guards })
            assertTrue(curated.filter { id -> pool.any { it.kanji == id } }
                .all { id -> options.any { it.kanji == id } })
            assertTrue(options.all { o -> pool.any { it.kanji == o.kanji && it.title == o.title } })
            if (poolName == "All" || poolName == "boundedCustom") {
                assertEquals((curated + target.kanji).toSet(), options.map { it.kanji }.toSet())
            }
            rows += buildJsonObject {
                put("pool", poolName)
                put("seed", seed)
                put("poolMembershipInOrder", JsonArray(pool.map { JsonPrimitive(it.kanji) }))
                put("options", JsonArray(options.map { option -> buildJsonObject {
                    put("kanji", option.kanji)
                    put("title", option.title)
                } }))
            }
        }
        val guardRows = mutableListOf<kotlinx.serialization.json.JsonObject>()
        for (excludedId in guards) {
            val pair = all.filter { it.kanji in setOf(target.kanji, excludedId) }
            assertEquals(2, pair.size)
            for (quizTarget in pair) repeat(16) { seed ->
                val excluded = pair.single { it.kanji != quizTarget.kanji }
                val sampled = pair + all.filter { it.kanji !in pair.map { p -> p.kanji } }
                    .shuffled(Random(766 + seed)).take(seed)
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
                    if (poolName == "pairOnly") assertEquals(1, options.size)
                    guardRows += buildJsonObject {
                        put("target", quizTarget.kanji)
                        put("excluded", excluded.kanji)
                        put("pool", poolName)
                        put("seed", seed)
                        put("poolMembershipInOrder", JsonArray(pool.map { JsonPrimitive(it.kanji) }))
                        put("options", JsonArray(options.map { JsonPrimitive(it.kanji) }))
                    }
                }
            }
        }
        val nontransitiveRows = mutableListOf<kotlinx.serialization.json.JsonObject>()
        val preexistingDirect = mutableSetOf<String>()
        for (left in guards) for (right in guards.filter { it != left }) {
            val pair = all.filter { it.kanji in setOf(left, right) }
            val leftCard = pair.single { it.kanji == left }
            val rightCard = pair.single { it.kanji == right }
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
                    put("options", JsonArray(options.map { JsonPrimitive(it.kanji) }))
                }
            }
        }
        assertEquals(64, rows.size)
        assertEquals(2912, guardRows.size)
        assertEquals((156 - preexistingDirect.size) * 16, nontransitiveRows.size)
        assertTrue(nontransitiveRows.isNotEmpty())
        val destination = File("C:\\Users\\stop-\\n1-kanji-workspace\\control\\logs\\38ec935d-0cc5-45ad-9482-052c00fc10aa")
        for ((name, value) in linkedMapOf(
            "choices" to JsonArray(rows), "direct-guards" to JsonArray(guardRows),
            "nontransitive" to JsonArray(nontransitiveRows),
            "preexisting-neighbor-edges" to JsonArray(preexistingDirect.sorted().map { JsonPrimitive(it) }))) {
            val file = File(destination, "meaning-766-$name.json")
            check(!file.exists()) { "Do not overwrite acceptance evidence: $file" }
            file.writeText(value.toString() + "\n")
        }
    }
}
