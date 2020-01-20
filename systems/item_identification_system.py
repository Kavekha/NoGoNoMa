from systems.system import System
from world import World
from data_raw_master.raw_master import RawsMaster
from components.character_components import PlayerComponent
from components.magic_item_components import IdentifiedItemComponent
from components.name_components import NameComponent, ObfuscatedNameComponent
from components.item_components import ItemComponent


class ItemIdentificationSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(PlayerComponent, IdentifiedItemComponent)
        master_dungeon = World.fetch('master_dungeon')

        identified_to_remove = list()
        for entity, (_player, identified) in subjects:
            if identified not in master_dungeon.identified_items and RawsMaster.is_tag_magic(identified.name):
                master_dungeon.identified_items.add(identified.name)
                identified_to_remove.append(entity)
                # This proc every time you use an item already identified (Scroll Missile after identifing another)Why?
                '''
                logs = World.fetch('logs')
                logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                                f'{Texts.get_text("YOU_IDENTIFIED_")}'
                                f'{Texts.get_text(identified.name)}.')
                '''

                # Every identic item are now identified
                for entity_item, (_item, named) in World.get_components(ItemComponent, NameComponent):
                    if named.name == identified.name:
                        World.remove_component(ObfuscatedNameComponent, entity_item)

        for entity in identified_to_remove:
            World.remove_component(IdentifiedItemComponent, entity)
