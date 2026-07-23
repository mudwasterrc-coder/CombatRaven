from combat_raven.models.effect import Effect
from combat_raven.models.effect_template import EffectTemplate

def test_create_effect_from_template():
    bless = EffectTemplate(
        name="Bless",
        default_duration=10,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )

    effect = Effect.from_template(bless)

    assert effect.template == bless
    assert effect.remaining_rounds == 10
    assert effect.concentration is True
    assert effect.enabled is True
    assert effect.notes == "+1d4 to attack rolls and saving throws"

def test_tick_reduces_remaining_rounds():
    template = EffectTemplate(
        name="Bless",
        default_duration=10,
        concentration=True,
        notes="+1d4 to attack rolls and saving throws",
    )

    effect = Effect.from_template(template)

    effect.tick()

    assert effect.remaining_rounds == 9