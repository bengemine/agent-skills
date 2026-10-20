#!/usr/bin/env python3
"""Sign in to, find, read and send to the user's Teams chats. Python stdlib only.

Each command runs on the personal account (teams.live.com), or on the work account
(an organization account) when --work is anywhere in the command.

Nothing personal lives in the skill folder. Per-user settings are in
~/.config/teams-hands-free/config.json (email, draft_with; the work account's under "work");
the logins and the people lists live under the user's home too.

Groups are found live by name. 1:1 chats have no name in Teams' chat list, so a
people list (name -> 1:1 chat) is kept and fills itself: a chat it has not seen is
named from messages the other person posted, there or in any other chat.

  teams_chats.py login                  device-code sign-in (run in background; prints a link and code)
  teams_chats.py status                 signed in? renews the session token if it is close to expiry
  teams_chats.py find <name>            groups and people; newest first
  teams_chats.py history <chat-id> [--limit N]
  teams_chats.py send <chat-id> <text>
  teams_chats.py send-file <chat-id> <path> [--text <text>]
  teams_chats.py edit <chat-id> <message-id> <text>
  teams_chats.py last                   the last chat sent to, on either account
  teams_chats.py index                  builds or refreshes the people index from every chat (slow)
  teams_chats.py new-test-chat          makes a "test conv" group with only the user in it; prints its id
"""
import html
import json
import os
import base64
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Read at import so converse.py, which imports this file, takes the same flag.
WORK = "--work" in sys.argv
if WORK:
  sys.argv.remove("--work")
ACCOUNT = "work" if WORK else "personal"
PREFIX = "work-" if WORK else ""

DATA = Path.home() / ".local/share/teams-hands-free"
PEOPLE = DATA / f"{PREFIX}people.json"
LAST_SEND = DATA / "last-send.json"
CREDS = Path.home() / f".config/teams-hands-free/{PREFIX}credentials.json"
CONFIG = Path.home() / ".config/teams-hands-free/config.json"
MSGAPI = "https://msgapi.teams.live.com/v1"  # the work account's server comes with its session token
READABLE_SUFFIXES = ("@thread.v2", "@thread.skype", "@p2p.thread.skype", "@unq.gbl.spaces")
ONE_ON_ONE = ("19:uni01_",)
WORK_ONE_ON_ONE = "@unq.gbl.spaces"  # 19:<user id>_<user id>@unq.gbl.spaces
USER_MESSAGE_TYPES = {"Text", "RichText", "RichText/Html", "RichText/Media_CallRecording"}

# Sign-in, as the Teams apps do it: device code -> refresh token -> token for the Skype chat
# service -> session ("skype") token that every chat call sends.
if WORK:
  CLIENT_ID = "1fec8e78-bce4-4aaf-ab1b-5451cc387264"  # Microsoft's Teams desktop app
  LOGIN = "https://login.microsoftonline.com/organizations/oauth2/v2.0"
  TEAMS_SCOPE = SKYPE_SCOPE = "https://api.spaces.skype.com/.default openid profile offline_access"
  AUTHZ = "https://teams.microsoft.com/api/authsvc/v1.0/authz"
else:
  CLIENT_ID = "5e3ce6c0-2b1f-4285-8d4b-75ee78787346"  # Microsoft's Teams web app
  LOGIN = "https://login.microsoftonline.com/9188040d-6c67-4c5b-b112-36a304b66dad/oauth2/v2.0"
  TEAMS_SCOPE = "service::api.fl.teams.microsoft.com::MBI_SSL openid profile offline_access"
  SKYPE_SCOPE = "service::api.fl.spaces.skype.com::MBI_SSL openid profile offline_access"
  AUTHZ = "https://teams.live.com/api/auth/v1.0/authz/consumer"
RENEW_BEFORE = 300
SIGN_IN = f"Run: teams_chats.py{' --work' if WORK else ''} login"

