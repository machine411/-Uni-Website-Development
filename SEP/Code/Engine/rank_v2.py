import os
import mysql.connector
import time
import numpy as np
import pandas as pd
import csv
import operator
import sys
def fetch_data(chal):
  # mycursor.execute('SELECT users.username,users.nickname,ai.score FROM users INNER JOIN ai ON users.username=ai.username;')
    tmp = "`"+chal+"`"
    mycursor.execute('SELECT username,best_mark FROM '+ tmp)
    result=mycursor.fetchall()
    for row in result:
        print(row)
    mydb.commit()
    mycursor.close()
    return result


if __name__ == '__main__':
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="123",
      database="test_version",
      auth_plugin="mysql_native_password"
    )
    mycursor = mydb.cursor()
    chal = sys.argv[1]

    data_list = fetch_data(chal)
    data_list = np.asarray(data_list)
    if(data_list.shape[0]==0):
        print("Empty Table")
        exit();
    username_list = data_list[0:,0]
    # nickname_list = data_list[0:,1]
    score_list    = data_list[0:,1]
    score_list    = [float(i) for i in score_list]
    print("------------------------------------ PARTICIPANTS ------------------------------------")
    print("username_list: ",username_list)
    # print("nickname_list: ",nickname_list)
    print("score_list:    ",score_list)
    print('\n')

    print("------------------------------------- RANK -------------------------------------------")
    dict_tmp = {}
    for i in range(len(username_list)):
        dict_tmp[username_list[i]] = score_list[i]
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
        dict_rank[key] = int(r)
        p_key = key
        p_value = value
        r += 1
    print("FINAL MARK: ",dict_tmp)
    # print("FINAL RANK: ",dict_rank)

    filename = "C:\\Users\\P\\Desktop\\SEP\\Code\\Engine\\Rank\\"+chal+".csv"
    with open(filename, 'w',newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dict_tmp.items():
           writer.writerow([key, value])
