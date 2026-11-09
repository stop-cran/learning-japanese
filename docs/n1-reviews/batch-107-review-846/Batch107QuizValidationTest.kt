package io.github.stopcran.kanji.core

import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.content.KanjiCard
import io.github.stopcran.kanji.core.quiz.QuizBuilder
import io.github.stopcran.kanji.core.quiz.QuizCard
import io.github.stopcran.kanji.core.reading.KanjiReadingQuiz
import io.github.stopcran.kanji.core.reading.ReadingCard
import io.github.stopcran.kanji.core.reading.ReadingKind
import io.github.stopcran.kanji.core.srs.Stacks
import io.github.stopcran.kanji.core.words.WordCard
import io.github.stopcran.kanji.core.words.WordDirection
import io.github.stopcran.kanji.core.words.WordOption
import io.github.stopcran.kanji.core.words.WordQuizBuilder
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import kotlin.random.Random

class Batch107QuizValidationTest {
    private fun excluded(a: WordCard, b: WordCard) =
        b.word in a.quizExclusions || a.word in b.quizExclusions

    private fun reading(card: KanjiCard) = ReadingCard(
        card.kanji, card.onyomi, card.kunyomi,
        card.quizOnyomi ?: card.onyomi, card.quizKunyomi ?: card.kunyomi, card.distractors,
    )

    private fun checkWords(
        options: List<WordOption>, target: WordCard, blocked: WordCard,
        cards: Map<String, WordCard>, expectedSize: Int,
    ) {
        assertEquals(expectedSize, options.size)
        assertEquals(1, options.count { it.word == target.word })
        assertFalse(options.any { it.word == blocked.word })
        assertEquals(options.size, options.map { it.word }.toSet().size)
        assertEquals(options.size, options.map { it.label }.toSet().size)
        val selected = options.map { cards.getValue(it.word) }
        selected.forEachIndexed { index, card ->
            selected.take(index).forEach { assertFalse(excluded(card, it)) }
        }
    }

