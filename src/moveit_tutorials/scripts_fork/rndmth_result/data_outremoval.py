import csv
import numpy as np
import math

def readfile(filename):
    data=[]
    with open(filename) as f:#encoding='utf8'
        reader=csv.reader(f)
        for i in reader:
            data.append(i)
    data=np.array(data)
    return data

def write(filename):
    f=open('rndmth_result/out_removal.csv','w')#newline=''
    data=filename
    writer=csv.writer(f)
    writer.writerows(data)
    f.closed

def zscore(data_col):
    threshold=2.5
    xi=np.array(data_col, dtype=float)

    mean=np.mean(xi)
    std=np.std(xi)
    zi=(xi-mean)/std

    idx_outliner=np.where((zi < -1*threshold) | (threshold < zi))
    return idx_outliner

def out_removal(data):
    idx=[]
    for i in range(data.shape[1]):
        column = data[:,i]
        idx_outliner=zscore(column)
        idx.append(np.array(idx_outliner, dtype=float))
        data=np.delete(data, idx_outliner,axis=0)

        
    return data[:num_rows_to_remove, :],idx

def out_removal_pose(data,idx):
    for i in list(idx):
        data = np.delete(data, i.astype(int),axis=0)    
    return data[:num_rows_to_remove, :]

def adjust_negative_values(data):
    xi=data.astype(float)
    for i in range(xi.shape[0]):
        if xi[i, 5] > 0:
            # print(i+1)
            # print(xi[i, 5])
            xi[i, 5] -= 2*math.pi
    return xi


# remove only joint 5th 
# def out_removal(data): 
#     column = data[:,4]
#     idx_outliner=zscore(column)
#     data=np.delete(data, idx_outliner,axis=0)
#     return data

num_rows_to_remove = int(input("How many rows do you want to keep？ n ="))

data=readfile('rndmth_result/random_theta_result.csv')
data1=readfile('rndmth_result/random_pose.csv')
data2=readfile('rndmth_result/random_poseor.csv')

newdata,idx = out_removal(data)

# print(idx)
write(newdata)

data1 = out_removal_pose(data1,idx)
f1=open('rndmth_result/random_posedel.csv','w')#newline=''
writer=csv.writer(f1)
writer.writerows(data1)
f1.closed

data2=out_removal_pose(data2,idx)
#リンク3の値を調整
# data2_adjusted = adjust_negative_values(data2)
f2=open('rndmth_result/random_poseordel.csv','w')#newline=''
writer=csv.writer(f2)
# writer.writerows(data2_adjusted)
writer.writerows(data2)
f2.closed




