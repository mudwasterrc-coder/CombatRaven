from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """
    Main application window for Combat Raven.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Combat Raven")
        self.resize(1000, 700)
        