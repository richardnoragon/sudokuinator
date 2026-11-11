"""Offline assistance, searchable actions and replayable guidance for the desktop shell."""
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QDockWidget, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QPushButton, QRubberBand, QTextBrowser, QVBoxLayout, QWidget,
)

# Keep behavior claims aligned with USER_GUIDE.md when changing these topics.
TOPICS = {
    "Getting Started": ("welcome first launch new puzzle demo", """
# Welcome to Sudoku-inator
This pre-alpha desktop application supports eight puzzle variants.

1. Choose **File → New Game** (Ctrl+N), a variant, difficulty, and hint allowance.
2. Click an empty cell and type a digit. Press F4 for values above nine.
3. Use P for pencil marks and Ctrl+Z to undo an editable move.
4. Choose **File → Save** (Ctrl+S) to keep your progress.
5. Return to Help at any time. F1 opens help for the current context.

A Standard puzzle is already open for exploration. Starting or opening another
puzzle uses the normal Save / Discard / Cancel safeguards.
"""),
    "User Guide": ("play rules variants import export notes hints", """
# User guide
**New Game:** Ctrl+N offers Standard, Jigsaw, Str8ts, Killer, Codewords, Kakuro,
KenKen (4/6/9), and 1–25 (25×25). Generation can be cancelled.

**Input:** click or navigate with arrows and Tab. Digits enter 1–9; F4 accepts the
full range. Delete, Backspace, or 0 clears an editable cell. P toggles pencil mode.
Fixed clues and black cells cannot be edited. F5 checks variant-aware conflicts.

**Hints:** choose Auto, Reveal, Elim., Naked, or Candidate in the status bar; press H.
Candidate is advisory and free. Successful other modes spend one hint per invocation.
Revealed values are fixed. Undo does not refund hints. Text imports have no solution.

**Codewords:** given mappings are locked. Blank mappings accept distinct digit
hypotheses, which are notes rather than changes to the hidden solution.

**Exchange:** File → Import Puzzle / Export Puzzle supports JSON and project text.
JSON preserves session data; text omits notes, hypotheses, history and solutions.
There is no puzzle-library or cloud-sync UI.

**Restart:** F9 keeps elapsed time; Shift+F9 resets it. Save first to retain progress.
F2 changes theme. Generation difficulty and the displayed SE grade are separate.
"""),
    "Save and Recovery": ("backup restore missing file json storage saves load open", """
# Save, backup and recovery
Save / Save As writes to the location you choose. Ctrl+O opens a saved JSON session.
Saves restore notes, time, statistics, grade, variant metadata and remaining hints.
Undo history and theme preferences are not saved.

Overwriting retains the previous file as `<filename>.bak`. Only one previous save
is kept. Copy important files to a separate trusted backup location.

To recover: use **File → Open**, select **All files**, and open the `.bak` sibling.
Then use **Save As** to write a new JSON file. Keep the damaged original until you
have verified the recovered board. Versions 1 and 2 are accepted; writes use 2.

If a file is missing, check the original Save As destination and your own backups.
The app does not locate moved files or provide cloud recovery automatically.
"""),
    "Troubleshooting": ("errors broken startup hints conflicts performance diagnostic", """
# Troubleshooting
**Cannot launch:** activate the installation environment and reinstall the app there.
Linux may require the OS Qt/EGL runtime (`libegl1` on Ubuntu). Offscreen mode is for
automated tests; interactive play requires a desktop session.

**Hints unavailable:** check the allowance and selected mode. Text imports contain
no solution; solution-based hints need a generated puzzle or a JSON session with one.

**Cannot enter a value:** fixed clues and black cells are locked. Use F4 for 10–25.

**Save will not open:** preserve the file, try its `.bak` sibling, and check whether
the file uses a newer unsupported schema. Invalid imports keep the existing board.

**Generation is slow:** cancel and try a smaller KenKen size or another variant.
Difficulty calibration and Str8ts layout variety remain limited.

Report reproducible failures with OS, version, variant, steps, and the error text.
Do not include private save data or credentials in a public report.
"""),
    "Keyboard Shortcuts": ("keys controls navigation", """
# Keyboard shortcuts
| Action | Keys |
| --- | --- |
| New / Open | Ctrl+N / Ctrl+O |
| Save / Save As | Ctrl+S / Ctrl+Shift+S |
| Select | Arrows, Tab / Shift+Tab |
| Enter / clear | 1–9, F4 / Delete, Backspace, 0 |
| Pencil / Hint / Check | P / H / F5 |
| Undo / Redo | Ctrl+Z / Ctrl+Y |
| Restart / reset timer | F9 / Shift+F9 |
| Theme | F2 |
| Context help / Search actions | F1 / Ctrl+Shift+P |
"""),
    "Core Concepts": ("learning center advanced candidates difficulty theory", """
# Core concepts
A **puzzle** contains fixed clues and editable cells. A **session** also contains
notes, elapsed time, statistics and hint usage. Use JSON to retain the session.

**Pencil marks** are candidate notes. A value edit recomputes candidates; loading
preserves saved notes until a value edit. Candidate-only undo restores the exact edit.

**Variants** add constraints such as irregular regions, consecutive runs, cage
arithmetic, or letter mappings. Check Board uses the current variant rules.

**Difficulty** chosen during generation is heuristic. The SE grade is computed
separately and is not a guarantee of equivalent difficulty across variants.

**Extensions** are developer work: the internal variant registry does not install
external plug-ins. See repository ARCHITECTURE.md for module boundaries.
"""),
    "Release Notes": ("version changes changelog", """
# Release notes
Version 0.1.0 remains pre-alpha; independent handoff and manual release checks are open.

This development update adds offline help search, welcome guidance, a feature tour,
guided tasks, context help, and action search. It does not change save schema 2.
See repository CHANGELOG.md for the full development history.
"""),
    "Report Problem": ("bug issue security contact", """
# Report a problem
Use the repository issue tracker for ordinary bugs:
https://github.com/richardnoragon/sudokuinator/issues

Include application version, OS, variant, difficulty, reproduction steps, expected
behavior and actual error. Remove private data from attachments.

For vulnerabilities, follow repository SECURITY.md and use a private maintainer
channel or GitHub private reporting if enabled. Do not publish vulnerability details
in an ordinary issue. No response-time guarantee is established.
"""),
    "About": ("license copyright GPL", """
# About Sudoku-inator
Python and PyQt6 desktop puzzle application. Version 0.1.0, pre-alpha.

Project code is licensed under GNU GPL version 3. See LICENSE.md in the repository
for the complete terms. Third-party components and reference material retain their
own licenses and attribution.
"""),
}


