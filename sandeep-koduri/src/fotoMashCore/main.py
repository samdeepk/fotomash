#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
from google.appengine.api import app_identity
from models.models import searchTags, usersSearchs
import urllib
spaths = sys.path
if 'lib2' not in spaths:
	apID = app_identity.get_application_id()
	for pat in spaths:
		if pat.find(apID)>0:
			currentpaths= pat
			
			sys.path=spaths+ ['lib2',pat+'/lib2']
    
    
import logging

import webapp2
import html5lib
from google.appengine.api import urlfetch
import os,BeautifulSoup
from base import BaseRequestHandler
from django.utils import simplejson as json
from secrets import app_config

resources ={
		
		"Yahoo":{"refUrl":"http://images.search.yahoo.com/search/images;_ylt=A0PDoTD7Oa5PSzIA7CaLuLkF?fr2=sg-gac-sy&p=%s&ei=utf-8&iscqry=&fr=sfp",'linkSourceDomain':"http://images.search.yahoo.com",'linkRules':{"node":"a","attr":"href"},"rules":["li","ld"],"keyRules":{},"node":"img","attr":"src"},
		"Picasa":{"refUrl":"https://picasaweb.google.com/data/feed/api/all?q=%s&max-results=30",'linkSourceDomain':"","rules":["entry"],'linkRules':{"node":"link","attr":"href","keyRules":{"type":'text/html'}},"keyRules":{},"node":"media:thumbnail","attr":"url"},
		"flickr":{"refUrl":"http://www.flickr.com/search/?q=%s&f=hp",'linkSourceDomain':"http://www.flickr.com","rules":["span","photo_container"],'linkRules':{"node":"a","attr":"href"},"keyRules":{},"node":"img","attr":"src"},
		#"gettyimages":{"refUrl":"http://www.gettyimages.in/Search/Search.aspx?contractUrl=2&language=en-GB&family=editorial&assetType=image&ep=3&mt=photography&p=%s","rules":["div","imgInner"],"keyRules":{},"node":"img","attr":"src"},
		"fotosearch":{"refUrl":"http://www.fotosearch.com/photos-images/%s.html",'linkSourceDomain':"http://www.fotosearch.com","rules":["div","ori"],'linkRules':{"node":"a","attr":"href"},"keyRules":{},"node":"img","attr":"src"},
		"ask":{"refUrl":"http://www.ask.com/pictures?qsrc=1&o=102140&l=dir&q=%s",'linkSourceDomain':"","rules":["div","rowresult"],'linkRules':{"node":"a","attr":"href"},"keyRules":{},"node":"img","attr":"src"},
		"photobucket":{"refUrl":"http://photobucket.com/images/%s/",'linkSourceDomain':"","rules":["div","thumbnail"],'linkRules':{"node":"a","attr":"href"},"keyRules":{},"node":"img","attr":"src"},
		"google":{"refUrl":"http://www.google.co.in/search?tbm=isch&hl=en&source=hp&biw=1280&bih=699&q=%s&gbv=2&oq=&aq=0&aqi=g5g-m2g-S3&aql=&gs_l=img.3.0.0l5j0i5l2j0i24l3.1999.3688.0.4767.10.8.0.2.2.0.144.776.3j5.8.0...0.0.kzNmYXEyt2Q",'linkSourceDomain':"http://www.google.co.in",'linkRules':{"node":"a","attr":"href"},"rules":["td"],"keyRules":{"style":"width:25%;word-wrap:break-word"},"node":"img","attr":"src"},

}
#
class MainHandler(BaseRequestHandler):
	def post(self):
		if self.logged_in:
			Cuser = {'user': self.current_user, 'session': self.auth.get_user_by_session()}
#		self.response.out.write('Hello world!')
#		sites=self.request.get_all("domains")
		sites=self.request.get("domains")
		keyWord= self.request.get("keyword")+('+"'+self.request.get("categories")+'"' if self.request.get("categories") else "")
		imagesList =[]
#		for domain in sites:
		if sites:
			domain = sites
#			self.response.out.write( "<br/><br/><H2>"+domain +"</H2>   --start------------------------------------------------------------<br/><br/>")
#			self.response.out.write( domain)
			if domain in resources:
#				self.response.out.write('Hello world!')
				siteData = urlfetch.fetch(resources[domain]["refUrl"]%(urllib.quote(keyWord)))
#				self.response.out.write(siteData.status_code)
				if siteData.status_code==200:
#					print siteData.content,"inside6555"
					
					#print 
					#print siteData.content
					#return
