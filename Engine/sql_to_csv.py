import mysql.connector
import csv
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123",
  database="a1680043",
  auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()
# Copy csv
mycursor.execute('SELECT users.username,users.nickname,ai.score FROM users INNER JOIN ai ON users.username=ai.username;')
result=mycursor.fetchall()
with open('ai.csv','w',newline='') as f:
    writer = csv.writer(f)
    for row in result:
        writer.writerow(row)
#
# # PRINTER
# mycursor.execute("SELECT * FROM users")
# result = mycursor.fetchall()
for row in result:
    print(row)
mydb.commit()
mycursor.close()
