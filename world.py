from systems.system import System


class World:
    _next_available_id = 0
    _entities = {}
    _components = {}
    _systems = []
    _ressources = {}

    @classmethod
    def add_component(cls, component_instance, entity_id):
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
