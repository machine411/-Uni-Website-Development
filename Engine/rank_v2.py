import os
import time
import numpy as np
import pandas as pd
import csv
import operator
chal = "ai"
# path = "C:\\Users\\mypc\\Desktop\\SEP\\Code\\Engine\\Table.csv"
path = "C:\\Users\\P\\Desktop\\SEP\\maptek\\"+chal+".csv"
data_list = []
with open(path,'rt',encoding='utf-8')as f:
    data = csv.reader(f)
    for row in data:
        data_list.append(row)
data_list = np.asarray(data_list)
username_list = data_list[0:,0]
nickname_list = data_list[0:,1]
score_list = data_list[0:,2]
score_list = [int(i) for i in score_list]


dict_tmp = {}
for i in range(len(nickname_list)):
    dict_tmp[nickname_list[i]] = score_list[i]
print(dict_tmp)
dict_tmp = sorted(dict_tmp.items(), key=operator.itemgetter(1),reverse=1)
dict_tmp = dict(dict_tmp)

for i in dict_tmp.copy():
    if dict_tmp[i] == '':
        dict_tmp.pop(i)
dict_rank = dict_tmp.copy()
r = 1
p_key = "df"
p_value = "df"
for key,value in dict_rank.items():
    # Check if two scores are identity
    if value == p_value:
        r -= 1
    dict_rank[key] = "Rank " + str(r)
    p_key = key
    p_value = value
    r += 1
print(dict_tmp)
print(dict_rank)

filename = "./rank/rank_"+chal+".csv"
with open(filename, 'w',newline='') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dict_rank.items():
       writer.writerow([key, value])
