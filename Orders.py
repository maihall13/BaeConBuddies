import sqlite3

import Items
import Users
import Cart
import ActiveUser
import datetime

class Database():
    def __init__(self):
        db = sqlite3.connect("baecon.sqlite")
        try:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE Orders(OrderNumber INTEGER PRIMARY KEY AUTOINCREMENT , UserID INTEGER, OrderDate text, OrderPrice text)")
            db.commit()
            cursor.execute(
                "CREATE TABLE OrderDetail(OrderNumber INTEGER, ItemID INTEGER, Quantity text, ItemPrice text)")
            db.commit()
        except Exception as e:
            print(e)

class Order():
    def __init__(self):
        Database()
        self.database = sqlite3.connect("baecon.sqlite")
        self.cursor = self.database.cursor()


    def createGuestOrder(self, order_date):
        date = order_date
        self.cursor.execute("INSERT INTO Orders(OrderDate) VALUES (?)", [date])
        self.database.commit()
        self.cursor.execute("SELECT * FROM Orders WHERE OrderDate=?", [date])
        added_order = self.cursor.fetchall()
        print("added: " + str(added_order))
        print(added_order[0][0])
        return (added_order[0][0])


    def createUserOrder(self, user_id, order_date):
        id = user_id
        date = order_date
        self.cursor.execute("INSERT INTO Orders(UserID, OrderDate) VALUES (?, ?)", [id, date])
        self.database.commit()
        self.cursor.execute("SELECT last_insert_rowid() FROM Orders")
        row = self.cursor.fetchall()
        rowid = row[0][0]
        self.cursor.execute("SELECT * FROM Orders WHERE ROWID = ?",[rowid])
        ordernum = self.cursor.fetchall()

        self.cursor.execute("SELECT * FROM Orders")
        orders = self.cursor.fetchall()
        print("All Orders: " + str(orders))
        return (ordernum[0][0])


    #Add each items from the cart to users order under a specific ordernumber
    def addCartToOrder(self, order_number):
        self.cursor.execute("SELECT UserID, ItemID, ItemPrice, Quantity FROM CartOrder WHERE UserID = ?", [order_number])
        order = self.cursor.fetchall()
        #iterates through order all the orders in the cart and adds them to order.
        #for ever order in order creates an order detail

        statement = "INSERT INTO OrderDetail(OrderNumber, ItemID, ItemPrice, Quantity) VALUES (?,?,?,?)"
        self.cursor.executemany(statement, order)
        self.database.commit()

        self.cursor.execute("SELECT * FROM OrderDetail")
        details = self.cursor.fetchall()
        print("All Order Details: " + str(details))

    def getAllOrders(self):
        self.cursor.execute("SELECT * FROM Orders")
        orders = self.cursor.fetchall()
        print("All Orders: " + str(orders))
        return orders

    def getAllOrderDetails(self):
        self.cursor.execute("SELECT * FROM OrderDetail")
        details = self.cursor.fetchall()
        print("All Order Details: " + str(details))
        return details

    def getOrderDetails(self, order_number):
        self.cursor.execute("SELECT Orders.OrderNumber, Orders.UserID, Orders.OrderDate, OrderDetail.ItemID, OrderDetail.ItemPrice, OrderDetail.Quantity FROM Orders INNER JOIN OrderDetail on OrderDetail.OrderNumber = Orders.OrderNumber")
        test = self.cursor.fetchall()
        return test

    def updateOrderPrice(self, orderPrice, ordernum):
        price = orderPrice
        ordernum = ordernum
        self.cursor.execute("UPDATE Orders SET OrderPrice = ? WHERE OrderNumber =?", [price, ordernum])
        self.database.commit()

    def removeAllOrders(self):
        try:
            self.cursor.execute("DELETE FROM Orders")
            self.database.commit()
        except:
            self.database.rollback()
    def removeGuestOrders(self):
        try:
            self.cursor.execute("DELETE FROM Orders WHERE UserId ISNULL")
            self.database.commit()
            print("remove guest orders")
            print(self.getAllOrders())
        except Exception as e:
            print(e)


    def removeAllOrderDetails(self):
        try:
            self.cursor.execute("DELETE FROM OrderDetail")
            self.database.commit()
        except:
            self.database.rollback()

    def closeDatabase(self):
        self.database.close()







