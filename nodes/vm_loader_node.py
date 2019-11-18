#!/usr/bin/env python

import rospy
from route_planner.msg import WaypointOM
from vm_loader_core import VMLoaderCore


if __name__ == '__main__':

    vm_loader_core = VMLoaderCore()

    try:
        vm_loader_core.run()
    except rospy.ROSInterruptException:
        pass
