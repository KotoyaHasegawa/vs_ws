# Install script for directory: /home/kotoya/vs_ws/src/moveit_tutorials

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/kotoya/vs_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/kotoya/vs_ws/install/_setup_util.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/kotoya/vs_ws/install" TYPE PROGRAM FILES "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/_setup_util.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/kotoya/vs_ws/install/env.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/kotoya/vs_ws/install" TYPE PROGRAM FILES "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/env.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/kotoya/vs_ws/install/setup.bash;/home/kotoya/vs_ws/install/local_setup.bash")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/kotoya/vs_ws/install" TYPE FILE FILES
    "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/setup.bash"
    "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/local_setup.bash"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/kotoya/vs_ws/install/setup.sh;/home/kotoya/vs_ws/install/local_setup.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/kotoya/vs_ws/install" TYPE FILE FILES
    "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/setup.sh"
    "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/local_setup.sh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/kotoya/vs_ws/install/setup.zsh;/home/kotoya/vs_ws/install/local_setup.zsh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/kotoya/vs_ws/install" TYPE FILE FILES
    "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/setup.zsh"
    "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/local_setup.zsh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/kotoya/vs_ws/install/.rosinstall")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/kotoya/vs_ws/install" TYPE FILE FILES "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/.rosinstall")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_tutorials/srv" TYPE FILE FILES
    "/home/kotoya/vs_ws/src/moveit_tutorials/srv/GetCurrentImage.srv"
    "/home/kotoya/vs_ws/src/moveit_tutorials/srv/GetCurrentImageData.srv"
    "/home/kotoya/vs_ws/src/moveit_tutorials/srv/GetCurrentCount.srv"
    "/home/kotoya/vs_ws/src/moveit_tutorials/srv/GetCurrentJointVel.srv"
    "/home/kotoya/vs_ws/src/moveit_tutorials/srv/GettfPose.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_tutorials/action" TYPE FILE FILES
    "/home/kotoya/vs_ws/src/moveit_tutorials/action/Empty.action"
    "/home/kotoya/vs_ws/src/moveit_tutorials/action/ValidJoints.action"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_tutorials/msg" TYPE FILE FILES
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/EmptyAction.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/EmptyActionGoal.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/EmptyActionResult.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/EmptyActionFeedback.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/EmptyGoal.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/EmptyResult.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/EmptyFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_tutorials/msg" TYPE FILE FILES
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/ValidJointsAction.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/ValidJointsActionGoal.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/ValidJointsActionResult.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/ValidJointsActionFeedback.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/ValidJointsGoal.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/ValidJointsResult.msg"
    "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/moveit_tutorials/msg/ValidJointsFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_tutorials/cmake" TYPE FILE FILES "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/moveit_tutorials-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/include/moveit_tutorials")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/roseus/ros/moveit_tutorials")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/common-lisp/ros/moveit_tutorials")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/share/gennodejs/ros/moveit_tutorials")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/lib/python3/dist-packages/moveit_tutorials")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/kotoya/vs_ws/devel/.private/moveit_tutorials/lib/python3/dist-packages/moveit_tutorials")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/moveit_tutorials.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_tutorials/cmake" TYPE FILE FILES "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/moveit_tutorials-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_tutorials/cmake" TYPE FILE FILES
    "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/moveit_tutorialsConfig.cmake"
    "/home/kotoya/vs_ws/build/moveit_tutorials/catkin_generated/installspace/moveit_tutorialsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/moveit_tutorials" TYPE FILE FILES "/home/kotoya/vs_ws/src/moveit_tutorials/package.xml")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/kotoya/vs_ws/build/moveit_tutorials/gtest/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/kinematics/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/robot_model_and_robot_state/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/planning/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/planning_scene/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/planning_scene_ros_api/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/motion_planning_api/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/motion_planning_pipeline/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/visualizing_collisions/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/move_group_interface/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/move_group_python_interface/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/state_display/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/interactivity/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/pick_place/cmake_install.cmake")
  include("/home/kotoya/vs_ws/build/moveit_tutorials/doc/perception_pipeline/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/kotoya/vs_ws/build/moveit_tutorials/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
