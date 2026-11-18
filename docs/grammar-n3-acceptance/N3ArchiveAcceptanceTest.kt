package io.github.stopcran.kanji.core

import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.content.GrammarCurriculumState
import io.github.stopcran.kanji.core.content.SafeZip
import io.github.stopcran.kanji.core.grammar.GrammarAvailability
import io.github.stopcran.kanji.core.grammar.GrammarChoices
import io.github.stopcran.kanji.core.grammar.GrammarEligibility
import io.github.stopcran.kanji.core.grammar.GrammarFocus
import io.github.stopcran.kanji.core.grammar.GrammarScope
import io.github.stopcran.kanji.core.srs.CardPhase
import io.github.stopcran.kanji.core.srs.SrsState
import org.junit.Assert.*
import org.junit.Test
import java.io.File
import java.security.MessageDigest
import java.time.Instant
import kotlin.random.Random

/** Run in app :core:test with N3_ACCEPTANCE_ARCHIVE pointing to the pinned LF Git archive. */
class N3ArchiveAcceptanceTest {
    companion object {
        private val parsed by lazy {
            val archive = File(requireNotNull(System.getenv("N3_ACCEPTANCE_ARCHIVE")) {
                "N3_ACCEPTANCE_ARCHIVE must name the complete archive; this test must not skip"
            })
            val digest = MessageDigest.getInstance("SHA-256")
            archive.inputStream().use { input ->
                val buffer = ByteArray(8192)
                while (true) {
                    val size = input.read(buffer)
                    if (size < 0) break
                    digest.update(buffer, 0, size)
                }
            }
            assertEquals(
                "912a9dfc4e19653bc5eedbbd4aaae55fab5ee6a63060b3293ea71362f5c37e6a",
                digest.digest().joinToString("") { "%02x".format(it) },
            )
            ContentParser.parse(archive.inputStream().use { SafeZip.read(it) }).also {
                assertTrue(it.problems.toString(), it.problems.isEmpty())
                assertTrue(it.listeningTasks.problems.toString(), it.listeningTasks.problems.isEmpty())
                assertTrue(it.listeningTasks.unsupported.toString(), it.listeningTasks.unsupported.isEmpty())
            }
        }
        private val newSetIds = setOf(
            "change-phase-trends", "time-during-immediacy", "cause-emphasis-purpose",
            "concession-supposition", "hearsay-naming-frames", "advice-certainty-denial",
            "degree-excess-addition", "focus-limits-intervals", "attitude-conjecture-adverbs",
            "negative-polarity-adverbs", "compound-verb-endings", "tendency-noun-suffixes",
            "basis-field-viewpoint", "comparison-role-relations", "correction-contrast-connectives",
            "result-topic-connectives", "attempts-compulsion-pretence", "written-register-negation",
            "sentence-composition-intermediate", "connected-text-grammar-intermediate",
        )
        private val now = Instant.parse("2026-11-17T17:00:00Z")
    }

    @Test
    fun exactArchiveImportsEveryN3SetAndTheCurriculum() {
        assertEquals(108, parsed.grammar.size)
        val exercises = parsed.grammar.flatMap { it.exercises }
        assertEquals(3336, exercises.size)
        assertEquals(1139, exercises.count { it.jlpt == 3 })
        val newSets = parsed.grammar.filter { it.id in newSetIds }
        assertEquals(newSetIds, newSets.map { it.id }.toSet())
        val added = newSets.flatMap { it.exercises }
        assertEquals(905, added.size)
        assertEquals(mapOf(3 to 888, 4 to 14, 5 to 3), added.groupingBy { it.jlpt }.eachCount())
        assertEquals(36, newSets.single { it.id == "sentence-composition-intermediate" }.exercises.size)
        assertEquals(46, newSets.single { it.id == "connected-text-grammar-intermediate" }.exercises.size)
        assertTrue(parsed.curriculum is GrammarCurriculumState.Ready)
        val curriculum = parsed.curriculum as GrammarCurriculumState.Ready
        val groups = newSets.flatMap { it.introductionGroups }
        assertEquals(125, groups.size)
        assertTrue(curriculum.graph.chapterByGroup.keys.containsAll(groups.map { it.id }))
    }

