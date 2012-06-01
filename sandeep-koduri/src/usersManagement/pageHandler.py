from google.appengine.api import users
from usersManagement import users

class manageUsers(requestHandler):
	def __init__(self):
		self.ConsoleMenu =True
		self.checkSession = True
		self.checkHandler = True
		self.validationType="View"


	@userInfo
	def get(self):
		pass

	@userInfo
	def post(self):

		pass

def main():
	application = webapp.WSGIApplication([
		 ("/users/logout", LogoutLink),
		 ("/users/login", loginPage),
		 ("/users/admin", loginPage),
		 ("/users/manage", manageUsers),
		 ("/users/permission", UserPermissions),
		 
		 ], debug=True)
	run_wsgi_app(application)

if __name__ == "__main__":
	main()

