import mysql.connector
import sys
from mysql.connector import Error
from time import sleep

import os
import time
from memory_profiler import *
import psutil 
from subprocess import *
import numpy as np
import tracemalloc
import mprof

# Update this file directory address when porting between different computers. 
local_computer_base_path = "C:\\Users\\ryanc\\SEP\\Code\\Engine"

# Compare two txt file
def file_comparison():

    # Read and parse the file with the correct answers
    ans_path = local_computer_base_path + "\\Challenge Answer\\" + challenge_title + "\\ans.txt"
    with open(ans_path) as f:
        correct_answers = f.read().split()
    for i in correct_answers:
        if i == '\n':
            user.remove(i)

    # Read the users ourput file by partitioning each result
    with open("users_output.txt") as f:
        user_answers = f.read().split()
    for i in user_answers:
        if i == '\n':
            user_answers.remove(i)
    matching_answers = []

    # Check for error case when users output length is not equal to ans 
        # (prevent exceeding list maximum index)
    range_for_check = len(user_answers)
    if len(user_answers) > len(correct_answers):
        range_for_check = len(correct_answers)
    else:
        range_for_check = len(user_answers)
    
    # Check if user's answer matches to the correct answer
        # If it does, append the INDEX to a list of matching cases
    for i in range (0,range_for_check):
        if correct_answers[i] == user_answers[i]:
            matching_answers.append(i)
    print("result: ", len(matching_answers),"/",len(correct_answers))
    
    # Update the correctness variable with proportion of correct answers
    global correctness
    correctness = len(matching_answers)/len(correct_answers)

# Check if the current submission is better than pervious, if it is, overwritten the user`s best_score with the current submission
def copy_to_attempts_table(correctness_mark, time_mark, memory_mark, total_mark):

    global user_id
    global challenge_id    

    tableName = "Attempts_" + str(user_id)

    # Check if the user has attempted this challenge before.
        # If not, insert empty row.
    mySQL_insertRowForChallenge = """INSERT IGNORE INTO {}
                                     SET challenge_id = {};""".format(tableName, challenge_id)
    cursor.execute(mySQL_insertRowForChallenge)
    connection.commit()

    # Find the corresponding table row in the user's attempts table
    mySQL_findUsersAttemptForChallenge = "SELECT * FROM "+tableName+" WHERE challenge_id = "+str(challenge_id)+";"
    cursor.execute(mySQL_findUsersAttemptForChallenge)
    row = cursor.fetchone()
    print("Users current attempts for for this challenge is: ")
    print(row)
    
    print("About to update with these values:")
    print(tableName, correctness_mark, time_mark, memory_mark, total_mark, challenge_id)
    print("")

    # Always update their latest attempt to match this submission.
    mySQL_updateLatestAttempt = """UPDATE {}
                                SET latest_correctness = {}, latest_time = {}, latest_memory = {}, latest_score = {}
                                WHERE challenge_id = {};""".format(tableName, correctness_mark, time_mark, memory_mark, total_mark, challenge_id)
    cursor.execute(mySQL_updateLatestAttempt)
    print("Updated latest attempt. \n")
    connection.commit()
    
    # If their new mark is better, update their best attempt in their attempts table
    if total_mark > row["best_score"]:
        mySQL_updateBestAttempt = """UPDATE {}
                                     SET best_correctness = {}, best_time = {}, best_memory = {}, best_score = {}
                                     WHERE challenge_id = {};""".format(tableName, correctness_mark, time_mark, memory_mark, total_mark, challenge_id)
        cursor.execute(mySQL_updateBestAttempt)
        print("New best attempt! \n")
        connection.commit()

    # Mark submission as being completely evaluated in the table
        # i.e. now submission files can be deleted, important records are stored in database
    global submission_id
    mySQL_setSubmissionAsEvaluated = """UPDATE Submissions
                                            SET is_evaluated = 1
                                            WHERE submission_id = {}""".format(submission_id)
    cursor.execute(mySQL_setSubmissionAsEvaluated)
    connection.commit()
    print("This submission has been fully evaluated. \n")

    
# Correctness 90%, Time Consumption 5%, Memory Consumption 5%
# Maximum time depends on the challenge
def marking():
    print("-------------------------------------- Marking --------------------------------------")
    global total_mark
    # Max admin set time is 10s
    max_time = 10
    # Max admin set memory usage is 100 Mib
    max_memory = 100
    # Calculate correctness mark
    correctness_mark = float(90)*correctness
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
    if correctness == 0:
        time_mark = 0
        memory_mark = 0
    print("time_mark ",time_mark)
    print("memory_mark ",memory_mark)
    print("correctness ",correctness)
    total_mark = correctness_mark + time_mark + memory_mark
    print("mark ",total_mark)
    print("-------------------------------------------------------------------------------------")

    # Call function to copy mark result into users attempts table.
    copy_to_attempts_table(correctness_mark, time_mark, memory_mark, total_mark)

