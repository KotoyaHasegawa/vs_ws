from ur_ikfast import ur_kinematics
from math import pi

ur5e_arm = ur_kinematics.URKinematics('ur5e')

# joint_angles = [-3.1, -1.6, 1.6, -1.6, -1.6, 0.]  # in radians

joint_goal2_deg =  [-30.34, -75.81, -114.68, -170.82, -29.33, 2.11] 
joint_angles = [x * pi/180 for x in joint_goal2_deg]


print("joint angles", joint_angles)

pose_quat = ur5e_arm.forward(joint_angles)
pose_matrix = ur5e_arm.forward(joint_angles, 'matrix')

print("forward() quaternion \n", pose_quat)
print("forward() matrix \n", pose_matrix)

# print("inverse() all", ur3e_arm.inverse(pose_quat, True))
print("inverse() one from quat", ur5e_arm.inverse(pose_quat, False, q_guess=joint_angles))

print("inverse() one from matrix", ur5e_arm.inverse(pose_matrix, False, q_guess=joint_angles))