class HelpCenter(QDockWidget):
    """Nonmodal offline topics: search includes titles, keywords and body text."""

    def __init__(self, parent):
        super().__init__("Help", parent)
        self.setObjectName("help_center")
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search help…")
        self.search.setAccessibleName("Search help")
        self.topics = QListWidget()
        self.topics.setAccessibleName("Help topics")
        self.topics.setMaximumHeight(180)
        self.article = QTextBrowser()
        self.article.setOpenExternalLinks(True)
        self.article.setAccessibleName("Help article")
        self.article.setMinimumWidth(300)
        self.empty = QLabel("No matching topics. Try ‘save’, ‘hint’, or ‘keyboard’.")
        for widget in (self.search, self.topics, self.empty, self.article):
            layout.addWidget(widget)
        self.setWidget(panel)
        self.search.textChanged.connect(self._filter)
        self.topics.currentTextChanged.connect(self._read)
        self._filter("")

    def _filter(self, query):
        self.topics.clear()
        words = query.casefold().split()
        for title, (keywords, body) in TOPICS.items():
            haystack = f"{title} {keywords} {body}".casefold()
            if all(word in haystack for word in words):
                self.topics.addItem(title)
        self.empty.setVisible(self.topics.count() == 0)
        self.article.clear()
        if self.topics.count():
            self.topics.setCurrentRow(0)

    def _read(self, title):
        if title in TOPICS:
            self.article.setMarkdown(TOPICS[title][1])

    def open_topic(self, title="Getting Started"):
        self.search.clear()
        matches = self.topics.findItems(title, Qt.MatchFlag.MatchExactly)
        if matches:
            self.topics.setCurrentItem(matches[0])
        self.show()
        self.raise_()
        self.search.setFocus()


