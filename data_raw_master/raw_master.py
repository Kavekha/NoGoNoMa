from data_raw_master.raw_compendium import RawCompendium

from components.position_components import PositionComponent
from components.name_components import NameComponent, ObfuscatedNameComponent
from components.renderable_component import RenderableComponent
from components.provide_effects_components import ProvidesHealingComponent, ProvidesCurseRemovalComponent, \
    ProvidesIdentificationComponent, ProvidesManaComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.ranged_component import RangedComponent
from components.area_effect_component import AreaOfEffectComponent
from components.status_effect_components import ConfusionComponent, DurationComponent, SlowSpellEffect, \
    DamageOverTimeEffect
from components.item_components import ItemComponent, MeleeWeaponComponent, WearableComponent, ConsumableComponent
from components.equip_components import EquippableComponent
from components.blocktile_component import BlockTileComponent, BlockVisibilityComponent
from components.viewshed_component import ViewshedComponent
from components.character_components import AttributesComponent, MonsterComponent, AttributeBonusComponent
from components.skills_component import SkillsComponent
from components.pools_component import Pools
from components.ability_components import NaturalAttackDefenseComponent, NaturalAttack, AbilitiesComponent, Ability
from components.magic_item_components import MagicItemComponent, CursedItemComponent
from components.hidden_component import HiddenComponent
from components.triggers_components import EntryTriggerComponent, ActivationComponent
from components.door_component import DoorComponent
from components.initiative_components import InitiativeComponent
from components.particule_components import SpawnParticuleBurstComponent, SpawnParticuleLineComponent
from components.spell_components import SpellTemplate, TeachesSpell

from data.random_table import RandomTable
from player_systems.game_system import npc_hp_at_lvl, mana_point_at_level
from data.components_enum import EquipmentSlots, WeaponAttributes, MagicItemClass
from world import World
import config


