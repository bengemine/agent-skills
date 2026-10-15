---
name: supervise-agents
description: Supervise long-running agent work through Herdr with one accountable controller, bounded workers, independent verification, and evidence-backed completion. Use when the user asks to babysit or keep watching another agent, orchestrate controller-worker or peer-reviewed work, prevent agent drift, or continue until explicit acceptance criteria pass.
---

# Supervise Agents

Act as the foreman: own the goal and judgment while agents perform bounded work. Before controlling Herdr, read the `herdr-orchestration` and `herdr` skills; they are the single source of truth for CLI mechanics, model choices, context continuity, and tab lifecycle.

## 1. Set the contract

State the goal, checkable acceptance criteria, allowed mutations, forbidden actions, and commit policy. Infer stable facts from available evidence. Ask only when a missing business decision or authority would materially change the outcome.

Done when every required outcome can be marked pass, fail, or blocked from evidence.

## 2. Freeze the baseline

Inspect the worktree, existing agents, relevant artifacts, and available machine resources. Before experiments or refinements, record the starting commit and dirty diff. Create a baseline commit only when the user authorized commits; otherwise preserve a diff or immutable artifact copy. Keep evaluation inputs frozen and separate evaluation from mutation.

Done when the starting state is recoverable and comparisons cannot silently use later edits.

## 3. Assign the smallest useful team

Keep one supervisor accountable for scope, trade-offs, and final judgment. Use a controller only when it reduces coordination work. Give each worker one bounded objective, allowed scope, required evidence, output path, and completion criterion. Add an independent verifier only for consequential or disputed claims.

Use fresh context for independent evaluation. Reuse the same agent for a continuation. Do not create equal peers that endlessly review each other. Do not use a fixed agent count; choose concurrency from task independence and current capacity.

Done when every agent has non-overlapping ownership and a checkable output.

## 4. Dispatch cleanly

Send only the context needed for the assignment. For blind comparisons, hide expected answers, prior diagnoses, and later skill edits. Confirm the prompt arrived, the agent entered working state, and its working directory and permissions match the contract.

Done when each assigned agent is working from the intended inputs with no answer leakage.

## 5. Watch without hovering

Use background status waits so the supervisor remains available to the user. On status changes, inspect the transcript and artifacts. Monitor resource pressure, runtime errors, blocked prompts, incomplete output, and controller context growth. Treat slowness as slowness, not failure. Retry only under a stated health rule; compact a continuing agent before context pressure becomes dangerous.

If resources are insufficient, show the measurements and let the user choose full parallel, a rolling pool, or waves. Never silently reduce the run to painfully small batches.

Done when all required artifacts exist and agents are finished, or a concrete blocker requires the user.

## 6. Judge evidence, not claims

Read the changed files, artifacts, tests, logs, and git state yourself. Resolve conflicting agent conclusions against source evidence. Distinguish a missed issue from a noisy accusation and a runtime failure from ordinary model variance. Require a positive target and a clean control when a rule is meant to catch a class of mistakes without creating noise.

Done when every acceptance criterion has direct evidence and material false positives are accounted for.

## 7. Refine only what earned a change

Apply the smallest correction supported by a reproduced failure. Reject speculative cleanup, broader strictness, duplicated rules, and incident-specific memorization. After a correction, rerun the affected target and a clean control. Preserve the baseline and keep refinements separate so their effect remains attributable.

Done when the correction fixes the demonstrated gap without regressing the control.

## 8. Hand off cleanly

Report the verdict, evidence, remaining uncertainty, artifacts, commits, and uncommitted changes in short concrete language. Never claim perfection or universal coverage. Save resumable session identifiers, then close worker tabs unless the user asked to keep them.

Done when the user can see what passed, what remains, and the exact next decision, if any.

## Guardrails

- A watcher does not take execution ownership unless the user asks or process correction is required.
- Do not commit, stage, push, or publish without authority.
- Do not let an audit modify the subject before its frozen comparison finishes.
- Stop irrelevant, drifting, or duplicate delegated work.
- Keep progress updates brief; escalate only decisions the agents and evidence cannot resolve.
