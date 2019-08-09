from database_setup import Restaurant, MenuItem
from RestaurantDB import RestaurantDB

rdb = RestaurantDB('sqlite:///restaurantmenu.db')
#rdb.addRestaurant(Restaurant(name = 'Pizza Palace'))
restaurants = rdb.getAllRestaurants()
for r in restaurants:
	print r.name

print "\n"
restaurants = rdb.filterRestaurants(name = "Pizza Palace")
for r in restaurants:
	print r.name