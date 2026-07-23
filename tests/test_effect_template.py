from combat_raven.models.effect_template import EffectTemplate


def test_create_effect_template():

    bless = EffectTemplate(
        name="Bless",
        default_duration=10,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )

    assert bless.name == "Bless"
    assert bless.default_duration == 10
    assert bless.concentration is True

