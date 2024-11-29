# Experiment in Real

## Initial Action


1. To properly run the system, you need to open **8 terminals** and execute the following commands in each terminal:

```
cd vs_ws/
```
```
source devel/setup.bash
```

2.  Run the following code in each terminal.

**1st terminal**:
```
roslaunch ur_robot_driver ur5e_bringup.launch robot_ip:=192.168.56.101 kinematics_config:=${HOME}/vs_ws/src/Universal_Robots_ROS_Driver/ur_calibration/ur5_calibration.yaml
```

**2nd terminal**:
```
roslaunch ur5e_moveit_config moveit_planning_execution.launch limited:=true
```

**3rd terminal**:
```
roslaunch realsense2_camera rs_camera.launch color_width:=1920 color_height:=1080 color_fps:=30 
```

**4th terminal**:
Adjust the Realsense here.
```
rosrun rqt_reconfigure rqt_reconfigure
```

3.  Move to the directory containing the executable files in the remaining four terminals using the following code.

```
cd src/moveit_tutorials/scripts_fork/
```
