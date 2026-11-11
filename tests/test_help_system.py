"""Assistance behavior and safeguards with real Qt controls."""
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog

from sudoku_inator.main import MainWindow
from sudoku_inator.ui.help_system import ActionSearch, welcome


def test_search_body_keywords_and_empty_state(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    help_center = window._help
    help_center.open_topic("User Guide")
    help_center.search.setText("backup restore")
    assert help_center.topics.count() == 1
    assert "Save, backup and recovery" in help_center.article.toPlainText()
    help_center.search.setText("nothingmatches123")
    assert help_center.topics.count() == 0
    assert help_center.article.toPlainText() == ""
    assert not help_center.empty.isHidden()
    help_center.open_topic("Keyboard Shortcuts")
    assert "Ctrl+Shift+P" in help_center.article.toPlainText()


def test_action_search_executes_enabled_action(qtbot):
    action = QAction("&Save")
    disabled = QAction("Save Disabled")
    disabled.setEnabled(False)
    called = []
    action.triggered.connect(lambda: called.append(True))
    dialog = ActionSearch(None, [action, disabled])
    qtbot.addWidget(dialog)
    dialog.search.setText("save")
    assert dialog.results.count() == 1
    dialog._invoke()
    assert called == [True]


def test_tour_back_close_and_finish_do_not_change_board(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    before = window._ctrl._board.to_dict()
    window._start_tour()
    guide = window._guidance
    assert not guide.back.isEnabled()
    guide.next.click()
    assert guide.index == 1
    guide.back.click()
    assert guide.index == 0
    for _ in guide.steps:
        guide.next.click()
    assert window._guidance is None
    after = window._ctrl._board.to_dict()
    assert before == after
    window._start_tour()
    window._guidance.close()
    assert window._guidance is None


def test_welcome_close_sets_flag_without_replacing_game(qtbot, tmp_path):
    from PyQt6.QtCore import QTimer
    window = MainWindow()
    qtbot.addWidget(window)
    board = window._ctrl._board
    settings = QSettings(str(tmp_path / "welcome.ini"), QSettings.Format.IniFormat)
    def dismiss():
        dialog = next(d for d in window.findChildren(QDialog)
                      if d.windowTitle() == "Welcome to Sudoku-inator")
        dialog.reject()
    QTimer.singleShot(0, dismiss)
    welcome(window, settings)
    assert settings.value("welcome_seen", False, type=bool)
    assert window._ctrl._board is board


def test_f1_opens_help_from_board(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.activateWindow()
    qtbot.waitUntil(window.isActiveWindow)
    window._grid.setFocus()
    qtbot.keyClick(window._grid, Qt.Key.Key_F1)
    assert not window._help.isHidden()
    assert window._help.topics.currentItem().text() == "User Guide"


def test_escape_removes_tour_highlight(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window._start_tour()
    guide = window._guidance
    marker = guide.marker
    qtbot.keyClick(guide, Qt.Key.Key_Escape)
    assert guide.marker is None
    assert marker.isHidden()
    assert window._guidance is None
