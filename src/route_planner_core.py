import rospy
from route_planner.msg._Waypoint import Waypoint
from route_planner.msg._Point3D import Point3D
from libs import VMLoader
from libs.struct_helper import VmMap
from route_planner.msg._Node import Node
from route_planner.msg._VectorMap import VectorMap
from route_planner.msg._MapObject import MapObject
from route_planner.msg._Edge import Edge
from route_planner.msg._Lane import Lane
from std_msgs.msg import Bool
import copy

class RoutePlannerCore:
    def __init__(self):
        rospy.init_node('route_planner')

        self.pub_1 = rospy.Publisher('/map_loaded', Bool, queue_size=1)

        self.sub_1 = rospy.Subscriber('/vm_map', VectorMap, self.get_vector_map)

        # self.path = rospy.get_param('map_path', '')
        #
        # self.direct_velocity = rospy.get_param('direct_velocity', 0)
        # self.reverse_velocity = rospy.get_param('reverse_velocity', 0)

    def run(self):
        rospy.spin()

    def get_vector_map(self, data):
        print(data)
        self.pub_1.publish(True)
