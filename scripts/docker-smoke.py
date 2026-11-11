"""Bounded container startup check using the selected Qt platform (xcb or offscreen)."""
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from sudoku_inator.main import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
window._help.open_topic("Getting Started")
window._start_tour()


def finish():
    assert window._ctrl._board is not None
    assert "Welcome to Sudoku-inator" in window._help.article.toPlainText()
    window._guidance.close()
    window.close()
    print(f"Desktop startup and help smoke check passed (Qt platform: {app.platformName()}).", flush=True)
    app.quit()


QTimer.singleShot(1000, finish)
raise SystemExit(app.exec())
