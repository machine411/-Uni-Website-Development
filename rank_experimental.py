import os
import time
import numpy as np
import pandas as pd
import csv
import operator

path = "C:\\Users\\ryanc\\SEP\\Code\\Engine\\Table.csv"

data_list = []
with open(path,'rt',encoding='utf-8')as f:
    data = csv.reader(f)
    for row in data:
        data_list.append(row)
data_list = np.asarray(data_list)
challenge_list = data_list[0,1:]
user_list = data_list[1:,0]
score_list = data_list[1:,1:]
# Sorting	AVL tree	Rat in maze	SVM
selected_chal = "AVL tree"
index_chal = np.where(challenge_list==selected_chal)
index_chal = int(index_chal[0])

dict_tmp = {}
for i in range(len(user_list)):
    dict_tmp[user_list[i]] = score_list[i][index_chal]

dict_tmp = sorted(dict_tmp.items(), key=operator.itemgetter(1))

dict_tmp = dict(dict_tmp)
for i in dict_tmp.copy():
    if dict_tmp[i] == '':
        dict_tmp.pop(i)
print(dict_tmp)
