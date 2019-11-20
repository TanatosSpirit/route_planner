#!/usr/bin/env python

import rospy
from route_planner_core import RoutePlannerCore


if __name__ == '__main__':

    route_planner_core = RoutePlannerCore()

    try:
        route_planner_core.run()
    except rospy.ROSInterruptException:
        pass