# Files go where the Teams app puts them: the sender's OneDrive, through its consumer API
# ("Vroom"), with the scope and auth scheme the Teams web app's own config names. The work
# account's OneDrive is reached through Microsoft Graph.
if WORK:
  ONEDRIVE, ONEDRIVE_SCOPE = "https://graph.microsoft.com/v1.0/me", "https://graph.microsoft.com/.default openid profile offline_access"
else:
  ONEDRIVE, ONEDRIVE_SCOPE = "https://api.onedrive.com/v1.0", "service::lw.onedrive.com::MBI_SSL openid profile offline_access"
CHAT_FILES = "Microsoft Teams Chat Files"
PERSONAL_CONTENT = "https://my.microsoftpersonalcontent.com/personal"
MAX_FILE_MB = 100


def http(url, data=None, headers=None, form=False, method=None, timeout=40):
  """Returns (status, parsed JSON body). data is raw bytes, or a dict sent as a form or as JSON."""
  body = None
  headers = dict(headers or {})
  if isinstance(data, bytes):
    body = data
    headers["Content-Type"] = "application/octet-stream"
  elif data is not None:
    if form:
      body = urllib.parse.urlencode(data).encode()
      headers["Content-Type"] = "application/x-www-form-urlencoded"
    else:
      body = json.dumps(data).encode()
      headers["Content-Type"] = "application/json"
  request = urllib.request.Request(url, data=body, headers=headers, method=method or ("POST" if body is not None else "GET"))
  try:
    with urllib.request.urlopen(request, timeout=timeout) as response:
      raw = response.read().decode()
      return response.status, json.loads(raw) if raw else {}
  except urllib.error.HTTPError as error:
    raw = error.read().decode()
    try:
      return error.code, json.loads(raw) if raw else {}
    except ValueError:
      return error.code, {"message": raw[:200]}


def setting(key):
  config = json.loads(CONFIG.read_text()) if CONFIG.exists() else {}
  if WORK:
    config = config.get("work") or {}
  if not config.get(key):
    sys.exit(f"Missing '{key}'{' under work' if WORK else ''} in {CONFIG}. Ask the user for it and add it.")
  return config[key]




# ---------- sign-in ----------

def save_creds(creds):
  CREDS.parent.mkdir(parents=True, exist_ok=True)
  os.chmod(CREDS.parent, 0o700)
  tmp = CREDS.with_suffix(".tmp")
  tmp.write_text(json.dumps(creds, indent=1))
  os.chmod(tmp, 0o600)
  tmp.replace(CREDS)


def redeem(refresh_token, scope):
  return http(f"{LOGIN}/token", {"client_id": CLIENT_ID, "grant_type": "refresh_token",
                                 "refresh_token": refresh_token, "scope": scope}, form=True)


def mint(refresh_token):
  """Refresh token -> new session token. Saves and returns the credentials."""
  status, body = redeem(refresh_token, SKYPE_SCOPE)
  if status != 200:
    sys.exit(f"Sign-in renewal failed ({body.get('error', status)}). {SIGN_IN}")
  status, authz = http(AUTHZ, {}, {"Authorization": f"Bearer {body['access_token']}", "Accept": "application/json; ver=1.0"})
  if WORK:
    token, ttl = (authz.get("tokens") or {}).get("skypeToken"), (authz.get("tokens") or {}).get("expiresIn")
  else:
    token, ttl = (authz.get("skypeToken") or {}).get("skypetoken"), (authz.get("skypeToken") or {}).get("skypeTokenExpiresIn")
  if status != 200 or not token:
    sys.exit(f"Could not get a Teams session token (HTTP {status}). {SIGN_IN}")
  creds = {"refresh_token": body.get("refresh_token") or refresh_token,
           "skype_token": token, "expires_at": int(time.time()) + int(ttl or 21600)}
  if WORK:
    creds["msgapi"] = authz["regionGtms"]["chatService"] + "/v1"
  save_creds(creds)
  return creds


def skype_token():
  if not CREDS.exists():
    sys.exit(f"Not signed in. {SIGN_IN}")
  creds = json.loads(CREDS.read_text())
  if creds["expires_at"] - time.time() < RENEW_BEFORE:
    creds = mint(creds["refresh_token"])
  return creds["skype_token"]


