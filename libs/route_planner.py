# в настроках проекта в PyCharm узал папку lib/ford-bellman как source
from ford_bellman import Graph

class route_planner:

    def __init__(self):
        self.map = {'vertex': [],
                     'node' : 0}
        self.g = 0
        self.current_pose = -1
        self.destination_pose = -1

    def create_map(self):
        #  Представляем карту в виде графа
        self.g = Graph(self.map['node'])
        for i in range(len(self.map['vertex'])):
            u = self.map['vertex'][i][0]
            v = self.map['vertex'][i][1]
            w = self.map['vertex'][i][2]
            self.g.addEdge(u, v, w)

    def load_map(self, route_map):
        #TODO Здесь нет проверки вменяемости карты
        self.map = route_map
        self.create_map()

    def set_current_pose(self, pose):
        self.current_pose = pose

    def set_destination_point(self, dest):
        self.destination_pose = dest

    def get_path(self):
        # Начинаем движение из узла current_pose и ищем путь до узла destination_pose. Для этого выполняем алгоритм
        # Беллмана-Форда и находим все кратчайшие пути от узла current_pose до всех других узлов. Здесь мы получаем
        # массив предков в котором порядковый номер элемента соответствует номеру узла,
        # а содержащееся значение говорит о предшественнике.
        predecessor_array = self.g.BellmanFord(self.current_pose)

        path = []
        # Прежде чем вернуть путь до точки назначение, нужно убедиться в ее доступности.
        if predecessor_array[self.destination_pose] != -1:

            # Затем восстанавливем путь по графу от узла 0 до 6.
            reached = False

            current = self.destination_pose
            while not reached:
                path.append(current)
                current = predecessor_array[current]

                if current == -1:
                    reached = True

            path.reverse()

            state = 'Route is found'
        else:
            state = 'Route is not found'

        output = [state, path]
        return output





# current_node = 2
# target_node = 0
#
# g = Graph(4)
# g.addEdge(0, 1, 8)
# g.addEdge(1, 2, 5)
# g.addEdge(2, 3, 8)
# g.addEdge(2, 0, 15)
# g.addEdge(3, 0, 5)
#
# searche = g.BellmanFord(current_node)
#
# achieved = False
# path = []
# path.append(target_node)
# next_node = target_node
# while not achieved:
#     path.append(searche[next_node])
#     next_node = searche[next_node]
#     if next_node == current_node:
#         achieved = True
#
# print(path)
# path = [0, 4, 3, 2]
#
#
# g = Graph(5)
# g.addEdge(0, 1, 8)
# g.addEdge(1, 2, 5)
# g.addEdge(2, 3, 8)
# g.addEdge(2, 0, 15)
# g.addEdge(3, 4, 2)
#
# new_current_node = 4
# pose = 1
#
# achievable = False
# while not achievable:
#     new_searche = g.BellmanFord(new_current_node)
#     if new_searche[target_node] == -1:
#         pose += 1
#         new_current_node = path[pose]
#     else:
#         achievable = True
#
# print(new_searche)