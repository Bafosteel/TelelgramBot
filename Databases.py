from mysql import connector as mysql
from mysql.connector import errors as con_error
from Settings import auth

class DataBase(object):
    def __init__(self):
        self.db = mysql.connect(
            host = "localhost",
            user = auth['user'],
            passwd = auth['password']
        )
        self.cursor = self.db.cursor(buffered=True)

    def create_data(self):
        try:
            self.cursor.execute('USE Advcheck')
        except con_error.ProgrammingError:
            self.cursor.execute('CREATE DATABASE IF NOT EXISTS Advcheck')
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users(campaign VARCHAR(255), links VARCHAR(255))")
        return self.db.commit()

    def insert_data(self, message):
        self.create_data()
        val = (str(message.text)[:str(message.text).find(':')], str(message.text)[str(message.text).find(':') + 1:])
        sql = "INSERT INTO users (campaign, links) VALUES (%s,%s)"
        self.cursor.execute(sql, val)
        return self.db.commit()

    def select_data(self):
        self.create_data()
        self.cursor.execute("SELECT * FROM users")
        self.db.commit()
        data = {}
        for elem in self.cursor:
            data[elem[0]] = elem[1]
        return data

    def delete_data(self, message):
        self.create_data()
        val = (message.text,)
        data = self.select_data()
        for elem in data:
            if elem == val[0]:
                sql = "DELETE FROM Advcheck.users WHERE campaign=%s"
                self.cursor.execute(sql, val)
                self.db.commit()
                status = 'Кампания удалена'
            else:
                status = "Doesn't found campaign"
                return status
        return status
