# Sudoku-inator

A Python + PyQt6 desktop puzzle app with eight registered variants, local saves,
pencil marks, hints, undo/redo, and SE-style difficulty grading.
Formerly known as Richards Sudoku (`richards_sudoku`). The distribution and command
are `sudoku-inator`; the Python package is `sudoku_inator`. See [the rebranding record](REBRANDING.md).

## Current status

Application version: **0.1.0**. Development stage: **pre-alpha; Alpha criteria remain open**.
[alpha.md](alpha.md) defines the developer handoff and end-to-end workflow standard.
Core and extended-variant foundations are implemented.
The workflow fixes have regression coverage; independent handoff and manual
release validation remain open. See
[project status](PROJECT_STATUS.md) for verified behavior and known gaps.

| Variant | Board size |
| --- | --- |
| Standard, Jigsaw, Str8ts, Killer, Codewords, Kakuro | 9×9 |
| KenKen | 4×4, 6×6, 9×9 |
| 1–25 | 25×25; use F4 / Enter Value for values 10–25 |

## Install and run

Requires Python 3.13+ and a desktop environment. PyQt6 >=6.10 is installed as a dependency.

Clone the repository and enter its directory:

```bash
git clone https://github.com/richardnoragon/sudokuinator.git
cd sudokuinator
```

Create a virtual environment:

```bash
python -m venv .venv
```

If your Linux Python reports that `ensurepip` is unavailable, install the matching
Python venv package supplied by your distribution, then repeat this command.

Activate with `source .venv/bin/activate` on Linux/macOS, or
`.venv\Scripts\Activate.ps1` in Windows PowerShell. Then run:

```bash
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
sudoku-inator
```

Use `sudoku-inator`; the former command was retired in the full rebrand.
For play without developer tools, install with `python -m pip install -e .`.

## Docker testing (Kubuntu / KDE Plasma)

Build and launch the checked-out application on your Linux desktop:

```bash
docker build --pull -t sudoku-inator:local .
./scripts/docker-run.sh
```

The launcher supports X11 and Plasma Wayland through XWayland, uses your session's
Xauthority file, and keeps saves and welcome settings under `docker-saves/`.
Use Save As under `/data` in the app. Docker must be accessible to your normal
desktop user.

For a headless regression run:

```bash
docker build --pull --target test -t sudoku-inator:test .
docker run --rm --init --network none sudoku-inator:test
```

See [Docker testing](DOCKER_TESTING.md) for prerequisites, desktop smoke checks,
image archive sharing, persistent folders, and troubleshooting.

## Playing

Use **File → New Game** to choose a variant, difficulty, and hint allowance.
Click a cell, enter digits (or **F4** for any value up to 25), and use **P** for
pencil mode or **H** for the selected hint mode.
Use **File → Save** and **File → Open** to save and resume JSON games.
See the [user guide](USER_GUIDE.md) for controls and current limitations.

## Help preview

![Desktop puzzle with searchable offline help](docs/images/help-center.png)

Open Help for the welcome flow, feature tour, guided tasks, and offline articles.
F1 provides context help; Ctrl+Shift+P searches available actions.

## Development checks

```bash
python -m ruff check src
python -m mypy
```

On Linux/macOS:

```bash
QT_QPA_PLATFORM=offscreen python -m pytest -q
```

See [TESTING.md](TESTING.md) for PowerShell commands, current results, and CI scope.

## Documentation

- [Documentation contents](TOC.md) and [frequently asked questions](FAQ.md)
- [Documentation index and authority](DOCUMENTATION.md)
- [Architecture](ARCHITECTURE.md) and [decisions](DECISIONS.md)
- [Requirements](prd.md) and [UX direction](UX_DESIGN_SPEC.md)
- [Roadmap](ROADMAP.md), [implementation issues](IMPLEMENTATION_ISSUES.md), and [tasks](speckit.tasks)
- [Contributing](CONTRIBUTING.md), [release process](RELEASE_PROCESS.md), and [release checklist](RELEASE_CHECKLIST.md)
- [Changelog](CHANGELOG.md), [save migrations](MIGRATIONS.md), and [security policy](SECURITY.md)

## License and community

Project code is licensed under [GNU GPL version 3](LICENSE.md) (`GPL-3.0-only`).
Third-party dependencies and attributed reference material retain their own terms.
See the [code of conduct](CODE_OF_CONDUCT.md) and
[in-app help overview](USER_ASSISTANCE.md).
