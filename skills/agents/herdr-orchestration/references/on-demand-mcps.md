# On-demand MCPs — 0 RAM until a worker needs one

Every globally configured MCP boots with every session (~80–150 MB each, per tab, used or not). Keep rarely used MCPs parked in `~/.claude/mcp-ondemand/<name>.json` (a full `{"mcpServers": {...}}` snippet) instead of the global config. Park one: save its entry to that file, then `claude mcp remove <name> -s user`.

To spawn a Claude worker WITH a parked MCP, add the flag at launch:

```
herdr agent start <name> --kind claude --pane <id> -- --mcp-config ~/.claude/mcp-ondemand/<mcp>.json
```

Space-separate several files after one `--mcp-config`. Scope: only that session loads the server, and it dies with the session. Gotcha: `-p` one-shot runs exit before the MCP finishes connecting — on-demand MCPs are for interactive sessions only. What's parked: `ls ~/.claude/mcp-ondemand/`.
