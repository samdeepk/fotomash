from google.appengine.api import users


class userData():

	def __init__(self):
		if not self.CURUser:
			user = users.get_current_user()

			if user:
					self.AdminInfo = users.is_current_user_admin()
					
					self.CURUser = user
					uremail = user.email()
					qry = dbUsers().all().filter("strUserEmail", uremail).get()
					if qry:
						self.CURUserInfo = qry
	
	
def userInfo(handler_method):
	
	def check_login(self, *args):

		haspermissions = {}
		self.HasHandlerPermission =[]
		self.userInfo = userData()
				
		
		if self.request.headers and "X-AppEngine-TaskName" in self.request.headers:
			self.userInfo.AdminInfo = True

		if self.userInfo.AdminInfo :handler_method(self, *args)
		else: self.redirect(Config.Handlers["loginConsole"]["path"]+"?redir="+self.request.uri)		
			return False
	return check_login
