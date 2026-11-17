# From sentence chunks to connected grammar

Knowing a verb ending is only part of using it. A complete sentence must also preserve **who does what,
which clause belongs to which expression, and which earlier facts still apply**.

This practice adds 16 sentence-composition questions and 12 closing-report questions across six short passages,
plus 36 N3 ordering questions built on the patterns in [Ordering sentences with N3 patterns](#ordering-sentences-with-n3-patterns).
It uses the ordinary choice and typing modes. It is not drag-and-drop, an official JLPT question collection,
a starred-position shortcut, or a timed exam simulator.

## Composing a whole sentence

Read the Japanese scene before arranging the labeled chunks. Use **every chunk exactly once**, with its printed
spelling and internal word order unchanged. Type the whole sentence without chunk labels, spaces, or punctuation.
The final `。` is already outside the blank. End with the supplied polite predicate.

The individual question also states its scope constraints. These matter: another grammatical sentence can use
the same words yet report the wrong person, reverse the events, or attach a time phrase to a different action.
The ordinary trim/NFKC input normalization still applies; this is not a request for arbitrary paraphrases or
different kana/kanji spellings.

### Participants are not determined by first position

In a receiving-side report, the person with **は** receives the help and the person with **に** performs it:

> 私は友達に道を教えてもらいました。  
> My friend gave me directions; I received that help.

The same roles survive a different phrase order:

> 友達に私は道を教えてもらいました。  
> From my friend, I received directions.

For these bounded tasks, the two marked people and the object phrase can appear in any of their six orders
before the intact final predicate. Some orders put unusual emphasis on a phrase; they are not six different
assignments of giver and receiver. **教えてもらえませんでした** instead says that the help could not be obtained:
the receiving-side participant is still identifiable, but no successful favor is asserted.

Reported instructions add a voice distinction:

> 私は先生に待つように言いました。  
> I told the teacher to wait.
>
> 私は先生に待つように言われました。  
> I was told by the teacher to wait.

The active/passive ending changes how the two marked people relate to the instruction. Passive reporting does
not automatically mean mistreatment. In the ordering questions, give one person **は** and the other **に**;
keep the reported instruction as one clause. The instruction clause and the two marked people may move before
the final reporting verb without exchanging their roles.

See [benefactive actions](benefactive-actions.md) and [embedded questions and reports](embedded-questions-and-reports.md).

### Keep the time phrase inside the intended scope

> 電話する前に掃除する予定です。  
> I plan to clean before phoning.

Here **電話する前に** belongs inside the action description modifying **予定（よてい, plan）**.
The sentence does not say that the plan itself was made before the phone call. In these ordering tasks,
that internal action-order reading is explicitly required.

**予定でした** recalls an earlier plan. It does not, by itself, tell us whether the plan succeeded.
Read the rest of the scene: one example follows the earlier sequence, while another explicitly changes it.
Keep the supplied plan tense and report the plan rather than replacing it with the actual outcome.

See [volition, plans and goals](volition-plans-and-goals.md).

### An embedded question is not an established event

> 部屋に戻った後で窓を閉めたかどうか確認します。  
> After returning to the room, I will check whether I closed the window.

Returning is established; closing the window is being checked. The embedded question can also precede the time phrase:

> 窓を閉めたかどうか部屋に戻った後で確認します。  
> I will check whether I closed the window, after returning to the room.

Both orders preserve the intended scope. Exchanging **後で** and **かどうか** between the clauses would instead
question the established return and assert the uncertain window-closing event. The full **かどうか** chunk must be
used here even though bare **か** can work in other unrestricted questions.

The answer explanation gives a canonical completion and discusses allowed orders. A different accepted typed
order may be displayed separately from that canonical model; it is not a mistake merely because it differs.

## Ordering sentences with N3 patterns

The intermediate composition set uses the same task as the "Composing a whole sentence" section: every chunk is printed, each is used once, and the
whole sentence is typed without labels, spaces or punctuation. The difference is the glue. Each sentence now hangs on an
N3 pattern, and the pattern decides which person, item or event goes where. The wrong option is always a grammatical
sentence built from the same chunks, so only the context can rule it out.

### Noun-phrase frames: which noun takes which marker

Five patterns attach directly after a noun. The learner places two noun chunks and gives each exactly one marker chunk.

| Pattern | Noun directly before the pattern | The other noun |
|---|---|---|
| Xは Yに比べて | Y, the standard of comparison | X, marked with は, is described |
| Xにとって Yの…は | X, whose standpoint counts | Y, owner of the thing judged |
| Xは Yに対して | Y, at whom the action or attitude is directed | X, marked with は, acts |
| Yに代わって Xが | Y, who would normally act | X, marked with が, acts instead |
| Yのおかげで Xは | Y, credited with helping | X, marked with は, gets the result |

Because the markers carry the roles, the two noun phrases may usually come in either order before the predicate:

- 妹は姉に比べて足が速いです。／姉に比べて妹は足が速いです。 — Compared with her older sister, the younger sister runs fast.
- 店長に代わって私が客に説明しました。／私が店長に代わって客に説明しました。 — I explained it to the customer in place of the store manager.

Swapping the markers is still good Japanese, but it states the opposite: 姉は妹に比べて足が速いです claims that the
older sister is the faster runner. Check the numbers or events in the context before choosing which noun is described.

### Clause frames: which event comes before the linker

Four patterns join two clauses. The linker goes directly after one complete clause, and the final chunk goes after the
other, so there is normally a single accepted order.

- 窓を開けたとたん冷たい風が入ってきたんです。 — The moment I opened the window, a cold wind came in. The clause
  before とたん happened first.
- 私が電話をかけようとしたとき友達が部屋に来ました。 — Just as I was about to make a phone call, a friend came to my room. The
  person before ようとしたとき was about to act; the other person interrupted.
- 日本語の新聞を読むために毎日漢字を練習しています。 — I practise kanji every day in order to read Japanese newspapers.
  The clause before ために is the goal; the clause after it is the step.
- この写真を見るたびに子どものころを思い出すんです。 — Every time I look at this photo, I remember my childhood. The clause before
  たびに is the repeated occasion; the clause after it is what happens each time.

Swapping the two clauses gives a sentence that is still grammatical but reverses the order of events, the goal, or the
habit. For example, 毎日漢字を練習するために日本語の新聞を読む would make reading newspapers a step towards practising kanji.

### Checking an ordering

1. Find the pattern chunk and the job it gives the noun or clause in front of it.
2. Use the context to decide which noun or event does that job.
3. Attach the remaining marker or final chunk to the other noun or clause.
4. Read the result once as a statement and compare it with the context.

For background on viewpoint and target phrases, see [targets and perspectives](about-targets-and-perspectives.md).
Comparisons are covered in [comparisons, change and degree](comparisons-change-and-degree.md), and cause and credit in
[reasons and contrasts](reasons-and-contrasts.md). For purpose and attempts, see
[volition, plans and goals](volition-plans-and-goals.md).

The JLPT levels attached to these exercises are editorial estimates; Bunpro's N3 list is the primary reference (for
example its [にとって entry](https://bunpro.jp/grammar_points/に取って)). There is no official JLPT grammar list.

## Reading across a short passage

Each passage supports two questions, but the questions share one context. Read the complete passage each time;
do not answer from the closing noun alone.

For rules, identify **who belongs to which category, whether an action has already been completed, and whether
an exception applies**. A member's permission is not automatically a nonmember's permission. An exception for
people who already submitted something does not remove the requirement for someone who has not.

**しなければなりません** says that an action is required. **しなくてもいいです** says that it is not required;
it does not forbid the action. The passages supply the particular rules rather than asking you to guess real-world
school or membership policies.

For event stages, keep **an existing purposeful result** separate from **a stated outstanding preparation**:

> 名前は紙に書いてあります。  
> The name has been written on the paper and is there.
>
> 名前は紙に書いておきます。  
> I will write the name on the paper in preparation.

These are interpretations of the supplied contexts and printed forms, not a universal rule that **ておく** must
refer to the future. It can also describe completed preparation or leaving something as it is. An existing result
does not forbid every later action, either. In these questions, report what the passage actually supplies:
do not invent another writing, printing, or cutting plan to justify a different completion.

Use the printed completion or its all-hiragana spelling, without punctuation. Other natural expressions are
outside that finite response task, not globally incorrect Japanese.

See [necessity, advice and instructions](necessity-advice-and-instructions.md) for obligation and permission,
and [actions, states and time](japanese-actions-states-and-time.md) for result-state background.
For the written connectives that link sentences across a passage (すなわち, また, あるいは, 前者／後者), see
[Result and topic connectives](result-and-topic-connectives.md).

## Scope and sources

The four composition families practise reported instructions, receiving-side favors, current/recalled plans,
and embedded questions. They are a bounded structural exercise, not comprehensive coverage of every use in
those families. The six passages add rule/reference and event-stage demands, not a claim of exam readiness.

The N3 composition section practises ordering with に比べて, にとって, に対して, に代わって, のおかげで, たとたん,
ようとする (ようとしたとき), purpose ために and たびに.

The [JLPT test-item description](https://www.jlpt.jp/e/guideline/testsections.html) distinguishes sentence
composition and text grammar. The [official sample page](https://www.jlpt.jp/e/samples/forlearners.html) explains
that samples illustrate item formats and may differ from actual booklets. Those pages are format references;
the scenes here are original.

Construction references include Bunpro's [reported instructions](https://bunpro.jp/grammar_points/ようにいう),
[whether questions](https://bunpro.jp/grammar_points/かどうか), [planned events](https://bunpro.jp/grammar_points/よていだ),
[receiving favors](https://bunpro.jp/grammar_points/てもらう), [existing results](https://bunpro.jp/grammar_points/てある),
[preparation](https://bunpro.jp/grammar_points/ておく), [optional actions](https://bunpro.jp/grammar_points/なくてもいい),
and [required actions](https://bunpro.jp/grammar_points/なければならない).
