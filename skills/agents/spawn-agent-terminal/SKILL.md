---
name: spawn-agent-terminal
description: Opens Codex or Claude in a fresh Windows Terminal WSL session with an initial prompt, then leaves a normal Bash shell open after the agent exits. Use when the user asks to spawn, open, or launch an independent Codex or Claude terminal/window/tab with a prompt, or wants autonomous agent windows started from WSL.
---

# Spawn Agent Terminal

Open an independent Codex or Claude session in Windows Terminal from WSL. Use the bundled script so prompts are passed through a temporary WSL script instead of fragile nested terminal quoting.

## Command

Run from the directory where the new agent terminal should start. `<skill-dir>` is the folder holding this file.

```bash
<skill-dir>/scripts/spawn-agent-terminal.sh --agent codex --prompt "<prompt text>"
```

```bash
<skill-dir>/scripts/spawn-agent-terminal.sh --agent claude --prompt "<prompt text>"
```

Optional flags:

- `--cwd <path>`: start directory. Defaults to `$PWD`.
- `--distro <name>`: WSL distro. Defaults to `$SPAWN_AGENT_DISTRO` if set, else the distro the current shell runs in (`$WSL_DISTRO_NAME`), else `Ubuntu`.
- `--title <text>`: Windows Terminal tab title.

## Behavior

- Starts Windows Terminal.
- Starts WSL in the selected distro.
- Opens in the requested working directory.
- Runs `bash -lic` so the normal shell setup loads.
- Starts Codex or Claude with the prompt.
- Runs `exec bash -l` after the agent exits, so the terminal stays open.

## Rules

- Use only `codex` or `claude` for `--agent`.
- Prefer the script over hand-written `wt.exe ... bash -lic "agent ...; exec bash -l"` commands.
- Do not put semicolons, newlines, or the full prompt directly in the `wt.exe` command line.
- Tell the user the spawned window is independent and will not report back automatically.
