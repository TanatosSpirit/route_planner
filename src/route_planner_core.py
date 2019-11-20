import rospy
from route_planner.msg._VectorMap import VectorMap
from route_planner.msg._Waypoint import Waypoint
from libs.route_planner import route_planner
from std_msgs.msg import Bool
import copy

class RoutePlannerCore:
    def __init__(self):
        rospy.init_node('route_planner')

        self.pub_1 = rospy.Publisher('/map_loaded', Bool, queue_size=1)

        self.sub_1 = rospy.Subscriber('/vm_map', VectorMap, self.vector_map_callback)
        self.sub_2 = rospy.Subscriber('/destination', Waypoint, self.destination_callback)
        self.sub_2 = rospy.Subscriber('/current_pose', Waypoint, self.current_pose_callback)

        self.rp = route_planner()
        self.vm = VectorMap()
        self.destination = Waypoint()
        self.current_pose = Waypoint()

        self.direct_velocity = rospy.get_param('direct_velocity', 0)
        self.reverse_velocity = rospy.get_param('reverse_velocity', 0)

        self.rp.settings(self.direct_velocity, self.reverse_velocity)

        # self.path = rospy.get_param('map_path', '')
        #
        # self.direct_velocity = rospy.get_param('direct_velocity', 0)
        # self.reverse_velocity = rospy.get_param('reverse_velocity', 0)

    def run(self):
        rospy.spin()

    def vector_map_callback(self, data):
        """

        :type data: VectorMap
        """
        self.vm = copy.deepcopy(data)
        self.pub_1.publish(True)

    def destination_callback(self, data):
        """

        :type data: Waypoint
        """
        self.destination = copy.deepcopy(data)

    def current_pose_callback(self, data):
        """

        :type data: Waypoint
        """
        self.rp.set_current_pose(data)
