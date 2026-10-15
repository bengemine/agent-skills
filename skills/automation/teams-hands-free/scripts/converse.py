#!/usr/bin/env python3
"""Fast turn-taking for a live Teams conversation. Run each call in the FOREGROUND.

  converse.py say <chat-id> "<text>"   send, then wait for their reply
  converse.py wait <chat-id>           wait for their next message(s)

Prints their new messages as JSON the moment they arrive (polls every 2 s) and shows
"typing…" to them straight away, so they see a reply is coming. Each call waits at most
9 minutes (under the shell tool's 10-minute cap) and then prints {"still_waiting": true};
call `wait` again. After 60 minutes of silence in total it prints {"silent_minutes": 60}
and exits 1. The last handled message id is kept per chat in
~/.local/share/teams-hands-free/converse-<chat>.json.
"""
import json
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import teams_chats as t

POLL_SECONDS = 2
CALL_LIMIT = 9 * 60
SILENCE_LIMIT = 60 * 60


def state_file(chat_id):
  return t.DATA / f"converse-{chat_id.split(':')[-1].split('@')[0][-24:]}.json"


def theirs(chat_id, me):
  # Matched by sender id: the user's own messages typed in the Teams app carry their name.
  return [m for m in t.messages(chat_id, 25) if m["from"] and m["from"] != me and m["id"].isdigit()]


def typing(chat_id):
  encoded = urllib.parse.quote(chat_id, safe="")
  t.msgapi(f"/users/ME/conversations/{encoded}/messages",
           {"content": "", "messagetype": "Control/Typing", "contenttype": "Application/Message"})


def wait(chat_id):
  me = t.my_id()
  path = state_file(chat_id)
  state = json.loads(path.read_text()) if path.exists() else {}
  if "last" not in state:
    state["last"] = max((int(m["id"]) for m in theirs(chat_id, me)), default=0)
  state.setdefault("silent_since", time.time())
  t.DATA.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(state))
  # Anchored on their last message, not the user's: a reply can land in the same second.
  call_end = time.time() + CALL_LIMIT
  while time.time() < call_end:
    new = sorted((m for m in theirs(chat_id, me) if int(m["id"]) > state["last"]), key=lambda m: int(m["id"]))
    if new:
      typing(chat_id)
      state.update(last=int(new[-1]["id"]), silent_since=time.time())
      path.write_text(json.dumps(state))
      print(json.dumps([{"time": m["timestamp"], "author": m["author"], "content": m["content"]} for m in new]))
      return
    if time.time() - state["silent_since"] > SILENCE_LIMIT:
      path.unlink()
      print(json.dumps({"silent_minutes": SILENCE_LIMIT // 60}))
      sys.exit(1)
    time.sleep(POLL_SECONDS)
  print(json.dumps({"still_waiting": True}))


def main():
  cmd, args = sys.argv[1:2], sys.argv[2:]
  if cmd == ["say"] and len(args) == 2:
    t.send(args[0], args[1])
    path = state_file(args[0])
    if path.exists():
      state = json.loads(path.read_text())
      state["silent_since"] = time.time()
      path.write_text(json.dumps(state))
    wait(args[0])
  elif cmd == ["wait"] and len(args) == 1:
    wait(args[0])
  else:
    sys.exit(__doc__)


if __name__ == "__main__":
  main()
