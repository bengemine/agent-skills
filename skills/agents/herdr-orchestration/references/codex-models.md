# Codex models & tiers — know these, don't re-research

> **Dated facts.** This table was written on 2026-10-13. On 2026-10-15 the Codex CLI (0.162.1) model list also showed newer models: `gpt-6.1-sol` ("latest workhorse"), `gpt-6-astra` ("frontier intelligence"), and `gpt-6-luna` ("fast and affordable"); it called `gpt-6-sol` the previous generation. Model names change often. If the user's Codex lists different models (`/model` in the Codex TUI), trust that list over this table, and update this file.

Set per launch with `-c` overrides; never mutate the global `~/.codex/config.toml`.

| Name | Model id | Use for | Typical effort |
|---|---|---|---|
| **Sol** | `gpt-6-sol` | Flagship. Ambiguous, consequential, premium work. | **medium** |
| **Terra** | `gpt-5.6-terra` | Everyday reasoning, better cost/speed (~GPT-5.5). | **high–xhigh** |
| **Luna** | `gpt-5.6-luna` | Fastest, cheapest. Clear, repeatable, high-volume. | **high** |

**Reasoning effort** (`-c model_reasoning_effort=`) — all three models support all four levels: **low < medium < high < xhigh** ("Extra High"). Higher = deeper, slower, more usage. Don't default blindly — **reason about the task and pick**: `low` mechanical, `medium` standard, `high` tricky/wide, `xhigh` hardest or most ambiguous. Typical effort above is the starting point, not a rule.

**Service tier** (`-c service_tier=`) — the usage-cost lever. `fast` (Codex Fast mode) = the **priority** lane, ~**2× usage**; use only when the user wants speed and accepts the cost. `default` = standard lane. `flex`/`batch` = cheaper, but `gpt-6-sol` rejects `flex` with a 400 (`Unsupported service_tier: flex`) — use `service_tier=default` for Sol.

**Autonomous launch:**
```
herdr agent start <name> --kind codex --pane <id> -- \
  -c model=gpt-6-sol -c model_reasoning_effort=medium \
  -c service_tier=default -c approval_policy=never
```
`approval_policy=never` → YOLO (no approval prompts, needed unattended). Verify in the TUI header: `model: gpt-6-sol medium`, `permissions: YOLO mode`.
