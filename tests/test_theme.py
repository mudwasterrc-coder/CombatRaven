from PySide6.QtWidgets import QApplication

from combat_raven.ui.theme import RAVEN_STYLESHEET, apply_theme


def test_apply_theme_sets_the_application_stylesheet(qtbot):
    app = QApplication.instance()

    apply_theme(app)

    assert app.styleSheet() == RAVEN_STYLESHEET

    app.setStyleSheet("")