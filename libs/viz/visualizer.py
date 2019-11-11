import matplotlib.pyplot as plt
import copy


class Visualizer:
    def __init__(self):
        self.figs = []
        self.vm_map = {'graph': [],
                        'lane': [],
                        'node': []}
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

    def show(self):
        plt.show()

    def new_fig(self):
        fig_graph, ax = plt.subplots(1, 1, sharex='all', sharey='all', figsize=(9, 9))
        self.figs.append([fig_graph, ax])

    def take_map(self, vm_map):
        self.vm_map = copy.deepcopy(vm_map)

        for lane in self.vm_map['lane']:
            x = [i[0] for i in lane.wp_array]
            y = [j[1] for j in lane.wp_array]
            z = [k[2] for k in lane.wp_array]

            self.x_wp.extend(x)
            self.y_wp.extend(y)
            self.z_wp.extend(z)

        self.figs[-1][1].scatter(self.x_wp, self.y_wp, s=10, color='green')

        for node in self.vm_map['node']:
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
        self.route_node = route.copy()

        x = [i[0] for i in self.route_node[2]]
        y = [j[1] for j in self.route_node[2]]
        z = [k[2] for k in self.route_node[2]]

        self.x_route.extend(x)
        self.y_route.extend(y)
        self.z_route.extend(z)

        self.figs[-1][1].scatter(self.x_route, self.y_route, s=10, color='red')


if __name__ == '__main__':
    viz = Visualizer()
    viz.new_fig()
    viz.new_fig()
    viz.show()