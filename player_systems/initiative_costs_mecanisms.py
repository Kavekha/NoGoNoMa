from components.initiative_components import InitiativeCostComponent
import config


def calculate_move_cost(user):
    """ return InitiativeCost with move cost"""
    print(f'user {user} move')
    return InitiativeCostComponent(config.DEFAULT_MOVE_INITIATIVE_COST)


def calculate_fight_cost(user):
    print(f'user {user} fight')
    return InitiativeCostComponent(config.DEFAULT_FIGHT_INITIATIVE_COST)


def wait_turn_cost(user):
    print(f'user {user} wait')
    return InitiativeCostComponent(config.DEFAULT_WAIT_INITIATIVE_COST)