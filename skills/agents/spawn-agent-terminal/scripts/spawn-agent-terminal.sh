#!/usr/bin/env bash
set -euo pipefail

agent=""
prompt=""
cwd="${PWD}"
# WSL distro to open. Order: --distro, then SPAWN_AGENT_DISTRO, then the distro this
# shell runs in (WSL sets WSL_DISTRO_NAME), then "Ubuntu".
distro="${SPAWN_AGENT_DISTRO:-${WSL_DISTRO_NAME:-Ubuntu}}"
title=""

usage() {
  printf 'Usage: %s --agent codex|claude --prompt "text" [--cwd path] [--distro name] [--title text]\n' "$0" >&2
  printf 'Default distro: $SPAWN_AGENT_DISTRO, else $WSL_DISTRO_NAME, else Ubuntu.\n' >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)
      agent="${2:-}"
      shift 2
      ;;
    --prompt)
      prompt="${2:-}"
      shift 2
      ;;
    --cwd)
      cwd="${2:-}"
      shift 2
      ;;
    --distro)
      distro="${2:-}"
      shift 2
      ;;
    --title)
      title="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ "$agent" != "codex" && "$agent" != "claude" ]]; then
  printf 'Error: --agent must be codex or claude.\n' >&2
  usage
  exit 2
fi

if [[ -z "$prompt" ]]; then
  printf 'Error: --prompt is required.\n' >&2
  usage
  exit 2
fi

if ! command -v wt.exe >/dev/null 2>&1; then
  printf 'Error: wt.exe was not found. Run this from WSL on Windows with Windows Terminal installed.\n' >&2
  exit 1
fi

tmp_dir="$(mktemp -d /tmp/spawn-agent-terminal.XXXXXX)"
prompt_file="${tmp_dir}/prompt.txt"
runner="${tmp_dir}/run-agent.sh"

printf '%s' "$prompt" > "$prompt_file"

cat > "$runner" <<EOF
#!/usr/bin/env bash
set -uo pipefail
prompt=\$(cat "$prompt_file")
rm -f "$prompt_file"
if [[ "$agent" == "claude" ]]; then
  claude "\$prompt"
else
  codex "\$prompt"
fi
status=\$?
printf '\\n[%s exited with code %s]\\n' "$agent" "\$status"
exec bash -l
EOF

chmod +x "$runner"

cmd=(wt.exe)
if [[ -n "$title" ]]; then
  cmd+=(new-tab --title "$title")
fi
cmd+=(wsl.exe -d "$distro" --cd "$cwd" -- bash -lic "$runner")

"${cmd[@]}"
