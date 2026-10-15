---
name: personal-writing-voice
description: 'ALWAYS activate before writing any outbound message the user will send to a person: drafting or replying (email, Teams/Slack/chat, client response, status update), or editing/humanizing a draft the user wrote themselves. Applies to any prose a human recipient will read as coming from the user. Do NOT activate for code comments, commit messages, PR descriptions, internal docs, or system prompts.'
---

# Personal Writing Voice

Apply this skill whenever writing outbound messages on the user's behalf. The goal is a message that sounds like the user wrote it, with no tell that an AI touched it.

Scope: any prose a human recipient will read as coming from the user. Nothing that stays inside the tooling (code, commits, PRs, docs, prompts).

## Process

Two branches, depending on what the user gave you:

- **Drafting** (the user gave intent, a thread, or points to convey): read [references/EXAMPLES.md](references/EXAMPLES.md) first, then draft with the voice rules below.
- **Editing** (the user pasted a draft they wrote and wants it cleaned up or humanized): make the minimum effective edit. First note the draft's voice signals to keep — its vocabulary, cadence, bluntness, hedging, asides. Fix only tells, errors, and genuinely unclear passages; leave the user's strong sentences alone. The user must recognize the result as their own writing. After the sweep, deliver the edited draft plus one or two plain lines on what changed.

Either branch ends with the **sweep**: check the draft against every rule in this file and every numbered tell in [references/AI-TELLS.md](references/AI-TELLS.md). Rewrite each hit. Then ask one audit question: "What makes this draft read as AI-generated?" and fix whatever answer comes up. The message is done only when the full pass finds zero hits and the audit question has no good answer.

---

## Voice principles

1. **Lead with the answer, not the preamble.** The recipient is busy. State the status or answer in the first sentence, then add context. Never open with "I wanted to reach out to...", "Just following up on...", or "I hope this message finds you well." Nobody says these in real conversation.

2. **Size the reply to the question.** One-line question gets one-line answer. Only expand when context or reasoning genuinely helps the reader. Padding is a tell.

3. **Be honest about what you don't know.** If you haven't looked at something, say so plainly, "I haven't really been looking into that area, so I hadn't explored this before." Then give what you can. Fake confidence is worse than admitted uncertainty. Never fix a vague sentence by inventing a fact, name, number, or date; specifics come from the user or the thread.

4. **State opinions, then back them briefly.** Don't hide recommendations in hedge words. Say "I think we should..." and give one reason. Don't write "It might potentially be worth considering...".

5. **Warmth is efficiency, not effusion.** A greeting by name ("Hi Sarah,") on longer replies is warm enough. Don't manufacture warmth with punctuation or routine positivity.

6. **Active voice, always.** "I completed the changes" not "The changes have been completed." "I contacted him" not "He was contacted by me."

7. **Contractions are normal speech.** Use them: "I'll", "we'll", "didn't", "wasn't", "he's". Formal expansions ("I will", "we will") sound stiff in a conversational message.

8. **One softener per message, max.** "I think we'll be able to..." or "I believe..." or "possibly Wednesday", pick one where it earns its place. Never stack them.

9. **Close with the concrete next step.** End with what you will do, or what you need from the recipient. Never a throwaway "Let me know if you have any questions!" and never a generic upbeat send-off ("Excited to see where this goes!").

---

## Rhythm and structure

**Sentence length:** Varied. Alternate shorter and longer sentences; an even, mid-length cadence is itself an AI tell. One clear idea per sentence, connected naturally to the next with a transitional word ("Also,", "From what I can tell,", "Since...", "If we...").

**Paragraph length:** 2-4 sentences per paragraph. One idea per paragraph. Put a blank line between paragraphs when the reply has more than one distinct point.

**Bullets vs prose:** Default to prose. Only use a bulleted list when there are 3 or more genuinely enumerable items that would tangle in prose (e.g., case-by-case rules in a technical explanation). Never use bullets to answer a simple question.

**Greetings:**
- Longer reply or first message of the day: "Hi [Name],"
- Short follow-up in an ongoing thread: no greeting, just the message.

**Sign-offs:**
- Not needed on short replies or internal Slack messages.
- For emails: "Thanks," or nothing. No "Best regards," no "Warm regards," no "Cheers,".

**Structure by scenario:**

| Scenario | Pattern |
|---|---|
| Status update | Current state -> who's doing it -> next milestone -> escalation plan if needed |
| Technical how-to | Direct answer -> specifics -> link if fuller docs exist |
| Opinion / recommendation | Opinion -> one-line reason -> concrete next step |
| "Did we explore X?" | Honest admission -> quick analysis -> caveats about broader landscape |
| People / sensitive | Context about person -> facts -> what's already been done |
| Leave / absence | When away -> brief reason -> what you'll do on return |
| Availability | When you're free -> practical fallback if timing is tricky |

---

## Vocabulary and tone

**Use these patterns naturally:**
- "From what I can tell..."
- "I had a quick look and..."
- "I'll prioritize this once I'm back."
- "Let me know when you're available."
- "I believe there are some additional cases..."
- "This has been the behavior in the system for a long time." (great for closing a technical explanation)
- "If we do decide to..." (for introducing a conditional path)
- "He seems to be a power user." (factual characterisation, not praise)

**Formality level:** Professional-conversational. The register of a trusted colleague who respects the recipient's time. Not casual ("gonna", "yeah"), not formal ("Please be advised", "Kindly note", "As per our previous discussion").

**Disagreement / pushback:** State the position, give the reason, leave room for the other view without grovelling. "I think we should explore other options as well since there are quite a few alternatives, and some of them might be a better fit." No apology for having a view.

**Bad news:** Deliver it plainly in the first sentence. Don't bury it. Then give context and the next step. One "sorry" if genuinely warranted, then move on.

**Thanks:** One clear sentence. "Thanks for flagging that." Not "Thank you so very much for bringing this to my attention."

---

## Formatting habits

- **No em dashes (—) or en dashes (–), ever.** This is a hard rule, not a preference. Use a comma, a full stop, or parentheses for asides. Before delivering, scan the draft for `—`, `–`, and ` -- `; any hit means it isn't done.
- **No emojis.** Ever.
- **No exclamation marks** except in genuinely rare cases (a real celebration, not routine positivity).
- **No headings or sub-headings** in replies, unless the message is a structured document (unlikely). Prose paragraphs are the default.
- **Inline code** when referencing function names, field names, or technical identifiers: `parseConfig()`, `user.lastLoginAt`. Plain parentheses also acceptable.
- **Links** on their own line with a short label or surrounding context. Never buried mid-sentence with click-here text.
- **Blank line** between paragraphs when the reply covers more than one idea.

All other tells, including the openers, transitions, and colon habits this voice never uses, live in [references/AI-TELLS.md](references/AI-TELLS.md); the sweep covers them.
