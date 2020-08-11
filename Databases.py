from mysql import connector as mysql
from mysql.connector import errors as con_error

db = mysql.connect(
    host = "localhost",
    user = "******",
    passwd = "********"
)

cursor = db.cursor(buffered=True)
cursor.execute("SHOW DATABASES")

def create_data():
    try:
        cursor.execute('USE Advcheck')
    except con_error:
        cursor.execute('CREATE DATABASE IF NOT EXISTS Advcheck')
        cursor.execute('DROP TABLE users')
        cursor.execute("CREATE TABLE IF NOT EXISTS users(campaign VARCHAR(255), links VARCHAR(255))")
        db.commit()

def insert_data(message):
    create_data()
    val = (str(message.text)[:str(message.text).find(':')], str(message.text)[str(message.text).find(':') + 1:])
    sql = "INSERT INTO users (campaign, links) VALUES (%s,%s)"
    cursor.execute(sql,val)
    return db.commit()

def select_data():
    create_data()
    cursor.execute("SELECT * FROM users")
    db.commit()
    data = {}
    for elem in cursor:
        data[elem[0]]=elem[1]
    return data

def delete_data(message):
    create_data()
    sql = "DELETE FROM users WHERE campaign=%s"
    cursor.execute(sql,message)
    return db.commit()
