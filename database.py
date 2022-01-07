import mysql.connector
from app import db

mydb = mysql.connector.connect(
    host= "localhost",
    user= "root",
    passwd = "password",  
)

my_cursor = mydb.cursor()

my_cursor.execute("SHOW DATABASES")

notthere=True

for dbs in my_cursor: 
    if dbs[0] == 'emp':
        notthere=False

if notthere:
    my_cursor.execute("CREATE DATABASE emp")

my_cursor.execute("USE emp")
db.create_all()