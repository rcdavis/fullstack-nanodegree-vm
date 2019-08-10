from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from RestaurantDB import RestaurantDB
from database_setup import Restaurant
import cgi

class WebserverHandler(BaseHTTPRequestHandler):

	db = RestaurantDB('sqlite:///restaurantmenu.db')

	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				restaurants = self.db.getAllRestaurants()

				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = "<html><body>"
				for restaurant in restaurants:
					output += "<h1>%s</h1>" % restaurant.name
					output += "<h3><a href='/restaurants/%s/edit'>Edit</a></h3>" % restaurant.id
					output += "<h3><a href='#'>Delete</a></h3>"
					output += "<br>"
				output += "</body></html>"

				self.wfile.write(output)

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='newRestaurantName' type='text'>"
				output += "<input type='submit' value='Create'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output

			if self.path.endswith("/edit"):
				restaurantId = self.path.split("/")[2]
				restaurant = self.db.filterRestaurants(id = restaurantId)[0]
				if restaurant:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = "<html><body>"
					output += "<h1>Rename %s?</h1>" % restaurant.name
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantId
					output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % restaurant.name
					output += "<input type='submit' value='Rename'></form>"
					output += "</body></html>"
					self.wfile.write(output)
					print output

		except IOError:
			self.send_error(404, "File Not Fount %s" % self.path)
			
	def do_POST(self):
		try:
			if self.path.endswith('/restaurants/new'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
				
					restaurant = Restaurant(name = messagecontent[0])
					self.db.addRestaurant(restaurant)

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			if self.path.endswith('/edit'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
					restaurantId = self.path.split("/")[2]

					restaurant = self.db.filterRestaurants(id = restaurantId)[0]
					restaurant.name = messagecontent[0]
					self.db.addRestaurant(restaurant)

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
		
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), WebserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
	
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()