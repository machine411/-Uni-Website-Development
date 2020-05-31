import os
import time
from memory_profiler import *
import psutil
from subprocess import *
import numpy as np
import tracemalloc
import mprof
#hello
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
    # Overwritten the correntness variable
    global correntness
    correntness = len(match)/len(ans)

# Correctness 90%, Time Consumption 5%, Memory Consumption 5%
# Maximum time depends on the challenge
def marking():
    print("-------------------------------------- Marking --------------------------------------")
    global total_mark
    # Max admin set time is 10s
    max_time = 10
    # Max admin set memory usage is 100 Mib
    max_memory = 100
    # Calculate correntness mark
    corrent_mark = float(90)*correntness
    # Calculate time mark, if user`s compile time is greater than max set by admin, mark will be 0
    if max_time > time_need:
        time_mark = float(5)*((float(max_time) - time_need)/float(max_time))
    else:
        time_mark = 0
    # Calculate memory mark, if user`s memory Consumption is greater than max set by admin, mark will be 0
    if max_memory > memory_usage :
        memory_mark = float(5)*((float(max_memory) - memory_usage)/float(max_memory))
    else:
        memory_mark = 0
    # If the user doesn`t match any case, time mark and memory mark will all set to 0
    if correntness == 0:
        time_mark = 0
        memory_mark = 0
    print("time_mark ",time_mark)
    print("memory_mark ",memory_mark)
    print("correntness ",correntness)
    total_mark = corrent_mark + time_mark + memory_mark
    print("mark ",total_mark)
    print("-------------------------------------------------------------------------------------")

# Check if the current submission is better than pervious, if it is, overwritten the user`s best_score with the current submission
def copy_to_best(file):
    loc = file + "\\" + look4_user + "\\" + challenge
    if total_mark > best_score:
        source = loc + "\\submission"
        des    = loc + "\\best_score"
        cmd = "xcopy " + source + " " + des + " /y"
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

# Detect the user`s submission files and put into the corresponding compiler
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

if __name__ == '__main__':
    # The user we are looking for
    look4_user = "u1"
    # Selected challenge
    challenge = "sorting"
    time_need = 0
    memory_usage = 0
    correntness = 0
    total_mark = 0
    # Pervious best score
    best_score = 30
    file = "C:\\Users\\P\\Desktop\\SEP\\Code\\Engine\\Users"
    found_path = ""
    # Change working directary
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
