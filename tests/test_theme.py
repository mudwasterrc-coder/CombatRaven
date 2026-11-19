from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase


from combat_raven.ui.theme import RAVEN_STYLESHEET, apply_theme


def test_apply_theme_sets_the_application_stylesheet(qtbot):
    app = QApplication.instance()

    apply_theme(app)

    assert app.styleSheet() == RAVEN_STYLESHEET

    app.setStyleSheet("")

def test_apply_theme_loads_the_cinzel_font(qtbot):
    app = QApplication.instance()

    apply_theme(app)

    assert "Cinzel" in QFontDatabase.families()

    app.setStyleSheet("")