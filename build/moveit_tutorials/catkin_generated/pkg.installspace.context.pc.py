# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/usr/include/eigen3".split(';') if "${prefix}/include;/usr/include/eigen3" != "" else []
PROJECT_CATKIN_DEPENDS = "moveit_core;moveit_visual_tools;moveit_ros_planning_interface;interactive_markers;tf2_geometry_msgs;message_runtime;std_msgs;rospy;roscpp".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-linteractivity_utils".split(';') if "-linteractivity_utils" != "" else []
PROJECT_NAME = "moveit_tutorials"
PROJECT_SPACE_DIR = "/home/kotoyah/vs_ws/install"
PROJECT_VERSION = "0.1.0"
