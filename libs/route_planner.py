# в настроках проекта в PyCharm юзал папку lib/bellman-ford как source
from bellman_ford import Graph

class route_planner:

    def __init__(self):
        self.map = {'vertex': [],
                     'node' : 0}
        self.r_map = {'vertex': [],
                    'node': 0}
        self.g = 0  #TODO переделать класс Graph, чтобы можно было создать объект
        self.current_pose = -1
        self.destination_pose = -1
        self.direct_velocity = 40 / 3.6  # тактов/лапоть
        self.reverse_velocity = 5 / 3.6   # тактов/лапоть

    def create_map(self, map):
        #  Представляем карту в виде графа
        self.g = Graph(map['node'])
        for i in range(len(map['vertex'])):
            u = map['vertex'][i][0]
            v = map['vertex'][i][1]
            w = map['vertex'][i][2]
            self.g.addEdge(u, v, w)

    def create_reverse_map(self):
        self.r_map = self.map.copy()

        for i in range(len(self.r_map['vertex'])):
            self.r_map['vertex'][i][0], self.r_map['vertex'][i][1] \
                = self.r_map['vertex'][i][1], self.r_map['vertex'][i][0]


    def load_map(self, route_map):
        # TODO Здесь нет проверки вменяемости карты
        self.map = route_map
        self.create_map(self.map)
        self.create_reverse_map()

    def set_current_pose(self, pose):
        self.current_pose = pose

    def set_destination_point(self, dest):
        self.destination_pose = dest

    def find_predecessors(self, node):
        predecessors = []
        for i in range(len(self.map['vertex'])):
            if self.map['vertex'][i][1] == node:
                predecessors.append(self.map['vertex'][i][0])
        return predecessors

    def find_common_elements(self, list):
        # convert list of list to list of sets
        sets = map(set, list)

        # perform intersection on each set present in list
        common_elements = set.intersection(*sets)

        return common_elements

    def get_path(self):
        # Начинаем движение из узла current_pose и ищем путь до узла destination_pose. Для этого выполняем алгоритм
        # Беллмана-Форда и находим все кратчайшие пути от узла current_pose до всех других узлов. Здесь мы получаем
        # массив предков в котором порядковый номер элемента соответствует номеру узла,
        # а содержащееся значение говорит о предшественнике.
        pred_and_distance_array = self.g.BellmanFord(self.current_pose)

        path = []
        # Прежде чем вернуть путь до точки назначение, нужно убедиться в ее доступности.
        if pred_and_distance_array[0][self.destination_pose] != -1:

            # Затем восстанавливем путь по графу от узла current_pose до destination_pose.
            reached = False

            current = self.destination_pose
            while not reached:
                path.append(current)
                current = pred_and_distance_array[0][current]

                if current == -1:
                    reached = True

            path.reverse()
            return path
            state = 'Direct route is found'
        else:

            # сбрасываю старую карту и загружаю обратную карту
            #TODO количество вершин НЕ обновляется!
            self.g.reset_map()
            self.create_map(self.r_map)

            pred_and_distance_array = self.g.BellmanFord(self.current_pose)

            src_pred = []
            for i in range(len(pred_and_distance_array[0])):
                if pred_and_distance_array[0][i] != -1:
                    src_pred.append(i)


            pred_and_distance_target = self.g.BellmanFord(self.destination_pose)

            target_pred = []
            for i in range(len(pred_and_distance_target[0])):
                if pred_and_distance_target[0][i] != -1:
                    target_pred.append(i)


            common_elements = list(self.find_common_elements([src_pred, target_pred]))
            print(common_elements)

            node_number = -1
            weight = float("Inf")
            for item in common_elements:
                if item != -1:  # в общем списке содержится -1

                    reverse_weight = pred_and_distance_array[1][item] / self.reverse_velocity
                    direct_weith = pred_and_distance_target[1][item] / self.direct_velocity
                    local_weight = reverse_weight + direct_weith
                    if (local_weight) < weight:
                        node_number = item
                        weight = local_weight

            print(node_number)



        #     predecessor = []
        #     reverse_path = []
        #
        #     pred = self.find_predecessors(self.current_pose)
        #     predecessor.extend(pred)
        #
        #     reverse_path.append(self.current_pose)
        #     for node in predecessor:
        #
        #         predecessor_array = self.g.BellmanFord(self.destination_pose)
        #
        #         # Затем восстанавливем путь по графу от узла current_pose до destination_pose.
        #         reached = False
        #
        #         current = self.current_pose
        #         while not reached:
        #             path.append(current)
        #             current = predecessor_array[current]
        #
        #             if current == -1:
        #                 reached = True
        #
        #         path.reverse()
        #         state = 'Direct route is not found'
        #
        #
        # output = [state, path]
        # return output





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