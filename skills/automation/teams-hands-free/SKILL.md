---
name: teams-hands-free
description: Microsoft Teams chat from the terminal — message, send a file to, ping, tell, reply to, or check what someone said, in a 1:1 or group chat, as the user on their personal Teams account (default) or their work Teams. Use whenever the user mentions Teams or asks to message a colleague or group there.
---

# Teams hands-free

Acts as the user on Microsoft Teams, on one of two accounts: **personal** (teams.live.com, the default) or **work** (the user's organization account). `--work` anywhere in a `teams_chats.py` or `converse.py` command runs that one command on the work account.

> **Warning: unofficial, use at your own risk.** This skill calls Microsoft's private Teams and OneDrive endpoints and signs in as Microsoft's own Teams apps. Microsoft does not document or support this. It may break at any time, and it may conflict with Microsoft's terms of use. Use it only with your own accounts. On a work account, the organization's IT rules also apply. Tell the user this once before the first sign-in on each account.

Everything runs through one script, Python stdlib only: `${SKILL_DIR}/scripts/teams_chats.py` (below, `teams_chats.py`; `SKILL_DIR` is the folder holding this file). Nothing personal lives in this folder. The settings used below (`draft_with`, `phrasings`, `test_chat`, `work.name`) are in `~/.config/teams-hands-free/config.json`. [references/setup.md](references/setup.md) lists every per-user file and how each is made.

**First use, or a new account:** if `config.json` is missing, a command says a setting is missing, the account has no people index file, or the user adds an account, then follow [references/setup.md](references/setup.md) for that account first.

**Reads are free. Every send waits for the user's OK.** A message they dictate word for word is already OK'd, unless you chose its account yourself (rules 2 and 4 below). Anything you write for them: draft it the way `draft_with` in their settings says, starting from their usual wording in `phrasings` when the situation matches (a common way they say it, not a fixed template), then show the account, recipient, exact text and any file, and wait. When they correct a draft to their usual wording for a recurring situation, offer to add it to `phrasings`. One OK covers one message.

## 1. Account

Pick the account fresh for every message. A switch to work lasts one message; the next one is personal again unless a rule below says otherwise.

1. If the user names the work account (work or office Teams, "the other Teams", or the `work.name` in settings), then use `--work`.
2. If the message follows up the last one sent (same person or group, or "again", "also tell him"), then use that message's account. If the last send is not in this conversation, then run `teams_chats.py last`; it counts only when under 60 minutes old.
3. Otherwise use personal.
4. If `find` finds nobody on the chosen account, then run the same `find` on the other account. If the person is there, then offer that account in the draft.

Done when you know the account for this one message.

## 2. Session

Run `teams_chats.py status` on the chosen account. Done when it prints `"signed_in": true`. It renews the session on its own from the stored refresh token.

If it says to sign in: run `teams_chats.py login` in the background. Its first output line has `open` (a link), `code` and `account`; give the user the link and code and ask them to approve while signed in as that account. The command finishes by itself once they approve and prints `signed in`.

## 3. Find the chat

`teams_chats.py find <name>` searches named groups (live from Teams), people (1:1 chats) and untitled groups (type `untitled group`, named by their members, as Teams shows them); every word must appear; newest first. Done when you have one chat.

- Several matches → take the top one only when it is clearly the person or group named and the rest are other people or older chats; otherwise ask.
- If the result carries a `note` about unnamed chats, or the user says someone is missing, then rebuild the people index (see [references/setup.md](references/setup.md)) and `find` again. If they are still unnamed, then tell the user; don't guess another chat.
- Someone with no known name shows by the readable part of their id (`midhun.mohan_7`), with `name_from_id: true`. If you pick one, then tell the user it was matched by id.
- "Unknown User" chats are out of scope.

## 4. Read or send

- Read: `teams_chats.py history <chat-id> --limit <n>`. Each message has `from` (sender id); the user's own sent through this script have an empty `author`. A message with attachments has `files` (name, link).
- Send: `teams_chats.py send <chat-id> "<text>"`, then read the last two messages back to confirm it landed. Newlines become line breaks, URLs become clickable links, and `**text**` becomes bold. Bold is for the one line the reader must not miss (a caution, a deadline), never decoration. No other formatting.
- Edit: `teams_chats.py edit <chat-id> <message-id> "<text>"` replaces the text of a message the user already sent (the `id` the send printed, or the message id from `history`). Teams marks it Edited; a file card on it stays. Use it to fix or add to a sent message instead of posting it again.
- Send a file: `teams_chats.py send-file <chat-id> <path> [--text "<text>"]`, confirmed the same way. Any file type up to 100 MB; it shows as a file card, images too. Like the Teams app, it stores the file in the user's OneDrive (`Microsoft Teams Chat Files`; deleting the message leaves it there) and links it view-only. On personal, anyone who has the link can open and download it without signing in. On work, only the chat's members can, signed in; someone added to the chat later cannot.
- Test: to try anything new or changed (a script fix, a new message format, an edit), use the `test_chat` from settings (`work.test_chat` on the work account), never a real person's or team's chat. Test messages there need no OK. Test the text only; files go to the real chat once the text is approved.

To hold a live back-and-forth conversation with someone (keep replying until they wrap up), read [references/live-conversation.md](references/live-conversation.md) first.

## Limits

- Works for Teams-native chats (`@thread.v2`, work 1:1 `@unq.gbl.spaces`) and old Skype-style ones (`@thread.skype`, `@p2p.thread.skype`); the script sends the header the Skype-style ones need (`ms-ic3-additional-product: Sfl`; without it the server answers `Invalid ThreadId`).
- It cannot start a chat with someone the user has never chatted with — they start it in the Teams app, then the skill finds it. The personal self-chat (`48:notes`) fails with `LocationLookupFailed`.
- No search inside messages. No work channels (`@thread.tacv2`).
- This uses Microsoft's private chat and OneDrive services, signing in as the Teams web app (work: the Teams desktop app). It can break without notice.
