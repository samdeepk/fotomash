# Copy this file into secrets.py and set keys, secrets and scopes.

# This is a session secret key used by webapp2 framework.
# Get 'a random and long string' from here: 
# http://clsc.net/tools/random-string-generator.php
# or execute this from a python shell: import os; os.urandom(64)
SESSION_KEY = '\x17\xd2\x9e\xe7\x82\x8e\x88\xbd\xfb2\x18\xbe\x90v\xe6\xc5\xb6\x0f\xc5\xff\x1d]\x07D\xf1\xa9\x87\xd0\xf9\x07\xda\x0b\x87\xef\xb5o\xa66\x9c\x16!\x90\x16\xe8\xc0\xf6r\x07\xa7\xf5\xb6\xda\xb6\x88}\xa0\x9f\x92\xc6{\xbb\xdds\xd9'

# Google APIs
GOOGLE_APP_ID = '502942566152.apps.googleusercontent.com'
GOOGLE_APP_SECRET = 'LjpkwwL6LBfBx0TllYBQ-rul'

# Facebook auth apis
FACEBOOK_APP_ID = '432784950078723'
FACEBOOK_APP_SECRET = '13aa54fd805e78bfcee5a593e5a5e71c'

# https://www.linkedin.com/secure/developer
LINKEDIN_CONSUMER_KEY = '8tx4jgx07mio'
LINKEDIN_CONSUMER_SECRET = 'US9OvudcIesN2r8f'

# https://manage.dev.live.com/AddApplication.aspx
# https://manage.dev.live.com/Applications/Index
WL_CLIENT_ID = '00000000400C2EF3'
WL_CLIENT_SECRET = 'nWgiSEH-W3Xse4k5fvkPYAMz3aMBX0mh'

# https://dev.twitter.com/apps    #/successAuth
TWITTER_CONSUMER_KEY = 'Fk9FMQvg1xnGJShk3xTmYA'
TWITTER_CONSUMER_SECRET = '3qXFgPGCxQ2eomiPEXpEuuofW4mHKA9i6DBtDtFJQeQ'

# config that summarizes the above
AUTH_CONFIG = {
  'google'      : (GOOGLE_APP_ID,         GOOGLE_APP_SECRET,        'https://www.googleapis.com/auth/userinfo.profile'),
  'facebook'    : (FACEBOOK_APP_ID,       FACEBOOK_APP_SECRET,      'user_about_me'),
  'windows_live': (WL_CLIENT_ID,          WL_CLIENT_SECRET,         'wl.signin'),
  'twitter'     : (TWITTER_CONSUMER_KEY,  TWITTER_CONSUMER_SECRET),
  'linkedin'    : (LINKEDIN_CONSUMER_KEY, LINKEDIN_CONSUMER_SECRET),
}


app_config = {
			
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': []
  }
}
    
