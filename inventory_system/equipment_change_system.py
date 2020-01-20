from systems.system import System
from world import World
from components.equip_components import EquipmentChangedComponent, EquippedComponent
from components.character_components import AttributesComponent, AttributeBonusComponent
from components.status_effect_components import StatusEffectComponent


class EquipmentChangeSystem(System):
    """ EquipementChanged is put on Entity when changing their stuff."""
    def update(self, *args, **kwargs):
        subjects = World.get_components(EquipmentChangedComponent)

        entity_to_update = list()
        for entity, (_equipment_dirty, *args) in subjects:
            entity_to_update.append(entity)

        World.remove_component_for_all_entities(EquipmentChangedComponent)

        entities_attributes_bonus = dict()
        subjects = World.get_components(AttributeBonusComponent)
        for entity, (attr_bonus, *args) in subjects:
            owner = False
            # item?
            item_equipped = World.get_entity_component(entity, EquippedComponent)
            if item_equipped:
                if item_equipped.owner in entity_to_update:
                    owner = item_equipped.owner
            # effect?
            status_effect = World.get_entity_component(entity, StatusEffectComponent)
            if status_effect:
                if status_effect.target in entity_to_update:
                    owner = status_effect.target

            if entity in entity_to_update:
                owner = entity

            if owner:
                if not entities_attributes_bonus.get(owner):
                    # creation du dict
                    entities_attributes_bonus[owner] = dict()
                    entities_attributes_bonus[owner]['might'] = 0
                    entities_attributes_bonus[owner]['body'] = 0
                    entities_attributes_bonus[owner]['quickness'] = 0
                    entities_attributes_bonus[owner]['wits'] = 0
                if attr_bonus.might:
                    entities_attributes_bonus[owner]['might'] += attr_bonus.might
                if attr_bonus.body:
                    entities_attributes_bonus[owner]['body'] += attr_bonus.body
                if attr_bonus.quickness:
                    entities_attributes_bonus[owner]['quickness'] += attr_bonus.quickness
                if attr_bonus.wits:
                    entities_attributes_bonus[owner]['wits'] += attr_bonus.wits

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
