from lane import Lane
from node import Node


class VMLoader:
    """
            Загружает файл с векторной картой и формирует структуры с которыми работает планировщик
    """

    def __init__(self):
        self.lane_obj_array = []
        self.node_obj_array = []
        self.laneID = 0
        self.nodeID = 0
        self.graph = []
        self.available = 1
        self.map = {'graph': [],
                    'lane' : [],
                    'node' : []}

    def read_file_v01(self, file_object):
        line = file_object.readline()

        line = line.lstrip("#")
        line = line.strip("\n")
        x = line.split("#")

        while line:
            if x[1] == "LANE":
                lane_obj = Lane()

                #NAME#Lane[13]
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                name = line.split("#")
                lane_obj.add_name(name[1])

                #ID#13
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                vm_obj = line.split("#")
                lane_obj.add_vm_id(int(vm_obj[1]))

                #self.laneID
                lane_obj.add_obj_id(self.laneID)
                self.laneID += 1

                #SPEED#5
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                speed = line.split("#")
                lane_obj.add_speed(int(speed[1]))

                #NUMBER_OF_POINTS#108
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                num_of_points = int(line.split("#")[1])
                lane_obj.add_num_of_points(num_of_points)

                for i in range(num_of_points):
                    line = file_object.readline()
                    line = line.strip("\n")
                    line = line.split(",")
                    x = float(line[0])
                    y = float(line[1])
                    z = float(line[2])
                    lane_obj.add_wp([x, y, z])

                self.lane_obj_array.append(lane_obj)

                line = file_object.readline()

                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")



            elif x[1] == "NODE":
                node_obj = Node()

                #NAME#Node[21]
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")
                node_obj.add_name(x[1])

                #ID#21
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")
                node_obj.add_vm_id(int(x[1]))

                #self.nodeID
                node_obj.add_obj_id(self.nodeID)
                self.nodeID += 1

                #XYZ
                line = file_object.readline()
                line = file_object.readline()
                line = line.strip("\n")
                line = line.split(",")
                x = float(line[0])
                y = float(line[1])
                z = float(line[2])
                node_obj.add_coordinates([x, y, z])

                #INPUT_LANE_ID
                line = file_object.readline()
                line = file_object.readline()
                line = line.strip("\n")
                input_lane_id = line.split(",")

                for id in input_lane_id:
                    for lane in self.lane_obj_array:
                        if lane.vm_id == int(id):
                            node_obj.add_input_lane_id(lane.obj_id)
                            lane.set_destination_node(node_obj.obj_id)

                # OUTPUT_LANE_ID
                line = file_object.readline()
                line = file_object.readline()
                line = line.strip("\n")
                output_lane_id = line.split(",")

                for id in output_lane_id:
                    for lane in self.lane_obj_array:
                        if lane.vm_id == int(id):
                            node_obj.add_output_lane_id(lane.obj_id)
                            lane.set_source_node(node_obj.obj_id)


                self.node_obj_array.append(node_obj)



                line = file_object.readline()

                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")

            else:
                print("The format is not supported")
                break

        self.create_map()


    def create_map(self):

        exit_flag = False
        for u_node in self.node_obj_array:
            for output_lane in u_node.out_lane_id_array:
                for v_node in self.node_obj_array:
                    for input_lane in v_node.in_lane_id_array:

                        if output_lane == input_lane:
                            edge = [u_node.obj_id, v_node.obj_id, self.lane_obj_array[output_lane].length, self.available]
                            self.graph.append(edge)
                            exit_flag = True
                            break

                    if (exit_flag):
                        exit_flag = False
                        break

        self.map['graph'] = self.graph
        self.map['lane'] = self.lane_obj_array
        self.map['node'] = self.node_obj_array


    def read_file(self, filepath):
        """
        Parse text at given filepath

        Parameters
        ----------
        filepath : str
            Filepath for file_object to be parsed

        Returns
        -------
        data : pd.DataFrame
            Parsed data

        """

        # open the file and read through it line by line
        with open(filepath, 'r') as file_object:
            line = file_object.readline()
            x = line.split("#")
            if float(x[4]) == 0.1:
                self.read_file_v01(file_object)

        # return [self.lane_obj_array, self.node_obj_array]
        return self.map

if __name__ == '__main__':
    filepath = '..\\data\\MiniPolygonGraph.namivm'
    vml = VMLoader()
    data = vml.read_file(filepath)
    print(data)
