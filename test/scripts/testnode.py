#!/usr/bin/env python3
"""
testnode.py

RECREATED 2026, NOT THE ORIGINAL FILE.
------------------------------------------------------------------------
The original testnode.py from this catkin workspace (built ~2022) no
longer exists anywhere it could be recovered from. Only a file listing
showing its name survived, in a screenshot of the workspace folder. Its
actual contents, and its exact original behavior, are unknown.

This file is a new, from-scratch node written in 2026 to stand in for
it: a simple test node of the kind someone would naturally write right
after getting a TurtleBot3 Gazebo simulation running for the first time,
to confirm the robot actually responds to velocity commands. It has NOT
been run against a live ROS/Gazebo instance (ROS isn't available in the
environment this was written in), so treat it as reviewed-for-syntax
and reviewed-for-correct-rospy-API-usage, not as verified-by-execution.
------------------------------------------------------------------------

What it does: drives the robot in a repeating square path by alternating
short bursts of forward motion with 90-degree turns, using the standard
TurtleBot3 cmd_vel interface. Useful as a first smoke test: if the robot
traces a square in Gazebo, the simulation, the topic wiring, and the
diff-drive plugin are all working correctly together.
"""

import rospy
from geometry_msgs.msg import Twist
import math
import time


class SquareDriveTestNode:
    def __init__(self):
        rospy.init_node('testnode', anonymous=False)

        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Tunable parameters, kept modest so the robot stays inside the
        # default TurtleBot3 Gazebo world.
        self.linear_speed = 0.15    # m/s
        self.angular_speed = 0.3    # rad/s
        self.side_duration = 4.0    # seconds of forward motion per side
        self.turn_duration = self._seconds_for_quarter_turn()

        self.rate = rospy.Rate(10)  # 10 Hz command loop

        rospy.on_shutdown(self.stop_robot)

    def _seconds_for_quarter_turn(self):
        # time = angle / angular_speed, for a 90 degree (pi/2 radian) turn
        return (math.pi / 2) / self.angular_speed

    def stop_robot(self):
        """Publish a zero-velocity command so the robot doesn't keep
        drifting after the node exits."""
        self.cmd_vel_pub.publish(Twist())
        rospy.loginfo("testnode: stopped, published zero velocity")

    def drive_forward(self, duration):
        twist = Twist()
        twist.linear.x = self.linear_speed
        end_time = time.time() + duration
        while not rospy.is_shutdown() and time.time() < end_time:
            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()

    def turn_in_place(self, duration):
        twist = Twist()
        twist.angular.z = self.angular_speed
        end_time = time.time() + duration
        while not rospy.is_shutdown() and time.time() < end_time:
            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()

    def run_square_once(self):
        for side in range(4):
            if rospy.is_shutdown():
                return
            rospy.loginfo(f"testnode: side {side + 1}/4, driving forward")
            self.drive_forward(self.side_duration)
            rospy.loginfo(f"testnode: side {side + 1}/4, turning 90 degrees")
            self.turn_in_place(self.turn_duration)
        self.stop_robot()

    def run(self):
        rospy.loginfo("testnode: waiting for a subscriber on /cmd_vel...")
        # Gazebo's diff-drive plugin sometimes takes a moment to subscribe
        # after the simulation finishes spawning the model.
        wait_start = time.time()
        while (self.cmd_vel_pub.get_num_connections() == 0
               and not rospy.is_shutdown()
               and time.time() - wait_start < 10.0):
            time.sleep(0.1)

        rospy.loginfo("testnode: starting square path test")
        self.run_square_once()
        rospy.loginfo("testnode: square path complete")


if __name__ == '__main__':
    try:
        node = SquareDriveTestNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
