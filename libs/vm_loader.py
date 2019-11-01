class vm_loader:

    def __init__(self):
        self.lane_array = []
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
                lane = []

                #NAME#Lane[13]
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")
                lane.append(x[1])

                #ID#13
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")
                lane.append(int(x[1]))

                #self.laneID
                lane.append(self.laneID)
                self.laneID += 1

                #SPEED#5
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                x = line.split("#")
                lane.append(int(x[1]))

                #NUMBER_OF_POINTS#108
                line = file_object.readline()
                line = line.lstrip("#")
                line = line.strip("\n")
                points_number = int(line.split("#")[1])
                lane.append(points_number)

                lane_wps = []
                for i in range(points_number):
                    line = file_object.readline()
                    line = line.strip("\n")
                    line = line.split(",")
                    x = float(line[0])
                    y = float(line[1])
                    z = float(line[2])
                    lane_wps.append([x, y, z])


                lane.append(lane_wps)
                self.lane_array.append(lane)

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

        data = []  # create an empty list to collect the data
        # open the file and read through it line by line
        with open(filepath, 'r') as file_object:
            line = file_object.readline()
            x = line.split("#")
            if float(x[4]) == 0.1:
                self.read_file_v01(file_object)
                print(self.lane_array)
                print(self.node_array)

        #     while line:
        #         # at each line check for a match with a regex
        #         key, match = _parse_line(line)
        #
        #         # extract school name
        #         if key == 'school':
        #             school = match.group('school')
        #
        #         # extract grade
        #         if key == 'grade':
        #             grade = match.group('grade')
        #             grade = int(grade)
        #
        #         # identify a table header
        #         if key == 'name_score':
        #             # extract type of table, i.e., Name or Score
        #             value_type = match.group('name_score')
        #             line = file_object.readline()
        #             # read each line of the table until a blank line
        #             while line.strip():
        #                 # extract number and value
        #                 number, value = line.strip().split(',')
        #                 value = value.strip()
        #                 # create a dictionary containing this row of data
        #                 row = {
        #                     'School': school,
        #                     'Grade': grade,
        #                     'Student number': number,
        #                     value_type: value
        #                 }
        #                 # append the dictionary to the data list
        #                 data.append(row)
        #                 line = file_object.readline()
        #
        #         line = file_object.readline()
        #
        #     # create a pandas DataFrame from the list of dicts
        #     data = pd.DataFrame(data)
        #     # set the School, Grade, and Student number as the index
        #     data.set_index(['School', 'Grade', 'Student number'], inplace=True)
        #     # consolidate df to remove nans
        #     data = data.groupby(level=data.index.names).first()
        #     # upgrade Score from float to integer
        #     data = data.apply(pd.to_numeric, errors='ignore')
        # return data

if __name__ == '__main__':
    filepath = 'D:\\workspace\\python\\route-planner\\data\\MiniPolygonGraph.namivm'
    vml = vm_loader()
    data = vml.read_file(filepath)
    # print(data)