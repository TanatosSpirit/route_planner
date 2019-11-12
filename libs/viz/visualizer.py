from struct_helper import VmMap

import matplotlib.pyplot as plt
import copy
import math


class Visualizer:
    def __init__(self):
        self.figs = []
        self.vm_map = VmMap()

        self.x_wp = []
        self.y_wp = []
        self.z_wp = []

        self.x_node = []
        self.y_node = []
        self.z_node = []

        self.route_node = []

        self.x_node_route = []
        self.y_node_route = []
        self.z_node_route = []

        self.x_route = []
        self.y_route = []
        self.z_route = []

        self.vehicle_pose = []

    def show(self):
        plt.show()

    def new_fig(self):
        fig_graph, ax = plt.subplots(1, 1, sharex='all', sharey='all', figsize=(9, 9))
        self.figs.append([fig_graph, ax])

    def take_map(self, input_map):
        self.vm_map = copy.deepcopy(input_map)

        for lane in self.vm_map.lanes:
            x = [i[0] for i in lane.wp_array]
            y = [j[1] for j in lane.wp_array]
            z = [k[2] for k in lane.wp_array]
            w = [l[2] for l in lane.wp_array]

            self.x_wp.extend(x)
            self.y_wp.extend(y)
            self.z_wp.extend(z)

            for x, y, z, w in lane.wp_array:
                self.figs[-1][1].arrow(x, y, 0.5 * math.cos(w), 0.5 * math.sin(w), head_width=0.2, head_length=0.3, alpha=0.6)

        self.figs[-1][1].scatter(self.x_wp, self.y_wp, s=10, color='green')

        for node in self.vm_map.nodes:
            x = node.xyz[0]
            y = node.xyz[1]
            z = node.xyz[2]

            self.x_node.append(x)
            self.y_node.append(y)
            self.z_node.append(z)

            # Annotate the nodes
            self.figs[-1][1].annotate(node.obj_id,
                                      xy=(x, y), xycoords='data',
                                      xytext=(20, 20), textcoords='offset points', fontsize=16,
                                      arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

        self.figs[-1][1].scatter(self.x_node, self.y_node, s=50, color='green')



    def take_route(self, route):
        self.route_node = copy.deepcopy(route)
        # self.route_node = route.copy()

        x = [i[0] for i in self.route_node[2]]
        y = [j[1] for j in self.route_node[2]]
        z = [k[2] for k in self.route_node[2]]

        self.x_route.extend(x)
        self.y_route.extend(y)
        self.z_route.extend(z)

        self.figs[-1][1].scatter(self.x_route, self.y_route, s=10, color='red')

    def take_vehicle_pose(self, vehicle_pose):
        self.vehicle_pose = copy.deepcopy(vehicle_pose)
        # self.vehicle_pose = vehicle_pose.copy()

        x = self.vehicle_pose[0]
        y = self.vehicle_pose[1]
        z = self.vehicle_pose[2]
        w = self.vehicle_pose[3]


        self.figs[-1][1].scatter(x, y, s=20, color='blue')
        self.figs[-1][1].arrow(x, y, 0.5 * math.cos(w), 0.5 * math.sin(w), head_width=0.2, head_length=0.3, alpha=0.6)

if __name__ == '__main__':
    viz = Visualizer()
    viz.new_fig()
    viz.new_fig()
    viz.show()