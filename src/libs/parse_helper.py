from map_objects.lane import Lane
from map_objects.node import Node
from math_helper import add_direction

def get_obj(file_object):

    line = file_object.readline()
    line = line.lstrip("#")
    line = line.strip("\n")
    obj = line.split("#")

    if len(line) == 0:
        obj = False

    return obj

def get_num(file_object):
    line = file_object.readline()
    line = line.strip("\n")
    coord = line.split(",")

    return coord


def get_lane_v01(file_object, lane_id):
    lane_obj = Lane()

    # NAME#Lane[13]
    name = get_obj(file_object)
    lane_obj.add_name(name[1])

    # ID#13
    vm_obj = get_obj(file_object)
    lane_obj.add_vm_id(int(vm_obj[1]))

    # self.laneID
    lane_obj.add_obj_id(lane_id)

    # SPEED#5
    speed = get_obj(file_object)
    lane_obj.add_speed(int(speed[1]))

    # NUMBER_OF_POINTS#108
    num_of_points = get_obj(file_object)
    num_of_points = int(num_of_points[1])

    lane_obj.add_num_of_points(num_of_points)

    alfa = 0
    for i in range(num_of_points):
        coord = get_num(file_object)
        x = float(coord[0])
        y = float(coord[1])
        z = float(coord[2])

        lane_obj.add_wp([x, y, z, alfa])

        if i > 0:
            add_direction(lane_obj, i)

    lane_obj.wp_array[-1][3] = alfa

    return lane_obj


def get_node_v01(file_object, node_id, lane_array):
    node = Node()

    # NAME#Node[21]
    name = get_obj(file_object)
    node.add_name(name[1])

    # ID#21
    id = get_obj(file_object)
    node.add_vm_id(int(id[1]))

    # self.nodeID
    node.add_obj_id(node_id)

    # XYZ
    file_object.readline()
    coord = get_num(file_object)
    x = float(coord[0])
    y = float(coord[1])
    z = float(coord[2])
    node.add_coordinates([x, y, z])

    # INPUT_LANE_ID
    file_object.readline()
    input_lane_id = get_num(file_object)

    for id in input_lane_id:
        for lane in lane_array:
            if lane.vm_id == int(id):
                node.add_input_lane_id(lane.obj_id)
                lane.set_destination_node(node.obj_id)

    # OUTPUT_LANE_ID
    file_object.readline()
    output_lane_id = get_num(file_object)

    for id in output_lane_id:
        for lane in lane_array:
            if lane.vm_id == int(id):
                node.add_output_lane_id(lane.obj_id)
                lane.set_source_node(node.obj_id)

    return node
