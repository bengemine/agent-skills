# AI tells

Sweep every outbound draft against each numbered tell below before delivering. A tell survives the sweep only if the recipient would genuinely write it that way themselves. Adapted from [blader/humanizer](https://github.com/blader/humanizer) (based on Wikipedia's "Signs of AI writing") and [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop). Em dashes, emojis, exclamation marks, passive voice, stacked hedges, and closing habits are governed by SKILL.md; this file holds everything else.

## Wording tells

1. **AI vocabulary.** Watch for: additionally, delve, leverage, robust, seamless, streamline, crucial, pivotal, vital, key (as adjective), enhance, foster, garner, utilize, facilitate, empower, harness, elevate, embark, supercharge, transformative, cutting-edge, ever-evolving, game changer, paradigm shift, underscore, highlight (as verbs), showcase, testament, landscape, tapestry or realm (abstract), vibrant, comprehensive, intricate, meticulous, paramount, multifaceted, align with, "I'd be happy to". Swap each for the plain word. One of these is fine; a cluster is a confession.
   - Before: "Additionally, this will significantly enhance our onboarding landscape."
   - After: "This will also make onboarding easier."

2. **Copula avoidance.** "Serves as", "stands as", "represents", "boasts", "features", "offers" where plain "is" or "has" works.
   - Before: "The portal serves as the entry point and boasts single sign-on."
   - After: "The portal is the entry point and has single sign-on."

3. **Fake-depth participles.** An "-ing" phrase tacked onto a sentence to add unearned significance. Cut it, or promote it to a real clause with a subject.
   - Before: "I've updated the config, ensuring the jobs run nightly, reflecting our reliability goals."
   - After: "I've updated the config so the jobs run nightly."

4. **Inflated significance.** "Plays a crucial role", "marks a pivotal step", "underscores the importance of". State what happened and let the reader judge the weight.
   - Before: "This fix plays a crucial role in stabilizing the release."
   - After: "This fix stops the crash that was blocking the release."

5. **Filler phrases.** "In order to" -> "to"; "due to the fact that" -> "because"; "at this point in time" -> "now"; "in the event that" -> "if"; "has the ability to" -> "can"; "when it comes to X" -> "for X"; "it is important to note that" -> cut it and just say the thing.

6. **Vague attributions.** "Experts say", "several people have mentioned", "there are concerns", with no actual source. Name the real source or drop the claim. Never invent a source to make a sentence sound backed.
   - Before: "Several people have raised concerns about the deploy process."
   - After: "Mark raised a concern about the deploy process yesterday."

## Structure tells

7. **Negative parallelism and tailing negations.** "It's not just X, it's Y", "This isn't about A, it's about B", "Not a X. Not a Y. A Z.", and clipped fragments hung off a sentence: "..., no guessing.", "..., no wasted motion." Write the plain claim, or make the negation a real clause.
   - Before: "This isn't just a bug fix, it's a redesign of the retry logic. No more guesswork."
   - After: "It fixes the bug and also redesigns the retry logic, so we no longer have to guess which job failed."

8. **Rule of three.** Forcing ideas into triads to sound complete. Two items or four are fine; keep only the items that matter.
   - Before: "The new flow is faster, cleaner, and more reliable."
   - After: "The new flow is faster and fails less often."

9. **False ranges.** "From X to Y" where X and Y aren't on a real scale.
   - Before: "This covers everything from onboarding to analytics to support."
   - After: "This covers onboarding and analytics. Support is out of scope for now."

10. **Synonym cycling.** Rotating "the ticket / the issue / the item / the request" for the same thing to avoid repetition. Repeating the natural word is what humans do.
    - Before: "The ticket is blocked. The issue needs sign-off before the item can move."
    - After: "The ticket is blocked until someone signs off on it."

11. **Staccato drama.** A run of clipped fragments for punch. One short sentence for emphasis is human; a stack of them is engineered.
    - Before: "No config. No setup. Just results."
    - After: "It works without any configuration or setup."

12. **Aphorism formulas.** "X is the Y of Z", "X isn't a tool, it's a mirror", "the currency of", "the architecture of". Replace the formula with the concrete claim it gestures at.
    - Before: "Documentation is the currency of trust."
    - After: "Good docs mean fewer questions later."

13. **Fake-profound kickers.** A final "deep" line that turns the point into a metaphor, aphorism, or mic-drop sentence. Delete it; do not rewrite it into a better metaphor and do not preserve the rhythm. End on the clearest concrete sentence already in the draft, or add a plain next step if the ending needs closure.
    - Before: "...so the fix is deployed. In the end, reliability isn't a feature. It's a promise."
    - After: "...so the fix is deployed. I'll monitor the logs overnight and confirm tomorrow."

14. **Bold decoration.** Mechanical **bolding** of phrases, and bullet lists shaped "**Header:** sentence that restates the header". In a message, write plain prose.

15. **Uniform hyphenation.** AI hyphenates compound pairs everywhere, including after the noun. Keep the hyphen when attributive, drop it in predicate position.
    - Before: "It was a high-quality report. The report is high-quality."
    - After: "It was a high-quality report. The report is high quality."

## Register tells

16. **Chat artifacts and flattery.** "Great question!", "You're absolutely right", "I hope this helps", "Happy to help!", "Would you like me to...", "Should I go ahead and...". These are chatbot correspondence, not a colleague's message. Cut them; answer the question instead.

17. **Announcing instead of doing.** "Let's dive in", "Here's what you need to know", "To break this down", "Without further ado". Start with the content; the reader doesn't need a trailer.
    - Before: "Here's what you need to know about the outage."
    - After: "The outage was caused by an expired certificate on the load balancer."

18. **Authority tropes.** "The real question is", "at its core", "what really matters", "fundamentally", "the heart of the matter". These pretend to cut through noise, then restate an ordinary point with ceremony.
    - Before: "At its core, what really matters is adoption."
    - After: "Whether people actually use it is what matters."

19. **Faux-insight setups.** "What most people get wrong", "Here's what nobody tells you", "The part everyone misses". These stage the writer as the lone expert. Cut the setup and let the claim stand on its own.
    - Before: "The part everyone misses: the cache is never invalidated."
    - After: "The cache is never invalidated, which is why the old values keep showing."

20. **Rhetorical setups.** "What if I told you...", "Think about it:", "Plot twist:", and self-answered "Question? Answer." pairs. Drop the staging and make the point.
    - Before: "Why does the import fail? Because the file is locked. What can we do? Retry after the sync."
    - After: "The import fails because the file is locked, so we should retry after the sync."

21. **Fake candor.** A standalone "Honestly?", "Look,", "Here's the thing", or "Let's be honest" staged as a pause before an ordinary point. A person being honest just says the thing. Mid-sentence "honestly" in casual writing is fine.
    - Before: "Honestly? I think we should wait for the next release."
    - After: "I think we should wait for the next release."

## Tells specific to this voice

Habits this voice never uses, beyond the generic tells above.

22. **Filler openers.** "Quick one.", "Quick question.", "QQ", "Heads up.", "Just a quick note.", "FYI", "Hey all, quick one." Cut these entirely. Open with the actual point. If a soft entry is needed, let the first real sentence do the work.

23. **Telegraphic openers (dropped subject + vague quantifier).** "Collecting some feedback on...", "Doing a quick review of...", "Running some tests on..." These read like Slack channel headlines, not how a person speaks. Lead with the full subject and the actual purpose: "I'm collecting feedback on X to see how it's holding up", "I'm reviewing Y because Z". Keep "I'm" / "I've" / "We're" in the opener and keep the "why" clause attached. Don't strip a sentence into a label to sound efficient, it sounds robotic.

24. **Mechanical labels in prose.** "Two columns only:", "Three things:", "Four points to consider:" sound like slide bullets, not human writing. Either fold the count into a natural sentence ("There are two columns, one for...") or drop the count and use a real list. Don't announce structure with a colon-tag.

25. **Robotic transitions.** "No pressure on length, even one line helps." reads like a form letter. Say the same thing as a person would: "Even a line or two is fine."

26. **Summary wrappers and recap endings.** "To sum it up,...", "In summary,...", "In conclusion,...", "To wrap up,...", "Long story short,...", "All in all,...", "At the end of the day,...", "Bottom line,..." Never open a closing line with one of these, and never end with a paragraph that restates what the message already said. The reader was just there. If a final point is worth making, state it directly ("So we still need to rotate the keys, but this file isn't where they leaked.") or end on the concrete next step.

27. **Setup-phrase-then-colon.** "The idea is simple: ...", "The goal is this: ...", "Here's the plan: ...", "The point is: ...", "It works like this: ...", "What we want is simple: ...", and colon reveals like "The best part: it learns." Never set up a sentence with a short phrase and a colon to announce what's coming. Just say the thing in a normal sentence. Instead of "The idea is simple: we want to use AI more", write "What we want to do is use AI more in our daily work." This applies everywhere, in any message, not just openers. No colon that introduces or builds up to the real content. A colon to join a label to a value in a real list is fine, but never in flowing prose.

## The human touch

Scrubbing tells is only half the job. A message can pass every check above and still read like a machine wrote it, because sterile, voiceless correctness is itself a tell. A real message has a person behind it:

- **Have a stance.** Say what you think and how sure you are: "I think option B is better, though I haven't tested it under load." Not a neutral survey of options.
- **Allow mixed feelings.** "This mostly works, but the retry logic still bothers me" is more human than a clean take. Don't resolve tension the user hasn't resolved.
- **Leave the rhythm uneven.** Don't polish every sentence to the same smoothness. A slightly lopsided paragraph reads as written, not generated.
- **Keep specifics.** "The job that failed Tuesday night" beats "a recent failure". Humans hoard concrete detail; AI rounds it off.
- **Small asides are fine** in parentheses, when they'd genuinely occur to the user (see worked example 2 in EXAMPLES.md).

Personality comes from stance, rhythm, and specifics that are already true. Never invent facts, events, or feelings the user doesn't have to manufacture it.

## Don't over-scrub

Signs of a human writing; deleting them makes a draft more AI-like, not less:

- Specific, hard-to-fabricate detail.
- One clipped sentence used for emphasis.
- Honest hedging on a genuinely uncertain point.
- Natural asides, parentheticals, and self-corrections.
- Ordinary transition words used once. A single "however" or "also" is not a tell; only clusters are.
- Natural spoken softeners in their place: "just checking in", "I had a quick look". These are this voice, not filler.

Never rewrite a watched phrase inside a quotation or a proper name, and never fabricate a specific to replace a vague sentence (see SKILL.md, principle 3).

The sweep is complete only when every numbered tell has been checked against the draft and no hits remain.
