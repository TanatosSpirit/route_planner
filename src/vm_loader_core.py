import rospy
from route_planner.msg._Waypoint import Waypoint
from route_planner.msg._Point3D import Point3D
from libs import VMLoader
from libs.struct_helper import VmMap

class VMLoaderCore:
    def __init__(self):
        rospy.init_node('vm_loader')

        self.pub_1 = rospy.Publisher('/vm_map', Waypoint, queue_size=1)

        self.path = rospy.get_param('map_path', '')

        self.direct_velocity = rospy.get_param('direct_velocity', 0)
        self.reverse_velocity = rospy.get_param('reverse_velocity', 0)

        self.rate = rospy.Rate(10)

        self.vm_map = VmMap()
        self.vml = VMLoader()

    def run(self):
        self.vm_map = self.vml.read_file(self.path)

        while not rospy.is_shutdown():
            wp = Waypoint()

            wp.x = 1
            wp.y = 2
            wp.z = 3
            wp.direction = 4

            self.pub_1.publish(wp)

            self.rate.sleep()

    def convert_map(self):

