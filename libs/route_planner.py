# в настроках проекта в PyCharm узал папку lib/ford-bellman как source
from ford_bellman import Graph

class route_planner:

    def load_map(self, route_map):
        self.map = route_map


#  Представляем карту в виде графа
g = Graph(8) # number of vertices

g.addEdge(0, 1, 5)
g.addEdge(1, 2, 2)
g.addEdge(2, 3, 7.14)
g.addEdge(2, 5, 39.6)
g.addEdge(3, 4, 2)
g.addEdge(1, 2, 2)
g.addEdge(4, 5, 10.14)
g.addEdge(4, 7, 18)
g.addEdge(5, 6, 5)
g.addEdge(7, 5, 38.7)

# Начинаем движение из узла 0 и ищем путь до узла 6. Для этого выполняем алгоритм Беллмана-Форда и находим все
# кратчайшие пути от узла 0 до всех других узлов. Здесь мы получаем массив предков в котором порядковый номер
# элемента соответствует номеру узла, а содержащееся значение говорит о предшественнике.

predecessor_array = g.BellmanFord(2)
print(predecessor_array)

# Затем восстанавливем путь по графу от узла 0 до 6. TODO Прежде чем получить путь, нужно убедиться в его доступности

def get_path(dist, predecessor_array):
    path = []
    reached = False

    current = dist
    while not reached:
        path.append(current)
        current = predecessor_array[current]

        if current == -1:
            reached = True

    path.reverse()
    return path


print("Path: ", get_path(5, predecessor_array))



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