class Guidance(QDialog):
    """Nonmodal step guide highlighting live widgets without modifying a game."""

    def __init__(self, parent, title, steps):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.steps = steps
        self.index = 0
        layout = QVBoxLayout(self)
        self.text = QLabel()
        self.text.setWordWrap(True)
        self.text.setMinimumWidth(300)
        layout.addWidget(self.text)
        buttons = QHBoxLayout()
        self.back = QPushButton("Back")
        self.next = QPushButton("Next")
        close = QPushButton("Close")
        for button in (self.back, self.next, close):
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.back.clicked.connect(lambda: self._move(-1))
        self.next.clicked.connect(lambda: self._move(1))
        close.clicked.connect(self.close)
        self.marker = None
        self.finished.connect(self._clear_marker)
        self._render()

    def _move(self, delta):
        self.index += delta
        if self.index == len(self.steps):
            self.close()
        else:
            self._render()

    def _render(self):
        self._clear_marker()
        message, target = self.steps[self.index]
        self.text.setText(f"Step {self.index + 1} of {len(self.steps)}\n\n{message}")
        self.back.setEnabled(self.index > 0)
        self.next.setText("Finish" if self.index == len(self.steps) - 1 else "Next")
        if target is not None:
            self.marker = QRubberBand(QRubberBand.Shape.Rectangle, target)
            self.marker.setGeometry(target.rect())
            self.marker.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self.marker.show()

    def _clear_marker(self):
        if self.marker is not None:
            self.marker.hide()
            self.marker.deleteLater()
            self.marker = None

    def closeEvent(self, event):
        self._clear_marker()
        super().closeEvent(event)


class ActionSearch(QDialog):
    """Search and invoke the existing actions with their enabled state intact."""

    def __init__(self, parent, actions: list[QAction]):
        super().__init__(parent)
        self.setWindowTitle("Search actions")
        layout = QVBoxLayout(self)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Type an action…")
        self.search.setAccessibleName("Search actions")
        self.results = QListWidget()
        layout.addWidget(self.search)
        layout.addWidget(self.results)
        self.actions = actions
        self.matches = []
        self.search.textChanged.connect(self._filter)
        self.results.itemActivated.connect(self._invoke)
        self.search.returnPressed.connect(self._invoke)
        self._filter("")

    def _filter(self, query):
        self.results.clear()
        self.matches = [a for a in self.actions if a.isEnabled()
                        and query.casefold() in a.text().replace("&", "").casefold()]
        for action in self.matches:
            self.results.addItem(action.text().replace("&", ""))
        self.results.setCurrentRow(0)

    def _invoke(self, *_args):
        row = self.results.currentRow()
        if 0 <= row < len(self.matches):
            action = self.matches[row]
            self.accept()
            action.trigger()


def welcome(parent, settings):
    """Replayable welcome with explicit choices; dismissing never replaces a game."""
    dialog = QDialog(parent)
    dialog.setWindowTitle("Welcome to Sudoku-inator")
    layout = QVBoxLayout(dialog)
    text = QLabel("Solve eight puzzle variants. Choose a first step; help is always available with F1.")
    text.setWordWrap(True)
    layout.addWidget(text)
    for label, callback in (
        ("Create New Puzzle", parent._on_new_game),
        ("Open Saved Game", parent._on_open),
        ("Explore Current Puzzle", lambda: parent._help.open_topic("Getting Started")),
        ("Feature Tour", parent._start_tour),
    ):
        button = QPushButton(label)
        def choose(_checked=False, action=callback):
            dialog.accept()
            action()
        button.clicked.connect(choose)
        layout.addWidget(button)
    buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    settings.setValue("welcome_seen", True)
    dialog.exec()
