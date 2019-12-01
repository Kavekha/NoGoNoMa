from systems.system import System


class World:
    _next_available_id = 1  # If 0, will return False when checking entity :D
    _entities = {}
    _components = {}
    _systems = []
    _ressources = {}

    @classmethod
    def get_next_available_id(cls):
        return cls._next_available_id

    @classmethod
    def add_component(cls, component_instance, entity_id):
        print(f'add component {component_instance} for entity {entity_id}')
        component_type = type(component_instance)
        # On enregistre les components
        try:
            cls._components[component_type].add(entity_id)
        except KeyError:
            cls._components[component_type] = set()
            cls._components[component_type].add(entity_id)
        # on enregistre les entités.
        try:
            cls._entities[entity_id][component_type] = component_instance
        except KeyError:
            cls._entities[entity_id] = dict()
            cls._entities[entity_id][component_type] = component_instance

    @classmethod
    def remove_component(cls, component_type, entity_id):
        try:
            cls._components[component_type].remove(entity_id)
        except KeyError:
            pass
        try:
            del cls._entities[entity_id][component_type]
        except:
            pass

    @classmethod
    def get_components(cls, *component_types):
        try:
            for entity in set.intersection(*[cls._components[component_type] for component_type in component_types]):
                yield entity, [cls._entities[entity][component_type] for component_type in component_types]
        except KeyError:
            pass

    @classmethod
    def create_entity(cls, *components):
        print(f'entity to create with following components : {components}')
        entity_id = cls._next_available_id
        for component in components:
            cls.add_component(component, entity_id)
            print(f'component add for the following entity : {entity_id}: {component}')
        cls._next_available_id += 1
        return entity_id

    @classmethod
    def delete_entity(cls, entity_id):
        for component in cls._entities[entity_id]:
            try:
                cls._components[component].remove(entity_id)
            except KeyError:
                pass
        del cls._entities[entity_id]

    @classmethod
    def add_system(cls, system):
        assert issubclass(system.__class__, System)
        system.main_system = cls
        cls._systems.append(system)

    @classmethod
    def remove_system(cls, system):
        cls._systems.remove(system)

    @classmethod
    def update(cls, *args, **kwargs):
        for system in cls._systems:
            system.update(*args, **kwargs)

    @classmethod
    def insert(cls, name, ressources):
        cls._ressources[name] = ressources

    @classmethod
    def fetch(cls, name):
        try:
            return cls._ressources[name]
        except KeyError:
            return False

    @classmethod
    def throw(cls, name):
        cls._ressources['name'] = None

    @classmethod
    def entity_has_component(cls, entity, component):
        try:
            if cls._entities[entity][component]:
                return True
            return False
        except:
            return False

    @classmethod
    def get_entity_component(cls, entity, component):
        if cls.entity_has_component(entity, component):
            return cls._entities[entity][component]

    @classmethod
    def get_all_systems(cls):
        return cls._systems

    @classmethod
    def get_all_entities(cls):
        return cls._entities

    @classmethod
    def get_all_ressources(cls):
        return cls._ressources

    @classmethod
    def override_next_id(cls, next_id):
        if next_id < cls._next_available_id:
            print('CRITICAL: next id reference change to a lower number. High risk of errors.')
        cls._next_available_id = next_id

    @classmethod
    def reset_all(cls):
        entities_to_delete = []
        for entity in cls._entities:
            entities_to_delete.append(entity)

        for entity in entities_to_delete:
            cls.delete_entity(entity)

        systems_to_remove = []
        for system in cls._systems:
            systems_to_remove.append(system)

        for system in systems_to_remove:
            cls.remove_system(system)

        ressource_to_delete = []
        for ressource in cls._ressources:
            ressource_to_delete.append(ressource)

        for ressource in ressource_to_delete:
            cls.throw(ressource)

        cls._next_available_id = 1  # If 0, will return False when checking entity :D

    @classmethod
    def reload_data(cls, data_file):
        print('------ RELOAD BEGINS ----------')
        next_id, systems_save, entities_save, ressources_save = data_file

        cls.override_next_id(next_id)

        entities_file = entities_save

        for entity, components in entities_file.items():
            print(f'------ entity {entity} ----------')
            for component_type, component_instance in components.items():
                cls.add_component(component_instance, entity)

        print('-----')

        ressources_file = ressources_save
        for ressource_name, ressource_content in ressources_file.items():
            cls.insert(ressource_name, ressource_content)

        # Player has to be updated, because entity player is not the same since we recreate everything.
        from components.player_component import PlayerComponent
        player_comp_list = cls.get_components(PlayerComponent)
        for entity, player in player_comp_list:
            # should have only one
            player = entity
            cls.insert('player', player)

        print('---------')

        systems_file = systems_save
        for system in systems_file:
            cls.add_system(system)

        print('----- END RELOAD -------')
        from components.position_component import PositionComponent
        player = cls.fetch('player')
        player_pos = cls.get_entity_component(player, PositionComponent)
        print(f'player is at {player_pos.x}, {player_pos.y} after reload')
