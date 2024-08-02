import csv
import numpy as np

def readfile(filename):
    data=[]
    with open(filename, encoding='utf8') as f:
        reader=csv.reader(f)
        writer=csv.writer(f)
        for i in reader:
            data.append(i)
    data=np.array(data)
    return data

def write(filename):
    f=open('out_removal.csv','w',newline='')
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
    for i in range(data.shape[1]):
        column = data[:,i]
        idx_outliner=zscore(column)
        data=np.delete(data, idx_outliner,axis=0)
    return data


data=readfile('random_theta_result.csv')


newdata=out_removal(data)
write(newdata)



