---
applyTo: "listening/**,listening-tasks/**,audio/**,task-audio/**,task-images/**,docs/listening*.md,docs/listening-task-*/**,tools/*listening*.py"
---

# Authoring listening exercises

Use the [legacy English-question contract](../../docs/listening-n5.md) or the
[Japanese task-package contract](../../docs/listening-tasks.md), as appropriate.
Their schemas, media namespaces, timing and approvals are not interchangeable.
Follow the [practical authoring sequence](../../docs/listening-tasks.md#practical-authoring-sequence)
and the shared [language/task review rules](../copilot-instructions.md).

- Define the tested operation, independent story identity, speaker roles, register,
  evidence and what must be heard versus seen before writing distractors. A different
  noun, title, rendering or ID does not create a new transfer context.
- Review every option as an actual utterance in that situation. A plausible polite
  refusal or contraction is not wrong simply because it differs from the model answer.
  For illustrated expression tasks, include plausible other-role utterances so the
  marked person matters; do not state the marked role redundantly in the narration.
- After shortening or revising a dialogue, reread the entire exchange, translations,
  options, evidence references and feedback. Remove replies to deleted questions;
  do not invent facts to justify a distractor or strengthen a conclusion.
- Use the established soft animated/editorial **still-illustration** style, not schematic
  people, as the default for natural scenes. Follow `tools/image_prompts.json`'s `style`
  and the [selected listening illustrations](../../docs/listening-task-pool/illustrations.json).
  A numbered grid must remain an equally presented comparison, not a decorative scene.
  Keep artwork original and text-free except necessary controlled labels; no named
  artist/franchise imitation, speech bubbles, brands or highlighted answer.
- Freeze visual invariants in the prompt: exact people/objects, left/right roles,
  action state, occupied/free hands, camera direction, open/closed doors, and the
  number/size/color map. Add crisp arrows and numbers locally **after inspecting the
  actual output**. Never change the question or key to accommodate a wrong picture.
- Inspect each finished, marked picture at 512px and 256px and in the native light/dark
  presentation. Check anatomy, props, role markers, readable labels and the nonvisual
  study boundary. A prompt, generated file or browser screenshot is not device approval.
- Use measured pilot speech rates and actual encoded stage durations to adjust scripts.
  Recheck all permitted section selections, not an average or one form. Never pad speech
  or add repeated stories merely to reach the section duration.
- Before paid generation, freeze scope and obtain bounded owner authorization. Verify
  the actual model/deployment's pricing and rate limits; pace requests before sending.
  Keep durable per-attempt accounting, including retries, and stop on uncertain outcomes.
  Do not reset a ledger or mistake a conservative reservation for an invoiced charge.
- Preserve previous runs and review copies. An image-only revision should reuse
  byte-identical verified audio and timings in a new plan, not regenerate speech.
  Rebind the complete media object and record the new selected image hashes; do not
  copy package/device approvals or spending authorization into the new plan.
- Record owner acceptance accurately and separately from unperformed checks. Ask only
  for genuinely missing approval evidence; do not repeatedly request already-given
  content/artwork acceptance. Do not infer physical-phone or full-section testing from
  general approval, nor enable drafts by manufacturing those declarations.

These checks consolidate observed lessons from content #38: dialogue-shortening,
role-dependent choices, translation/feedback corrections, the owner-selected illustration
revision, and image-service throttling. They add no mandatory reviewer count or new
linguistic certification.
