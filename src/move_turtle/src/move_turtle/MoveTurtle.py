#!/usr/bin/python
# Noa Or
# 208385534

import sys, rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


PI = 3.1415926535897
flag = True


def pose_callback(pose_msg):
    global flag
    if flag:
        # if the glag is on- print the position
        rospy.loginfo("x: %.2f, y: %.2f" % (pose_msg.x, pose_msg.y))
        flag = False


# start move the turtle
def move():
    global flag

    # Initialize the node
    rospy.init_node("move_turtle")

    # A publisher for the movement data
    velocity_publisher = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size=10)
    # A listener for pose
    velocity_subscriber = rospy.Subscriber("turtle1/pose", Pose, pose_callback, queue_size=10)

    vel_msg = Twist()

    #Receiveing the user's input
    speed = 0.5
    distance = 1
    angle = 45

    vel_msg.linear.x = abs(speed)
    # Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        # Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        # Loop to move the turtle in an specified distance
        while current_distance < distance:
                # Publish the velocity
                velocity_publisher.publish(vel_msg)
                rate.sleep()
                # Takes actual time to velocity calculus
                t1 = rospy.Time.now().to_sec()
                # Calculates distancePoseStamped
                current_distance = speed * (t1 - t0)

        speed = 10
        # After the loop, stop the robot
        vel_msg.linear.x = 0
        # Force the robot to stop
        velocity_publisher.publish(vel_msg)
        flag = True
        rate.sleep()

        # Converting from angles to radians
        angular_speed = speed * PI / 180
        relative_angle = angle * PI / 180

        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        flag = False

        vel_msg.angular.z = abs(angular_speed)

        # Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        while current_angle < relative_angle:
            velocity_publisher.publish(vel_msg)
            rate.sleep()
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed * (t1 - t0)

        # Forcing our robot to stop
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        rate.sleep()
        rospy.spin()


if __name__ == "__main__":
    try:
        move()
    except rospy.ROSInterruptException:
        pass