    @Test
    fun realN2ItemsStayOutsideNewN3IntakeButStartedReviewsRemain() {
        val exercises = parsed.grammar.flatMap { it.exercises }
        val eligible = GrammarEligibility.pool(exercises, emptyMap(), GrammarScope.N3, true).ids.toSet()
        assertEquals(2711, eligible.size)
        assertEquals(exercises.filter { it.jlpt in setOf(3, 4, 5) }.map { it.id }.toSet(), eligible)
        val n2 = exercises.filter { it.jlpt == 2 }
        assertEquals(104, n2.size)
        assertTrue(n2.none { it.id in eligible })
        assertTrue(n2.all { GrammarScope.N2.matches(it.jlpt, false) && GrammarScope.All.matches(it.jlpt, false) })
        assertEquals(1139, exercises.count { GrammarScope.N3.matches(it.jlpt, false) })
        val started = n2.first().id
        val states = mapOf(started to SrsState(CardPhase.Review, due = now.minusSeconds(1)))
        assertEquals(eligible + started, GrammarEligibility.pool(exercises, states, GrammarScope.N3, true).ids.toSet())
    }

    @Test
    fun newGroupsAreCoherentAndRealFoundationsStillGateIntroductions() {
        val groups = GrammarFocus.groups(parsed.grammar)
        val exercises = parsed.grammar.flatMap { it.exercises }.associateBy { it.id }
        val newGroups = GrammarFocus.groups(parsed.grammar.filter { it.id in newSetIds })
        assertEquals(125, newGroups.size)
        assertTrue(newGroups.all { it.authored })
        val ready = groups.map { it.id }.toSet()
        val available = GrammarAvailability.evaluate(
            groups, exercises, emptyMap(), GrammarScope.N3, true, ready, 10, now,
        )
        newGroups.forEach { group ->
            assertNull(group.id, available.getValue(group.id).guidedBlock)
        }
        assertTrue(newGroups.any { group ->
            group.members.map { exercises.getValue(it.exerciseId).jlpt }.toSet().size > 1
        })
        val dependent = groups.single { it.id == "causative-perspective-short-forms" }
        val started = dependent.members.first().exerciseId
        val blocked = GrammarAvailability.evaluate(
            groups, exercises, mapOf(started to SrsState(CardPhase.Review, due = now.minusSeconds(1))),
            GrammarScope.N3, true, emptySet(), 10, now,
        ).getValue(dependent.id)
        assertEquals(dependent.requires, blocked.missingPrerequisites)
        assertFalse(blocked.missingPrerequisites.isEmpty())
        assertTrue(blocked.targetedNew.isEmpty())
        assertEquals(listOf(started), blocked.due)
        assertNull(available.getValue(dependent.id).guidedBlock)
        val unguided = groups.filterNot { it.authored }
        assertTrue(unguided.any { available.getValue(it.id).targetedNew.isNotEmpty() })
    }

    @Test
    fun allNewAnswersAndChoiceVariantsFitTheExistingModes() {
        val exercises = parsed.grammar.filter { it.id in newSetIds }.flatMap { it.exercises }
        var multiCorrectSnapshots = 0
        exercises.forEach { exercise ->
            assertTrue(exercise.id, exercise.acceptedAnswers.isNotEmpty())
            exercise.acceptedAnswers.forEach {
                assertTrue("${exercise.id}: typed answer exceeds 80 UTF-16 units", it.length <= 80)
            }
            val accepted = exercise.acceptedAnswers.map(GrammarChoices::normalizeAnswer).toSet()
            repeat(25) { seed ->
                val snapshot = GrammarChoices.build(exercise, Random(seed))
                assertTrue(exercise.id, snapshot.options.size in 2..4)
                assertTrue(snapshot.correctOptionIds.isNotEmpty())
                snapshot.options.forEach { option ->
                    assertEquals(exercise.id, option.id in snapshot.correctOptionIds,
                        GrammarChoices.normalizeAnswer(option.label) in accepted)
                }
                if (snapshot.correctOptionIds.size > 1) multiCorrectSnapshots++
            }
        }
        assertTrue("Real additional-correct choices must be exercised", multiCorrectSnapshots > 0)
    }
}
