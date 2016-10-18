#!/usr/bin/python

import roslib 
import rospy
#import simple action client
import actionlib
#imports messages used by move_base_msgs 
import move_base_msgs.msg
from geometry_msgs.msg import PoseWithCovarianceStamped

def amclpose(msg):
	print str(msg.pose.pose)
	global thor_state
	thor_state = [msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.orientation.w] 

def nav_goal_client(goal, client, goal_x, goal_y, goal_w):
	goal.target_pose.header.stamp = rospy.get_rostime()
	goal.target_pose.pose.position.x = goal_x
	goal.target_pose.pose.position.y = goal_y 
	goal.target_pose.pose.orientation.w = goal_w
	#sends goal to action server 
	client.send_goal(goal)
	#waits for the server to finish performing action 
	client.wait_for_result()
	return client.get_result()

def dist_offset(x_des, y_des, x_actual, y_actual):
	x_offset=x_des-x_actual
	y_offset=y_des-y_actual
	print "x offset: ", str(x_offset), "y offset: ", str(y_offset)
	return (x_offset, y_offset)

def accurate_nav(threshold):
	client=actionlib.SimpleActionClient("move_base",move_base_msgs.msg.MoveBaseAction)
        client.wait_for_server()
        #creates goal to send to action server
        goal=move_base_msgs.msg.MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        print "current frame: ", goal.target_pose.header.frame_id
        global x, y, w
        x = float(input("x coordinate: "))
        y = float(input("y coordinate: "))
        w = float(input("orientation: "))
	(x_offset, y_offset) = (1, 1)
	while abs(x_offset) > threshold and abs(y_offset) > threshold:
		result = nav_goal_client(goal, client, x, y, w)
		print "updated position" 
		rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,amclpose)
		rospy.sleep(1)
		(x_offset, y_offset) = dist_offset(x, y, thor_state[0], thor_state[1])
		x = x + x_offset
		y = y + y_offset
	return True

if __name__ == '__main__':
	try: 
		rospy.init_node('nav_goal')
		task = accurate_nav(0.1)
		print "arrived!"	

	except rospy.ROSInterruptException:
		print "program interrupted before completion"

