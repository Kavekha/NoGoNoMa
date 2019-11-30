import shelve
import os


def has_saved_game():
    if not os.path.isfile('savegame.dat'):
        return False
    return True


def save_game(world):
    from world import World
    from components.position_component import PositionComponent
    player = world.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)
    print(f'player is at {player_pos.x}, {player_pos.y} at save')

    with shelve.open('savegame', 'n') as data_file:

        data_file['systems'] = world.get_all_systems()
        data_file['entities'] = world.get_all_entities()
        data_file['ressources'] = world.get_all_ressources()

        print(f'save: data file ressources is {data_file["ressources"]}')
        print(f'save: data file entities is {data_file["entities"]}')


def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame', 'r') as data_file:
        systems = data_file['systems']
        entities = data_file['entities']
        ressources = data_file['ressources']
    return systems, entities, ressources