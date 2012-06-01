from google.appengine.ext import db



from google.appengine.api import users, namespace_manager, blobstore, memcache
from google.appengine.api.datastore import Key

import logging

import datetime

class dataModel(db.Model):
	updatedOn = db.DateTimeProperty(auto_now=True)
	createdOn = db.DateTimeProperty(auto_now_add=True)

	



class searchTags(dataModel):
	tags = db.StringListProperty(default=[])
	hits = db.IntegerProperty(default=0)
	topList = db.TextProperty(default='[]')
	def getSearchKey(self,search="",updateCount=True,topList='{}'):
		search = search.lower()
		dataRow = self.get_or_insert(search)
		dataRow.hits = dataRow.hits +1
		if topList!='[]':dataRow.topList = topList 
		#dataRow.tags=list(set([ search[tagSplit:tagSplit+s+1] for tagSplit in range(len(search)) for s in range(len(search[tagSplit:])) if search[tagSplit:tagSplit+s+1] ]))
		yest = dataRow.put()
		
		return dataRow
	def getSearchList(self,order='-hits',order2='updatedOn',fetch=5,startFrom=0):
		data = self.all()
		if order : data.order(order)
		if order2 : data.order(order2)
		
#		db.Key().id_or_name()

		return data.fetch(fetch,startFrom)
		
class usersSearchs(dataModel):
	userKey = db.StringProperty()
	search = db.ReferenceProperty(searchTags,default=None)
	hits = db.IntegerProperty(default=0)
	def updateIntrest(self,search = "" ,user = ""):
		if search and user:
			isSearch = self.all().filter("userKey", str(user)).filter("search", search).get()
			if isSearch: 
				isSearch.hits = isSearch.hits +1
			else: isSearch = usersSearchs(userKey= str(user),search=search,hits=1)
			return isSearch.put()
	def getSearchList(self,userKey="",order='-hits',fetch=5,startFrom=0):
		data = self.all()
		if userKey:data.filter("userKey", str(userKey))
		if order : data.order(order)

		return data.fetch(fetch,startFrom)			
		