import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="B4if0r6et.GREAT!",
    database="education_management"
)
print("Connected!")

# CREATE
cursor = connection.cursor()
sql = "INSERT INTO course_profile (course_name, course_code) VALUES (%s, %s)"
values = ("Numerical Computing", "COMP 350")
cursor.execute(sql, values)
connection.commit()
print(f"{cursor.rowcount} record inserted.")

# READ
cursor = connection.cursor()
cursor.execute("SELECT * FROM course_profile")
results = cursor.fetchall()
for row in results:
    print(row)

# UPDATE
cursor = connection.cursor()
sql = "UPDATE course_profile SET course_desc = %s WHERE course_name = %s"
values = ("MATLAB operations", "Numerical Computing")
cursor.execute(sql, values)
connection.commit()
print(f"{cursor.rowcount} record(s) updated.")

cursor = connection.cursor()
cursor.execute("SELECT * FROM course_profile")
results = cursor.fetchall()
for row in results:
    print(row)

# DELETE
cursor = connection.cursor()
sql = "DELETE FROM course_profile WHERE course_name = %s"
values = ("Numerical Computing",)
cursor.execute(sql, values)
connection.commit()
print(f"{cursor.rowcount} record(s) deleted.")

cursor = connection.cursor()
cursor.execute("SELECT * FROM course_profile")
results = cursor.fetchall()
for row in results:
    print(row)

cursor.close()
connection.close()