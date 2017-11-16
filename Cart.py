import sqlite3
import Items
import Users
from decimal import Decimal
from re import sub

class Database():
    def __init__(self):
        db = sqlite3.connect("baecon.sqlite")
        try:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE CartOrder(ItemID int, UserID int, ItemPrice text, Quantity text)")
            db.commit()
            print("created CartOrder table")
        except Exception as e:
            print(e)
        db.close()

class Cart():
    def __init__(self):
        Database()
        self.database = sqlite3.connect("baecon.sqlite")
        self.cursor = self.database.cursor()


    def addItem(self, item_number):
        id = item_number
        #check if item is in cart
        self.cursor.execute("SELECT ItemID FROM CartOrder WHERE ItemID=?", [id])
        added_item = self.cursor.fetchall()

        #If item is not in cart. Add to cart from Items table
        if not added_item:
            self.cursor.execute("SELECT ItemID, ItemPrice FROM Items WHERE ItemID=?", [id])
            item = self.cursor.fetchall()
            add_id = item[0][0]
            price = item[0][1]
            quantity = "1"
            self.cursor.execute("INSERT INTO CartOrder(ItemID, ItemPrice, Quantity) VALUES (?, ?, ?)", [add_id, price, quantity])
            self.database.commit()
            print("added item " + str(id) + " to CartOrder")

        #If item is found update the quantity of that item in the cart table
        else:
            self.cursor.execute("SELECT ItemID, ItemPrice, Quantity FROM CartOrder WHERE ItemID=?", [id])
            item = self.cursor.fetchall()
            quantity = int(item[0][2]) + 1
            quantity = str(quantity)
            self.cursor.execute("UPDATE CartOrder SET Quantity = ? WHERE ItemID =?", [quantity, id])
            self.database.commit()
            print("updated item " + str(id) + " in CartOrder")
            self.cursor.execute("SELECT ItemPrice FROM Items WHERE ItemID =?",[id])
            itemprice = self.cursor.fetchall()
            price = 0
            for row in itemprice:
                price = Decimal(sub(r'[^\d.]', '', (list(row))[0]))
            print(price)
            price = (int(item[0][2])+1) * price
            price = "$"+ str(price)
            print(price)
            self.cursor.execute("UPDATE CartOrder SET ItemPrice = ? WHERE ItemID =?", [price, id])
            self.database.commit()
            self.cursor.execute("SELECT * FROM CartOrder")
            print(self.cursor.fetchall())


    def setOrderNum(self, ordernum):
        ordernum = ordernum
        self.cursor.execute("UPDATE CartOrder SET UserID = ? WHERE UserID ISNULL", [ordernum])
        self.database.commit()
        print("Set order number for all cart items")


    def getCartOrder(self):
        self.cursor.execute("SELECT * FROM CartOrder")
        print(self.cursor.fetchall())

    def getCartItems(self):
        self.cursor.execute("SELECT Items.ItemID, Items.ItemName, Items.ItemImage, CartOrder.ItemPrice, CartOrder.Quantity, CartOrder.UserID FROM Items INNER JOIN CartOrder on CartOrder.ItemID = Items.ItemID")
        cart = self.cursor.fetchall()
        print("Cart items: " + str(cart))
        return cart

    def updateItem(self, id, quant):
        i = id
        q = quant
        if quant == "0":
            self.cursor.execute("DELETE FROM CartOrder WHERE ItemID =?", [i])
            self.database.commit()
            print("removed item " + i + " from CartOrder")
        else:
            self.cursor.execute("UPDATE CartOrder SET Quantity = ? WHERE ItemID =?", [q, i])
            self.database.commit()
            print("updated item " + i + " in CartOrder")

            self.cursor.execute("SELECT ItemPrice FROM Items WHERE ItemID =?", [id])
            itemprice = self.cursor.fetchall()
            price = 0
            for row in itemprice:
                price = Decimal(sub(r'[^\d.]', '', (list(row))[0]))
            print(price)
            price = (int(q) * price)
            price = "$" + str(price)
            print(price)
            self.cursor.execute("UPDATE CartOrder SET ItemPrice = ? WHERE ItemID =?", [price, id])
            self.database.commit()
            self.cursor.execute("SELECT * FROM CartOrder")
            print(self.cursor.fetchall())

    def removeAllItems(self):
        self.cursor.execute("DELETE FROM CartOrder")
        self.database.commit()
        print("all rows deleted from CartOrder")

    def closeDatabase(self):
        self.database.close()


