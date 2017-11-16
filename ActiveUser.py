import sqlite3

#user = current.user
#user.user i


class Database():
    def __init__(self):
        db = sqlite3.connect("baecon.sqlite")
        try:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE ActiveUser(UserID int, Username text)")
            db.commit()
            print("created table Users")
        except Exception as e:
            print(e)
        db.close()

class ActiveUser():
    def __init__(self):
        Database()
        self.database = sqlite3.connect("baecon.sqlite")
        self.cursor = self.database.cursor()

    def createActiveUser(self, user_id, user_name):
        id = user_id
        username = user_name
        self.cursor.execute("INSERT INTO ActiveUser(UserID, Username) VALUES (?,?)", [id, username])
        self.database.commit()
        self.cursor.execute("SELECT * FROM ActiveUser")
        test = self.cursor.fetchall()
        print("Created active user: " + str(test))
        return (test)

    def getUserID(self):
        self.cursor.execute("SELECT * FROM ActiveUser")
        test = self.cursor.fetchone()
        return (test[0])

    def getUserName(self):
        try:
            self.cursor.execute("SELECT * FROM ActiveUser")
            test = self.cursor.fetchone()
            return (test[1])
        except:
            self.database.rollback()

    def getAll(self):
        self.cursor.execute("SELECT * FROM ActiveUser")
        all = self.cursor.fetchall()
        return (all)


    def removeAllItems(self):
        self.cursor.execute("DELETE FROM ActiveUser")
        self.database.commit()
        self.cursor.execute("SELECT * FROM ActiveUser")
        users = self.cursor.fetchall()
        print("Remove all active users: " + str(users))
        return (users)


    def closeDatabase(self):
        self.database.close()

