# Frequently asked questions

## Is Sudoku-inator ready for ordinary users?

The application is version 0.1.0 and pre-alpha. Independent developer handoff,
manual platform validation, and release approval remain open. See
[project status](PROJECT_STATUS.md) for evidence and limitations.

## How do I install and start it?

Follow [installation and quick start](README.md#install-and-run). The application
requires Python 3.13+, PyQt6, and a desktop session. Run `sudoku-inator` from the
environment where it is installed.

## Which puzzles are available?

Standard, Jigsaw, Str8ts, Killer, Codewords, Kakuro, KenKen, and 1–25 are registered.
KenKen supports 4×4, 6×6, and 9×9; 1–25 uses a 25×25 board. See the
[user guide](USER_GUIDE.md) for controls and generation limitations.

## How do I enter numbers above nine?

Select a cell and press F4, or choose **Edit → Enter Value**. The dialog supports
the full board range in normal and pencil modes.

## Why are hints unavailable after importing text?

Text exchange does not include a solution or full session state. Solution-based
hints require a stored solution. Use JSON to preserve a session. See
[import/export](USER_GUIDE.md#importexport-and-codewords).

## Where are my saves, and how do I back them up?

You choose the destination in Save / Save As. Copy important JSON saves to a
separate trusted location. Overwriting retains only the previous save in a `.bak`
sibling; it is not a backup history. See
[save and recovery instructions](USER_GUIDE.md#save-resume-and-recover).

## Why did my undo history disappear after opening a save?

Undo/redo history is session-local and is not serialized. Saved notes, elapsed
time, statistics, and supported variant metadata are restored; UI preferences
are not. See [save compatibility](MIGRATIONS.md).

## Does the app have a puzzle library or cloud synchronization?

There is no puzzle-library UI or built-in cloud synchronization. Puzzle-pack
exchange exists as a developer API. See [architecture](ARCHITECTURE.md#text-exchange)
and the [roadmap](ROADMAP.md) for implemented boundaries and future scope.

## Where can I find help or report a problem?

Start with the [user guide](USER_GUIDE.md), its
[troubleshooting section](USER_GUIDE.md#troubleshooting), and the
[documentation index](TOC.md). For a reproducible bug, use the repository issue
tracker and include your revision, OS, variant, steps, and error message. Follow
[SECURITY.md](SECURITY.md#vulnerability-reporting) for security reports.
