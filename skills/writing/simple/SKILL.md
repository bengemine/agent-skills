---
name: simple
description: Rewrite the last reply in short, simple, plain English.
disable-model-invocation: true
---

Rewrite your last reply in very simple plain English. Do not answer a new question. Keep every fact and warning.

If there is no earlier reply, say there is nothing to rewrite.

This applies to this one reply only. It does not change how later replies are written.

Use these rules for the rewrite:

- **Be SHORT. The user hates reading a lot.** Total reply length matters as much as sentence length.
- Use very short sentences. Aim for 10 words or fewer per sentence.
- Use small everyday words. No fancy phrasing. No corporate filler. Concretely:
  - Say what a thing **does**, not what it is called in code: "asks the database for", not "executes a query"; "sends back", not "returns a struct"; "the page", not "the consumer".
  - Keep identifiers, table and column names, and endpoint names out of the opening sentence. Name them after the point has landed, where they are actionable.
  - Prefer a short second sentence over a dash, a parenthesis, or a subordinate clause.
  - Avoid abstract nouns that hide the fact: state, path, flow, layer, source of truth, data integrity, lifecycle. If one feels necessary, the concrete fact has not been found yet — find it.
- Cut everything that is not needed. No restating. No hedges. No recap of what they asked.
- Keep all critical info. Do not drop facts or warnings to save words.
- Default to bullets and tables, not paragraphs.
- Skip headers unless the answer has 3+ distinct parts.
- If a technical word is needed, explain it in brackets right next to it.
- Skip "I would be happy to", "certainly", "absolutely", etc.
- One question at a time at the end. Not three. Not a list of next-step options.

Test before you reply: re-read your message. If it is more than ~150 words for a normal answer, cut it. If a sentence has more than 20 words, rewrite it shorter. If you used a word you would not say to a friend, swap it.
