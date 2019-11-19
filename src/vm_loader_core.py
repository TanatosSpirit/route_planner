import rospy
from route_planner.msg._Waypoint import Waypoint
from route_planner.msg._Point3D import Point3D
from libs import VMLoader
from libs.struct_helper import VmMap
from route_planner.msg._Node import Node
from route_planner.msg._VectorMap import VectorMap
from route_planner.msg._MapObject import MapObject
import copy

class VMLoaderCore:
    def __init__(self):
        rospy.init_node('vm_loader')

        self.pub_1 = rospy.Publisher('/vm_map', VectorMap, queue_size=1)

        self.path = rospy.get_param('map_path', '')

        self.direct_velocity = rospy.get_param('direct_velocity', 0)
        self.reverse_velocity = rospy.get_param('reverse_velocity', 0)

        self.rate = rospy.Rate(10)

        self.vm_map = VmMap()
        self.vml = VMLoader()
        self.map_loaded = False

        self.vector_map = VectorMap()

    def run(self):
        self.vm_map = self.vml.read_file(self.path)

        while not rospy.is_shutdown():

            if not self.map_loaded:
                self.convert_map()
                self.map_loaded = True

            self.pub_1.publish(self.vector_map)

            self.rate.sleep()

    def convert_map(self):

        for node in self.vm_map.nodes:
            node_obj = Node()
            obj_header = MapObject()
            point_3d = Point3D()

            obj_header.Name = node.name
            obj_header.vm_id = node.vm_id
            obj_header.obj_id = node.obj_id

            point_3d.x = node.xyz[0]
            point_3d.y = node.xyz[1]
            point_3d.z = node.xyz[2]

            node_obj.obj_header = copy.deepcopy(obj_header)
            node_obj.pose = point_3d
            node_obj.input = copy.deepcopy(node.in_lane_id_array)
            node_obj.output = copy.deepcopy(node.out_lane_id_array)

            self.vector_map.nodes.append(node_obj)

