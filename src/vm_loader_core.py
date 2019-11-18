import rospy
from route_planner.msg import WaypointOM

class VMLoaderCore:
    def __init__(self):
        rospy.init_node('vm_loader')

        self.pub_1 = rospy.Publisher('/vm_map', WaypointOM, queue_size=1)

        self.path = rospy.get_param('map_path', '')

        self.rate = rospy.Rate(10)



    def run(self):
        while not rospy.is_shutdown():
            wp = WaypointOM()

            wp.x = 1
            wp.y = 2
            wp.z = 3
            wp.direction = 4

            self.pub_1.publish(wp)

            self.rate.sleep()
