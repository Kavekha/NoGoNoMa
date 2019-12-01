from systems.system import System
from components.wants_use_item_component import WantsToUseComponent
from components.combat_stats_component import CombatStatsComponent
from components.provides_healing_component import ProvidesHealingComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.name_component import NameComponent
from components.consumable_component import ConsumableComponent
from components.suffer_damage_component import SufferDamageComponent
from components.area_effect_component import AreaOfEffectComponent
from components.viewshed_component import ViewshedComponent
from components.confusion_component import ConfusionComponent
from components.equippable_component import EquippableComponent
from components.equipped_component import EquippedComponent
from components.in_backpack_component import InBackPackComponent
from gmap.utils import xy_idx
from world import World
from texts import Texts
import config


class ItemUseSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToUseComponent, CombatStatsComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')
        for entity, (wants_to_use, stats, *args) in subjects:

            item_inflicts_dmg = World.get_entity_component(wants_to_use.item, InflictsDamageComponent)
            item_provides_healing = World.get_entity_component(wants_to_use.item, ProvidesHealingComponent)
            item_causes_confusion = World.get_entity_component(wants_to_use.item, ConfusionComponent)
            item_name = World.get_entity_component(wants_to_use.item, NameComponent)
            item_equippable = World.get_entity_component(wants_to_use.item, EquippableComponent)

            targets = []
            if wants_to_use.target:
                target_x, target_y = wants_to_use.target
                idx = xy_idx(target_x, target_y)
                current_map = World.fetch('current_map')
                aoe = World.get_entity_component(wants_to_use.item, AreaOfEffectComponent)

                if aoe:
                    blast_tiles_idx = []
                    view = World.get_entity_component(entity, ViewshedComponent)
                    radius = aoe.radius // 2
                    for y in range(- radius, radius + 1):
                        for x in range(- radius, radius + 1):
                            radius_x = target_x + x
                            radius_y = target_y + y
                            if view.visible_tiles[radius_y][radius_x]:
                                new_idx = xy_idx(radius_x, radius_y)
                                blast_tiles_idx.append(new_idx)
                    for tile in blast_tiles_idx:
                        for mob in current_map.tile_content[tile]:
                            targets.append(mob)
                else:
                    for mob in current_map.tile_content[idx]:
                        targets.append(mob)
            else:
                # not target
                targets.append(entity)

            for target in targets:
                target_name = World.get_entity_component(target, NameComponent)
                if World.get_entity_component(target, CombatStatsComponent):
                    if item_inflicts_dmg:
                        suffer_dmg = SufferDamageComponent(item_inflicts_dmg.damage)
                        World.add_component(suffer_dmg, target)
                        if entity == player:
                            logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]'
                                            f'{Texts.get_text("YOU_USE_ITEM").format(item_name.name, target_name.name)}'
                                            f'{Texts.get_text("_FOR_DMG").format(item_inflicts_dmg.damage)}'
                                            f'[/color]')

                    if item_provides_healing:
                        if entity == player:
                            stats.hp = min(stats.max_hp, stats.hp + item_provides_healing.healing_amount)
                            logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]{Texts.get_text("YOU_DRINK_ITEM").format(item_name.name)}'
                                            f'{Texts.get_text("YOU_ARE_HEAL_FOR").format(item_provides_healing.healing_amount)}[/color]')

                    if item_causes_confusion:
                        add_confusion = ConfusionComponent(item_causes_confusion.turns)
                        World.add_component(add_confusion, target)
                        if entity == player:
                            logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]'
                                            f'{Texts.get_text("YOU_USE_ITEM").format(item_name.name, target_name.name)}'
                                            f'{Texts.get_text("_CONFUSING_THEM")}')

            consumable = World.get_entity_component(wants_to_use.item, ConsumableComponent)
            if consumable:
                World.delete_entity(wants_to_use.item)

            if item_equippable:
                to_unequip = []
                if targets:
                    target = targets[0]
                else:
                    target = entity

                subjects = World.get_components(EquippedComponent, NameComponent)
                for item_entity, (already_equipped, name, *args) in subjects:
                    if already_equipped.owner == target and already_equipped.slot == item_equippable.slot:
                        to_unequip.append(item_entity)
                        if target == player:
                            logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                                            f'{Texts.get_text("YOU_UNEQUIP").format(name.name)}[/color]')

                for item_entity in to_unequip:
                    World.remove_component(EquippedComponent, item_entity)
                    backpack = InBackPackComponent(target)
                    World.add_component(backpack, item_entity)

                equipped = EquippedComponent(target, item_equippable.slot)
                World.add_component(equipped, wants_to_use.item)
                World.remove_component(InBackPackComponent, wants_to_use.item)
                if target == player:
                    item_name = World.get_entity_component(wants_to_use.item, NameComponent).name
                    logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                                    f'{Texts.get_text("YOU_EQUIP").format(item_name)}'
                                    f'[/color]')

            World.remove_component(WantsToUseComponent, entity)
