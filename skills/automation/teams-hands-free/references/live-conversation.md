# Live conversation

For when the user asks you to hold a back-and-forth chat with someone on Teams and keep replying on their behalf. Not for one-off sends.

**Standing OK:** only when the user explicitly gives it, and only for the one chat they named. Then send without showing drafts, and never message any other chat.

**Be open about it.** Unless the user has already told the other person, say in your first message that an AI agent is replying for the user.

**Keep it light.** Do not agree to work tasks, approvals, deadlines, money or decisions on the user's behalf, and share nothing private. If the other person asks for something like that, say you'll check and get back, and flag it to the user at the end.

## Reply fast

The other person is waiting, so every second between their message and yours counts.

- Before the first message, load the voice once (the `draft_with` setting) and keep it in mind. Don't re-read voice files during the chat.
- One tool call per turn. Run `scripts/converse.py` in the **foreground**, never in the background: it returns the moment they reply.
- Keep each reply short and casual, as in chat. Don't deliberate over it.
- `converse.py` shows them "typing…" as soon as their message arrives, so a short think is fine.

## Loop

1. Find the chat (`teams_chats.py find`).
2. `scripts/converse.py say <chat-id> "<text>"` sends your message, then waits. Its first output line confirms the send; the next is their new message(s) as JSON.
3. Reply to everything they sent with `say` again, and repeat.
4. `{"still_waiting": true}` means 9 minutes passed with no reply: run `scripts/converse.py wait <chat-id>` to keep waiting.

Done when they wrap up (bye, ok then, talk later and similar, in whatever language they use): send the closing with `teams_chats.py send`, not `say`, and stop. Also stop on `{"silent_minutes": 60}` (exit code 1). Log each message (local time, who, text) to a file as you go, and add a one-line summary at the end.

## Gotchas

- Never stop a wait with `pkill -f` / `pgrep -f` on a pattern from its command line: it matches your own shell.
- Their messages are tracked by the last one you handled, not by your own last message; if you lose track, delete `~/.local/share/teams-hands-free/converse-*.json` for that chat and `wait` again.
