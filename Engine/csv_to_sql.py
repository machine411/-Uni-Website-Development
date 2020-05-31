import mysql.connector
import csv
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123",
  database="a1680043",
  auth_plugin="mysql_native_password"
)

# INSERT VALUE INTO MYSQL
mycursor = mydb.cursor()
mycursor.execute("DELETE FROM users ")
# Copy csv
csv_data = csv.reader(open('C:\\Users\\P\\Desktop\\SEP\\maptek\\test\\test.csv'))
for row in csv_data:
    row[0] = int(row[0])
    mycursor.execute('INSERT INTO users(userid,username,password) VALUES(%s, %s, %s)',row)
print("------------------------------------------")
# Copy users
mycursor.execute("SELECT * FROM users")
myresult = mycursor.fetchall()
for row in myresult:
    print(row)
mydb.commit()
mycursor.close()
