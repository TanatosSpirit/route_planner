from libs.route_planner import route_planner

test_map = {'vertex': [[0, 1, 5],
            [1, 2, 2],
            [2, 3, 7.14],
            [2, 5, 39.6],
            [3, 4, 2],
            [1, 2, 2],
            [4, 5, 10.14],
            [4, 7, 18],
            [5, 6, 5],
            [7, 5, 38.7]],
            'node': 8}

# создаем планировщик (запустили ROSноду)
rp = route_planner()

# загрузили карту (прослушали топик с векторной картой)
rp.load_map(test_map)

vehicle_pose = 5  # номер узла
# установили текущее положение ТС (прослушали топик с положением машины)
rp.set_current_pose(vehicle_pose)

destination_pose = 4  # номер узла
# указали куда нужно приехать
rp.set_destination_point(destination_pose)

# Получаем вывод о доступности точки назначени и маршрут до нее
route = rp.get_path()
print(route)