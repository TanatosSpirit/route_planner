import rospy
from route_planner.msg import *
from libs.route_planner import route_planner
from libs.struct_helper import VmMap
from libs.map_objects.lane import Lane
from libs.map_objects.node import Node
from libs.math_helper import euler_to_quaternion, quaternion_to_euler
import copy


class RoutePlannerCore:
    def __init__(self):
        rospy.init_node('route_planner')

        self.pub_1 = rospy.Publisher('/track', Track, queue_size=1)

        self.sub_1 = rospy.Subscriber('/vm_map', VectorMap, self.vector_map_callback)
        self.sub_2 = rospy.Subscriber('/destination', Waypoint, self.destination_callback)
        self.sub_2 = rospy.Subscriber('/current_pose', Waypoint, self.current_pose_callback)

        self.rp = route_planner()
        self.vm = VmMap()
        self.destination = Waypoint()
        self.current_pose = Waypoint()
        self.route = []

        self.direct_velocity = rospy.get_param('direct_velocity', 0)
        self.reverse_velocity = rospy.get_param('reverse_velocity', 0)

        self.setup_route_planner()

        self.is_set_current_pose = False
        self.is_set_destination_pose = False
        self.is_map_loaded = False

    def setup_route_planner(self):
        self.rp.settings(self.direct_velocity, self.reverse_velocity)

    def run(self):
        rospy.spin()

    def vector_map_callback(self, data):
        """

        :type data: VectorMap
        """
        self.msg2map(data)
        self.rp.load_map(self.vm)

        self.is_map_loaded = True

        if self.is_set_current_pose and self.is_set_destination_pose:
            self.generate_path()

    def destination_callback(self, data):
        """

        :type data: Waypoint
        """
        is_change_dest_wp = self.compare_wps(self.destination, data)

        if is_change_dest_wp:
            self.destination = copy.deepcopy(data)
            self.rp.set_destination_point(self.get_list_from_wp(self.destination))

            self.is_set_destination_pose = True

            if self.is_set_current_pose and self.is_map_loaded:
                self.generate_path()

    def current_pose_callback(self, data):
        """

        :type data: Waypoint
        """
        self.current_pose = copy.deepcopy(data)
        self.rp.set_current_pose(self.get_list_from_wp(self.current_pose))

        self.is_set_current_pose = True

        if self.is_set_destination_pose and self.is_map_loaded:
            self.generate_path()

    def get_list_from_wp(self, wp): # TODO can be helper function
        """

        :type wp: Waypoint
        """
        angles = quaternion_to_euler(wp.orientation)
        return [wp.pose.x, wp.pose.y, wp.pose.z, angles[0]]

    def generate_path(self):
        self.route = self.rp.get_path()
        self.publish_track()

    def msg2map(self, data):
        """

        :type data: VectorMap
        """
        for lane in data.lanes:
            lane_obj = Lane()

            lane_obj.name = lane.obj_header.Name
            lane_obj.vm_id = lane.obj_header.vm_id
            lane_obj.obj_id = lane.obj_header.obj_id
            lane_obj.length = lane.length
            lane_obj.identification[0] = lane.identification.source
            lane_obj.identification[1] = lane.identification.destination

            for wp in lane.wps:
                x = wp.pose.x
                y = wp.pose.y
                z = wp.pose.z
                angles = quaternion_to_euler(wp.orientation)
                alfa = angles[0]
                lane_obj.wp_array.append([x, y, z, alfa])

            self.vm.lanes.append(lane_obj)

        for edge in data.graph:
            u = edge.u
            v = edge.v
            w = edge.length
            a = edge.available
            self.vm.graph.append([u, v, w, a])

        for node in data.nodes:
            node_obj = Node()

            node_obj.name = node.obj_header.Name
            node_obj.vm_id = node.obj_header.vm_id
            node_obj.obj_id = node.obj_header.obj_id
            node_obj.xyz = node.pose
            node_obj.in_lane_id_array = node.input
            node_obj.out_lane_id_array = node.output

            self.vm.nodes.append(node_obj)

        self.vm.num_of_nodes = len(self.vm.nodes)

    def compare_wps(self, destination, data):
        is_change = False

        if destination.pose.x != data.pose.x or \
                destination.pose.y != data.pose.y or \
                destination.pose.z != data.pose.z or \
                destination.orientation.x != data.orientation.x or\
                destination.orientation.y != data.orientation.y or\
                destination.orientation.z != data.orientation.z or\
                destination.orientation.w != data.orientation.w:
            is_change = True

        return is_change

    def publish_track(self):

        track_obj = Track()
        for wp in self.route[2]:  ## TODO REDO
            wp_obj = Waypoint()
            wp_obj.pose.x = wp[0]
            wp_obj.pose.y = wp[1]
            wp_obj.pose.z = wp[2]
            quat = euler_to_quaternion(0, 0, wp[3])
            wp_obj.orientation.x = quat[0]
            wp_obj.orientation.y = quat[1]
            wp_obj.orientation.z = quat[2]
            wp_obj.orientation.w = quat[3]
            wp_obj.current = False


            track_obj.waypoints.append(wp_obj)

        self.pub_1.publish(track_obj)
