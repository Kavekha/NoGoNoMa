from systems.system import System
from world import World
from data.load_raws import RawsMaster
from components.character_components import PlayerComponent
from components.magic_item_components import IdentifiedItemComponent
from components.name_components import NameComponent, ObfuscatedNameComponent
from components.items_component import ItemComponent


class ItemIdentificationSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(PlayerComponent, IdentifiedItemComponent)
        master_dungeon = World.fetch('master_dungeon')

        for entity, (_player, identified) in subjects:
            if identified not in master_dungeon.identified_items and RawsMaster.is_tag_magic(identified.name):
                master_dungeon.identified_items.add(identified.name)

                for entity_item, (_item, name) in World.get_components(ItemComponent, NameComponent):
                    if name.name == identified.name:
                        World.remove_component(ObfuscatedNameComponent, entity_item)

            World.remove_component(IdentifiedItemComponent, entity)
