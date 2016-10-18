#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <iostream>
#include <geometry_msgs/Twist.h>
using namespace std;

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

void poseCallback(const geometry_msgs::Twist& amcl_pose)
{
  ROS_INFO("Thor is at ([%f], [%f])", amcl_pose.linear.x, amcl_pose.linear.y);
  std::cout << "Twist Received. " << std::endl;
}

int main(int argc, char **argv){

  ros::init(argc, argv, "map_nav_goal");

  //tell the action client that we want to spin a thread by default
  MoveBaseClient ac("move_base", true);

  //wait for the action server to come up
  while(!ac.waitForServer(ros::Duration(5.0))){
    ROS_INFO("Waiting for the move_base action server to come up");
  }

  move_base_msgs::MoveBaseGoal goal;
  //we'll send a goal to the robot to move 0.5 meter forward
  goal.target_pose.header.frame_id = "map";
  goal.target_pose.header.stamp = ros::Time::now();
  cout << "Frame: " << goal.target_pose.header.frame_id << "\n";
  float x , y; 
  cout << "Enter x coordinate: ";
  cin >> x; 
  cout << "Enter y coordinate: ";
  cin >> y;  
  goal.target_pose.pose.position.x = x;
  goal.target_pose.pose.position.y = y;
  goal.target_pose.pose.orientation.w = 1.0;

  ROS_INFO("Sending goal");
  ac.sendGoal(goal);

  ac.waitForResult();

  if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
    ROS_INFO("Moved to destination");
  else
    ROS_INFO("Failed to move to position");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("/amcl_pose", 1000, poseCallback); 

  return 0;
  ros::spin();
}

