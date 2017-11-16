import sqlite3

flavors = ["Honey Glazed", "Chipotle", "Black Pepper",
               "Hickory Smoked", "Applewood"]
images = [
        "http://food.fnr.sndimg.com/content/dam/images/food/fullset/2015/12/1/3/AS0617H_Honey-Bourbon-Glazed-Bacon_s4x3.jpg",
        "http://www.simplecomfortfood.com/wp-content/uploads/2009/12/chipotle-bacon.jpg",
        "http://www.berniesfinemeats.com/assets/images/New%20Pictures%202011/D30_3932.jpg",
        "https://www.baconscouts.com/wp-content/uploads/2016/10/GCM-thick-cut-bacon-HERO.jpg",
        "http://premierproteins.com/assets/uploads/2014/11/bacon-300x300.jpg"]

class Database():
    def __init__(self):
        db = sqlite3.connect("baecon.sqlite")
        print("database connected")
        try:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE Items(ItemID INTEGER PRIMARY KEY AUTOINCREMENT, ItemName text, ItemImage text, ItemPrice text)")
            db.commit()

            name = "Honey Glazed"
            image = "http://food.fnr.sndimg.com/content/dam/images/food/fullset/2015/12/1/3/AS0617H_Honey-Bourbon-Glazed-Bacon_s4x3.jpg"
            price = "$5.00"
            cursor.execute("INSERT INTO Items(ItemName, ItemImage,ItemPrice) VALUES (?, ?, ?)", [name, image, price])
            db.commit()

            name = "Chipotle"
            image = "http://www.simplecomfortfood.com/wp-content/uploads/2009/12/chipotle-bacon.jpg"
            price = "$5.00"
            cursor.execute("INSERT INTO Items(ItemName, ItemImage,ItemPrice) VALUES (?, ?, ?)", [name, image, price])
            db.commit()

            name = "Black Pepper"
            image = "http://www.berniesfinemeats.com/assets/images/New%20Pictures%202011/D30_3932.jpg"
            price = "$5.00"
            cursor.execute("INSERT INTO Items(ItemName, ItemImage,ItemPrice) VALUES (?, ?, ?)", [name, image, price])
            db.commit()

            name = "Hickory Smoked"
            image = "https://www.baconscouts.com/wp-content/uploads/2016/10/GCM-thick-cut-bacon-HERO.jpg"
            price = "$5.00"
            cursor.execute("INSERT INTO Items(ItemName, ItemImage,ItemPrice) VALUES (?, ?, ?)", [name, image, price])
            db.commit()

            name = "Applewood"
            image = "http://premierproteins.com/assets/uploads/2014/11/bacon-300x300.jpg"
            price = "$5.00"
            cursor.execute("INSERT INTO Items(ItemName, ItemImage,ItemPrice) VALUES (?, ?, ?)", [name, image, price])
            db.commit()
            print("created table Items")
        except Exception as e:
            print(e)
        db.close()
        print("database closed")



class Items():
    def __init__(self):
        Database()
        self.database = sqlite3.connect("baecon.sqlite")
        self.cursor = self.database.cursor()
        print("database connected")

    def getAllItems(self):
        self.cursor.execute("SELECT ItemID, ItemName, ItemImage, ItemPrice FROM Items")
        items = self.cursor.fetchall()
        return (items)

    def getInfoFromID(self, number):
        self.cursor.execute("SELECT ItemID, ItemName, ItemImage, ItemPrice FROM Items WHERE ItemID=?", (number))
        displayinfo = self.cursor.fetchall()
        return (displayinfo)

    def getIDList(self):
        self.cursor.execute("SELECT ItemID FROM Items")
        test4 = self.cursor.fetchall()
        return (test4)

    def closeDatabase(self):
        self.database.close()
        print("database closed")





