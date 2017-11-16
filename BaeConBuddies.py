import sqlite3
import document as document

from flask import Flask, render_template, url_for, request
from decimal import Decimal
from re import sub
import Items
app = Flask(__name__)
import Users
import Orders
import Cart
import datetime
import ActiveUser

@app.route('/')
def menu_page():
    items = Items.Items()
    menu = items.getAllItems()
    return render_template("menu.html", iteminfo=menu)


@app.route('/menu/return')
def return_menu_page():
    cart = Cart.Cart()
    cart.removeAllItems()
    cart.closeDatabase()

    order = Orders.Order()
    order.removeGuestOrders()
    order.closeDatabase()

    auser = ActiveUser.ActiveUser()
    auser.removeAllItems()
    auser.closeDatabase()

    items = Items.Items()
    menu = items.getAllItems()
    return render_template("menu.html", iteminfo=menu)

@app.route('/logout')
def logout_page():
    auser = ActiveUser.ActiveUser()
    auser.removeAllItems()
    items = Items.Items()
    menu = items.getAllItems()
    return render_template("menu.html", iteminfo=menu)

#route from navigation
@app.route('/viewcart')
def viewcart_page():
    cart = Cart.Cart()
    items = cart.getCartItems()
    return render_template("cart.html", cart=items)


@app.route('/addcart', methods=['POST'])
def addcart_page():
    if request.method == 'POST':
        result = request.form['add']
        cart = Cart.Cart()
        cart.addItem(result)
        items = cart.getCartItems()

    return render_template("cart.html", cart=items)


@app.route('/savecart', methods=['POST'])
def savecart_page():
    if request.method == 'POST':
        q = request.form['quantity']
        id = request.form['save']
        cart = Cart.Cart()
        cart.updateItem(id, q)
        items = cart.getCartItems()
    return render_template("cart.html", cart=items)


@app.route('/checkout')
def checkout_page():
    cart = Cart.Cart()
    items = cart.getCartItems()
    prices = []
    for i in range(len(items)):
        p = items[i][3]
        prices.append(p)
    final = 0
    for price in prices:
        final = final + int(Decimal(sub(r'[^\d.]', '', price)))
    final = "$" + str(final) + ".00"
    return render_template("checkout.html", summary = items, total = final)

@app.route('/orderconfirm', methods=['POST'])
def orderconfirm_page():
    date = datetime.datetime.now()
    guestorder = Orders.Order()
    #create order
    gorder_num = (guestorder.createGuestOrder(str(date)))
    guestorder.addCartToOrder(gorder_num)
    guestorder.closeDatabase()
    cart = Cart.Cart()
    cart.getCartOrder()
    cart.closeDatabase()

    #final = guestorder.getOrderDetails(gorder_num)

    return render_template("orderconfirm.html", msg = gorder_num)











#login stuff

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/newuser', methods=['POST'])
def newuser_page():
    return render_template("newuser.html")

@app.route('/user', methods=['POST'])
def user_page():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        user = Users.User()


        if (user.isUser(username) == False):
            user_info = "Username or Password is incorrect"
            #user_info = user.getAllUsers()
            return render_template("login.html", error=user_info)

        else:
            if password != user.getPassword(username):
                user_info = "Username or Password is incorrect"
                return render_template("login.html", error=user_info)
            else:
                user_info = user.getLoginInfo(username)
                update_id = user_info[0][0]
                user.closeDatabase()
                auser = ActiveUser.ActiveUser()
                auser.createActiveUser(update_id, username)
                auser.closeDatabase()
                items = Items.Items()
                menu = items.getAllItems()
                return render_template("usermenu.html", iteminfo=menu)


@app.route('/newuser/profile', methods=['POST'])
def newuser_profile_page():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = Users.User()

        if (user.isUser(email) == True):
            user_info = "Email already exists"
            #user_info = user.getAllUsers()
            user.closeDatabase()
            return render_template("login.html", error=user_info)
        else:
            user_info = user.getLoginInfo(email)
            update_id = user_info[0][0]
            user.closeDatabase()
            auser = ActiveUser.ActiveUser()
            auser.createActiveUser(update_id, email)
            id = auser.getUserID()
            auser.closeDatabase()
            user = Users.User()

            user = Users.User()
            return render_template("userprofile.html", name=user.getName(id),phone=user.getPhone(id),email=user.getEmail(id),street=user.getStreet(id),city=user.getCity(id),zip=user.getZip(id), state=user.getState(id))

@app.route('/deleteaccount', methods=['POST'])
def delete_account():
    auser = ActiveUser.ActiveUser()
    id = auser.getUserID()
    auser.removeAllItems()
    auser.closeDatabase()

    user = Users.User()
    user.removeUser(id)
    user.closeDatabase()

    items = Items.Items()
    menu = items.getAllItems()
    return render_template("menu.html", iteminfo=menu)


#User interface
@app.route('/usermenu')
def usermenu_page():
    items = Items.Items()
    menu = items.getAllItems()
    items.closeDatabase()

    return render_template("usermenu.html", iteminfo=menu)

@app.route('/user/viewcart')
def user_viewcart_page():
    cart = Cart.Cart()
    items = cart.getCartItems()
    return render_template("usercart.html", cart=items)

