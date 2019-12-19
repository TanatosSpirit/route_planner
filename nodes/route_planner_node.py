#!/usr/bin/env python

import rospy
import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.route_planner_core import RoutePlannerCore


if __name__ == '__main__':

    route_planner_core = RoutePlannerCore()

    try:
        route_planner_core.run()
    except rospy.ROSInterruptException:
        pass
