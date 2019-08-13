from database_setup import Restaurant, MenuItem
from RestaurantDB import RestaurantDB

rdb = RestaurantDB('sqlite:///restaurantmenu.db')
restaurant = rdb.filterRestaurants(name = "Kurger Bing")[0]
rdb.addMenuItem(MenuItem(name = 'Bepis', description = 'Delicious drink', price = '$1.99', restaurant_id = restaurant.id))
restaurants = rdb.getAllRestaurants()
for r in restaurants:
	print r.name

print "\n"
menuitems = rdb.getAllMenuItems()
for m in menuitems:
	print m.name
	print m.description
	print m.price
	print "\n"