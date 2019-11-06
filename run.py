from libs.route_planner import route_planner
from test_map import test_map

# создаем планировщик (запустили ROS-ноду)
rp = route_planner()

# загрузили карту (прослушали топик с векторной картой)
rp.load_map(test_map)

vehicle_pose = 8  # номер узла
# установили текущее положение ТС (прослушали топик с положением машины)
rp.set_current_pose(vehicle_pose)

destination_pose = 6  # номер узла
# указали куда нужно приехать
rp.set_destination_point(destination_pose)

# Получаем вывод о доступности точки назначения и маршрут до нее
route = rp.get_path()
print(route)
