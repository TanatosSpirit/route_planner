from map_object import MapObject


class Node(MapObject):
    def __init__(self, name, vm_id, object_id, xyz):
        MapObject.__init__(name, vm_id, object_id)
        self.xyz = xyz
        self.in_lane_id_array = []
        self.out_lane_id_array = []

    def add_input_lane_id(self, in_id):
        self.in_lane_id_array.append(in_id)

    def add_output_lane_id(self, out_id):
        self.out_lane_id_array.append(out_id)
