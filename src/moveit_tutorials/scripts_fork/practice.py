import tf.transformations


def euler_to_quaternion(eule_x, euler_y, euler_z):
    """Convert Euler Angles to Quaternion

    euler: geometry_msgs/Vector3
    quaternion: geometry_msgs/Quaternion
    """
    q = tf.transformations.quaternion_from_euler(eule_x, euler_y, euler_z)
    return q[0], q[1], q[2], q[3]

def quaternion_to_euler(current_pose):
    """Convert Quaternion to Euler Angles

    quarternion: geometry_msgs/Quaternion
    euler: geometry_msgs/Vector3
    """
    e = tf.transformations.euler_from_quaternion((current_pose[0],current_pose[1],current_pose[2],current_pose[3]), 'sxyz')
    return e[0], e[1], e[2]


pose_quaternion = [0, 0, 0, 0]
pose_euler = [1.5795364808130279,-0.014457145346956305, 3.1292023158569346]

pose_quaternion[0], pose_quaternion[1], pose_quaternion[2], pose_quaternion[3] = euler_to_quaternion(pose_euler[0], pose_euler[1], pose_euler[2])
print(euler_to_quaternion(pose_euler[0], pose_euler[1], pose_euler[2]))

print(quaternion_to_euler(pose_quaternion))
