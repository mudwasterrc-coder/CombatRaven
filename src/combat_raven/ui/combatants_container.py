from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from combat_raven.models.combatant import Combatant
from combat_raven.ui.combatant_widget import CombatantWidget


class CombatantsContainer(QWidget):
    """
    Container for combatant widgets.
    """
    drop_requested = Signal(Combatant,int)

    def __init__(self) -> None:
        super().__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event) -> None:
        """
        Accepts drag operations from combatant widgets.
        """
        if isinstance(event.source(), CombatantWidget):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:
        """
        Emits a request when a combatant widget is dropped.
        """
        widget = event.source()

        if not isinstance(widget, CombatantWidget):
            event.ignore()
            return

        index = self.drop_index_at(event.position())

        self.drop_requested.emit(
            widget.combatant,
            index,
        )

        event.acceptProposedAction()

    def drop_index_at(self, position) -> int:
        """
        Returns the layout index corresponding to a drop position.
        """
        layout = self.layout()

        if layout is None:
            return 0

        for index in range(layout.count()):
            widget = layout.itemAt(index).widget()

            if widget is None:
                continue

            if position.y() <= widget.geometry().center().y():
                return index

        return layout.count()