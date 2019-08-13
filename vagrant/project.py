from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from RestaurantDB import RestaurantDB
from database_setup import Restaurant, MenuItem

app = Flask(__name__)

db = RestaurantDB('sqlite:///restaurantmenu.db')

@app.route('/restaurants/json', methods=['GET'])
def getRestaurants():
    items = db.getAllRestaurants()
    return jsonify(Restaurants=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurantId>/menu/json', methods=['GET'])
def getRestaurantMenuItems(restaurantId):
    items = db.filterMenuItems(restaurant_id = restaurantId)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurantId>/menu/<int:menuId>/json', methods=['GET'])
def getMenuItem(restaurantId, menuId):
    item = db.filterMenuItems(restaurant_id = restaurantId, id = menuId)[0]
    return jsonify(item.serialize)

@app.route('/restaurants/<int:restaurantId>/', methods=['GET'])
def restaurantMenu(restaurantId):
    restaurant = db.filterRestaurants(id = restaurantId)[0]
    items = db.filterMenuItems(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurantId>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurantId):
    if request.method == 'POST':
        if request.form['name']:
            db.addMenuItem(MenuItem(name = request.form['name'], restaurant_id = restaurantId))
            flash("Menu Item created")
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('NewMenuItem.html', restaurantId = restaurantId)

@app.route('/restaurants/<int:restaurantId>/<int:menuId>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurantId, menuId):
    editedItem = db.filterMenuItems(id = menuId)[0]
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            db.addMenuItem(editedItem)
            flash("Menu Item updated")
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('EditMenuItem.html', restaurantId = restaurantId, menuId = menuId, item = editedItem)

@app.route('/restaurants/<int:restaurantId>/<int:menuId>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurantId, menuId):
    item = db.filterMenuItems(id = menuId)[0]
    if request.method == 'POST':
        db.removeMenuItem(item)
        flash("Menu Item deleted")
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('DeleteMenuItem.html', item = item)

if __name__ == '__main__':
    app.secret_key = 'secretKey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)