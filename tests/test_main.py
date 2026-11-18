from combat_raven.main import build_window


def test_app_starts_with_an_empty_combat(qtbot, tmp_path):
    window = build_window(tmp_path)
    qtbot.addWidget(window)

    assert window.combat.combatants == []
    assert not window.combat.started
    assert window.combat_repository is not None