    @Test
    fun importedContentUsesTheActualMeaningAndReadingBuilders() {
        val root = File("../../learning-japanese")
        assertTrue("The actual sibling content checkout is required", File(root, "manifest.json").isFile)
        val parsed = ContentParser.parse(PublishableContentFixture.load(root))
        assertEquals(emptyList<String>(), parsed.problems)

        val words = parsed.words.map {
            WordCard(it.word, it.reading, it.title, it.type, it.kanji, it.tags,
                it.jlpt, it.quizExclusions, it.quizDistractors, it.quizImage)
        }
        val byWord = words.associateBy { it.word }
        assertEquals(words.size, byWord.size)
        val newPairs = listOf("勘" to "感覚", "勘定" to "支払う", "勘定" to "給与")
        val preservedPairs = listOf(
            "勘定" to "計算", "勘定" to "会計", "勘定" to "支払",
            "給与" to "支払", "給与" to "支払う",
            "勘違い" to "誤解", "勘違い" to "間違い", "勘違い" to "誤り",
            "勘違い" to "ミス", "勘違い" to "失敗",
        )
        assertEquals(listOf("感覚"), byWord.getValue("勘").quizExclusions)
        assertEquals(listOf("計算", "支払う", "給与"), byWord.getValue("勘定").quizExclusions)
        assertEquals("intuition; hunch", byWord.getValue("勘").title)
        assertEquals("sense; sensation", byWord.getValue("感覚").title)
        assertEquals("reckoning; bill", byWord.getValue("勘定").title)
        assertEquals("pay", byWord.getValue("支払う").title)

        val directions = listOf(WordDirection.JpToEn, WordDirection.EnToJp)
        for ((first, second) in newPairs + preservedPairs) {
            val a = byWord.getValue(first)
            val b = byWord.getValue(second)
            assertTrue("$first / $second must be a direct pair", excluded(a, b))
            for (direction in directions) {
                for ((target, blocked) in listOf(a to b, b to a)) {
                    repeat(10) { seed ->
                        checkWords(WordQuizBuilder.options(target, listOf(a, b), direction, Random(seed)),
                            target, blocked, byWord, 1)
                    }
                }
            }
        }

        for ((first, second) in newPairs) {
            val a = byWord.getValue(first)
            val b = byWord.getValue(second)
            val filler = mutableListOf<WordCard>()
            for (candidate in words.sortedBy { it.word }) {
                if (candidate.word in setOf(first, second) || candidate.title in setOf(a.title, b.title) ||
                    excluded(candidate, a) || excluded(candidate, b) ||
                    filler.any { it.title == candidate.title || excluded(it, candidate) }) continue
                filler += candidate
                if (filler.size == 5) break
            }
            assertEquals(5, filler.size)
            val custom = listOf(a, b) + filler
            val unguardedA = a.copy(quizExclusions = a.quizExclusions - b.word)
            val unguardedB = b.copy(quizExclusions = b.quizExclusions - a.word)
            for (direction in directions) {
                for ((target, blocked) in listOf(a to b, b to a)) {
                    for ((name, pool) in listOf("all" to words, "custom" to custom)) {
                        repeat(10) { seed ->
                            val options = WordQuizBuilder.options(target, pool, direction, Random(seed))
                            checkWords(options, target, blocked, byWord, 4)
                            if (seed == 0) println("WORD $name $direction ${target.word}: $options")
                        }
                    }
                }
                val oldPool = listOf(unguardedA, unguardedB)
                for (target in oldPool) {
                    assertEquals(setOf(first, second),
                        WordQuizBuilder.options(target, oldPool, direction, Random(0)).map { it.word }.toSet())
                }
                val neutral = filler.first()
                repeat(20) { seed ->
                    val options = WordQuizBuilder.options(neutral, listOf(neutral, a, b), direction, Random(seed))
                    assertEquals(2, options.size)
                    assertEquals(1, options.count { it.word == first || it.word == second })
                }
            }
        }
        val originalWords = words.map {
            when (it.word) {
                "勘" -> it.copy(quizExclusions = emptyList())
                "勘定" -> it.copy(quizExclusions = listOf("計算"))
                else -> it
            }
        }
        for (direction in directions) {
            val before = WordQuizBuilder.options(
                originalWords.single { it.word == "支払う" }, originalWords, direction, Random(0))
            val after = WordQuizBuilder.options(byWord.getValue("支払う"), words, direction, Random(0))
            assertEquals(before, after)
            assertTrue(after.map { it.word }.containsAll(listOf("支払う", "支払")))
            println("LEGACY unchanged $direction payment pair: $after")
        }

        val quizCards = parsed.kanji.map {
            QuizCard(it.kanji, it.title, it.tags, it.distractors, it.quizExclusions)
        }
        val byKanji = quizCards.associateBy { it.kanji }
        assertEquals(quizCards.size, byKanji.size)
        val member = byKanji.getValue("勘")
        val guards = listOf("感", "思", "考", "判", "査", "比", "算", "察")
        assertEquals(guards, member.quizExclusions)
        val n1Stack = Stacks.find("jlpt-n1", Stacks.available(parsed.kanji.map { it.tags }))
        assertEquals("jlpt-n1", n1Stack.tag)
        val n1 = quizCards.filter { n1Stack.contains(it.tags) }
        assertTrue(n1.any { it.kanji == member.kanji })
        val custom = (listOf("勘", "勤", "助", "期") + guards).map { byKanji.getValue(it) }
        for ((name, pool) in listOf("N1" to n1, "all" to quizCards, "custom" to custom)) {
            val observed = sortedSetOf<String>()
            repeat(20) { seed ->
                val options = QuizBuilder.options(member, pool, Random(seed))
                assertEquals(4, options.size)
                assertEquals(1, options.count { it.kanji == "勘" })
                assertEquals(options.size, options.map { it.title }.toSet().size)
                assertTrue(options.none { it.kanji in guards })
                val selected = options.map { byKanji.getValue(it.kanji) }
                selected.forEachIndexed { index, card ->
                    selected.take(index).forEach {
                        assertFalse(it.kanji in card.quizExclusions || card.kanji in it.quizExclusions)
                    }
                }
                observed += options.filter { it.kanji != "勘" }.map { "${it.kanji}:${it.title}" }
            }
            println("KANJI $name observed choices: ${observed.joinToString(" | ")}")
        }
        for (guard in guards) {
            val other = byKanji.getValue(guard)
            for (target in listOf(member, other)) {
                repeat(10) { seed ->
                    assertEquals(listOf(target.kanji),
                        QuizBuilder.options(target, listOf(member, other), Random(seed)).map { it.kanji })
                }
            }
        }
        val legacyFallbacks = listOf("人", "休", "何", "入", "出", "口", "女", "日", "月", "男", "買")
        for (id in legacyFallbacks) {
            val target = byKanji.getValue(id)
            assertTrue(target.distractors.size < 3)
            val incoming = (listOf(target, member) + target.distractors.mapNotNull { byKanji[it] })
                .distinctBy { it.kanji }
            repeat(10) { seed ->
                val options = QuizBuilder.options(target, incoming, Random(seed))
                assertTrue(options.any { it.kanji == id })
                assertTrue(options.any { it.kanji == "勘" })
                assertEquals(options.size, options.map { it.title }.toSet().size)
                if (seed == 0) println("LEGACY incoming $id: $options")
            }
        }
        val readingCards = parsed.kanji.map(::reading)
        val memberReading = readingCards.single { it.kanji == "勘" }
        assertEquals(listOf("かん"), memberReading.quizKeys(ReadingKind.On))
        assertTrue(memberReading.quizKeys(ReadingKind.Kun).isEmpty())
        repeat(10) { seed ->
            val question = requireNotNull(KanjiReadingQuiz.question(
                memberReading, ReadingKind.On, readingCards, Random(seed), reading = "かん"))
            assertEquals("かん", question.correctKey)
            assertEquals(4, question.options.size)
            assertEquals(1, question.options.count { it.key == question.correctKey })
            assertTrue(question.options.filter { it.key != question.correctKey }
                .none { it.key in KanjiReadingQuiz.excludedKeys(memberReading) })
        }
        for (kanji in listOf("定", "違")) {
            val legacy = readingCards.single { it.kanji == kanji }
            println("LEGACY $kanji offered kun readings: ${legacy.quizReadings(ReadingKind.Kun)}")
        }
    }
}
