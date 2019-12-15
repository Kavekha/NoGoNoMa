import shelve
import os


def has_saved_game():
    if not os.path.isfile('savegame.dat'):
        return False
    return True


def save_game(world):
    with shelve.open('savegame', 'n') as data_file:
        data_file['next_available_id'] = world.get_next_available_id()
        data_file['systems'] = world.get_all_systems()
        data_file['entities'] = world.get_all_entities()
        data_file['ressources'] = world.get_all_ressources()


def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame', 'r') as data_file:
        next_id = data_file['next_available_id']
        systems = data_file['systems']
        entities = data_file['entities']
        ressources = data_file['ressources']
    return next_id, systems, entities, ressources
