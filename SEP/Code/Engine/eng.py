import mysql.connector
import numpy as np
import mprof
import time
import sys
import os
from memory_profiler import *
# Compare two txt file
def file_comparison():
    # Read answer
    ans_path = "C:\\Users\\P\\Desktop\\SEP\\Code\\Engine\\Challenge Answer\\" + challenge + "\\ans.txt"
    with open(ans_path) as f:
        ans = f.read().split()
    for i in ans:
        if i == '\n':
            user.remove(i)
    # Read user
    with open("the_output.txt") as f:
        user = f.read().split()
    for i in user:
        if i == '\n':
            user.remove(i)
    match = []
    # Check for error case when users output length is not equal to ans (pervent exceed list maximum index)
    range_for_check = len(user)
    if len(user) > len(ans):
        range_for_check = len(ans)
    else:
        range_for_check = len(user)
    # Check numbers of match cases
    for i in range (0,range_for_check):
        if ans[i] == user[i]:
            match.append(i)
    print("result: ", len(match),"/",len(ans))
    # Overwritten the correctness variable
    global correctness
    correctness = len(match)/len(ans)

# Correctness 90%, Time Consumption 10%
# Maximum time depends on the challenge
def marking():
    print("-------------------------------------- Marking --------------------------------------")
    global final_mark
    # Max admin set time is 10s
    max_time = 10
    # Max admin set memory usage is 100 Mib
    max_memory = 100
    # Calculate correctness mark
    global correct_mark
    correct_mark = float(90)*correctness
    # Calculate time mark, if user`s compile time is greater than max set by admin, mark will be 0
    if max_time > time_need:
        global time_mark
        time_mark = float(5)*((float(max_time) - time_need)/float(max_time))
    else:
        time_mark = 0
    # Calculate memory mark, if user`s memory Consumption is greater than max set by admin, mark will be 0
    if max_memory > memory_usage :
        global memory_mark
        memory_mark = float(5)*((float(max_memory) - memory_usage)/float(max_memory))
    else:
        memory_mark = 0
    # If the user doesn`t match any case, time mark and memory mark will all set to 0
    if correctness == 0:
        time_mark = 0
        memory_mark = 0
    final_mark = correct_mark + time_mark + memory_mark
    print("mark ",final_mark)
    print("correct_mark ",correct_mark)
    print("time_mark ",time_mark)
    print("memory_mark ",memory_mark)

    print("-------------------------------------------------------------------------------------")

# Check if the current submission is better than pervious, if it is, overwritten the user`s best_score with the current submission
def copy_to_best(file):
    loc = file + "\\" + look4_user + "\\" + challenge
    if final_mark > best_score:
        source = loc + "\\submission"
        des    = loc + "\\best_score"
        os.system("del /S /Q "+des)
        cmd = "copy " + source + " " + des + " /y"
        os.system(cmd)

# Check the peak memory consumption of the program
def memory(cmd):
    # Clean up the mprof files
    os.system("mprof clean")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    # Use mprof module to run the user`s code
    cmd = "mprof run "+cmd+" > memoryout.txt"
    os.system(cmd)
    # Remove the unwanted output
    os.system("del memoryout.txt")
    n = "default"
    # Get the file name for the .dat file created by mprof
    for file in os.listdir(os.getcwd()):
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".dat":
            n = filename
    # Get the full file name for .dat file
    n = n+".dat"
    # Read the library`s function [function will read the mprof output file`s data]
    mp = mprof.read_mprofile_file(n)
    # Extract the runtime memory usage for user`s script
    memory_list = mp['mem_usage']
    global memory_usage
    # Overwritten the maximum memory usage for the user`s script
    memory_usage = max(memory_list)
    print("MAX MEMORY: ",memory_usage," Mib")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    # Clean up the folder
    os.system("mprof clean")

# Compiler used for Python
def python_compiler(file):
    global time_need
    cmd = "python "+ file
    cmd_compile = cmd + " > the_output.txt"
    start_time = time.time()
    os.system(cmd_compile)
    time_need = time.time() - start_time
    os.system("type the_output.txt")
    print("Time Consumption: ",time_need)
    file_comparison()
    memory(cmd)

