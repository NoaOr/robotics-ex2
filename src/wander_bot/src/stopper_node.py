#!/usr/bin/python
#
# stopper_node.py
#
#  Created on: Nov 13, 2017
#      Author: Mika Barkan
#
import rospy, sys
from stopper import Stopper
if __name__ == "__main__":
    rospy.init_node("stopper_node", argv=sys.argv)
    forward_speed = 0.5
    min_scan_angle = -150
    max_scan_angle = 150
    rotation_speed = 0.3
    if rospy.has_param('~forward_speed'):
        forward_speed = rospy.get_param('~forward_speed')
    if rospy.has_param('~min_scan_angle'):
        min_scan_angle = rospy.get_param('~min_scan_angle')
    if rospy.has_param('~max_scan_angle'):
        max_scan_angle = rospy.get_param('~max_scan_angle')
    if rospy.has_param('~rotation_speed'):
        rotation_speed = rospy.get_param('~rotation_speed')
    my_stopper = Stopper(forward_speed, min_scan_angle, max_scan_angle, rotation_speed)
    my_stopper.start_moving()
