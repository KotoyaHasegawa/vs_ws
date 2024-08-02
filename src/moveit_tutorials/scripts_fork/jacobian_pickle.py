#! /usr/bin/env python3
#coding: UTF-8

import numpy as np
import pandas as pd

###orig
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat.csv', header=None)
# csvdata.to_pickle('./pinv_int_mat_pickle/pinv_int_mat.pickle')

# pickledata = pd.read_pickle('./pinv_int_mat_pickle/pinv_int_mat.pickle')
# pinv_int_mat = np.array
# pinv_int_mat = pickledata.values

###double
print('henkan start')
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double1_ibvs.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_input_IBVS.csv', header=None)

#背景を一般に
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_IBVS_6.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_input_IBVS_6.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_ABVS.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_input_ABVS.csv', header=None)

#やり直し
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_ibvs2.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_input_ibvs2.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_input_avs2.csv', header=None)

#治具変更
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avs3.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_input_avs3.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avs4.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avs5.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avs6.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avs7.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avs8.csv', header=None)
# csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avs9.csv', header=None)
csvdata = pd.read_csv('./pinv_int_mat/pinv_int_mat_double_remove_avspos.csv', header=None)

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