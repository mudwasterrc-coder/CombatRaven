"""
Raven night theme for Combat Raven.
"""

from PySide6.QtWidgets import QApplication

RAVEN_STYLESHEET = """
QMainWindow, QDialog, QMessageBox, QInputDialog {
    background: #111117;
}

QWidget {
    color: #ECEAF4;
    font-size: 14px;
}

QScrollArea, QScrollArea > QWidget > QWidget {
    background: transparent;
    border: none;
}

QLabel {
    background: transparent;
    border: none;
}

QPushButton {
    background: #22222D;
    color: #ECEAF4;
    border: 1px solid #3A3A4A;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background: #2A2A36;
    border-color: #4A4A5C;
}

QPushButton:pressed {
    background: #1A1A23;
}

QPushButton:disabled {
    background: transparent;
    color: #5C5A6B;
    border-color: #26262F;
}

QPushButton#primaryButton {
    background: #8E7DFF;
    color: #120E2A;
    border: none;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 700;
}

QPushButton#primaryButton:hover {
    background: #A294FF;
}

QPushButton#primaryButton:disabled {
    background: #2A2640;
    color: #6E6890;
}

QPushButton#damageButton {
    background: #3A1F22;
    color: #FF8C8C;
    border-color: #5A2A2E;
}

QPushButton#healButton {
    background: #17322A;
    color: #6FE0A8;
    border-color: #22503F;
}

QPushButton#removeButton {
    background: transparent;
    color: #FF8C8C;
    border-color: #3A2427;
}

QSpinBox, QLineEdit, QListWidget {
    background: #111117;
    color: #ECEAF4;
    border: 1px solid #3A3A4A;
    border-radius: 10px;
    padding: 6px 10px;
    selection-background-color: #8E7DFF;
    selection-color: #120E2A;
}

QSpinBox::up-button, QSpinBox::down-button {
    width: 0;
    border: none;
}

QSpinBox:focus, QLineEdit:focus {
    border-color: #8E7DFF;
}

QFrame#combatantCard {
    background: #1A1A23;
    border: 1px solid #2A2A36;
    border-radius: 14px;
}

QFrame#combatantCard[current="true"] {
    background: #1E1B33;
    border: 2px solid #8E7DFF;
}

QFrame#combatantCard[down="true"] {
    background: #15151B;
    border: 1px dashed #34343F;
}

QLabel#nameLabel {
    font-size: 18px;
    font-weight: 600;
}

QLabel#concentrationLabel {
    color: #B9B2E0;
}

QLabel#roundLabel {
    font-size: 22px;
    font-weight: 700;
}

QLabel#currentTurnLabel {
    color: #8E7DFF;
    font-size: 20px;
    font-weight: 700;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #2E2E3B;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QProgressBar {
    background: #2E2E3B;
    border: none;
    border-radius: 5px;
    max-height: 10px;
}

QProgressBar::chunk {
    background: #4CC38A;
    border-radius: 5px;
}

QProgressBar[health="bloodied"]::chunk {
    background: #F2B24C;
}

QProgressBar[health="critical"]::chunk {
    background: #FF5C5C;
}
QLabel#healthTag {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 9px;
}

QLabel#healthTag[health="bloodied"] {
    background: #3A2E17;
    color: #F2B24C;
}

QLabel#healthTag[health="critical"] {
    background: #3A1F22;
    color: #FF8C8C;
}

QLabel#healthTag[health="down"] {
    background: #ECEAF4;
    color: #111117;
}
QToolButton#menuButton {
    background: transparent;
    color: #ECEAF4;
    border: 1px solid #2E2E3B;
    border-radius: 10px;
    font-size: 18px;
    font-weight: 700;
    min-width: 36px;
    min-height: 32px;
}

QToolButton#menuButton:hover {
    background: #2A2A36;
}

QToolButton#menuButton::menu-indicator {
    image: none;
    width: 0;
}

QMenu {
    background: #1E1E28;
    color: #ECEAF4;
    border: 1px solid #34343F;
    border-radius: 10px;
    padding: 6px;
}

QMenu::item {
    padding: 8px 18px;
    border-radius: 6px;
}

QMenu::item:selected {
    background: #2A2A36;
}

QMenu::item:disabled {
    color: #5C5A6B;
}
"""


def apply_theme(app: QApplication) -> None:
    """
    Applies the Raven night theme to the whole application.
    """
    app.setStyleSheet(RAVEN_STYLESHEET)