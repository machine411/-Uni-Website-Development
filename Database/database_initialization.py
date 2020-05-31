import mysql.connector
import sys
from mysql.connector import Error

#-------------------------------------------------------------
# CONNECTING TO THE mySQL DATABASE
#-------------------------------------------------------------
try: 
	#attempt to connect to mysql database hosted locally
	connection = mysql.connector.connect(host='localhost',
										database='test_database',
										user='root',
										password='password')


	#check that database has connected, else can't continue on
	if connection.is_connected():		
		
		#if connection succeeded, demonstrate by printing version
		db_server_version = connection.get_server_info()
		print("MySQL server version is: ", db_server_version)

		#next, need a cursor object for interfacing to the database
		cursor = connection.cursor()
		cursor.execute("select database();")
		print("Database name is: ", cursor.fetchall())

	#couldn't connect to database - stop script
	else:
		sys.exit("Initial connection was unsuccessful, terminating script.")

except mysql.connector.Error as mySQL_error:
	print("Failed to make table in mySQL: {}".format(mySQL_error))
except Error as e:
	print("Error connecting: ", e)

#-------------------------------------------------------------
# DELETING EXISTING TABLES IN THE DATABASE
#-------------------------------------------------------------

print(" ")
print("WARNING! INITIALIZATION WILL DELETE DATABASE. PLEASE TYPE 'yes' TO CONTINUE")
warning = input("")
print(" ")

#initialization will destroy existing tables
if warning != "yes":
	sys.exit("You have not deleted and reinitialized the database. Initialization stopped. Bye.")

#delete leaderboard table
mySQL_deleteLeaderboardTable = """DROP TABLE IF EXISTS test_database.LeaderBoard
							
							"""
result = cursor.execute(mySQL_deleteLeaderboardTable)
print("LeaderBoard table deleted")

#delete submissions table
mySQL_deleteSubmissionTable = """DROP TABLE IF EXISTS test_database.Submissions
							
							"""
result = cursor.execute(mySQL_deleteSubmissionTable)
print("Submission table deleted")

#delete user table
mySQL_deleteUserTable = """DROP TABLE IF EXISTS test_database.Users
					
					"""
result = cursor.execute(mySQL_deleteUserTable)
print("User table deleted")

#delete challenge table
mySQL_deleteChallengeTable = """DROP TABLE IF EXISTS test_database.Challenges
					
							"""
result = cursor.execute(mySQL_deleteChallengeTable)
print("Challenge table deleted")


#-------------------------------------------------------------
# CREATING NEW TABLES IN THE DATABASE
#-------------------------------------------------------------

#create user table
mySQL_createUserTable = """CREATE TABLE IF NOT EXISTS Users (
						user_id int NOT NULL AUTO_INCREMENT,
						nickname varchar(30) NOT NULL,
						email varchar(100) NOT NULL,
						password varchar(60) NOT NULL,
						is_privileged bit,
						PRIMARY KEY (user_id));"""
result = cursor.execute(mySQL_createUserTable)
print("User table created")

#create challenge table
mySQL_createChallengeTable = """CREATE TABLE IF NOT EXISTS Challenges (
						challenge_id int NOT NULL,
						title varchar(100) NOT NULL,
						overview varchar(1000),
						language_restriction varchar(100),
						is_input_text_file bit,
						public_tests varchar(1000),
						private_tests varchar(1000),						
						answers varchar(1000),
						start_date date,
						due_date date,
						close_date date,
						PRIMARY KEY(challenge_id));"""
result = cursor.execute(mySQL_createChallengeTable)
print("Challenge table created")

#create submission table
mySQL_createSubmissionTable = """CREATE TABLE IF NOT EXISTS Submissions (
						submission_id int NOT NULL,
						submission_challenge_id int NOT NULL,
						submission_user_id int NOT NULL,
						file_address varchar(255),
						language varchar(20) NOT NULL,
						submission_date date,
						is_being_evaluated bit,
						is_evaluated bit,
						PRIMARY KEY (submission_id),
						FOREIGN KEY (submission_challenge_id) REFERENCES Challenges(challenge_id),
						FOREIGN KEY (submission_user_id) REFERENCES Users(user_id));"""
result = cursor.execute(mySQL_createSubmissionTable)
print("Submission table created")

#create leaderboard table
mySQL_createLeaderBoardTable = """CREATE TABLE IF NOT EXISTS LeaderBoard (
						leaderboard_challenge_id int NOT NULL,
						submission_one_id int,
						submission_two_id int,
						submission_three_id int,
						PRIMARY KEY (leaderboard_challenge_id),
						FOREIGN KEY	(leaderboard_challenge_id) REFERENCES Challenges(challenge_id),
						FOREIGN KEY (submission_one_id) REFERENCES Submissions(submission_id),
						FOREIGN KEY (submission_two_id) REFERENCES Submissions(submission_id),
						FOREIGN KEY (submission_three_id) REFERENCES Submissions(submission_id));"""
result = cursor.execute(mySQL_createLeaderBoardTable)
print("Leaderboard table created")

#-------------------------------------------------------------
# END OF SCRIPT CLEAN-UPS
#-------------------------------------------------------------

#close connection once complete
cursor.close()
connection.close()