#					doc = html5lib.parse(siteData.content, treebuilder='lxml')
#					elems = doc.xpath("//*[local-name() = 'a']")
#					self.response.out.write(len(elems))

#					tree = html.fromstring(siteData.content)
#					[td.text for td in tree.xpath("//td")]
#					xx  = html5lib.parse(StringIO.StringIO(siteData.content))
#					data  =   xpath.find('//li', )
#					print data
#					data.findall()
					soup =  BeautifulSoup.BeautifulSoup(siteData.content)
#					print soup.prettify()
#					print soup.title
					
					for link in  soup.findAll(*resources[domain]["rules"],**resources[domain]["keyRules"]):
						#print 
						#print link,"stupi"
						dataHolder = {'refURL':"",'imagePath':"",'alt':keyWord}
						
						nodeX = link
						if nodeX:
							nodeX = nodeX.find(resources[domain]['linkRules']['node'],**resources[domain]['linkRules']["keyRules"] if 'keyRules' in resources[domain]['linkRules'] else {})
						if nodeX:
							if 'attr' in resources[domain]['linkRules'] and resources[domain]['linkRules']['attr']:
								for attr, value in nodeX.attrs:
									if attr == resources[domain]['linkRules']['attr']:
										dataHolder['refURL'] = resources[domain]['linkSourceDomain']+value
							
						
						nodeX = link.find(resources[domain]['node'])
						if nodeX:
							for attr, value in nodeX.attrs:
								if attr==resources[domain]['attr']:
									dataHolder['imagePath'] = value
								if attr=='alt' and value:
									dataHolder['alt'] = value
						
						
						if dataHolder['imagePath']:imagesList.append(dataHolder)
#									self.response.out.write( "<img src='%s' style='max-height:200px;'/>"%(value) +domain)
							#print link.find("img"),"stupi"

#					for row in xx.soup('li', {'class' : 'ld'}):
#					  tds = row('img')
#					  print tds[0].string, tds[1].string
		self.response.out.write(json.dumps({"images":imagesList,'source':sites}))
#					pass#self.perocessData(siteData.content)
	def perocessData(self,searchData="",domainInfo=""):
		self.response.out.write(searchData)

class RootHandler(BaseRequestHandler):
	def get(self):
		"""Handles default langing page"""
#		print "xxxxxx"
		data = searchTags()
		topTrending = data.getSearchList(fetch=10)
		Cuser={}
		if self.logged_in:
			data = usersSearchs()
			yourTopTrending = data.getSearchList(userKey=self.current_user.key,)
			Cuser = {'user': self.current_user, 'session': self.auth.get_user_by_session(),}
			Cuser["yourTopTrending"]=[{'rowOBJ':itm,'keyWrd':itm.search.key().id_or_name(),"tags": itm.search.tags,"hits":itm.hits, "topList":(json.loads(itm.search.topList)[0] if len(json.loads(itm.search.topList))>0 else{})} for itm in  yourTopTrending]
		Cuser["topTrending"]=[{'rowOBJ':itm,'keyWrd':itm.key().id_or_name(),"tags": itm.tags,"hits":itm.hits, "topList":(json.loads(itm.topList)[0] if len(json.loads(itm.topList))>0 else {})} for itm in  topTrending]
		self.render('index.html',Cuser)
		
		
class udateSearchHistory(BaseRequestHandler):
	def post(self):
		"""Handles default langing page"""
#		print "xxxxxx"
		trackSearch = True if self.request.get("SearchHistory") == "1" else False
		search = self.request.get("Search").strip() if self.request.get("Search") else None
		topList = json.dumps(json.loads(self.request.get("topList"))) if self.request.get("topList") else "[]"
		if search:
			searchKeyOBJ = searchTags()
			searchKey =searchKeyOBJ.getSearchKey(search=search,updateCount=True,topList=topList)
			if self.logged_in and trackSearch and searchKey:
				usersSearchObj =usersSearchs()
				logging.info(self.current_user.key)
				logging.info(self.current_user.key.id())

				usersSearchObj.updateIntrest(search = searchKey ,user = self.current_user.key)
				#Cuser = {'user': self.current_user, 'session': self.auth.get_user_by_session()}
#		self.render('index.html',Cuser)

app_config["webapp2_extras.jinja2.default_config"] = {'template_path':"templates"}
app = webapp2.WSGIApplication([
							('/', RootHandler),
							('/search', MainHandler),
							('/searchTrack', udateSearchHistory)
							],config=app_config,
                              debug=True)
