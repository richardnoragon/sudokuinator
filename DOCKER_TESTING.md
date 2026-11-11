# Docker testing on Kubuntu

This packages the checked-out pre-alpha application for developer evaluation.
Kubuntu with KDE Plasma is the priority host. The image uses Debian slim and
Python 3.13, matching the CI Python line; it is not a full Kubuntu desktop image.
The app runs on the host desktop through X11 or Plasma Wayland's XWayland.

## Prerequisites

Install Docker Engine using the Docker documentation for your Ubuntu/Kubuntu
version. Ensure `docker version` can reach the server from your normal desktop
user. The desktop launcher also requires Bash, `realpath`, and a working X11 or
XWayland session. Run it from a terminal inside your graphical session.

Build from the repository root:

```bash
docker build --pull -t sudoku-inator:local .
```

## Launch and test the desktop

```bash
./scripts/docker-run.sh
```

The launcher uses your numeric user/group IDs so saves belong to you. It reads
`DISPLAY` and the session's `XAUTHORITY`; KDE Plasma commonly puts its cookie file
under `/run/user/<uid>/xauth_*`, rather than `~/.Xauthority`. It mounts that file
and the local X11 socket, keeping authentication enabled without `xhost +`.

Use **File → Save As** to save under `/data`. This maps to the checkout's
`docker-saves/` folder. Welcome/onboarding settings persist in
`docker-saves/.config/`. The folder is ignored by Git and the image build.
Closing the app removes the container; saves remain in the host folder.

Customize the image tag or persistent folder:

```bash
SUDOKU_IMAGE=sudoku-inator:local \
SUDOKU_DATA_DIR="$HOME/sudoku-testing" ./scripts/docker-run.sh
```

A bounded check shows the board, help and tour for one second, then exits:

```bash
./scripts/docker-run.sh --smoke-test
```

The launcher disables container networking, drops capabilities, uses a read-only
root filesystem and a temporary `/tmp`, and mounts saves read/write. Normal
puzzle play and offline help work without network access. Browser links may not
open because there is no browser or host desktop portal inside the container;
copy report URLs into your host browser.

## Headless tests

Build the separate test image and run the packaged suite without a desktop:

```bash
docker build --pull --target test -t sudoku-inator:test .
docker run --rm --init --network none sudoku-inator:test
```

The runtime image also supports a headless startup smoke check:

```bash
docker run --rm --init --network none \
  -e QT_QPA_PLATFORM=offscreen \
  sudoku-inator:local python /app/docker-smoke.py
```

The image installs its source at build time. Rebuild after changing code; it does
not mount your source checkout. Tests exercise the installed package. Both targets
include the project license, and the runtime target excludes development tools.

## Share the image with another developer

Create an image archive and checksum on the build machine:

```bash
docker image save -o /tmp/sudoku-inator-linux-amd64.tar sudoku-inator:local
sha256sum /tmp/sudoku-inator-linux-amd64.tar
```

Transfer the archive and checksum along with the repository revision. On the
other Kubuntu/Linux amd64 machine, verify the checksum, then load it:

```bash
sha256sum sudoku-inator-linux-amd64.tar
docker image load -i sudoku-inator-linux-amd64.tar
./scripts/docker-run.sh
```

The recipient needs the launcher from this repository and Docker. Loading the
runtime archive does not provide the test-target image; build that separately
for automated tests. The archive is architecture-specific; build locally for
other architectures. Do not commit image archives to Git.

## Manual developer checklist

Record the image ID (`docker image inspect sudoku-inator:local --format '{{.Id}}'`),
source revision, Kubuntu version, Plasma session type, and results:

- Welcome, Help search, F1, action search and tour placement.
- New Game, representative variants, input including F4 values 10–25 and pencil marks.
- Hints, undo/redo, Codewords hypotheses, and Check Board.
- Save under `/data`, close, relaunch, reopen, and confirm progress/settings persist.
- Backup recovery, import/export, Save/Discard/Cancel, and generation cancellation.

Headless tests and startup checks do not certify manual gameplay, screen-reader
support, or independent Alpha handoff. Follow [TESTING.md](TESTING.md) and
[CONTRIBUTING.md](CONTRIBUTING.md) for those evidence requirements.

## Troubleshooting

- **Docker socket permission denied:** configure Docker access for your normal
  desktop user, then start a new login session if required. Do not run the desktop
  launcher with `sudo`: that changes your user IDs and may discard session variables.
- **Missing DISPLAY:** run inside the graphical session. On Plasma Wayland,
  ensure XWayland is installed and running. SSH/headless sessions are not the
  supported desktop path; use the headless test target there.
- **Missing Xauthority:** inspect `printf '%s\n' "$XAUTHORITY"` in a working desktop
  terminal. Set `XAUTHORITY` to the session's actual readable cookie file. The
  launcher deliberately does not guess among multiple users' or sessions' files.
- **Qt cannot connect to display:** verify the session cookie and local X11 socket;
  rerun from the same desktop terminal. Native Wayland forwarding is not configured.
- **Save permission denied:** use a folder writable by your current user and select
  a path under `/data` in the application. Existing root-owned saves need their
  ownership corrected by their owner/administrator.
- **Changes are missing:** rebuild the image or load the latest archive, and verify
  the image ID. Containers do not automatically update from GitHub.
