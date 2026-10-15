---
name: teams-hands-free
description: Microsoft Teams chat from the terminal — message, send a file to, ping, tell, reply to, or check what someone said, in a 1:1 or group chat, as the user on their personal Teams account (teams.live.com). Use whenever the user mentions Teams or asks to message a colleague or group there.
---

# Teams hands-free

Acts as the user on their **personal** Microsoft Teams account (teams.live.com). Work (organization) accounts are not supported.

> **Warning: unofficial, use at your own risk.** This skill calls Microsoft's private consumer Teams and OneDrive endpoints and signs in with the Teams web app's client id. Microsoft does not document or support this. It may break at any time, and it may conflict with Microsoft's terms of use. Use it only with your own personal account. Tell the user this once before the first sign-in.

Everything runs through one script, Python stdlib only: `${SKILL_DIR}/scripts/teams_chats.py` (below, `teams_chats.py`; `SKILL_DIR` is the folder holding this file). Nothing personal lives in this folder:

| Per-user data | Where |
|---|---|
| Settings: `email`, `draft_with`, `phrasings` (situation → the user's usual wording), `test_chat` (name and id of their test group) | `~/.config/teams-hands-free/config.json` |
| Login | `~/.config/teams-hands-free/credentials.json` (never print it) |
| People list (name → 1:1 chat; fills itself) | `~/.local/share/teams-hands-free/people.json` |

If `config.json` does not exist, copy [config.example.json](config.example.json) there (mode 600) and fill it in with the user. If a command says a setting is missing, ask the user for it and add it to `config.json`.

**Reads are free. Every send waits for the user's OK.** A message they dictate word for word is already OK'd. Anything you write for them: draft it the way `draft_with` in their settings says, starting from their usual wording in `phrasings` when the situation matches (a common way they say it, not a fixed template), then show the recipient, exact text and any file, and wait. When they correct a draft to their usual wording for a recurring situation, offer to add it to `phrasings`. One OK covers one message.

## 1. Session

Run `teams_chats.py status`. Done when it prints `"signed_in": true`. It renews the session on its own from the stored refresh token.

If it says to sign in: run `teams_chats.py login` in the background. Its first output line has `open` (a link), `code` and `account`; give the user the link and code and ask them to approve while signed in as that account. The command finishes by itself once they approve and prints `signed in`.

## 2. Find the chat

`teams_chats.py find <name>` searches named groups (live from Teams) and people (1:1 chats); every word must appear; newest first. Done when you have one chat.

- Several matches → take the top one only when it is clearly the person or group named and the rest are other people or older chats; otherwise ask.
- A person the user has just started chatting with is picked up automatically, named from messages they posted. If they have not posted anywhere yet, the result carries a `note` saying so — tell the user; don't guess another chat.
- Unnamed groups (shown in Teams by member names) and "Unknown User" chats are out of scope.

## 3. Read or send

- Read: `teams_chats.py history <chat-id> --limit <n>`. Each message has `from` (sender id); the user's own sent through this script have an empty `author`. A message with attachments has `files` (name, link).
- Send: `teams_chats.py send <chat-id> "<text>"`, then read the last two messages back to confirm it landed. Plain text only; newlines become line breaks and URLs become clickable links.
- Send a file: `teams_chats.py send-file <chat-id> <path> [--text "<text>"]`, confirmed the same way. Any file type up to 100 MB; it shows as a file card, images too. Like the Teams app, it stores the file in the user's OneDrive (`Microsoft Teams Chat Files`; deleting the message leaves it there) and links it with a view-only link that anyone who has it can open and download without signing in.
- Test: to try anything new or changed (a script fix, a new message format, an edit), use the `test_chat` from settings, never a real person's or team's chat. Test messages there need no OK.

To hold a live back-and-forth conversation with someone (keep replying until they wrap up), read [references/live-conversation.md](references/live-conversation.md) first.

## Limits

- Works for Teams-native chats (`@thread.v2`) and old Skype-style ones (`@thread.skype`, `@p2p.thread.skype`); the script sends the header the Skype-style ones need (`ms-ic3-additional-product: Sfl`; without it the server answers `Invalid ThreadId`).
- It cannot start a chat with someone the user has never chatted with — they start it in the Teams app, then the skill finds it. The self-chat (`48:notes`) fails with `LocationLookupFailed`.
- No search inside messages.
- This uses Microsoft's private chat and OneDrive services, signing in as the Teams web app. It can break without notice.
