#! /usr/bin/env python3
#coding: UTF-8

import numpy as np
import pandas as pd

###double
print('henkan start')
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_remove_avspos_1st.csv', header=None)#pice of 1500
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avspos3000.csv', header=None)#pice of 3000
csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avspos.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avspos_2value.csv', header=None)

print('read csv file')
csvdata.to_pickle('./pinv_int_mat_pickle/pinv_int_mat_double.pickle')
print('done')



csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mnipulator_jac.csv', header=None)

print('read csv file')
csvdata.to_pickle('./pinv_int_mat_pickle/pinv_int_mnipulator_jac.pickle')
print('done')


###normalized
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_normalized.csv', header=None)
# csvdata.to_pickle('./pinv_int_mat_pickle/pinv_int_mat_normalized.pickle')