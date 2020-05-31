import mysql.connector
import sys
from mysql.connector import Error

def createUserAttemptsTable(user_id):

	tableName = "Attempts_" + str(user_id)

	mySQL_resetAttemptsTable = "DROP TABLE IF EXISTS {}".format(tableName)
	result = cursor.execute(mySQL_resetAttemptsTable)
	print("Deleted any old attempts tables for user: ", user_id)

	mySQL_createAttemptsTable = """CREATE TABLE IF NOT EXISTS {} (
								challenge_id int NOT NULL,
								best_correctness float DEFAULT 0,
								best_time float DEFAULT 0,
								best_memory float DEFAULT 0,
								best_score float DEFAULT 0,
								latest_correctness float DEFAULT 0,
								latest_time float DEFAULT 0,
								latest_memory float DEFAULT 0,
								latest_score float DEFAULT 0,
								PRIMARY KEY(challenge_id));""".format(tableName)
	result = cursor.execute(mySQL_createAttemptsTable)
	print("Create attempts table for user: ", user_id)
	print("")


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
		
		print("")
		print("CONNECTION TO mySQL DATABASE WAS SUCCESSFUL")

		#if connection succeeded, demonstrate by printing version
		db_server_version = connection.get_server_info()
		print("MySQL server version is: ", db_server_version)

		#next, need a cursor object for interfacing to the database
		cursor = connection.cursor(dictionary=True)
		cursor.execute("select database();")
		print("Database name is: ", cursor.fetchone())
		print("")

	#couldn't connect to database - stop script
	else:
		sys.exit("Initial connection was unsuccessful, terminating script.")

except mysql.connector.Error as mySQL_error:
	print("Failed to make table in mySQL: {}".format(mySQL_error))
except Error as e:
	print("Error connecting: ", e)

#-------------------------------------------------------------
# FIRST: LETS INSERT SOME USERS INTO THE DATABASE
#-------------------------------------------------------------

#sql statement to insert the entries
mySQL_insertUsers = """INSERT INTO Users(user_id, email, password, is_privileged, nickname)
					VALUES
						(1, 'Fred@gmail.com', 'PasswordForFred', 1, 'u1'),
						(2, 'George@gmail.com', 'CheeseyPassword', 0, 'u2'),
						(3, 'Harry@gmail.com', 'password', 0, 'u3');
					"""
result = cursor.execute(mySQL_insertUsers)
print("Sample users inserted")

createUserAttemptsTable(1)
createUserAttemptsTable(2)
createUserAttemptsTable(3)



#-------------------------------------------------------------
# SECOND: CHALLENGES
#-------------------------------------------------------------

mySQL_insertChallenge = """INSERT INTO Challenges(challenge_id, title, public_tests, private_tests)
						VALUES
							(1, 'sorting', '1 3 4 7 9', '2 5 6.5');
						"""
result = cursor.execute(mySQL_insertChallenge)
print("Challenge one inserted")




#-------------------------------------------------------------
# THIRD: SUBMISSIONS
#-------------------------------------------------------------

mySQL_insertSubmissions = """INSERT INTO Submissions(submission_id, submission_challenge_id, submission_user_id, language, is_being_evaluated, is_evaluated)
						VALUES
							(1, 1, 3, 'CPP', 1, 1),
							(2, 1, 3, 'CPP', 1, 1),
							(3, 1, 1, 'PYTHON', 0, 0);
						"""
result = cursor.execute(mySQL_insertSubmissions)
print("Submissions for challenge one made by user 1 <twice> and 3")

#commit changes
connection.commit()


sub_id = 3


######GETTING USER ID FROM A SUBMISSION ID AND UPDATING A VALUE
#first, find user id of the submission
mySQL_userFromSubmission_findUser = "SELECT * FROM Submissions where submission_id = " +str(sub_id) + ";"
cursor.execute(mySQL_userFromSubmission_findUser)
#result is in the form of a list of tuples
result = cursor.fetchone()
print("This submission information is: ", result)
#element is now in the form of a tuple
id_user = result["submission_user_id"]
#return that users info
mySQL_returnUserOfSubmission = "SELECT * FROM Users WHERE user_id = " + str(id_user) + ";"
cursor.execute(mySQL_returnUserOfSubmission)
result = cursor.fetchone()
#print("Selected: ", result)
print(result["email"])



#-------------------------------------------------------------
# END OF SCRIPT, COMMIT AND CONNECTION
#-------------------------------------------------------------



#close connection once complete
cursor.close()
connection.close()
print("\n\n\n\n")