class RawsMaster:
    """ Utilisé pour créer les entités sur la base des infos du RawCompendium"""
    @staticmethod
    def get_spawn_table_for_depth(depth):
        table_depth = RandomTable()
        for table in RawCompendium.spawn_table:
            available_spawns = []
            for entry in table.spawn_infos:
                mind, maxd = table.spawn_infos[entry].get('min_depth', 0), table.spawn_infos[entry].get('max_depth', 0)
                if mind <= depth <= maxd:
                    available_spawns.append((entry, table.spawn_infos[entry].get('weight', 0)))

            if available_spawns:
                for spawn, weight in available_spawns:
                    table_depth.add(spawn, weight)

        for entry in table_depth.entries:
            print(f'- {entry.name}, {entry.weight}')

        return table_depth

    @staticmethod
    def spawn_named_spell(name):
        print(f'name is {name}')
        if RawCompendium.spell_index.get(name):
            template = RawCompendium.spells[RawCompendium.spell_index.get(name) - 1]
            print(f'template is {template}')
            effects = RawsMaster.apply_effects(template.get("effects"))
            spell = World.create_entity(SpellTemplate(mana_cost=template.get("mana_cost", 0)),
                                        NameComponent(name=template.get("name"))
                                        )
            for effect in effects:
                World.add_component(effect, spell)

    @staticmethod
    def spawn_all_spells():
        for spell in RawCompendium.spells:
            RawsMaster.spawn_named_spell(spell.get('name'))

    @staticmethod
    def spawn_named_entity(name, x, y):
        print(f'------ spawn something')
        print(f'spawn name entity: {name},'
              f' \n index item is {RawCompendium.item_index} \n index mob is {RawCompendium.mob_index}')
        if RawCompendium.item_index.get(name):
            return RawsMaster.create_item(name, x, y)
        if RawCompendium.mob_index.get(name):
            return RawsMaster.create_mob(name, x, y)
        if RawCompendium.props_index.get(name):
            return RawsMaster.create_prop(name, x, y)
        else:
            print(f'WARNING : Name entity not found : {name}')
        return

    @staticmethod
    def create_prop(name, x, y):
        to_create = RawCompendium.props[RawCompendium.props_index[name] - 1]
        components_for_entity = list()

        if to_create.get("name"):
            components_for_entity.append(NameComponent(to_create.get("name")))

        if to_create.get("renderable"):
            components_for_entity.append(RenderableComponent(glyph=to_create["renderable"].get('glyph'),
                                                             char_color=to_create["renderable"].get('fg'),
                                                             render_order=to_create["renderable"].get('order'),
                                                             sprite=to_create["renderable"].get('sprite')
                                                             ))

        if to_create.get("hidden"):
            components_for_entity.append(HiddenComponent())

        if to_create.get("entry_trigger"):
            components_for_entity.append(EntryTriggerComponent())
            if to_create['entry_trigger'].get('effects'):
                if to_create['entry_trigger']['effects'].get('damage'):
                    damage = InflictsDamageComponent(int(to_create['entry_trigger']['effects'].get('damage')))
                    components_for_entity.append(damage)
                if to_create['entry_trigger']['effects'].get('activations'):
                    activations = ActivationComponent(int(to_create['entry_trigger']['effects'].get('activations')))
                    components_for_entity.append(activations)

        if to_create.get("blocks_tile"):
            components_for_entity.append(BlockTileComponent())

        if to_create.get('blocks_visibility'):
            components_for_entity.append(BlockVisibilityComponent())

        if to_create.get('door_close'):
            components_for_entity.append(DoorComponent(to_create.get('door_close')))

        prop_id = World.create_entity(PositionComponent(x, y))

        for component in components_for_entity:
            World.add_component(component, prop_id)

    @staticmethod
    def create_mob(name, x, y):
        to_create = RawCompendium.mobs[RawCompendium.mob_index[name] - 1]

        components_for_entity = list()
        components_for_entity.append(MonsterComponent())
        components_for_entity.append(InitiativeComponent(config.BASE_MONSTER_INITIATIVE))

        if to_create.get("name"):
            components_for_entity.append(NameComponent(to_create.get("name")))

        if to_create.get('renderable'):
            renderable = to_create.get('renderable')
            components_for_entity.append(RenderableComponent(glyph=renderable.get('glyph'),
                                                             char_color=renderable.get('fg'),
                                                             render_order=renderable.get('order'),
                                                             sprite=renderable.get('sprite')
                                                             )
                                         )

        if to_create.get('blocks_tile'):
            components_for_entity.append(to_create.get('blocks_tile'))

        if to_create.get('vision_range'):
            components_for_entity.append(ViewshedComponent(to_create.get('vision_range')))

        if to_create.get('attributes'):
            attributes = to_create.get('attributes')
            mob_attr = AttributesComponent(might=attributes.get('might', 1),
                                           body=attributes.get('body', 1),
                                           quickness=attributes.get('quickness', 1),
                                           wits=attributes.get('wits', 1)
                                           )
            components_for_entity.append(mob_attr)

            # attributes needed for pv & mana
            if to_create.get('lvl'):
                mob_lvl = to_create.get('lvl')
            else:
                mob_lvl = 1
            mob_hp = npc_hp_at_lvl(mob_attr.body, mob_lvl)
            mob_mana = mana_point_at_level(mob_attr.wits,
                                           mob_lvl)

            components_for_entity.append(Pools(mob_hp, mob_mana, mob_lvl))

        if to_create.get('skills'):
            skills = to_create.get('skills')
            skill_component = SkillsComponent()
            for skill in skills:
                skill_component.skills[skill] = skills[skill]
            components_for_entity.append(skill_component)

        if to_create.get('natural'):
            natural = to_create.get('natural')
            natural_def_attack_component = NaturalAttackDefenseComponent(natural.get('armor', 0))

            attacks = natural.get('attacks')
            if attacks:
                for attack in attacks:
                    attack_to_create = RawCompendium.natural_attacks[RawCompendium.natural_attacks_index[attack] - 1]
                    natural_attack = NaturalAttack(
                        attack_to_create.get('name', 'Unknown attack'),
                        attack_to_create.get('attribute', WeaponAttributes.MIGHT),
                        attack_to_create.get('min_dmg', config.DEFAULT_MIN_DMG),
                        attack_to_create.get('max_dmg', config.DEFAULT_MAX_DMG),
                        attack_to_create.get('dmg_bonus', 0),
                        attack_to_create.get('hit_bonus', 0)
                    )
                    natural_def_attack_component.attacks.append(natural_attack)
            components_for_entity.append(natural_def_attack_component)

        if to_create.get('abilities'):
            abilities_component = AbilitiesComponent()
            for ability in to_create.get("abilities"):
                ability_component = Ability(ability.get('spell'),
                                            ability.get('chance'),
                                            ability.get('range'),
                                            ability.get('min_range'))
                abilities_component.abilities.append(ability_component)
            components_for_entity.append(abilities_component)

        mob_id = World.create_entity(PositionComponent(x, y))

        for component in components_for_entity:
            print(f'CREATE MOB: Component : {component}')
            World.add_component(component, mob_id)

        return True

    @staticmethod
    def create_item(name, x, y):
        to_create = RawCompendium.items[RawCompendium.item_index[name] - 1]

        components_for_entity = [ItemComponent()]

        if to_create.get('name'):
            components_for_entity.append(NameComponent(to_create.get('name')))

        if to_create.get('renderable'):
            renderable = to_create.get('renderable')
            components_for_entity.append(RenderableComponent(glyph=renderable.get('glyph'),
                                                             char_color=renderable.get('fg'),
                                                             render_order=renderable.get('order'),
                                                             sprite=renderable.get('sprite')
                                                             )
                                         )

        if to_create.get('consumable'):
            consumable_comp = ConsumableComponent()
            consumable_dic = to_create.get('consumable')

            if consumable_dic.get('effects'):
                effect_components = RawsMaster.apply_effects(consumable_dic.get('effects'))

                for effect_component in effect_components:
                    components_for_entity.append(effect_component)

            if consumable_dic.get('charges'):
                consumable_comp.charges = consumable_dic.get('charges', 1)

            components_for_entity.append(consumable_comp)

        if to_create.get('weapon'):
            weapon = to_create.get('weapon')
            components_for_entity.append(EquippableComponent(EquipmentSlots.MELEE))

            weap_attribute = weapon.get('attribute', WeaponAttributes.MIGHT)
            weap_min_dmg = weapon.get('min_dmg')
            weap_max_dmg = weapon.get('max_dmg')
            weap_dmg_bonus = weapon.get('dmg_bonus')
            weap_hit_bonus = weapon.get('hit_bonus')
            weap_proc_chance = weapon.get('proc_chance', 0)
            weap_proc_target = weapon.get('proc_target', 0)
            weap_proc_effects = weapon.get('proc_effects')

            components_for_entity.append(MeleeWeaponComponent(weap_attribute, weap_min_dmg,
                                                              weap_max_dmg, weap_dmg_bonus, weap_hit_bonus,
                                                              weap_proc_chance, weap_proc_target))

            if weap_proc_effects:
                effects_list = RawsMaster.apply_effects(weap_proc_effects)
                for effect in effects_list:
                    components_for_entity.append(effect)

        if to_create.get('wearable'):
            wearable = to_create.get('wearable')
            components_for_entity.append(EquippableComponent(wearable.get('slot')))

            if wearable.get('armor'):
                components_for_entity.append(WearableComponent(wearable.get('armor')))

        if to_create.get('magic'):
            magic = to_create.get('magic')
            identified_items = World.fetch('master_dungeon').identified_items
            magic_class = magic.get('class', MagicItemClass.COMMON)
            magic_naming_convention = magic.get('naming')
            magic_cursed = magic.get('cursed', False)

            # si nom inconnu, on utilise l'obfuscation
            print(f'create magic item: name is {name}')
            if name not in identified_items:
                if magic_naming_convention == 'scroll':
                    scroll_names = World.fetch('master_dungeon').scroll_mappings
                    components_for_entity.append(ObfuscatedNameComponent(scroll_names.get(name)))
                elif magic_naming_convention == 'potion':
                    print(f'create magic item potion: name is {name}')
                    potion_names = World.fetch('master_dungeon').potion_mappings
                    print(f'create magic potion potion names get :  {potion_names.get(name)} ')
                    components_for_entity.append(ObfuscatedNameComponent(potion_names.get(name)))
                else:
                    components_for_entity.append(ObfuscatedNameComponent(magic_naming_convention))

            components_for_entity.append(MagicItemComponent(magic_class=magic_class,
                                                            naming=magic_naming_convention,
                                                            cursed=magic_cursed))

            if magic_cursed:
                components_for_entity.append(CursedItemComponent())

        if to_create.get('attributes'):
            attributes = to_create.get('attributes')
            components_for_entity.append(AttributeBonusComponent(
                might=attributes.get('might'),
                body=attributes.get('body'),
                quickness=attributes.get('quickness'),
                wits=attributes.get('wits')
            ))

        item_id = World.create_entity(PositionComponent(x, y))
        for component in components_for_entity:
            World.add_component(component, item_id)

        return True

    @staticmethod
    def apply_effects(effects):
        effects_list = list()
        if effects.get('provides_healing'):
            effects_list.append(ProvidesHealingComponent(effects.get('provides_healing')))

        if effects.get('provides_mana'):
            effects_list.append(ProvidesManaComponent(effects.get('provides_mana')))

        if effects.get('damage'):
            effects_list.append(InflictsDamageComponent(effects.get('damage')))

        if effects.get('ranged'):
            effects_list.append(RangedComponent(effects.get('ranged')))

        if effects.get('area_of_effect'):
            effects_list.append(AreaOfEffectComponent(effects.get('area_of_effect')))

        if effects.get('confusion'):
            effects_list.append(ConfusionComponent())
            effects_list.append(DurationComponent(effects.get('confusion')))

        if effects.get('particule'):
            particule_infos = effects.get('particule')
            effects_list.append(SpawnParticuleBurstComponent(particule_infos['glyph'],
                                                                      particule_infos['color'],
                                                                      particule_infos['sprite']))

        if effects.get('particule_line'):
            particule_infos = effects.get('particule_line')
            effects_list.append(SpawnParticuleLineComponent(particule_infos['glyph'],
                                                                     particule_infos['color'],
                                                                     particule_infos['sprite']))

        if effects.get('remove_curse'):
            effects_list.append(ProvidesCurseRemovalComponent())

        if effects.get('identify'):
            effects_list.append(ProvidesIdentificationComponent())

        if effects.get('teach_spell'):
            effects_list.append(TeachesSpell(effects.get('teach_spell')))

        if effects.get('damage_over_time'):
            effects_list.append(DamageOverTimeEffect(effects.get('damage_over_time')))
            effects_list.append(DurationComponent(config.DEFAULT_DOT_DURATION))

        if effects.get('slow'):
            effects_list.append(SlowSpellEffect(initiative_penality=effects.get('slow', 0)))
            effects_list.append(DurationComponent(config.DEFAULT_SLOW_DURATION))

        return effects_list

    @staticmethod
    def get_scroll_tags():
        result = list()
        for item in RawCompendium.items:
            magic = item.get('magic')
            if magic:
                if magic.get('naming') == 'scroll':
                    result.append(item.get("name"))
        return result

    @staticmethod
    def get_potion_tags():
        result = list()
        for item in RawCompendium.items:
            magic = item.get('magic')
            if magic:
                if magic.get('naming') == 'potion':
                    result.append(item.get("name"))
        return result

    @staticmethod
    def is_tag_magic(tag):
        magic_tag = RawCompendium.item_index.get(tag)
        if magic_tag:
            item = RawCompendium.items[RawCompendium.item_index[tag] - 1]
            return item.get('magic')
        return False
