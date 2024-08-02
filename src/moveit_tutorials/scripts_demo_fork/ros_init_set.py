import rospy
import numpy as np
import cv2
import pandas as pd
#for switch controller
from controller_manager_msgs.srv import SwitchController
import atexit


class RosSet():
    def __init__(self,img_jacobi_pickle, mnip_jacobi_pickle, dsr_img ):
        self.img_jacobi_pickle = img_jacobi_pickle
        self.mnip_jacobi_pickle = mnip_jacobi_pickle
        self.dsr_img = dsr_img


    def switch_controller(self, start_controllers, stop_controllers):
        switch_service = rospy.ServiceProxy('/controller_manager/switch_controller', SwitchController)
        resp = switch_service(start_controllers=start_controllers, 
                            stop_controllers=stop_controllers,
                            strictness=2,
                            start_asap=False,
                            timeout=5.0)
        print(resp.ok)

    def switch_to_joint_group_vel(self):
        self.switch_controller(['joint_group_vel_controller'], ['scaled_pos_joint_traj_controller'])

    def switch_to_scaled_pos(self):
        self.switch_controller(['scaled_pos_joint_traj_controller'], ['joint_group_vel_controller'])

    def readpickle(self):
        global pinv_int_mat_double
        pickledata = pd.read_pickle(self.img_jacobi_pickle)
        pinv_int_mat_double = pickledata.values
        return pinv_int_mat_double

    def readpickle1(self):
        global pinv_int_manip
        pickledata1 = pd.read_pickle(self.mnip_jacobi_pickle)
        pinv_int_manip = pickledata1.values
        return pinv_int_manip


    def gen_dsrimvec(self): 
        global I_dsr_vec
        I_dsr = cv2.imread(self.dsr_img)
        I_dsr_gry = cv2.cvtColor(I_dsr, cv2.COLOR_BGR2GRAY)
        I_dsr_arr = np.array(I_dsr_gry, dtype = 'float64')
        I_dsr_vec = I_dsr_arr.reshape(-1,1)
        return I_dsr_vec
    
    def main(self):    
        self.switch_to_joint_group_vel()
        atexit.register(self.switch_to_scaled_pos)
        self.readpickle()
        self.readpickle1()
        self.gen_dsrimvec()
    