# Compiler used for C++
def cpp_compiler(file):
    global time_need
    cmd = "g++ "+ file + " -o out & out"
    cmd_compile = cmd + " > the_output.txt"
    start_time = time.time()
    os.system(cmd_compile)
    time_need = time.time() - start_time
    os.system("type the_output.txt")
    print("Time Consumption: ",time_need)
    file_comparison()
    memory(cmd)

# Compiler used for java
def java_compiler(file):
    global time_need
    cmd = "java " + file
    cmd_compile = cmd + " > the_output.txt"
    start_time = time.time()
    os.system(cmd_compile)
    time_need = time.time() - start_time
    os.system("type the_output.txt")
    print("Time Consumption: ",time_need)
    file_comparison()
    memory(cmd)

# Compiler used for C
def c_compiler(file):
    global time_need
    cmd = "gcc "+ file + " -o out & out "
    cmd_compile = cmd +"> the_output.txt"
    start_time = time.time()
    os.system(cmd_compile)
    time_need = time.time() - start_time
    os.system("type the_output.txt")
    print("Time Consumption: ",time_need)
    file_comparison()
    memory(cmd)

# cwd = C:\Users\P\Desktop\SEP\Code\Engine\User Submit\uxxx
def file_detecter(path):
    path = path + "\\submission"
    os.chdir(path)
    for file in os.listdir(path):
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".py":
            python_compiler(file)
        elif file_extension == ".cpp":
            cpp_compiler(file)
        elif file_extension == ".java":
            java_compiler(file)
        elif file_extension == ".c":
            c_compiler(file)

def update_mark(best_score):
    # UPDATE `test_version`.`bubblesort` SET `final_mark` = '1' WHERE (`username` = 'test@test.com');
    if (final_mark > best_score):
        print("BETTER SUBMISSION FOUND :)")
        best_score = final_mark
    else: print("WORSE THAN PERVIOUS :(")
    if (user_exist==1):
        query = ("UPDATE "+challenge+" SET final_mark = %s, correct_mark=%s, time_mark=%s, memory_mark=%s,best_mark=%s WHERE (username = %s);")
        data  = (final_mark, correct_mark, time_mark, memory_mark,best_score,look4_user)
    else:
        query = (
          "INSERT INTO "+challenge+" (username, final_mark, correct_mark, time_mark, memory_mark,best_mark) "
          "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        data = (look4_user, final_mark, correct_mark, time_mark, memory_mark,final_mark)
    mycursor.execute(query,data)
    mydb.commit()

def check_users():
    query = ("SELECT * FROM "+challenge+" WHERE username = %(username)s;")
    mycursor.execute(query,{ 'username': look4_user })
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        print ("It Does Not Exist")
        return 0
    else:
        return 1

def check_pervious_score():
    query = ("SELECT * FROM "+challenge+" WHERE username = %(username)s;")
    mycursor.execute(query,{ 'username': look4_user })
    myresult = mycursor.fetchall()
    tmp = myresult[0]
    # global best_score
    best_score = tmp[5]
    # print("best_score: ",best_score)
    print("check pervious",best_score)
    return best_score



if __name__ == '__main__':
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="123",
      database="test_version",
      auth_plugin="mysql_native_password"
    )
    mycursor = mydb.cursor()
    look4_user = sys.argv[1]
    challenge = sys.argv[2]
    # Check if exist user in table
    user_exist = check_users()
    time_need = 0
    correctness  = 0
    final_mark   = 0
    correct_mark = 0
    time_mark    = 0
    memory_mark  = 0
    best_score   = 0
    if (user_exist == 1):
        best_score = check_pervious_score()
    else:
        best_score = 0
    file = "C:\\Users\\P\\Desktop\\SEP\\Code\\Engine\\Users"
    found_path = ""

    #cwd -> current working dir
    os.chdir(file)

    # looking for the user in the system
    found = 0
    for filename in os.listdir(file):
        cwd = os.getcwd()
        if filename == look4_user:
            found = 1
            found_path = "C:\\Users\\P\\Desktop\\SEP\\Code\\Engine\\Users\\" + look4_user + "\\" + challenge
        os.chdir(file)
    if found == 0:
        print("User not exist")
    # Access the folder and check for the language
    file_detecter(found_path)
    marking()
    copy_to_best(file)
    update_mark(best_score)
    # mydb.commit()
    mycursor.close()
