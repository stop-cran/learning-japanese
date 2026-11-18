# From sentence chunks to connected grammar

Knowing a verb ending is only part of using it. A complete sentence must also preserve **who does what,
which clause belongs to which expression, and which earlier facts still apply**.

This practice adds 16 sentence-composition questions and 12 closing-report questions across six short passages,
plus 36 N3 ordering questions built on the patterns in [Ordering sentences with N3 patterns](#ordering-sentences-with-n3-patterns),
and 46 passage gap-fill questions in [Reading a whole passage before filling a blank](#reading-a-whole-passage-before-filling-a-blank).
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

## Reading a whole passage before filling a blank

The intermediate passage set uses short texts of about 130–200 characters, each with one blank. When a passage
holds several decisions, it becomes several exercises. In each one, the other spot is printed with wording that
is not one of the candidates, so you cannot rule out a candidate just because it already appears in the text.
Most blanks sit inside the passage, not in its last line. If the passage shows the deciding information after
the blank, read to the end before you choose. In typed mode the options are hidden, so the instruction line
always lists every candidate.

### Connectives in a passage

**すると, その結果 and そこで.** すると introduces the next development or a discovery after an event.

> 古い箱のふたを開けてみた。すると、中から祖母の手紙が出てきた。  
> I tried opening the lid of an old box, and out came a letter from my grandmother.

その結果 marks a causal result of what precedes. When the passage simply tells what came next after an event,
すると (or そうすると) is accepted too.

> 毎朝三十分ずつ英語のニュースを聞き続けた。その結果、半年で先生の話がほとんど分かるようになった。  
> I kept listening to English news for thirty minutes every morning. As a result, within six months I could follow almost everything the teacher said.

そこで introduces a deliberate step chosen in response to the situation. If the passage shows the writer's own
decision or plan (〜ことにした, 〜てみようと思う), use そこで: すると presents what happened next or what someone
found, and does not introduce the writer's own decision.

> 会議室のエアコンが急に止まってしまった。そこで、私たちは隣の部屋に移ることにした。  
> The air conditioner in the meeting room suddenly stopped, so we decided to move to the room next door.

**ところが and ところで.** ところが says that the facts went against an expectation that the passage has just
set up.

> 簡単な試験だと聞いていた。ところが、問題を開くと、知らない言葉ばかりだった。  
> I had heard it was an easy test. But when I opened the paper, it was full of words I didn't know.

ところで leaves the current story for a new topic, often with a question to the reader or listener.

> 来週の練習は、いつもどおり水曜日の六時からです。ところで、夏の大会の申し込みはもう済みましたか。  
> Next week's practice is at six on Wednesday as usual. By the way, have you already entered the summer tournament?

**つまり, また and あるいは.** つまり restates or sums up what came before in other words.

> この店は月曜日と火曜日が休みで、ほかの日は夜八時まで開いている。つまり、平日の夜に行けるのは水曜日から金曜日までだ。  
> This shop is closed on Mondays and Tuesdays and open until eight on other days. In other words, on weekday evenings you can only go from Wednesday to Friday.

また adds a separate point of the same kind.

> この公園には大きな池がある。また、春には桜を見に多くの人が訪れる。  
> This park has a large pond. Also, many people visit in spring to see the cherry blossoms.

あるいは joins two alternatives.

> 会場へは、駅からバスに乗るか、あるいは二十分ほど歩くかして来てください。  
> Please come to the venue from the station either by bus or on foot, which takes about twenty minutes.

**かえって and やはり.** かえって marks a result that is the opposite of what the action was meant to achieve.

> 近道をしようと細い道に入ったら、かえって時間がかかってしまった。  
> I turned into a narrow street to take a shortcut, but it actually took longer.

やはり marks a result or conclusion that matches what was usual or expected.

> 新しい店のラーメンも食べてみたが、やはり、いつもの店の味が一番だと思った。  
> I tried the ramen at the new shop too, but I decided that my usual shop tastes best after all.

**〜一方で and 〜代わりに.** 一方で sets two facts side by side, and both are true.

> この仕事は給料がいい一方で、休みがとても少ない。  
> This job pays well, but on the other hand it has very few days off.

In these passages, 代わりに has its substitution sense: one thing takes the place of another, so the first does
not happen.

> 社長が急に来られなくなったので、副社長が代わりにあいさつをした。  
> The president suddenly couldn't come, so the vice-president gave the speech instead.

代わりに also has an exchange or compensation sense, in which both things happen: 英語を教えてもらう代わりに、
日本語を教えてあげる ("in return for being taught English, I teach Japanese").

### The beginning and the end must agree

When a sentence opens with なぜなら, its end gives the reason. In these plain-style examples, なぜなら pairs
with 〜からだ or 〜からである. In polite style, 〜からです is used.

> 私はできるだけ階段を使うようにしている。なぜなら、少しでも体を動かしたいからだ。  
> I try to use the stairs whenever I can. That's because I want to move my body even a little.

When a sentence opens with そのため, it states a consequence of what was just said and ends with an ordinary
predicate. If the blank opens a sentence, read to the end of that sentence before you choose the opener.

> 大雪で、町へ向かう道路が通れなくなった。そのため、多くの店がその日は休みになった。  
> Heavy snow made the road into town impassable. For this reason, many shops were closed that day.

### One text, one style

An essay or a report keeps plain だ／である throughout.

> この調査の目的は、高校生の睡眠時間を調べることである。調査は三つの学校で行った。  
> The aim of this survey is to examine high-school students' sleeping hours. The survey was carried out at three schools.

A speech, a notice or a letter keeps です／ます throughout. Decide the style of a blank from the other sentences of
the text, not only from the blank's own sentence.

> 皆さん、こんにちは。今日は私の町の祭りについて紹介します。この祭りは三百年前から続いています。  
> Hello, everyone. Today I'll introduce the festival in my town. It has continued for three hundred years.

### Familiar forms, decided by the whole story

Some items reuse N4 forms. Their level reflects that, but the decision still needs the whole passage.

**Passive or causative.** The general rule is about who acts on whom.
- If someone marked with に does something that affects the narrator, use the passive.
- If the narrator makes or lets someone else do something, use the causative.

The passage gives the cues: the narrator's embarrassment or hurt after being criticised points to the passive.
A decision to hand a task to someone (〜に…させることにした), or that person improving afterwards, points to the
causative.

> 混んだ電車の中で、隣の人に足を踏まれた。  
> On a crowded train, the person next to me stepped on my foot.

> 毎朝、中学生の息子にごみを出させている。  
> Every morning I have my junior-high-school son take out the rubbish.

**〜てあげた or 〜てもらった.** Look for who thanks whom later in the passage. Thanks from the other person point to
あげた.

> 宿題が分からないと言う弟に、算数の問題を説明してあげた。  
> My little brother said he didn't understand his homework, so I explained the maths problems to him.

Gratitude from the narrator points to もらった, with the helper marked by に.

> 先輩に、作文の間違いを直してもらった。  
> An older student corrected the mistakes in my essay for me.

**〜ていた, 〜てあった or 〜ておいた.** 〜ていた reports a state as the narrator found it, without saying how or why it
arose. It is never wrong merely because someone arranged the state, but if the passage shows that the state came
about by itself or by accident, only 〜ていた fits.

> 朝起きると、夜の間の雪の重さで、庭の木の枝が一本折れていた。  
> When I got up in the morning, a branch of the tree in the garden had broken under the weight of the night's snow.

〜てあった foregrounds that someone deliberately arranged the state. The thing in that state is marked with が.

> 会場に入ると、机の上に名札が並べてあった。  
> When I entered the hall, name cards had been set out on the tables.

〜ておいた is the preparer's own action, done in advance. The doer is the subject and the object takes を, so it does
not fit when the narrator only finds a state that someone else prepared.

> 発表の前の日に、資料を二十部コピーしておいた。  
> The day before the presentation, I made twenty copies of the handout in advance.

See [result and topic connectives](result-and-topic-connectives.md),
[correction and contrast connectives](correction-and-contrast-connectives.md),
[emphatic causes and reason connectives](emphatic-causes-and-reason-connectives.md),
[written register and casual markers](written-register-and-casual-markers.md),
[passive and affected participants](passive-and-affected-participants.md),
[making, letting and being made to act](making-letting-and-being-made-to-act.md),
[benefactive actions](benefactive-actions.md) and
[actions, events and results](actions-events-and-results.md).

## Scope and sources

The four composition families practise reported instructions, receiving-side favors, current/recalled plans,
and embedded questions. They are a bounded structural exercise, not comprehensive coverage of every use in
those families. The six passages add rule/reference and event-stage demands, not a claim of exam readiness.

The N3 composition section practises ordering with に比べて, にとって, に対して, に代わって, のおかげで, たとたん,
ようとする (ようとしたとき), purpose ために and たびに.

The N3 passage section practises choosing a connective from the rest of a passage (すると, その結果, そこで,
ところが, ところで, つまり, また, あるいは, かえって, やはり, 一方で, 代わりに, なぜなら〜からだ and そのため),
keeping one style through a text (である against です), and N4 contrasts decided by the whole story: passive
against causative, てあげた against てもらった, and ていた, てあった and ておいた. Levels are editorial estimates,
because JLPT publishes no official grammar list; items whose decisive form is N4 are labelled N4. References
include Bunpro's [すると](https://bunpro.jp/grammar_points/すると), [その結果](https://bunpro.jp/grammar_points/その結果),
[そこで](https://bunpro.jp/grammar_points/そこで), [ところが](https://bunpro.jp/grammar_points/ところが),
[ところで](https://bunpro.jp/grammar_points/ところで), [つまり](https://bunpro.jp/grammar_points/つまり),
[あるいは](https://bunpro.jp/grammar_points/あるいは), [却って](https://bunpro.jp/grammar_points/却って),
[一方で](https://bunpro.jp/grammar_points/一方で) and [代わりに](https://bunpro.jp/grammar_points/代わりに).

The [JLPT test-item description](https://www.jlpt.jp/e/guideline/testsections.html) distinguishes sentence
composition and text grammar. The [official sample page](https://www.jlpt.jp/e/samples/forlearners.html) explains
that samples illustrate item formats and may differ from actual booklets. Those pages are format references;
the scenes here are original.

Construction references include Bunpro's [reported instructions](https://bunpro.jp/grammar_points/ようにいう),
[whether questions](https://bunpro.jp/grammar_points/かどうか), [planned events](https://bunpro.jp/grammar_points/よていだ),
[receiving favors](https://bunpro.jp/grammar_points/てもらう), [existing results](https://bunpro.jp/grammar_points/てある),
[preparation](https://bunpro.jp/grammar_points/ておく), [optional actions](https://bunpro.jp/grammar_points/なくてもいい),
and [required actions](https://bunpro.jp/grammar_points/なければならない).
