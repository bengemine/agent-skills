---
name: herdr-orchestration
description: "Drive another coding agent (Claude, Codex, etc.) in a separate Herdr tab or pane, and recall or decide Codex model and tier settings without re-researching. Use when the user says to open or spawn Claude/Codex in another tab, send a prompt to another tab or agent, do part of a job in a separate tab, resume or continue an agent in an existing tab, orchestrate across tabs, or asks which Codex model, reasoning effort, or priority tier to use (Sol/Terra/Luna, low–xhigh, fast/priority vs flex)."
---

# Herdr Orchestration — drive agents in other tabs

> **Keep this skill self-improving.** When a run hits a hiccup this skill should have caught — a new gotcha, a wrong model/tier choice, a missed step — fold the fix back in here so the next run avoids it. Add only a durable lesson that changes behavior, in one place, pruned to the fewest words. Skip the edit otherwise; an unrefined addition is just sediment.

When the user says "open Claude", "open Codex", "send this to another tab", "do part of the job in a separate tab", "resume that tab", or "orchestrate", they mean **driving** another agent through the [Herdr](https://github.com/herdrdev/herdr) CLI, with you as orchestrator. Requires `HERDR_ENV=1`. The raw CLI syntax lives in the **`herdr` skill** that ships with Herdr — read it; this skill adds the recipe, the Codex model facts, and the gotchas.

When the user asks which Codex model, reasoning effort, or service tier to use, answer from [references/codex-models.md](references/codex-models.md).

## Recipe: drive an agent in a tab

1. **Find the target.** `herdr tab list` / `herdr agent list`. Target by agent name or pane id; match an existing tab by its label when the user names one.
2. **Launch only if needed.** `herdr tab create --workspace <ws> --cwd <path> --label "<name>" --no-focus` → read `root_pane.pane_id`. Then `herdr agent start <name> --kind codex|claude --pane <pane_id> [-- <args>]`.
   - Claude workers: launch with `--model opus`. The alias always resolves to the newest Opus, so it cannot go stale the way a pinned id does. Pass **no permission flags**, so workers inherit the user's default permission mode; never `--dangerously-skip-permissions` unless the user explicitly ordered bypass for a specific task. If one goes `blocked` on a permission prompt, read its pane and answer via `send-keys`.
   - Codex workers: read [references/codex-models.md](references/codex-models.md) first for the model, effort and tier flags.
   - A worker that needs a rarely used MCP server: see [references/on-demand-mcps.md](references/on-demand-mcps.md).
   - A launch flag pins the mode (shift+tab won't cycle off bypass); to change it without losing work, exit the TUI and `agent start` again with `-- --resume <agent_session.value from agent list>` — same session, new flags.
   - `herdr agent wait` may report "agent not found" for a few seconds after launch — retry. Wait for `idle` before prompting.
3. **Send, then submit.** `herdr agent prompt <target> "<text>"`. A multi-line prompt only **pastes** (shows `[Pasted text #N]`) and does not send — follow with `herdr agent send-keys <target> Enter` and confirm status went `working`. A Claude worker may treat a long sent prompt as pasted text and stop to ask "run it as written?" — check the pane a few minutes in and answer `yes` when the user authorised the run.
4. **Wait in the background.** Run `herdr agent wait <target> --until idle --until done --until blocked --timeout <ms>` as a background task (e.g. Claude Code `run_in_background`) — a foreground wait blocks the orchestrator and the user's conversation with it. One long wait beats chained short ones. Status **flaps** to done/idle for seconds during subagent handoffs, so a naive wait fires mid-run — re-check after ~30s before believing it. Snapshot long transcripts to a file; uncaptured scrollback is gone.
5. **Judge by artifacts.** Ground truth is files, git status, commits, and the run's output files — never the transcript's own claim of success.

Done when: the target went `idle`/`done`, its artifacts prove the work landed, AND its tab is fully closed (Worker lifecycle below) — unless it is about to be reused or the user said keep it.

## The ghost trap

An idle input shows a greyed, auto-suggested next message — a **ghost**, not text the user typed. It clears the moment anything is typed; only Tab accepts it. Never treat a ghost as a pending prompt or as work you would clobber. Detect it: `herdr agent read <target> --source visible --format ansi` — ghost text carries the dim code `\e[2m` (SGR 2); real text does not.

## Worker lifecycle: fresh by default, fully closed when done

Unrelated task → a fresh agent in a fresh tab, always. Same-task continuation → reuse the live agent and preserve its context; this includes pause/resume, the next workflow phase, and follow-up work on its own output. Start a separate agent only when the task requires independence, such as verification. A finished worker is not done until its tab is **fully closed**: capture `agent_session` from `herdr agent list` (that id recalls the work later via `agent start … -- --resume <id>`), then `herdr tab close <tab_id>` and confirm the tab is gone from `herdr tab list`. Exiting the TUI but leaving the tab open does not count — leftover tabs burn RAM and pile up across orchestrations.

## Context continuity

For the same task, use `/compact`, never `/clear`: wait for `idle`, verify the Ctx counter dropped, then continue. `/clear` erases working memory and is only for deliberately repurposing a tab to an unrelated task; send `Escape` first to drop any ghost or unsubmitted text, then wait for `idle` before prompting. A prompt sent immediately after `/compact`, `/clear`, or `--resume` can be swallowed while context processing runs, or glued onto the command (`/clearThis…` = unknown command) — `wait --until idle` returns at once on an already-idle agent, so before prompting confirm the pane's Ctx counter changed. After any send, confirm delivery by grepping the pane for the prompt's first line — status alone lies; if the pane returns to an empty `❯` without it, re-send. `/model` opens a confirm dialog — follow with `send-keys Enter`. Model and reasoning survive context commands but not a process restart.

## Abort, recovery, load

- **Abort:** `Esc` interrupts only the main agent — its subagents keep burning resources. To truly pause or abort, prompt the agent to stop its own subagents and read back its confirmation; prefer this self-abort over killing the pane.
- **Restart:** a host restart silently kills your background waiters, resets the agent to its default model, and shows a session-resume dialog (Esc for fresh context). Afterward re-check pane state, model, git tree, and leftover artifacts before relaunching. `/tmp` does not survive restarts — keep logs in `~/`.
- **Hibernated tab** (a `💤` label from [herdr-hibernate](https://github.com/bengemine/herdr-hibernate); the pane shows "press Enter to resume"): `agent start` fails with `agent_pane_busy`. Send `C-c` to the pane for a plain shell, then `agent start … -- --model <m> --resume <session>`; the pane stub prints the session id.
- **Load:** peak cost is the count of concurrent live agent tabs plus their MCP servers, not any one run. On a tight machine run sequentially — stacking sessions causes swap thrash → tool-call timeouts → incomplete results, worst case OOM kills.

## Safety

- Target by explicit pane id or agent name, never another client's focused pane.
- Don't close or interrupt tabs you didn't create unless asked. A paused tab (an orchestrator waiting for "resume") is not finished — leave it.
