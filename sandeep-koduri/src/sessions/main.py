# -*- coding: utf-8 -*-
import sys
from secrets import app_config
from sessions import handlers
from webapp2 import WSGIApplication, Route

# inject './lib' dir in the path so that we can simply do "import ndb" 
# or whatever there's in the app lib dir.
import sys
from google.appengine.api import app_identity
spaths = sys.path
if 'lib2' not in spaths:
	apID = app_identity.get_application_id()
	for pat in spaths:
		print 
		if pat.find(apID)>0:
			currentpaths= pat
			
			sys.path=spaths+ ['lib2',pat+'/lib2']
    

# webapp2 config

    
# Map URLs to handlers
routes = [
  Route('/profile', handler='handlers.ProfileHandler', name='profile'),
  
  Route('/auth/<provider>', handler='sessions.handlers.AuthHandler:_simple_auth', name='auth_login'),
  Route('/auth/<provider>/callback', handler='sessions.handlers.AuthHandler:_auth_callback', name='auth_callback'),
  Route('/logout', handler='sessions.handlers.AuthHandler:logout', name='logout')
]

app = WSGIApplication(routes, config=app_config, debug=True)
