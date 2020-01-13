from systems.system import System
from world import World
from components.equip_components import EquipmentChanged, EquippedComponent
from components.item_components import ItemAttributeBonusComponent
from components.character_components import AttributesComponent


class EquipmentChange(System):
    """ EquipementChanged is put on Entity when changing their stuff."""
    def update(self, *args, **kwargs):
        subjects = World.get_components(EquipmentChanged)

        entity_to_update = list()
        for entity, (_equipment_dirty, *args) in subjects:
            entity_to_update.append(entity)

        World.remove_component_for_all_entities(EquipmentChanged)

        entities_attributes_bonus = dict()
        subjects = World.get_components(EquippedComponent, ItemAttributeBonusComponent)
        for item, (item_equipped, item_bonus) in subjects:
            if item_equipped.owner in entity_to_update:
                if entities_attributes_bonus.get(entity_to_update):
                    entities_attributes_bonus[entity_to_update]['might'] += item_bonus.might
                    entities_attributes_bonus[entity_to_update]['body'] += item_bonus.body
                    entities_attributes_bonus[entity_to_update]['quickness'] += item_bonus.quickness
                    entities_attributes_bonus[entity_to_update]['wits'] += item_bonus.wits
                else:
                    entities_attributes_bonus[entity_to_update] = dict()
                    entities_attributes_bonus[entity_to_update]['might'] = item_bonus.might
                    entities_attributes_bonus[entity_to_update]['body'] = item_bonus.body
                    entities_attributes_bonus[entity_to_update]['quickness'] = item_bonus.quickness
                    entities_attributes_bonus[entity_to_update]['wits'] = item_bonus.wits

        for entity in entity_to_update:
            entity_attr = World.get_entity_component(entity, AttributesComponent)
            if entity_attr and entities_attributes_bonus.get(entity):
                entity_attr.might.bonus_value = entity_attr.might.value + entities_attributes_bonus[entity].get(
                    'might', 0)
                entity_attr.body.bonus_value = entity_attr.body.value + entities_attributes_bonus[entity].get(
                    'body', 0)
                entity_attr.quickness.bonus_value = entity_attr.quickness.value + entities_attributes_bonus[entity].get(
                    'quickness', 0)
                entity_attr.wits.bonus_value = entity_attr.wits.value + entities_attributes_bonus[entity].get(
                    'wits', 0)




