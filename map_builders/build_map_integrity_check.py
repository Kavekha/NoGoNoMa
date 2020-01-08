from tcod import tcod

import config


def test_builded_map(build_data):
    print(f'INTEGRITY TESTING')
    # Test 1: We can go from start to finish.
    path_from_start_to_finish = False
    # Test 2: Taille du chemin suffisant pour un parcours interressant. Sur du 80 / 50 en DLA, nous avons du 20 environ.
    distant_path_between_start_and_finish = False

    starting_position_x, starting_position_y = build_data.starting_position
    exit_position_x, exit_position_y = build_data.exit_position

    dij_path = tcod.path.Dijkstra(build_data.map.fov_map, 1.41)
    dij_path.set_goal(exit_position_x, exit_position_y)
    my_path = dij_path.get_path(starting_position_x, starting_position_y)

    if my_path:
        # test 1
        path_from_start_to_finish = True
        print(f'MAP INTEGRITY #1: Available path from Start to Exit.')

        # test 2
        if len(my_path) >= config.BUILDER_MIN_PATH_BETWEEN_START_EXIT_TEST:
            distant_path_between_start_and_finish = True
            print(f'MAP INTEGRITY #2: Long enough path between Start and Exit: {len(my_path)} tiles.')

    # check all tests
    if path_from_start_to_finish and distant_path_between_start_and_finish:
        print(f'map build integrity : TRUE')
        return True

    # fail requirements
    print(f'map build integrity : FALSE')
    return False
