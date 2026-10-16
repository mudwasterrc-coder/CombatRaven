from combat_raven.ui.concentration_dialog import ConcentrationDialog


def test_concentration_dialog_builds_template_from_inputs(qtbot):
    dialog = ConcentrationDialog()
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Bless")
    dialog.duration_input.setValue(10)

    template = dialog.create_template()

    assert template.name == "Bless"
    assert template.default_duration == 10
    assert template.concentration is True

def test_concentration_dialog_zero_rounds_means_no_limit(qtbot):
    dialog = ConcentrationDialog()
    qtbot.addWidget(dialog)

    dialog.name_input.setText("Hex")
    dialog.duration_input.setValue(0)

    assert dialog.duration_input.specialValueText() == "∞"
    assert dialog.create_template().default_duration is None