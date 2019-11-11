from node import Node
from libs.struct_helper import VmMap
from libs.parse_helper import get_obj, get_lane_v01, get_node_v01


class VMLoader:
    """
            Загружает файл с векторной картой и формирует структуры с которыми работает планировщик
    """

    def __init__(self):
        self.laneID = 0
        self.nodeID = 0
        self.vm_map = VmMap()

    def read_file_v01(self, file_object):

        data = get_obj(file_object)

        while data:
            if data[1] == "LANE":
                lane = get_lane_v01(file_object, self.laneID)
                self.laneID += 1
                self.vm_map.lanes.append(lane)
                data = get_obj(file_object)

            elif data[1] == "NODE":
                node = get_node_v01(file_object, self.nodeID, self.vm_map.lanes)
                self.nodeID += 1
                self.vm_map.nodes.append(node)
                data = get_obj(file_object)

            else:
                print("The format is not supported")
                break


    def create_map(self):
        available = 1

        exit_flag = False
        for u_node in self.vm_map.nodes:
            for output_lane in u_node.out_lane_id_array:
                for v_node in self.vm_map.nodes:
                    for input_lane in v_node.in_lane_id_array:

                        if output_lane == input_lane:
                            edge = [u_node.obj_id, v_node.obj_id, self.vm_map.lanes[output_lane].length, available]
                            self.vm_map.graph.append(edge)
                            exit_flag = True
                            break

                    if (exit_flag):
                        exit_flag = False
                        break

    def read_file(self, filepath):

        # open the file and read through it line by line
        with open(filepath, 'r') as file_object:
            line = file_object.readline()
            x = line.split("#")
            if float(x[4]) == 0.1:
                self.read_file_v01(file_object)

        self.create_map()

        return self.vm_map


if __name__ == '__main__':
    file_path = '..\\data\\MiniPolygonGraph.namivm'
    vml = VMLoader()
    data = vml.read_file(file_path)
    print(data)
