# в настроках проекта в PyCharm юзал папку lib/bellman-ford как source
# from bellman_ford import Graph
from bellman_ford_extended import Graph
import copy

class route_planner:

    def __init__(self):
        self.map = {'graph': [],
                    'lane' : [],
                     'node' : []}
        self.r_map = {'graph': [],
                    'lane': [],
                    'node': []}
        self.num_of_nodes = 0
        self.g = Graph()
        self.current_pose = -1
        self.destination_pose = -1
        self.direct_velocity = 40 / 3.6  # тактов/лапоть
        self.reverse_velocity = 5 / 3.6   # тактов/лапоть

    def create_map(self, vm_map):
        #  Представляем карту в виде графа
        self.g.set_num_vertices(self.num_of_nodes)
        for edge in vm_map['graph']:
            u = edge[0]
            v = edge[1]
            w = edge[2]
            a = edge[3]
            self.g.addEdge(u, v, w, a)

    def create_reverse_map(self):
        # TODO может лучше сделать флаг "Назад" для обработки алгоритмом поиска назад? Вместо копированиея карты
        self.r_map = copy.deepcopy(self.map)

        for edge in self.r_map['graph']:
            edge[0], edge[1] = edge[1], edge[0]


    def load_map(self, route_map):
        # TODO Здесь нет проверки вменяемости карты
        self.map = copy.deepcopy(route_map)
        self.num_of_nodes = len(route_map['node'])

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
            # TODO восстановление пути можно сделать проще или вынести в отдельный метод
            reached = False

            current = self.destination_pose
            while not reached:
                path.append(current)
                current = pred_and_distance_array[0][current]

                if current == -1:
                    reached = True

            path.reverse()
            state = 'Direct route is found'

            output = [state, path]
            return output
        else:

            # сбрасываю старую карту и загружаю обратную карту
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


            # TODO найти машрут от общей точки до src и dist

            self.g.reset_map()
            self.create_map(self.map)

            pred_and_distance_array = self.g.BellmanFord(node_number)

            # Затем восстанавливем путь по графу от узла current_pose до destination_pose.
            # TODO восстановление пути можно сделать проще или вынести в отдельный метод
            reached = False
            path_backward = []
            current = self.current_pose
            while not reached:
                path_backward.append(current)
                current = pred_and_distance_array[0][current]

                if current == -1:
                    reached = True


            # Затем восстанавливем путь по графу от узла current_pose до destination_pose.
            # TODO восстановление пути можно сделать проще или вынести в отдельный метод
            reached = False

            current = self.destination_pose
            while not reached:
                path.append(current)
                current = pred_and_distance_array[0][current]

                if current == -1:
                    reached = True



            path.reverse()


            state = 'Direct route is not found'

            output = [state, path_backward, path]
            return output
