import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Expense_tracker"
)

cursor = connection.cursor()
cursor.execute("SHOW TABLES")

for table in cursor:
    print(table)

connection.close()
print("Connected successfully!")