# Check the peak memory consumption of the program
def memory(cmd):
    # Clean up the mprof files
    os.system("mprof clean")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    # Use mprof module to run the user`s code
    cmd = "mprof run "+cmd+" > memoryout.txt"
    for retry in range(100):
        try:
            os.system(cmd)
    # Remove the unwanted output
            os.system("del memoryout.txt")
            break
        except:
            print ("retrying admin command...")
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
    cmd_compile = cmd + " > users_output.txt"
    start_time = time.time()
    os.system(cmd_compile)
    time_need = time.time() - start_time
    os.system("type users_output.txt")
    print("Time Consumption: ",time_need)
    file_comparison()
    memory(cmd)
# Compiler used for C++
def cpp_compiler(file):
    global time_need
    cmd = "g++ "+ file + " -o out & out"
    cmd_compile = cmd + " > users_output.txt"
    start_time = time.time()
    os.system(cmd_compile)
    time_need = time.time() - start_time
    os.system("type users_output.txt")
    print("Time Consumption: ",time_need)
    file_comparison()
    memory(cmd)
# Compiler used for java
def java_compiler(file):
    global time_need
    cmd = "java " + file
    cmd_compile = cmd + " > users_output.txt"
    start_time = time.time()
    os.system(cmd_compile)
    time_need = time.time() - start_time
    os.system("type users_output.txt")
    print("Time Consumption: ",time_need)
    file_comparison()
    memory(cmd)

# Compiler used for C
def c_compiler(file):
    global time_need
    cmd = "gcc "+ file + " -o out & out "
    cmd_compile = cmd +"> users_output.txt"
    start_time = time.time()
    os.system(cmd_compile)
    time_need = time.time() - start_time
    os.system("type users_output.txt")
    print("Time Consumption: ",time_need)
    file_comparison()
    memory(cmd)

# Detect the user`s submission files and put into the corresponding compiler
# cwd = C:\.....\Engine\User Submit\uxxx
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

    connection = mysql.connector.connect(host='localhost',
                                        database='test_database',
                                        user='root',
                                        password='password')
    cursor = connection.cursor(dictionary=True)

    while 1:

        print("Continue searching submissions? Type 'yes' to continue.")
        continue_searching = input("")
        print("")

        if continue_searching != "yes":
            print("Searching has been terminated. Bye.")
            break

        print("Looking for submissions")
        print("")

        try: 
            mySQL_lookForSubmissions = "SELECT * FROM Submissions where is_being_evaluated = 0 LIMIT 1;"
            cursor.execute(mySQL_lookForSubmissions)
            next_submission = cursor.fetchone()
            print("Next submission found is: ", next_submission)
            print("")
        except: 
            print("No submissions left to evaluate, program terminating.")
            print("\n\n\n\n")
            cursor.close()
            connection.close()
            sleep(5)
            exit()

        submission_id = next_submission["submission_id"]
        mySQL_setSubmissionAsBeingEvaluated = """UPDATE Submissions
                                                SET is_being_evaluated = 1
                                                WHERE submission_id = {}""".format(submission_id)
        cursor.execute(mySQL_setSubmissionAsBeingEvaluated)
        connection.commit()
        print("Marking submission as being evaluated (i.e. prevent other).")

        # next submission to evaluate found, extract user id and challenge id
        user_id = next_submission["submission_user_id"]
        challenge_id = next_submission["submission_challenge_id"]

        mySQL_userNicknameFromID = "SELECT nickname FROM Users where user_id = "+str(user_id)+";"
        cursor.execute(mySQL_userNicknameFromID)
        row = cursor.fetchone()
        user_nickname = row["nickname"]

        mySQL_challengeTitleFromID = "SELECT title FROM Challenges where challenge_id = "+str(challenge_id)+";"
        cursor.execute(mySQL_challengeTitleFromID)
        row = cursor.fetchone()
        challenge_title = row["title"]

        # output for verification in testing        
        print("User nickname should be: ", user_nickname)
        print("Challenge title should be: ", challenge_title)

        #initialize challenge scores to zero
        time_need = 0
        memory_usage = 0
        correctness = 0
        total_mark = 0



        file = local_computer_base_path + "\\Users"
        found_path = ""
        # Change working directary
        os.chdir(file)
        # looking for the user in the system
        found = 0
        for filename in os.listdir(file):
            cwd = os.getcwd()
            if filename == user_nickname:
                found = 1
                found_path = local_computer_base_path + "\\Users\\" + user_nickname + "\\" + challenge_title
            os.chdir(file)
        if found == 0:
            print("User not exist")
        # Access the folder and check for the language
        file_detecter(found_path)
        marking()


    cursor.close()
    connection.close()
    print("Connections closed, program terminating. \n\n\n\n")