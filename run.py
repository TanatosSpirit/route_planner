from libs.global_path_planner import global_route_planner

test_map = [[0, 1, 5],
            [1, 2, 2],
            [2, 3, 7.14],
            [2, 5, 39.6],
            [3, 4, 2],
            [1, 2, 2],
            [4, 5, 10.14],
            [4, 7, 18],
            [5, 6, 5],
            [7, 5, 38.7]]

grp = global_route_planner()

grp.load_map(test_map)