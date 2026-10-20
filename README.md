# agent-skills

These are skills I use every day to run many AI agents at once, and to write and explain things plainly.

They work in Claude Code and Codex. Each skill is a folder with a `SKILL.md` file. Some also have scripts and reference files.

## Skills

There are two kinds of skill here:

- **Model-invoked.** The agent can start it on its own when your request matches.
- **User-invoked.** Only you can start it. Type `/name` in Claude Code or `$name` in Codex.

| Category | Skill | Kind | What it does |
|---|---|---|---|
| Agents | [herdr-orchestration](skills/agents/herdr-orchestration/SKILL.md) | Model | Starts, prompts, waits for and closes Claude or Codex agents in other Herdr tabs. |
| Agents | [supervise-agents](skills/agents/supervise-agents/SKILL.md) | Model | Runs long multi-agent work with one supervisor, small bounded jobs, and checks based on evidence. |
| Agents | [spawn-agent-terminal](skills/agents/spawn-agent-terminal/SKILL.md) | Model | Opens Codex or Claude in a new Windows Terminal tab from WSL, with a first prompt. |
| Writing | [personal-writing-voice](skills/writing/personal-writing-voice/SKILL.md) | Model | Drafts or cleans up a message to a person so it does not read like AI wrote it. |
| Writing | [grounded](skills/writing/grounded/SKILL.md) | User | Explains something at full depth in very simple English, starting from the basics. |
| Writing | [simple](skills/writing/simple/SKILL.md) | User | Rewrites the last reply in short, plain English. |
| Automation | [teams-hands-free](skills/automation/teams-hands-free/SKILL.md) | Model | Reads and sends Microsoft Teams chats and files from the terminal, on a personal or work account. Asks before every send. |

## Install

Pick one way per agent. If you use two ways, you get every skill twice.

### Claude Code

```bash
claude plugin marketplace add bengemine/agent-skills
claude plugin install bengemine-skills@bengemine
```

### Codex

```bash
codex plugin marketplace add bengemine/agent-skills
codex plugin add bengemine-skills@bengemine
```

### Any agent, or one skill at a time

```bash
npx skills add bengemine/agent-skills
```

You can also copy one skill folder by hand. Put it in `~/.claude/skills/` for Claude Code, or in `~/.agents/skills/` for Codex.

## What each skill needs

- **herdr-orchestration** and **supervise-agents** need [Herdr](https://github.com/herdrdev/herdr) and the `herdr` skill that comes with it.
- **spawn-agent-terminal** needs Windows, WSL and Windows Terminal. To choose the WSL distro, pass `--distro` or set `SPAWN_AGENT_DISTRO`. If you do neither, it uses the distro you run it from. If that is unknown, it uses `Ubuntu`.
- **teams-hands-free** needs Python 3. It uses only the standard library. It also needs a personal Microsoft account, a work account, or both.

## Make them yours

- **personal-writing-voice** follows my writing rules. Replace `references/EXAMPLES.md` with a few of your own messages. Then it will sound more like you.
- **teams-hands-free** keeps your settings outside the skill folder. The first time you use it, the agent walks you through setup. You can also copy `config.example.json` to `~/.config/teams-hands-free/config.json` and fill it in. Remove the `work` part if you have no work account.
- **herdr-orchestration** has a Codex model table in `references/codex-models.md`. It is dated. Check it against the models your Codex lists.

## teams-hands-free warning

Use this skill at your own risk.

- It uses Microsoft's private Teams endpoints. It signs in as Microsoft's own Teams apps: the web app for a personal account, the desktop app for a work account. Microsoft does not document or support this.
- It may break at any time.
- It may conflict with Microsoft's terms of use.
- Use it only with your own accounts. On a work account, check your company's IT rules first. Some companies block this kind of sign-in.
- Your sign-ins are saved in `~/.config/teams-hands-free/credentials.json` and `work-credentials.json`. Keep those files private.
- A file you send goes to your OneDrive. The chat gets a view-only link. On a personal account, anyone who has that link can open the file without signing in. On a work account, only the people in the chat can open it.

## Credits

- `AI-TELLS.md` in personal-writing-voice adapts parts of [blader/humanizer](https://github.com/blader/humanizer) and [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop). Both are MIT licensed. Humanizer's pattern list comes from Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) page. See [NOTICE](NOTICE).
- [Herdr](https://github.com/herdrdev/herdr) is the terminal tool the agent skills drive. It is not part of this repo.
- The folder layout and the split between model-invoked and user-invoked skills follow [mattpocock/skills](https://github.com/mattpocock/skills).

## License

MIT. See [LICENSE](LICENSE).
