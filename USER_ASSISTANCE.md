# User assistance

## Implemented desktop assistance

The Help menu provides Getting Started, Welcome, Feature Tour, Guided Tasks,
User Guide, Search Help, Troubleshooting, Keyboard Shortcuts, Release Notes,
Report Problem, About, Context Help, and Search Actions.

- First application launch shows a welcome dialog with Create New Puzzle, Open
  Saved Game, Explore Current Puzzle, and Feature Tour. Dismissal keeps the current
  puzzle. A QSettings flag records that the welcome was shown. Help → Welcome
  replays it. No puzzle data is stored in that setting.
- The tour highlights real menus, toolbar, board, and status bar. Back, Next,
  Finish, and Close control a nonmodal guide; users can interact with the app.
- Guided Tasks covers playing/saving, importing, and recovering a backup. Steps
  are user-advanced instructions; they do not automatically verify task completion.
- Offline search matches topic titles, keywords and article text. A no-results
  message suggests alternative terms. Articles cover controls, concepts, recovery,
  troubleshooting, and reporting; no connection is needed to read them.
- F1 opens control-context guidance for the board and Codewords fields, with
  Getting Started as the fallback. Action tooltips and What's This text describe
  existing commands. Ctrl+Shift+P searches and invokes enabled application actions.

This application starts with a Standard puzzle rather than an empty library, so
Explore Current Puzzle uses the existing session. Library creation, hashing, NAS
repair, and other examples in the generic template do not apply to this app.

## Maintenance and accessibility

`ui/help_system.py` owns offline articles and assistance widgets; `main.py` binds
commands and tour targets. Keep articles aligned with [USER_GUIDE.md](USER_GUIDE.md)
and update the release-note topic alongside [CHANGELOG.md](CHANGELOG.md).

Search fields and article widgets have accessible names; dialogs use standard Qt
buttons and keyboard focus. Automated checks cover searching, action invocation,
tour navigation, and welcome dismissal. Screen-reader, visual tour placement,
and platform usability review remain manual release work.

## Later improvements

The generic outline also proposes automatic task-completion detection, adaptive
learning, occasional discovery tips, AI help, and richer troubleshooting diagnostics.
These remain future work. The current guides do not modify puzzles or run repairs.
Maintain that distinction in product claims and release evidence.