def onedrive_token():
  """A fresh OneDrive token from the same login; it is not stored."""
  skype_token()
  creds = json.loads(CREDS.read_text())
  status, body = redeem(creds["refresh_token"], ONEDRIVE_SCOPE)
  if status != 200:
    sys.exit(f"Could not get a OneDrive token ({body.get('error', status)}). {SIGN_IN}")
  creds["refresh_token"] = body.get("refresh_token") or creds["refresh_token"]
  save_creds(creds)
  return body["access_token"]


def my_id():
  claims = skype_token().split(".")[1]
  claims += "=" * (-len(claims) % 4)
  return "8:" + json.loads(base64.urlsafe_b64decode(claims))["skypeid"]


def login():
  status, code = http(f"{LOGIN}/devicecode", {"client_id": CLIENT_ID, "scope": TEAMS_SCOPE}, form=True)
  if status != 200:
    sys.exit(f"Device code request failed: {code.get('error_description', status)}")
  print(json.dumps({"open": f"{code['verification_uri']}?otc={code['user_code']}", "code": code["user_code"],
                    "account": setting("email")}), flush=True)
  wait = int(code.get("interval", 5))
  deadline = time.time() + int(code.get("expires_in", 900))
  while time.time() < deadline:
    time.sleep(wait)
    status, body = http(f"{LOGIN}/token", {"client_id": CLIENT_ID, "device_code": code["device_code"],
                                           "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}, form=True)
    if status == 200:
      mint(body["refresh_token"])
      print("signed in")
      return
    error = body.get("error")
    if error == "slow_down":
      wait += 5
    elif error == "expired_token":
      break
    elif error != "authorization_pending":
      sys.exit(f"Sign-in failed: {error or status}")
  sys.exit("Sign-in code expired before approval.")


def show_status():
  token = skype_token()
  creds = json.loads(CREDS.read_text())
  left = int((creds["expires_at"] - time.time()) / 60)
  print(json.dumps({"signed_in": bool(token), "session_minutes_left": left}))


# ---------- chat service ----------

def chat_headers():
  token = skype_token()
  if WORK:
    return {"Authentication": f"skypetoken={token}", "X-Skypetoken": token, "Accept": "application/json"}
  # The ms-ic3 header makes old Skype-style chats readable; normal Teams chats accept it too.
  return {"X-Skypetoken": token, "ms-ic3-additional-product": "Sfl", "Accept": "application/json"}


def chat_url(path):
  """Call after chat_headers(): a renewed work session can move to another server."""
  return (json.loads(CREDS.read_text())["msgapi"] if WORK else MSGAPI) + path


def msgapi(path, body=None, method=None):
  headers = chat_headers()
  status, data = http(chat_url(path), body, headers, method=method)
  if status >= 400:
    sys.exit(f"Teams call failed: {data.get('message') or f'HTTP {status}'}")
  return data


def readable(chat_id):
  return chat_id.endswith(READABLE_SUFFIXES)


def strip_html(content):
  if not content:
    return ""
  text = content
  for tag in ("<br>", "<br/>", "<br />", "</p>", "</div>"):
    text = text.replace(tag, "\n")
  out = []
  skip = False
  for ch in text:
    if ch == "<":
      skip = True
    elif ch == ">":
      skip = False
    elif not skip:
      out.append(ch)
  text = html.unescape("".join(out))
  return "\n".join(line.strip() for line in text.splitlines()).strip()


def attached_files(msg):
  raw = (msg.get("properties") or {}).get("files") or "[]"
  try:
    files = json.loads(raw) if isinstance(raw, str) else raw
  except ValueError:
    return []
  return [{"name": f.get("fileName") or f.get("title") or "",
           "url": (f.get("fileInfo") or {}).get("shareUrl") or f.get("objectUrl") or ""} for f in files]


def messages(chat_id, limit):
  encoded = urllib.parse.quote(chat_id, safe="")
  data = msgapi(f"/users/ME/conversations/{encoded}/messages?startTime=0&view=msnp24Equivalent&pageSize={limit}")
  out = []
  for msg in data.get("messages") or []:
    if msg.get("messagetype") and msg["messagetype"] not in USER_MESSAGE_TYPES:
      continue
    entry = {"id": msg.get("id") or "", "author": msg.get("imdisplayname") or "",
             "from": (msg.get("from") or "").rsplit("/", 1)[-1],
             "content": strip_html(msg.get("content")),
             "timestamp": msg.get("composetime") or msg.get("originalarrivaltime") or ""}
    files = attached_files(msg)
    if files:
      entry["files"] = files
    out.append(entry)
  return out[:limit]


def each_conversation():
  path = "/users/ME/conversations?view=msnp24Equivalent&pageSize=500"
  for _ in range(8):
    data = msgapi(path)
    yield from data.get("conversations") or []
    link = urllib.parse.urlparse((data.get("_metadata") or {}).get("backwardLink") or "")
    base = urllib.parse.urlparse(chat_url(""))
    if link.netloc != base.netloc:
      return
    path = link.path.removeprefix(base.path) + "?" + link.query


# ---------- people and groups ----------

def is_one_on_one(chat_id):
  return chat_id.startswith(ONE_ON_ONE) or chat_id.endswith(("@p2p.thread.skype", WORK_ONE_ON_ONE))


def load_people():
  data = json.loads(PEOPLE.read_text()) if PEOPLE.exists() else {}
  return {"chats": data.get("chats", {}), "names": data.get("names", {}), "groups": data.get("groups", {})}


def save_people(people):
  DATA.mkdir(parents=True, exist_ok=True)
  PEOPLE.write_text(json.dumps(people, indent=1))


def other_members(chat_id, me):
  if chat_id.endswith(WORK_ONE_ON_ONE):
    return [f"8:orgid:{user}" for user in chat_id[3:].split("@")[0].split("_") if f"8:orgid:{user}" != me]
  encoded = urllib.parse.quote(chat_id, safe="")
  for attempt in range(4):
    headers = chat_headers()
    status, thread = http(chat_url(f"/threads/{encoded}?view=msnp24Equivalent"), headers=headers)
    if status == 200:
      return [m["id"] for m in thread.get("members") or [] if m["id"] != me and m["id"].startswith("8:")]
    time.sleep(2 * (attempt + 1))
  return []


def untitled_group(conv):
  return not is_one_on_one(conv["id"]) and readable(conv["id"]) and not (conv.get("threadProperties") or {}).get("topic")


MEMBER_NAME = re.compile(r"<id>(8:[^<]+)</id>\s*<friendlyName>([^<]+)</friendlyName>")


def learn_names(people, chat_id):
  """Records the name of everyone who posted or was added recently in this chat."""
  encoded = urllib.parse.quote(chat_id, safe="")
  headers = chat_headers()
  status, data = http(chat_url(f"/users/ME/conversations/{encoded}/messages?startTime=0&view=msnp24Equivalent&pageSize=100"),
                      headers=headers)
  for msg in data.get("messages") or [] if status == 200 else []:
    sender = (msg.get("from") or "").rsplit("/", 1)[-1]
    if sender and msg.get("imdisplayname"):
      people["names"][sender] = msg["imdisplayname"]
    # "Added to the chat" notices name people who never posted.
    for member, name in MEMBER_NAME.findall(msg.get("content") or ""):
      people["names"].setdefault(member, html.unescape(name))


def learn_new_chats(people, conversations):
  """Adds 1:1 chats and untitled groups not seen before. Returns the 1:1 chats whose person still has no name."""
  me = my_id()
  unnamed = []
  for conv in conversations:
    chat_id = conv["id"]
    if untitled_group(conv) and chat_id not in people["groups"]:
      # Named in Teams by its members, so kept with its members' ids.
      people["groups"][chat_id] = other_members(chat_id, me)
      if any(member not in people["names"] for member in people["groups"][chat_id]):
        learn_names(people, chat_id)
    if not is_one_on_one(chat_id) or chat_id in people["chats"]:
      continue
    person = next(iter(other_members(chat_id, me)), None)
    # Saved even when empty (only the user is left), so the chat is not checked again.
    people["chats"][chat_id] = person
    if not person:
      continue
    if person not in people["names"]:
      learn_names(people, chat_id)
    if person not in people["names"]:
      unnamed.append(chat_id)
  save_people(people)
  return unnamed


def id_name(person):
  """The readable part of a Skype-style id (8:live:midhun.mohan_7 -> midhun.mohan_7), for someone with no
  known name. Work ids are bare numbers, so they give none."""
  if not person or not person.startswith("8:") or person.startswith("8:orgid:"):
    return None
  return person.removeprefix("8:").removeprefix("live:")


def last_activity(conv):
  last = conv.get("lastMessage") or {}
  return last.get("composetime") or last.get("originalarrivaltime") or ""


def find(query):
  words = query.lower().split()
  matches = lambda name: name and all(w in name.lower() for w in words)
  conversations = list(each_conversation())
  people = load_people()
  unnamed = learn_new_chats(people, conversations)
  hits = []
  for conv in conversations:
    chat_id = conv["id"]
    topic = (conv.get("threadProperties") or {}).get("topic")
    if topic and not is_one_on_one(chat_id) and matches(topic):
      hits.append({"name": topic, "type": "group", "id": chat_id, "last": last_activity(conv)})
    elif is_one_on_one(chat_id):
      person = people["chats"].get(chat_id)
      name = people["names"].get(person) or id_name(person)
      if matches(name):
        hit = {"name": name, "type": "person", "id": chat_id, "last": last_activity(conv)}
        if person not in people["names"]:
          hit["name_from_id"] = True
        hits.append(hit)
    elif people["groups"].get(chat_id):
      known = [n for n in (people["names"].get(m) or id_name(m) for m in people["groups"][chat_id]) if n]
      unknown = len(people["groups"][chat_id]) - len(known)
      name = ", ".join(known + ([f"{unknown} more"] if unknown else []))
      if known and matches(name):
        hits.append({"name": name, "type": "untitled group", "id": chat_id, "last": last_activity(conv)})
  hits.sort(key=lambda c: c["last"], reverse=True)
  result = {"matches": hits}
  if not hits and unnamed:
    result["note"] = (f"{len(unnamed)} 1:1 chat(s) have no name yet. `index` reads every chat for names; "
                      "if that leaves them unnamed, their names appear once they post.")
  print(json.dumps(result, indent=1))


def index():
  """Reads every chat once to name everyone the user can see and refresh untitled groups' members. Slow (minutes)."""
  conversations = list(each_conversation())
  people = load_people()
  people["groups"] = {}  # re-read, in case members changed
  learn_new_chats(people, conversations)
  for conv in conversations:
    if conv["id"].startswith("19:"):
      learn_names(people, conv["id"])
  save_people(people)
  unnamed = [c for c, person in people["chats"].items() if person and person not in people["names"]]
  print(json.dumps({"people": sum(1 for person in people["chats"].values() if person) - len(unnamed),
                    "untitled_groups": len(people["groups"]), "unnamed_people": len(unnamed)}))


URL = re.compile(r"https?://[^\s<]+")


def linkify(escaped):
  """Teams shows a URL as a link only when the sender wraps it in this anchor; the app does it while
  typing, so a bare URL sent here stays plain text. Sentence punctuation after a URL stays outside."""
  def wrap(match):
    url = match.group(0)
    tail = ""
    while url[-1] in ".,;:!?)":
      url, tail = url[:-1], url[-1] + tail
    return (f'<a href="{url}" itemtype="http://schema.skype.com/HyperLink" rel="noreferrer noopener" '
            f'title="{url}" target="_blank">{url}</a>{tail}')
  return URL.sub(wrap, escaped)


BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)


def bolden(escaped):
  """**text** in the message becomes bold, the one bit of formatting a caution line needs."""
  return BOLD.sub(r"<b>\1</b>", escaped)


def post(chat_id, text, properties=None):
  """Posts a message; returns its id."""
  if not readable(chat_id):
    sys.exit("Sending to this chat is not supported.")
  encoded = urllib.parse.quote(chat_id, safe="")
  # clientmessageid lets the server drop a duplicate if a send is retried.
  body = {
    "content": linkify(bolden(html.escape(text))).replace("\n", "<br>"),
    "messagetype": "RichText/Html",
    "contenttype": "text",
    "clientmessageid": str(random.randrange(10**18, 10**19)),
  }
  if properties:
    body["properties"] = properties
  data = msgapi(f"/users/ME/conversations/{encoded}/messages", body)
  return str(data.get("OriginalArrivalTime") or "")


def edit(chat_id, message_id, text):
  """Replaces the text of a message the user sent earlier; Teams marks it Edited. Attachments stay."""
  if not readable(chat_id):
    sys.exit("Editing in this chat is not supported.")
  encoded = urllib.parse.quote(chat_id, safe="")
  body = {
    "content": linkify(bolden(html.escape(text))).replace("\n", "<br>"),
    "messagetype": "RichText/Html",
    "contenttype": "text",
  }
  msgapi(f"/users/ME/conversations/{encoded}/messages/{message_id}", body, method="PUT")
  print(json.dumps({"id": message_id, "chat_id": chat_id, "content": text}))


def send(chat_id, text):
  print(json.dumps({"id": post(chat_id, text), "chat_id": chat_id, "content": text}))


def remember(chat_id):
  """Keeps the last chat sent to, with its account, so a follow-up message goes to the same place."""
  people = load_people()
  name = people["names"].get(people["chats"].get(chat_id))
  if not name:
    headers = chat_headers()
    status, conv = http(chat_url(f"/users/ME/conversations/{urllib.parse.quote(chat_id, safe='')}?view=msnp24Equivalent"),
                        headers=headers)
    name = (conv.get("threadProperties") or {}).get("topic") if status == 200 else None
  DATA.mkdir(parents=True, exist_ok=True)
  LAST_SEND.write_text(json.dumps({"account": ACCOUNT, "chat_id": chat_id, "name": name or "", "sent_at": int(time.time())}))


def last():
  if not LAST_SEND.exists():
    print("{}")
    return
  sent = json.loads(LAST_SEND.read_text())
  sent["minutes_ago"] = int((time.time() - sent.pop("sent_at")) / 60)
  print(json.dumps(sent))


def new_test_chat():
  """Makes a group chat named "test conv" with only the user in it, for trying things out."""
  body = {"members": [{"id": my_id(), "role": "Admin"}],
          "properties": {"threadType": "chat", "fixedRoster": False, "uniquerosterthread": False, "topic": "test conv"}}
  headers = chat_headers() | {"Content-Type": "application/json"}
  request = urllib.request.Request(chat_url("/threads"), json.dumps(body).encode(), headers, method="POST")
  try:
    with urllib.request.urlopen(request, timeout=40) as response:
      # The new chat's id is only in the Location header: .../threads/<id>
      print(json.dumps({"name": "test conv", "id": response.headers["Location"].rsplit("/", 1)[-1]}))
  except urllib.error.HTTPError as error:
    sys.exit(f"Could not make the test chat (HTTP {error.code}).")


def onedrive(method, path, data, token, timeout=40):
  auth = f"Bearer {token}" if WORK else f"WLID1.1 t={token}"
  status, body = http(ONEDRIVE + path, data, {"Authorization": auth}, method=method, timeout=timeout)
  if status >= 400:
    error = body.get("error")
    message = error.get("message") if isinstance(error, dict) else body.get("message")
    sys.exit(f"OneDrive call failed: {message or f'HTTP {status}'}")
  return body


def send_file(chat_id, path, text=""):
  """Uploads to the user's OneDrive and posts it as a file card, the way the Teams app does."""
  if not readable(chat_id):
    sys.exit("Sending to this chat is not supported.")
  file = Path(path).expanduser()
  if not file.is_file():
    sys.exit(f"No such file: {path}")
  if file.stat().st_size > MAX_FILE_MB * 2**20:
    sys.exit(f"File is over {MAX_FILE_MB} MB.")
  token = onedrive_token()
  # A name already taken in the folder gets " 1" added, as in the Teams app.
  where = urllib.parse.quote(f"{CHAT_FILES}/{file.name}")
  rename = "@microsoft.graph.conflictBehavior" if WORK else "@name.conflictBehavior"
  item = onedrive("PUT", f"/drive/root:/{where}:/content?{rename}=rename", file.read_bytes(), token, 600)
  if WORK:
    # A view-only link only the chat's members can open, signed in.
    members = [{"objectId": m.removeprefix("8:orgid:")} for m in other_members(chat_id, my_id()) if m.startswith("8:orgid:")]
    link = onedrive("POST", f"/drive/items/{item['id']}/createLink",
                    {"type": "view", "scope": "users", "recipients": members, "sendNotification": False}, token)
    site, url = item["webUrl"].split("/Documents/")[0] + "/", item["webUrl"]
  else:
    # A view-only link that opens without sign-in (the Teams app makes an edit link).
    link = onedrive("POST", f"/drive/items/{item['id']}/action.createLink", {"type": "view", "scope": "anonymous"}, token)
    site = f"{PERSONAL_CONTENT}/{item['parentReference']['driveId']}"
    url = f"{site}/Documents/{CHAT_FILES}/{item['name']}"
  name, share = item["name"], link["link"]["webUrl"]
  unique_id = re.search(r"\{([0-9A-Fa-f-]{36})\}", item["eTag"]).group(1).lower()
  ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
  card = {"@type": "http://schema.skype.com/File", "version": 2, "id": unique_id, "itemid": unique_id,
          "fileName": name, "fileType": ext, "type": ext, "title": name, "state": "active",
          "baseUrl": site, "objectUrl": url,
          "fileInfo": {"itemId": None if WORK else item["id"], "fileUrl": url, "siteUrl": site, "serverRelativeUrl": "",
                       "shareUrl": share, "shareId": link.get("shareId") or link["id"]},
          "fileChicletState": {"serviceName": "p2p", "state": "active"}, "providerData": "",
          "botFileProperties": {}, "permissionScope": "users" if WORK else None,
          "filePreview": {"previewUrl": "", "previewHeight": 0, "previewWidth": 0}}
  message_id = post(chat_id, text, {"files": json.dumps([card])})
  print(json.dumps({"id": message_id, "chat_id": chat_id, "file": name, "url": share, "content": text}))


if __name__ == "__main__":
  cmd, args = sys.argv[1:2], sys.argv[2:]
  if cmd == ["login"]:
    login()
  elif cmd == ["status"]:
    show_status()
  elif cmd == ["find"] and args:
    find(" ".join(args))
  elif cmd == ["history"] and args:
    limit = 20
    if "--limit" in args:
      at = args.index("--limit")
      limit = int(args[at + 1])
      del args[at:at + 2]
    if len(args) != 1:
      sys.exit(__doc__)
    if not readable(args[0]):
      sys.exit("This chat cannot be read here. The self-chat (48:notes) still fails.")
    print(json.dumps(messages(args[0], limit)))
  elif cmd == ["edit"] and len(args) == 3:
    edit(*args)
  elif cmd == ["send"] and len(args) == 2:
    send(args[0], args[1])
    remember(args[0])
  elif cmd == ["send-file"] and len(args) in (2, 4) and (len(args) == 2 or args[2] == "--text"):
    send_file(args[0], args[1], args[3] if len(args) == 4 else "")
    remember(args[0])
  elif cmd == ["last"]:
    last()
  elif cmd == ["index"]:
    index()
  elif cmd == ["new-test-chat"]:
    new_test_chat()
  else:
    sys.exit(__doc__)
