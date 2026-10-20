# Setup and per-user files

The skill folder holds only instructions and scripts. Everything about one person lives under their home, in the files below. Each file is made by a setup step or by the scripts themselves. Add `--work` to a command to run it on the work account.

| File | What it holds | How it is made |
|---|---|---|
| `~/.config/teams-hands-free/config.json` (mode 600) | Settings: `email`, `draft_with`, `phrasings`, `test_chat`; under `work`: `email`, `name`, `test_chat` | Steps 1 and 3 |
| `~/.config/teams-hands-free/credentials.json`, work: `work-credentials.json` | Login. Never print them. | Step 2 |
| `~/.local/share/teams-hands-free/people.json`, work: `work-people.json` | People index (below) | Step 4, then `find` |
| `~/.local/share/teams-hands-free/last-send.json` | Last chat sent to, on either account (`teams_chats.py last`) | Each send |
| `~/.local/share/teams-hands-free/converse-*.json` | Last message handled in a live conversation | `converse.py` |

## Setup steps

Run once per person, and again for any account they add later. Skip a step whose result already exists.

1. **Settings.** If `config.json` is missing, then copy [config.example.json](../config.example.json) there with mode 600. Fill in each value with the user:
   - `email`: their personal Microsoft account.
   - `draft_with`: how to write messages for them. This is a writing-voice skill to load, or `plain`.
   - `phrasings`: start as `{}`. It fills as they correct drafts.
   - `work`: only if they also use a work (organization) Teams account. It holds `email`, and `name`: what they call that account, usually the company name. If they have none, then remove `work`.

   Done when every account they use has its `email`, and `draft_with` and `phrasings` exist.
2. **Sign in.** Run `teams_chats.py login` in the background, as in SKILL.md step 2. Some organizations block this kind of sign-in. If the approval page shows an error, then tell the user the work account cannot be used, and remove `work` from the settings. Done when `teams_chats.py status` prints `"signed_in": true`.
3. **Test chat.** Run `teams_chats.py new-test-chat`. It makes a group named "test conv" with only the user in it. Save its output (`name`, `id`) as `test_chat`, or `work.test_chat` for the work account. Done when that setting holds the chat's name and id.
4. **People index.** Run `teams_chats.py index` in the background, and tell the user it takes minutes. Done when the account's index file exists.

Setup is done when every account the user uses has passed all four steps.

## People index

Teams' chat list gives no name for a 1:1 chat or an untitled group. So each account keeps a local index of who each 1:1 chat is with, who is in each untitled group, and everyone's name. `find` cannot name a chat without it.

- Build or rebuild: `teams_chats.py index`, in the background. It reads every chat once and takes names from messages and "added to chat" notices. Work takes about 3 minutes, personal about 25. It prints how many people still have no name.
- Kept current: every `find` adds chats that are new since the last run. A new person gets a name only from messages in their own chat; anyone else waits for the next rebuild.
- Rebuild when `find` reports unnamed chats, or when a group's members look out of date.
- Deleting an index file changes nothing in Teams; a rebuild restores it.
