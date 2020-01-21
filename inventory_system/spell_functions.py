from world import World
from components.intent_components import WantsToCastSpellComponent


def cast_spell(entity_id, target_position):
    player = World.fetch('player')
    use_intent = WantsToCastSpellComponent(entity_id, target_position)
    World.add_component(use_intent, player)
