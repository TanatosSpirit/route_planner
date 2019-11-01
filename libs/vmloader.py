from lane import Lane


class VMLoader:

    def __init__(self):
        self.lane_obj_array = []
        self.node_array = []
        self.laneID = 0
        self.nodeID = 0

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

                lane_wps = []
                for i in range(num_of_points):
                    line = file_object.readline()
                    line = line.strip("\n")
                    line = line.split(",")
                    x = float(line[0])
                    y = float(line[1])
                    z = float(line[2])
                    lane_wps.append([x, y, z])
                    lane_obj.add_wp([x, y, z])

                self.lane_obj_array.append(lane_obj)

                line = file_object.readline()

                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")



            elif x[1] == "NODE":
                node = []

                #NAME#Node[21]
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")
                node.append(x[1])

                #ID#21
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")
                node.append(int(x[1]))

                #self.nodeID
                node.append(self.nodeID)
                self.nodeID += 1

                #XYZ
                line = file_object.readline()
                line = file_object.readline()
                line = line.strip("\n")
                line = line.split(",")
                x = float(line[0])
                y = float(line[1])
                z = float(line[2])
                node.append([x, y, z])

                #INPUT_LANE_ID
                line = file_object.readline()
                line = file_object.readline()
                line = line.strip("\n")
                input_lane_id = line.split(",")

                in_lane_id_array = []
                for id in input_lane_id:
                    in_lane_id_array.append(id)

                node.append(in_lane_id_array)
                self.node_array.append(node)

                # OUTPUT_LANE_ID
                line = file_object.readline()
                line = file_object.readline()
                line = line.strip("\n")
                output_lane_id = line.split(",")

                out_lane_id_array = []
                for id in output_lane_id:
                    out_lane_id_array.append(id)

                node.append(out_lane_id_array)
                self.node_array.append(node)



                line = file_object.readline()

                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")

            else:
                print("The format is not supported")
                break


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
                print(self.node_array)


if __name__ == '__main__':
    filepath = '..\\data\\MiniPolygonGraph.namivm'
    vml = VMLoader()
    data = vml.read_file(filepath)
    print(data)