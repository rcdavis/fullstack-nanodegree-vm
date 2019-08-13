from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

class RestaurantDB:
	'Encapsulates CRUD operations for restaurant and menu items'
	
	def __init__(self, url):
		self.__engine = create_engine(url)
		Base.metadata.bind = self.__engine
		DBSession = sessionmaker(bind = self.__engine)
		self.__session = DBSession()
	
	# Restaurant operations
	def addRestaurant(self, restaurant):
		self.__session.add(restaurant)
		self.__session.commit()
	
	def removeRestaurant(self, restaurant):
		self.__session.delete(restaurant)
		self.__session.commit()
	
	def getAllRestaurants(self):
		return self.__session.query(Restaurant).all()
	
	def filterRestaurants(self, **kwargs):
		return self.__session.query(Restaurant).filter_by(**kwargs).all()
	
	# MenuItem operations
	def addMenuItem(self, menuItem):
		self.__session.add(menuItem)
		self.__session.commit()
	
	def removeMenuItem(self, menuItem):
		self.__session.delete(menuItem)
		self.__session.commit()
	
	def getAllMenuItems(self):
		return self.__session.query(MenuItem).all()
	
	def filterMenuItems(self, **kwargs):
		return self.__session.query(MenuItem).filter_by(**kwargs).all()