import sqlite3
import Items
import Orders
#username is email
#name is name
import Cart
import Orders


class Database():
    def __init__(self):
        db = sqlite3.connect("baecon.sqlite")
        try:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE Users(UserID INTEGER PRIMARY KEY AUTOINCREMENT, Username text, Password text,"
                           "Street text, City text, State text, Zip text, CardNumber int, SecurityCode text, ExpirationDate text, Phone text, Name text)")
            db.commit()
            print("created table Users")
        except Exception as e:
            print(e)
        db.close()

class User():
    def __init__(self):
        Database()
        self.database = sqlite3.connect("baecon.sqlite")
        self.cursor = self.database.cursor()

    def addUser(self, user_email, user_password, user_name):
        email = user_email
        name = user_name
        pw = user_password
        self.cursor.execute("INSERT INTO Users(Username, Password, Name) VALUES (?, ?, ?)", [email, pw, name])
        self.database.commit()
        self.cursor.execute("SELECT UserID, Username, Password, Name FROM Users")
        user = self.cursor.fetchone()
        print("created user: " + str(user[1]))
        return (user[0])

    def getPassword(self, username):
        username = username
        self.cursor.execute("SELECT * FROM Users WHERE Username=?", [username])
        info = self.cursor.fetchall()
        password = ""
        for row in info:
            row = list(row)
            password = row[2]
        print(password)
        return (password)

    def setPassword (self, user_id, new_pw):
        id = user_id
        pw = new_pw
        self.cursor.execute("UPDATE Users SET Password =? WHERE UserID =?", [pw, id])
        self.database.commit()
        self.cursor.execute("SELECT * FROM Users")
        users = self.cursor.fetchall()
        print(users)


    def getAllUsers(self):
        self.cursor.execute("SELECT UserID, Username, Password, Name FROM Users")
        users = self.cursor.fetchall()
        print("All Users: " + str(users))
        return (users)

    def isUser(self, user_name):
        u = user_name
        print(u)
        self.cursor.execute("SELECT UserID, Username, Password FROM Users WHERE Username=?", [u])
        user = self.cursor.fetchall()
        if not user:
            print("username " + str(user) + " not found")
            return False
        else:
            print("username " + str(user) + " found")
            return True

    def getLoginInfo(self, user_name):
        u = user_name
        self.cursor.execute("SELECT UserID, Username, Password FROM Users WHERE Username=?", [u])
        user = self.cursor.fetchall()
        return(user)


    def getName(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id])
        info = self.cursor.fetchall()
        name = ""
        for row in info:
            row = list(row)
            name = str(row[11])
        print(name)
        return str(name)

    def setName (self, user_id, user_name):
        id = user_id
        username = user_name
        self.cursor.execute("UPDATE Users SET Name =? WHERE UserID =?", [username, id])
        self.database.commit()




    def getPhone(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id])
        info = self.cursor.fetchall()
        phone = ""
        for row in info:
            row = list(row)
            phone = row[10]
        print(phone)
        return (phone)

    def setPhone(self, user_id, number):
        id = user_id
        number = number
        self.cursor.execute("UPDATE Users SET Phone =? WHERE UserID =?", [number, id])
        self.database.commit()
        info = self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id]).fetchall()
        print(info)


    def getEmail(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id])
        info = self.cursor.fetchall()
        email = ""
        for row in info:
            row = list(row)
            email = row[1]
        print(email)
        return (email)

    def setEmail(self, user_id, mail):
        id = user_id
        mail = mail
        self.cursor.execute("UPDATE Users SET Username =? WHERE UserID =?", [mail, id])
        self.database.commit()






    def getAddress(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id])
        info = self.cursor.fetchall()
        address = []
        for row in info:
            row = list(row)
            address.append(row[3])
            address.append(row[4])
            address.append(row[5])
            address.append(row[6])
        print(address)
        return (address)


    def getStreet(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id])
        info = self.cursor.fetchall()
        street = ""
        for row in info:
            row = list(row)
            street = (row[3])
        print(street)
        return (street)


    def setStreet(self, user_id, street):
        id = user_id
        street = street
        self.cursor.execute("UPDATE Users SET Street =? WHERE UserID =?", [street, id])
        self.database.commit()



    def getCity(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id])
        info = self.cursor.fetchall()
        city = ""
        for row in info:
            row = list(row)
            city = row[4]
        print(city)
        return (city)

    def setCity(self, user_id, city):
        id = user_id
        city = city
        self.cursor.execute("UPDATE Users SET City =? WHERE UserID =?", [city, id])
        self.database.commit()


    def getState(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id])
        info = self.cursor.fetchall()
        state = ""
        for row in info:
            row = list(row)
            state = row[5]
        print(state)
        return (state)

    def setState(self, user_id, state):
        id = user_id
        state = state
        self.cursor.execute("UPDATE Users SET State =? WHERE UserID =?", [state, id])
        self.database.commit()



    def getZip(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Users WHERE UserID=?", [id])
        info = self.cursor.fetchall()
        zip = ""
        for row in info:
            row = list(row)
            zip = row[6]
        print(zip)
        return (zip)

    def setZip(self, user_id, zip):
        id = user_id
        zip = zip
        self.cursor.execute("UPDATE Users SET Zip =? WHERE UserID =?", [zip, id])
        self.database.commit()



    def setAddress(self, user_id, street, city, state, zip):
        id = user_id
        street = street
        city = city
        state = state
        zip = zip
        self.cursor.execute("UPDATE Users SET Street =?, City=?, State=?, Zip = ? WHERE UserID =?", [street, city, state, zip, id])
        self.database.commit()


    def getCard(self, user_id):
        id = user_id
        self.cursor.execute("SELECT CardNumber, SecurityCode, ExpirationDate FROM Users WHERE UserID=?", [id])
        card = self.cursor.fetchone()
        if not card:
            return ("NONE")
        else:
            return (card)

    def setCard(self, user_id, number, code, date):
        id = user_id
        number = number
        code = code
        date = date
        self.cursor.execute("UPDATE Users SET CardNumber =?, SecurityCode=?, ExpirationDate=? WHERE UserID =?", [number, code, date, id])
        self.database.commit()

    def getOrders(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM Orders WHERE UserID =?", [id])
        orders = self.cursor.fetchall()
        print("User #" + str(user_id) + " orders: " + str(orders))
        return (orders)


    def getOrderHistory(self, user_id):
        id = user_id
        self.cursor.execute("SELECT OrderNumber, OrderDate FROM Orders WHERE UserID =?", [id])

        ordernums = self.cursor.fetchall()
        print("All orders: " + str(ordernums))



        self.cursor.execute("DROP TABLE IF EXISTS OrderHistory")
        self.database.commit()
        self.cursor.execute("CREATE TABLE OrderHistory AS SELECT Orders.OrderNumber, Orders.UserID, Orders.OrderDate, orderDetail.ItemID, orderDetail.Quantity, orderDetail.ItemPrice FROM Orders INNER JOIN orderDetail ON Orders.OrderNumber = orderDetail.OrderNumber WHERE Orders.UserID=?",[user_id])
        self.cursor.execute("SELECT * FROM OrderHistory")
        test3 =self.cursor.fetchall()
        #print(test3)

        details = []
        for order in ordernums:
            self.cursor.execute("SELECT * FROM OrderHistory WHERE OrderNumber =?", [order[0]])
            detail = self.cursor.fetchall()
            details.append(detail)
        print("details: " + str(details))

        return (details)

    def getOrderDetails(self, order_num):
        ordernum = order_num
        #self.cursor.execute("SELECT * FROM OrderDetail WHERE OrderNumber =?", [ordernum])
        #self.cursor.execute("SELECT Orders.OrderNumber, Orders.UserID, Orders.OrderDate, OrderDetail.ItemID, OrderDetail.ItemPrice, OrderDetail.Quantity FROM Orders INNER JOIN OrderDetail on OrderDetail.OrderNumber = Orders.OrderNumber WHERE Orders.OrderNumber = ?", [ordernum])
        self.cursor.execute("SELECT Orders.OrderNumber, Orders.UserID, Orders.OrderDate, Orders.OrderPrice, Items.ItemName, orderDetail.Quantity, orderDetail.ItemPrice FROM Items INNER JOIN (Orders INNER JOIN orderDetail ON Orders.OrderNumber = orderDetail.OrderNumber) ON Items.ItemID = orderDetail.ItemID WHERE (((Orders.OrderNumber)=?))", [ordernum])
        details = self.cursor.fetchall()
        allDets = []
        for row in details:
            allDets.append(list(row))
        #print(allDets)
        return allDets



    def removeAllItems(self):
        try:
            self.cursor.execute("DELETE FROM Users")
            self.database.commit()
            print("all rows deleted from Users")
        except Exception as e:
            print(e)
            self.database.rollback()

    def removeUser(self, id):
        id = id
        self.cursor.execute("DELETE FROM Users WHERE UserID = ?", [id])
        self.database.commit()
        users = self.cursor.execute("SELECT * FROM Users").fetchall()
        print(users)

        print(str(id) + " has been deleted from Users")

    def closeDatabase(self):
        self.database.close()





