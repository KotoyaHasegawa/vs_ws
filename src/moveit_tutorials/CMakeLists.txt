cmake_minimum_required(VERSION 3.1.3)
project(moveit_tutorials)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(catkin REQUIRED
  COMPONENTS
    interactive_markers
    moveit_core
    moveit_visual_tools
    moveit_ros_planning
    moveit_ros_planning_interface
    moveit_ros_perception
    pluginlib
    geometric_shapes
    pcl_ros
    pcl_conversions
    rosbag
    tf2_ros
    tf2_eigen
    tf2_geometry_msgs
    #added
    #opencv2
    sensor_msgs
    cv_bridge
    roscpp
    rospy
    std_msgs
    #for message and service definition
    message_generation
    actionlib_msgs
)

find_package(Eigen3 REQUIRED)
find_package(Boost REQUIRED system filesystem date_time thread)
find_package(OpenCV)#simply just add OpenCV here is enough

#added
#catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES ros_lecture
  #CATKIN_DEPENDS roscpp rospy std_msgs message_runtime
#  DEPENDS system_lib
#)


#added
add_message_files(
  DIRECTORY msg
  FILES
  #nantoka.msg wo koko ni tsuika
)

add_service_files(
  DIRECTORY srv
  FILES
  GetCurrentImage.srv
  GetCurrentImageData.srv
  GetCurrentCount.srv
  GetCurrentJointVel.srv
  GettfPose.srv
  #nantoka.srv wo koko ni tsuika
)
add_action_files(
  DIRECTORY action
  FILES 
  Empty.action
  ValidJoints.action
  #nantoka.action wo koko ni tsuika
)

#added
generate_messages(
  DEPENDENCIES
  std_msgs
  actionlib_msgs
  geometry_msgs
  sensor_msgs
)

set(THIS_PACKAGE_INCLUDE_DIRS
  doc/interactivity/include
)

catkin_package(
  LIBRARIES
    interactivity_utils
  INCLUDE_DIRS
    ${THIS_PACKAGE_INCLUDE_DIRS}
  CATKIN_DEPENDS
    moveit_core
    moveit_visual_tools
    moveit_ros_planning_interface
    interactive_markers
    tf2_geometry_msgs
    #added
    message_runtime
    std_msgs
    rospy
    roscpp
  DEPENDS
    EIGEN3
)

###########
## Build ##
###########

include_directories(${THIS_PACKAGE_INCLUDE_DIRS} ${catkin_INCLUDE_DIRS} ${Boost_INCLUDE_DIR} ${EIGEN3_INCLUDE_DIRS})

add_subdirectory(doc/kinematics)
add_subdirectory(doc/robot_model_and_robot_state)
add_subdirectory(doc/planning)
add_subdirectory(doc/planning_scene)
add_subdirectory(doc/planning_scene_ros_api)
add_subdirectory(doc/motion_planning_api)
add_subdirectory(doc/motion_planning_pipeline)
add_subdirectory(doc/visualizing_collisions)
add_subdirectory(doc/move_group_interface)
add_subdirectory(doc/move_group_python_interface)
add_subdirectory(doc/state_display)
add_subdirectory(doc/interactivity)
add_subdirectory(doc/pick_place)
add_subdirectory(doc/perception_pipeline)
