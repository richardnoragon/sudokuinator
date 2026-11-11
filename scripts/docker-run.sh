#!/usr/bin/env bash
# Launch the desktop tester image on Linux, including KDE Plasma Wayland/XWayland.
set -euo pipefail

usage() {
    cat <<'HELP'
Usage: scripts/docker-run.sh [--smoke-test] [--help]

Run from your Kubuntu/Linux desktop session. Build the image first:
  docker build --pull -t sudoku-inator:local .

Options:
  --smoke-test  Show the app briefly and exit after checking Qt and help startup.
  --help        Show this help.

Environment:
  SUDOKU_IMAGE     Image tag (default: sudoku-inator:local).
  SUDOKU_DATA_DIR  Persistent host folder (default: <repository>/docker-saves).
  XAUTHORITY      Desktop authentication file (KDE normally sets this).
HELP
}

smoke=false
case "${1:-}" in
    --help|-h) usage; exit 0 ;;
    --smoke-test) smoke=true; shift ;;
    '') ;;
    *) usage >&2; exit 2 ;;
esac
if (( $# )); then usage >&2; exit 2; fi
if [[ $(uname -s) != Linux ]]; then
    echo 'This desktop launcher requires Linux with X11 or XWayland.' >&2
    exit 1
fi
if [[ -z ${DISPLAY:-} || ! -d /tmp/.X11-unix ]]; then
    echo 'Run in a desktop terminal with DISPLAY set and X11/XWayland available.' >&2
    exit 1
fi
# KDE Plasma Wayland normally exports /run/user/<uid>/xauth_<suffix>.
# Use that exact session file rather than assuming ~/.Xauthority.
auth_file=${XAUTHORITY:-${HOME}/.Xauthority}
if [[ ! -r $auth_file || ! -f $auth_file ]]; then
    echo 'No readable Xauthority file. Set XAUTHORITY to your desktop session file.' >&2
    exit 1
fi
command -v docker >/dev/null || { echo 'Docker is required.' >&2; exit 1; }
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_dir=$(cd -- "$script_dir/.." && pwd)
data_dir=${SUDOKU_DATA_DIR:-$repo_dir/docker-saves}
mkdir -p -- "$data_dir"
data_dir=$(cd -- "$data_dir" && pwd)
auth_file=$(realpath -- "$auth_file")
image=${SUDOKU_IMAGE:-sudoku-inator:local}
args=(run --rm --init
    --user "$(id -u):$(id -g)"
    --hostname "$(hostname)"
    --network none
    --cap-drop ALL
    --security-opt no-new-privileges
    --read-only
    --tmpfs /tmp:rw,nosuid,nodev,size=256m
    --env "DISPLAY=$DISPLAY"
    --env XAUTHORITY=/run/desktop.xauth
    --env HOME=/tmp
    --env XDG_CONFIG_HOME=/data/.config
    --env QT_QPA_PLATFORM=xcb
    --env QT_X11_NO_MITSHM=1
    --mount type=bind,src=/tmp/.X11-unix,dst=/tmp/.X11-unix,readonly
    --mount "type=bind,src=$auth_file,dst=/run/desktop.xauth,readonly"
    --mount "type=bind,src=$data_dir,dst=/data"
)
if $smoke; then
    exec docker "${args[@]}" "$image" python /app/docker-smoke.py
fi
exec docker "${args[@]}" "$image"
