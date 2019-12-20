import rospy
from libs.math_helper import euler_to_quaternion
from route_planner.msg import *
from libs import VMLoader
from libs.struct_helper import VmMap
import copy


class VMLoaderCore:
    def __init__(self):
        rospy.init_node('vm_loader')

        self.pub_1 = rospy.Publisher('/vm_map', VectorMap, latch=True, queue_size=1)

        self.path = rospy.get_param('map_path', '')

        self.vm_map = VmMap()
        self.vml = VMLoader()
        self.map_loaded = False

        self.vector_map = VectorMap()

    def run(self):
        self.vm_map = self.vml.read_file(self.path)

        if not self.map_loaded:
            self.convert_map()
            self.map_loaded = True

        self.pub_1.publish(self.vector_map)

        rospy.spin()

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

        for edge in self.vm_map.graph:
            edge_obj = Edge()

            edge_obj.u = edge[0]
            edge_obj.v = edge[1]
            edge_obj.length = edge[2]
            edge_obj.available = edge[3]

            self.vector_map.graph.append(edge_obj)

        for lane in self.vm_map.lanes:
            lane_obj = Lane()

            lane_obj.obj_header.Name = lane.name
            lane_obj.obj_header.vm_id = lane.vm_id
            lane_obj.obj_header.obj_id = lane.obj_id

            lane_obj.speed = lane.speed
            for wp in lane.wp_array:
                wp_obg = Waypoint()
                wp_obg.pose.x = wp[0]
                wp_obg.pose.y = wp[1]
                wp_obg.pose.z = wp[2]
                quat = euler_to_quaternion(0, 0, wp[3])
                wp_obg.orientation.x = quat[0]
                wp_obg.orientation.y = quat[1]
                wp_obg.orientation.z = quat[2]
                wp_obg.orientation.w = quat[3]
                wp_obg.current = False

                lane_obj.wps.append(wp_obg)

            lane_obj.length = lane.length
            lane_obj.identification.source = lane.identification[0]
            lane_obj.identification.destination = lane.identification[1]

            self.vector_map.lanes.append(lane_obj)





