#!/usr/bin/python
#
# stopper.py
#
#  Created on: Nov 13, 2017
#      Author: Mika Barkan
#

import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class Stopper(object):

    def __init__(self, forward_speed, min_scan_angle, max_scan_angle, rotation_speed):
        self.forward_speed = forward_speed
        self.min_scan_angle = min_scan_angle/180*math.pi
        self.max_scan_angle = max_scan_angle/180 * math.pi
        self.rotation_speed = rotation_speed
        self.min_dist_from_obstacle = 1
        self.keep_moving = True
        self.move_msg = Twist()
        self.command_pub = rospy.Publisher("/cmd_vel_mux/input/teleop", Twist, queue_size=10)
        self.laser_subscriber = rospy.Subscriber("scan",LaserScan, self.scan_callback, queue_size=1)

    def start_moving(self):
        rate = rospy.Rate(10)
        rospy.loginfo("Starting to move")
        while not rospy.is_shutdown() and self.keep_moving:
            self.move_forward()
            rate.sleep()

    def move_forward(self):
        self.move_msg.linear.x = self.forward_speed
        self.command_pub.publish(self.move_msg)

    # def rotate(self, goal_angle):
    #     angular_speed = self.rotation_speed * math.pi / 180
    #     relative_angle = goal_angle * math.pi / 180
    #
    #     self.move_msg.linear.x = 0
    #     self.move_msg.linear.y = 0
    #     self.move_msg.linear.z = 0
    #     self.move_msg.angular.x = 0
    #     self.move_msg.angular.y = 0
    #
    #     self.move_msg.angular.z = relative_angle
    #
    #     # Setting the current time for distance calculus
    #     t0 = rospy.Time.now().to_sec()
    #     current_angle = 0
    #     rate = rospy.Rate(10)
    #
    #     while current_angle < relative_angle:
    #         self.command_pub.publish(self.move_msg)
    #         rate.sleep()
    #         t1 = rospy.Time.now().to_sec()
    #         current_angle = angular_speed * (t1 - t0)
    #
    #     # Forcing our robot to stop
    #     self.move_msg.angular.z = 0
    #     self.command_pub.publish(self.move_msg)
    #     rate.sleep()
    #     rospy.spin()

    def scan_callback(self, scan_msg):
        for dist in scan_msg.ranges:
            if dist < self.min_dist_from_obstacle:
                self.keep_moving = False
                ##################### start lital
                min = LaserScan.angle_min
                inc = LaserScan.angle_increment

                i = 0
                while min + inc*i < self.min_scan_angle:
                    i += 1

                best_index = i
                while min + inc*i < self.max_scan_angle:
                    if scan_msg.ranges[i] > scan_msg.ranges[best_index]:
                        best_index = i
                    i += 1
                self.move_msg.angular.z = min + inc * best_index
                self.command_pub.publish(self.move_msg)
                self.move_msg.angular.z = 0
                self.command_pub.publish(self.move_msg)
                break



                # counter1 = 0
                # counter2 = 0
                # size = len(scan_msg.ranges)
                # for i in range(0, size / 2):
                #     counter1 += scan_msg.ranges[i]
                # for i in range(size / 2, size):
                #     counter2 += scan_msg.ranges[i]
                #
                # if counter1 < counter2:
                #     self.move_msg.angular.z = self.max_scan_angle
                # else:
                #     self.move_msg.angular.z = self.min_scan_angle
                # break
        self.keep_moving = True