@app.route('/user/addcart', methods=['POST'])
def user_addcart_page():
    if request.method == 'POST':
        result = request.form['add']
        cart = Cart.Cart()
        cart.addItem(result)
        items = cart.getCartItems()
    return render_template("usercart.html", cart=items)

@app.route('/user/savecart', methods=['POST'])
def user_savecart_page():
    if request.method == 'POST':
        q = request.form['quantity']
        id = request.form['save']
        cart = Cart.Cart()
        cart.updateItem(id, q)
        items = cart.getCartItems()
    return render_template("usercart.html", cart=items)


@app.route('/user/update', methods=['POST'])
def update_userpage():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        auser = ActiveUser.ActiveUser()
        id = auser.getUserID()
        user = Users.User()
        user.setName(id, name)
        user.setEmail(id, email)
        user.setPhone(id, phone)
        user.setStreet(id, street)
        user.setCity(id, city)
        user.setState(id, state)
        user.setZip(id, zip)
        return render_template("userprofile.html", name=user.getName(id),phone=user.getPhone(id),email=user.getEmail(id),street=user.getStreet(id),city=user.getCity(id),zip=user.getZip(id), state=user.getState(id))

@app.route('/user/checkout')
def user_checkout_page():
    cart = Cart.Cart()
    items = cart.getCartItems()
    prices = []
    for i in range(len(items)):
        p = items[i][3]
        prices.append(p)
    final = 0
    for price in prices:
        final = final + int(Decimal(sub(r'[^\d.]', '', price)))
    final = "$" + str(final) + ".00"
    auser = ActiveUser.ActiveUser()
    id = auser.getUserID()
    auser.closeDatabase()
    user = Users.User()

    return render_template("usercheckout.html", summary = items, total = final,
                           firstname = user.getName(id), street = user.getStreet(id),
                           city = user.getCity(id), state = user.getState(id), zip = user.getZip(id))


@app.route('/user/orderconfirm', methods=['POST'])
def user_orderconfirm_page():
    if request.method == 'POST':
        price = request.form['price']
        print (price)
        auser = ActiveUser.ActiveUser()
        id = auser.getUserID()
        auser.closeDatabase()

        date = datetime.datetime.now()

        #create order
        order = Orders.Order()
        order_num = order.createUserOrder(id, str(date))
        order.updateOrderPrice(price,order_num)
        order.closeDatabase()

        #assigns cart items to the ordernumber
        cart = Cart.Cart()
        cart.setOrderNum(order_num)
        cart.closeDatabase()

        #Add all cart details to orderDetails
        order = Orders.Order()
        order.addCartToOrder(order_num)
        order.closeDatabase()
        return render_template("userorderconfirm.html", msg = order_num, test = price)


@app.route('/viewprofile')
def profile_page():
    auser = ActiveUser.ActiveUser()
    id = auser.getUserID()
    auser.closeDatabase()
    user = Users.User()
    return render_template("userprofile.html", name=user.getName(id), phone=user.getPhone(id), email=user.getEmail(id),
                           street=user.getStreet(id), city=user.getCity(id), zip=user.getZip(id),
                           state=user.getState(id))


@app.route('/usermenu/return')
def return_usermenu_page():
    cart = Cart.Cart()
    cart.removeAllItems()
    cart.closeDatabase()

    items = Items.Items()
    menu = items.getAllItems()
    items.closeDatabase()
    return render_template("usermenu.html", iteminfo=menu)



@app.route('/changepassword')
def change_password():
    return render_template("changepw.html")

@app.route('/user/changepassword', methods=['POST'])
def savechange_password():
    if request.method == 'POST':
        auser = ActiveUser.ActiveUser()
        username = auser.getUserName()
        id = auser.getUserID()
        auser.closeDatabase()
        user = Users.User()
        current_pw = user.getPassword(username)
        old_password = request.form['old_password']

        if old_password == current_pw:
            error = "correct passwords"
            new_password = request.form['new_password']
            confirm_pw = request.form['confirm_password']
            if new_password == confirm_pw:
                user.setPassword(id, new_password)
                error = "Your password has been changed!"
                return render_template("changepw.html", error=error)

            else:
                error = "Passwords do not match"
                return render_template("changepw.html", error=error)
        else:
            error = "The password you enter is incorrect"
            return render_template("changepw.html", error = error)



@app.route('/orderhistory')
def orderhistory():
    auser = ActiveUser.ActiveUser()
    id = auser.getUserID()
    auser.closeDatabase()
    user = Users.User()

    orders = user.getOrders(id)

    #get a list of orders to iterate through
    details = []
    for order in orders:
        details.append(user.getOrderDetails(order[0]))

    #print(details)
    #iterate through list of orderdetails

    for detail in details:
        print(detail[0])
        for d in detail:
            print("new: " +  str(d))
    user.closeDatabase()




    return render_template("orderhistory.html", orders = details)


if __name__ == '__main__':

    orders = Orders.Order()
    #orders.removeAllOrderDetails()
    #orders.removeAllOrders()

    orders.getAllOrders()
    orders.getAllOrderDetails()
    orders.closeDatabase()

    user = Users.User()
    user.getAllUsers()

    # get a list of orders to iterate through
    user.closeDatabase()


    app.run()

