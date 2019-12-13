# coding=cp1251

# в настроках проекта в PyCharm юзал папку lib/bellman-ford как source
from libs.bellman_ford.bellman_ford_extended import Graph
from struct_helper import RelativeInfo, VmMap
import copy
import numpy as np

class route_planner:  # TODO rename class

    def __init__(self):
        self.vm_map = VmMap()
        self.r_vm_map = VmMap()
        self.g = Graph()
        self.current_pose = []
        self.destination_pose = []
        self.direct_velocity = 0   # тактов/лапоть
        self.reverse_velocity = 0    # тактов/лапоть

        self.src_relative = RelativeInfo()
        self.dist_relative = RelativeInfo()

        self.disconnect = False

    def settings(self, direct, reverse):
        self.direct_velocity = direct / 3.6
        self.reverse_velocity = reverse / 3.6

    def create_map(self, vm_map):
        #  Представляем карту в виде графа
        self.g.set_num_vertices(vm_map.num_of_nodes)
        for edge in vm_map.graph:
            u = edge[0]
            v = edge[1]
            w = edge[2]
            a = edge[3]
            self.g.addEdge(u, v, w, a)

    def create_reverse_map(self):
        # TODO может лучше сделать флаг "Назад" для обработки алгоритмом поиска назад? Вместо копированиея карты
        self.r_vm_map = copy.deepcopy(self.vm_map)

        for edge in self.r_vm_map.graph:
            edge[0], edge[1] = edge[1], edge[0]


    def load_map(self, vector_map):
        # TODO Здесь нет проверки вменяемости карты
        self.vm_map = copy.deepcopy(vector_map)

        self.create_map(self.vm_map)
        self.create_reverse_map()

    def set_current_pose(self, pose):
        self.current_pose = pose

    def set_destination_point(self, dest):
        self.destination_pose = dest

    def find_predecessors(self, node):
        # TODO не используется
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

    def compute_dif_angle(self):
        pass

    def find_nearest_node(self, direction, pose):
        # if direction == 'forward':
        #     pose = [self.current_pose[0], self.current_pose[1], self.current_pose[2]]
        # else:
        #     pose = [self.destination_pose[0], self.destination_pose[1], self.destination_pose[2]]

        nearest_wp = float("Inf")
        nearest_node = -1

        lane_id = 0
        for lane in self.vm_map.lanes:
            for i in range(len(lane.wp_array)):
                wp = lane.wp_array[i]
                dist = np.linalg.norm(np.array(pose) - np.array([wp[0], wp[1], wp[2]]))

                if dist < nearest_wp:

                    if direction == 'forward':
                        nearest_node = lane.identification[1]
                        self.src_relative.wp_id = i
                        self.src_relative.lane_id = lane_id
                        self.src_relative.nearest_wp = dist
                    else:
                        nearest_node = lane.identification[0]
                        self.dist_relative.wp_id = i
                        self.dist_relative.lane_id = lane_id
                        self.dist_relative.nearest_wp = dist

                    nearest_wp = dist




            lane_id += 1

        return nearest_node

    def get_path(self):
        pose = [self.current_pose[0], self.current_pose[1], self.current_pose[2]]
        self.src_relative.node_id = self.find_nearest_node('forward', pose)

        # Начинаем движение из узла current_pose и ищем путь до узла destination_pose. Для этого выполняем алгоритм
        # Беллмана-Форда и находим все кратчайшие пути от узла current_pose до всех других узлов. Здесь мы получаем
        # массив предков в котором порядковый номер элемента соответствует номеру узла,
        # а содержащееся значение говорит о предшественнике.
        pred_and_distance_array = self.g.BellmanFord(self.src_relative.node_id)

        path = []
        wps = []
        # Прежде чем вернуть путь до точки назначение, нужно убедиться в ее доступности.
        pose = [self.destination_pose[0], self.destination_pose[1], self.destination_pose[2]]
        self.dist_relative.node_id = self.find_nearest_node('backward', pose)

        if self.src_relative.nearest_wp > 4:
            state = 'Lane is too far'
            path = []
            wps = []

            output = [state, path, wps]
            return output

        if not self.disconnect:
        # if pred_and_distance_array[0][self.dist_relative.node_id] != -1:

            # Затем восстанавливем путь по графу от узла current_pose до destination_pose.
            # TODO восстановление пути можно сделать проще или вынести в отдельный метод
            reached = False

            current = self.dist_relative.node_id
            while not reached:
                path.append(current)
                current = pred_and_distance_array[0][current]

                if current == -1:
                    reached = True

            path.reverse()
            state = 'Direct route is found'

            for i in range(self.src_relative.wp_id, len(self.vm_map.lanes[self.src_relative.lane_id].wp_array)):
                wps.append(self.vm_map.lanes[self.src_relative.lane_id].wp_array[i])

            for lane in self.vm_map.lanes:
                for i in range(len(path)-1):
                    if lane.identification[0] == path[i] and lane.identification[1] == path[i+1]:
                        wps.extend(lane.wp_array)

            for i in range(0, self.dist_relative.wp_id):
                wps.append(self.vm_map.lanes[self.dist_relative.lane_id].wp_array[i])

            output = [state, path, wps]
            return output
        else:

            # сбрасываю старую карту и загружаю обратную карту
            self.g.reset_map()
            self.create_map(self.r_vm_map)

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

    def disconnect_node(self):
        self.disconnect = True

        pose = [self.current_pose[0], self.current_pose[1], self.current_pose[2]]

        next_node_id = self.find_nearest_node('forward', pose)
        prev_node_id = self.find_nearest_node('backward', pose)

        for edge in self.vm_map.graph:
            if edge[0]==prev_node_id and edge[1]==next_node_id:
                edge[3] = 0

        self.g.reset_map()
        self.create_map(self.vm_map)
        pass


