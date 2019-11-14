# coding=cp1251

from route_planner import route_planner
from test_map import test_map
from vmloader import VMLoader
from visualizer import Visualizer

test = False

viz = Visualizer()

# создаем планировщик (запустили ROS-ноду)
rp = route_planner()

# настраиваем параметы (запустили config)
rp.settings(40, 5) # км/ч

# создаем загрузчик карты (запустили ROS-ноду)
vml = VMLoader()

# загрузили карта из файла и получили структуру с файлом (создали топик с картой)
filepath = r'data/MiniPolygonGraph.namivm'
vm_map = vml.read_file(filepath)

viz.new_fig()
viz.take_map(vm_map)

# передали карту планировщику (прослушали топик с векторной картой)
if test == True:
    rp.load_map(test_map)
else:
    rp.load_map(vm_map)

vehicle_pose = [-26., -11., 42., 0]  # вектор положения в пространстве (x, y, z, азимут)
# установили текущее положение ТС (прослушали топик с положением машины)
rp.set_current_pose(vehicle_pose)
viz.take_vehicle_pose(vehicle_pose)

destination_pose = [16., 25., 0, 0]  # вектор положения в пространстве (x, y, z, азимут)
# указали куда нужно приехать
rp.set_destination_point(destination_pose)

# Получаем вывод о доступности точки назначения и маршрут(траекторию) до нее
route = rp.get_path() # TODO это набор путевых точек, что это? Траектория?
print(route[0], ": ", route[1])
viz.take_route(route)

viz.show()
