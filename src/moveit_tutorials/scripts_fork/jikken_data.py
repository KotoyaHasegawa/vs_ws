import cv2
import csv
from cv_bridge import CvBridge
import matplotlib.pyplot as plt
import numpy as np


class DATA():
    def __init__(self, bgr_full, bgr, dsr_img, init_img, rmse_data, dist_trans_x, dist_trans_y, dist_trans_z, 
                 dist_rot_x, dist_rot_y, dist_rot_z, error_rot_axis, error_rot_ang, dist_data, 
                 time_series, base_joint_data, shoulder_joint_data, elbow_joint_data, wrist1_joint_data, wrist2_joint_data, wrist3_joint_data, 
                 rmseth, iteration):
        self.bgr_full = bgr_full
        self.bgr= bgr
        self.dsr_img = dsr_img
        self.init_img = init_img
        self.last_img_full = cv2.cvtColor(bgr_full, cv2.COLOR_BGR2GRAY)
        self.last_img = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        self.rmse_data = rmse_data

        self.dist_trans_x = dist_trans_x
        self.dist_trans_y = dist_trans_y 
        self.dist_trans_z = dist_trans_z
        self.dist_rot_x = dist_rot_x
        self.dist_rot_y = dist_rot_y 
        self.dist_rot_z = dist_rot_z

        self.error_rot_axis = error_rot_axis
        self.error_rot_ang = error_rot_ang
        self.dist_data = dist_data 

        self.time_series = time_series
 
        self.base_joint_data = base_joint_data
        self.shoulder_joint_data = shoulder_joint_data
        self.elbow_joint_data = elbow_joint_data
        self.wrist1_joint_data = wrist1_joint_data
        self.wrist2_joint_data = wrist2_joint_data
        self.wrist3_joint_data = wrist3_joint_data

        self.rmseth = rmseth
        self.iteration = iteration

    def hand_eye_last_img(self):
        #位置決め後￥ハンドアイ画像        
        bgr = self.bgr
        bgr_full = self.bgr_full
        cv2.imwrite('./servo_data/kensyo_last_image.png', bgr)
        cv2.imwrite('./servo_data/kensyo_last_image.png', bgr_full)
    
    def init_difference_img(self):
        difference_init = cv2.absdiff(self.dsr_img, self.init_img)
        difference_image_path = './servo_data/init_difference_image.jpg'
        cv2.imwrite(difference_image_path, difference_init)      
        
        dsr_img_full = cv2.imread('./input_dsrim/kensyo_desired_image(full).png', cv2.IMREAD_GRAYSCALE)
        init_img_full = cv2.imread('./servo_data/kensyo_initial_image_full.png', cv2.IMREAD_GRAYSCALE)
        difference_init_full = cv2.absdiff(dsr_img_full , init_img_full)
        difference_image_path_full = './servo_data/init_difference_image_full.jpg'
        cv2.imwrite(difference_image_path_full, difference_init_full)      


    def last_difference_img(self):
        difference_init = cv2.absdiff(self.dsr_img, self.last_img)
        difference_image_path = './servo_data/last_difference_image.jpg'
        cv2.imwrite(difference_image_path, difference_init) 

        dsr_img_full = cv2.imread('./input_dsrim/kensyo_desired_image(full).png', cv2.IMREAD_GRAYSCALE)
        difference_init_full = cv2.absdiff(dsr_img_full , self.last_img_full)
        difference_image_path_full = './servo_data/last_difference_image_full.jpg'
        cv2.imwrite(difference_image_path_full, difference_init_full) 

    def save_csv(self):
        filename = './servo_data/loop_rmse_data.csv'
        filename2 = './servo_data/2posedist.csv'
        filename3 = './servo_data/y_dist.csv'
        filename4 = './servo_data/rotation_axis.csv'
        filename5 = './servo_data/rotation_angle.csv'
        filename6 = './servo_data/last_position_traslation.csv'

        with open (filename, 'w') as f, open(filename2, 'w')as f2, open(filename3, 'w')as f3, \
        open(filename4, 'w')as f4, open(filename5, 'w')as f5, open(filename6, 'w')as f6:
            writer = csv.writer(f)
            writer.writerow(self.rmse_data)
            writer2 = csv.writer(f2)
            writer2.writerow(self.dist_data)
            writer3 = csv.writer(f3)
            writer3.writerow(self.dist_trans_y)
            writer4 = csv.writer(f4)
            writer4.writerow(self.error_rot_axis)
            writer5 = csv.writer(f5)
            writer5.writerow(self.error_rot_ang)
            writer6 = csv.writer(f6)
            writer6.writerow(["2dist", "x", "y", "z", "rx", "ry", "rz"])
            writer6.writerow([self.dist_data[-1], self.dist_trans_x[-1], self.dist_trans_y[-1], self.dist_trans_z[-1] ,
                                self.dist_rot_x[-1], self.dist_rot_y[-1], self.dist_rot_z[-1]])
                
    def joint_vel_data(self):
        #6つのグラフの配置
        fig = plt.figure(figsize = (10,10))
        ax1 = fig.add_subplot(3,2,1)
        ax2 = fig.add_subplot(3,2,2)
        ax3 = fig.add_subplot(3,2,3)
        ax4 = fig.add_subplot(3,2,4)
        ax5 = fig.add_subplot(3,2,5)
        ax6 = fig.add_subplot(3,2,6)
        
        #各ループごとの各ジョイント角プロット
        ax1.plot(self.time_series, self.base_joint_data, color = 'blue', label = 'current joint velocity')
        ax2.plot(self.time_series, self.shoulder_joint_data, color = 'blue', label = 'current joint velocity')
        ax3.plot(self.time_series, self.elbow_joint_data, color = 'blue', label = 'current joint velocity')
        ax4.plot(self.time_series, self.wrist1_joint_data, color = 'blue', label = 'current joint velocity')
        ax5.plot(self.time_series, self.wrist2_joint_data, color = 'blue', label = 'current joint velocity')
        ax6.plot(self.time_series, self.wrist3_joint_data, color = 'blue', label = 'current joint velocity')
        
        # #目標角度をプロットscrewdriver
        ax1.axhline(y = 0.0, color = 'red')
        ax2.axhline(y = 0.0, color = 'red')
        ax3.axhline(y = 0.0, color = 'red')
        ax4.axhline(y = 0.0, color = 'red')
        ax5.axhline(y = 0.0, color = 'red')
        ax6.axhline(y = 0.0, color = 'red')
        
        #x軸のラベル
        ax1.set_xlabel('Time[s]')
        ax2.set_xlabel('Time[s]')
        ax3.set_xlabel('Time[s]')
        ax4.set_xlabel('Time[s]')
        ax5.set_xlabel('Time[s]')
        ax6.set_xlabel('Time[s]')
        
        #y軸のラベル
        ax1.set_ylabel('base joint velocity[rad/s]')
        ax2.set_ylabel('shoulder joint velocity[rad/s]')
        ax3.set_ylabel('elbow joint velocity[rad/s]')
        ax4.set_ylabel('wrist1 joint velocity[rad/s]')
        ax5.set_ylabel('wrist2 joint velocity[rad/s]')
        ax6.set_ylabel('wrist3 joint velocity[rad/s]')
        
        #凡例表示
        ax1.legend(ncol = 2, loc = 'lower right')
        ax2.legend(ncol = 2, loc = 'lower right')
        ax3.legend(ncol = 2, loc = 'lower right')
        ax4.legend(ncol = 2, loc = 'lower right')
        ax5.legend(ncol = 2, loc = 'lower right')
        ax6.legend(ncol = 2, loc = 'lower right')
        
        #重なり解消
        plt.tight_layout()
        
        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        ax5.grid()
        ax6.grid()
        
        #縦軸横軸の最大値、最小値、目盛り自動設定のグラフ保存
        fig.savefig('./servo_data/joint_vel_values.png')
        
        # y-axisの最大値と最小値を計算
        y_min = min(min(self.base_joint_data), min(self.shoulder_joint_data), min(self.elbow_joint_data), min(self.wrist1_joint_data), min(self.wrist2_joint_data), min(self.wrist3_joint_data))
        y_max = max(max(self.base_joint_data), max(self.shoulder_joint_data), max(self.elbow_joint_data), max(self.wrist1_joint_data), max(self.wrist2_joint_data), max(self.wrist3_joint_data))

        # 各サブプロットのy-axisのスケールを一致させる
        ax1.set_ylim(y_min, y_max)
        ax2.set_ylim(y_min, y_max)
        ax3.set_ylim(y_min, y_max)
        ax4.set_ylim(y_min, y_max)
        ax5.set_ylim(y_min, y_max)
        ax6.set_ylim(y_min, y_max)

        # 保存
        fig.savefig('./servo_data/joint_values_double_scaled.png')  

    def orther_data(self):
        fig_rmse_it = plt.figure()
        iteration = np.linspace(0, len(self.rmse_data), len(self.rmse_data))
        plt.xlabel('iteration')
        plt.ylabel('RMSE')
        plt.plot(iteration, self.rmse_data, 'b-')
        plt.xlim([0, self.iteration])
        plt.ylim([self.rmseth, 60])
        plt.grid()
        fig_rmse_it.savefig('./servo_data/rmse_iteration.png')

        fig_dist = plt.figure()
        iteration = np.linspace(0, len(self.dist_data), len(self.dist_data))
        plt.xlabel('iteration')
        plt.ylabel('Distance in XZ plane[mm]')
        plt.plot(iteration, self.dist_data, 'b-')
        plt.xlim([0, self.iteration])
        plt.ylim([0.0, 30.0])
        plt.grid()
        fig_dist.savefig('./servo_data/2posedist.png')
    
        fig_y_dist = plt.figure()
        iteration = np.linspace(0, len(self.dist_trans_y), len(self.dist_trans_y))
        plt.xlabel('iteration')
        plt.ylabel('Distance on Y axis[mm]')
        plt.plot(iteration, self.dist_trans_y, 'b-')
        plt.xlim([0, self.iteration])
        plt.ylim([0.0, 5.0])
        plt.grid()
        fig_y_dist.savefig('./servo_data/ydist.png')

        rot_axis_dist = plt.figure()
        iteration = np.linspace(0, len(self.error_rot_axis), len(self.error_rot_axis))
        plt.xlabel('iteration')
        plt.ylabel('Error of rotation axis[deg]')
        plt.plot(iteration, self.error_rot_axis, 'b-')
        plt.xlim([0, self.iteration])
        plt.ylim([0.0, 2.0])
        plt.grid()
        rot_axis_dist.savefig('./servo_data/rot_axis.png')

        rot_ang_dist = plt.figure()
        iteration = np.linspace(0, len(self.error_rot_ang), len(self.error_rot_ang))
        plt.xlabel('iteration')
        plt.ylabel('Error of rotation angle[deg]')
        plt.plot(iteration, self.error_rot_ang, 'b-')
        plt.xlim([0, self.iteration])
        plt.ylim([0.0, 2.0])
        plt.grid()
        rot_ang_dist.savefig('./servo_data/rot_ang.png')      


        print('2dist = %f' % self.dist_data[-1])        
        print('x = %f' % self.dist_trans_x[-1])
        print('y = %f' % self.dist_trans_y[-1])
        print('z = %f' % self.dist_trans_z[-1])
        print('rx = %f' % self.dist_rot_x[-1])
        print('ry = %f' % self.dist_rot_y[-1])
        print('rz = %f' % self.dist_rot_z[-1])



        fig_rt_dist = plt.figure()
        ax1 = fig_rt_dist.add_subplot()
        ax2 = ax1.twinx() 

        ax1.plot(self.time_series, self.dist_trans_x, 'r-', label = "X axis translation")
        ax1.plot(self.time_series, self.dist_trans_y, 'b-', label = "Y axis translation")
        ax1.plot(self.time_series, self.dist_trans_z,'g-', label = "Z axis translation")
        ax2.plot(self.time_series, self.dist_rot_x, 'k--', label = "X axis rotation" ,markersize = 1)
        ax2.plot(self.time_series, self.dist_rot_y, 'y--', label = "Y axis rotation" ,markersize = 1)
        ax2.plot(self.time_series, self.dist_rot_z, 'm--', label = "Z axis rotation" ,markersize = 1)

        ax1.set_xlabel('Time[s]')  #x軸ラベル
        ax1.set_ylabel("Position error[mm]")  #y1軸ラベル
        ax2.set_ylabel("Rotation error[deg]")  #y2軸ラベル
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2 ,loc='upper right')
        ax1.set_ylim([0, 30])
        ax2.set_ylim([0, 2.0])

        ax1.grid()
        fig_rt_dist.savefig('./servo_data/trans_rot_dist.png')     

        fig_rt_dist = plt.figure()
        iteration = np.linspace(0, len(self.rmse_data), len(self.rmse_data))
        ax1 = fig_rt_dist.add_subplot()
        ax2 = ax1.twinx() 

        ax1.plot(iteration, self.dist_trans_x, 'r-', label = "X axis translation")
        ax1.plot(iteration, self.dist_trans_y, 'b-', label = "Y axis translation")
        ax1.plot(iteration, self.dist_trans_z,'g-', label = "Z axis translation")
        ax2.plot(iteration, self.dist_rot_x, 'k--', label = "X axis rotation" ,markersize = 1)
        ax2.plot(iteration, self.dist_rot_y, 'y--', label = "Y axis rotation" ,markersize = 1)
        ax2.plot(iteration, self.dist_rot_z, 'm--', label = "Z axis rotation" ,markersize = 1)

        ax1.set_xlabel('iteration')  #x軸ラベル
        ax1.set_ylabel("Position error[mm]")  #y1軸ラベル
        ax2.set_ylabel("Rotation error[deg]")  #y2軸ラベル
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2 ,loc='upper right')
        ax1.set_ylim([0, 30])
        ax2.set_ylim([0, 2.0])

        ax1.grid()
        fig_rt_dist.savefig('./servo_data/trans_rot_dist_iteration.png') 


    def main(self):
        self.hand_eye_last_img()
        self.init_difference_img()
        self.last_difference_img()
        self.save_csv()
        self.joint_vel_data()
        self.orther_data()




        return print("data OK")