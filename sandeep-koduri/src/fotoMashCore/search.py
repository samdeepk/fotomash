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

from templateHandler import templateServeHandler
import webapp2
import html5lib
from google.appengine.api import urlfetch
import os,BeautifulSoup

from google.appengine.api import channel


from time import gmtime, strftime
from django.utils import simplejson as json
import logging
from google.appengine.ext import db



resources ={
		
		"Yahoo":{"refUrl":"http://images.search.yahoo.com/search/images;_ylt=A0PDoTD7Oa5PSzIA7CaLuLkF?fr2=sg-gac-sy&p=%s&ei=utf-8&iscqry=&fr=sfp","rules":["li","ld"],"keyRules":{},"node":"img","attr":"src"},
		"Picasa":{"refUrl":"https://picasaweb.google.com/data/feed/api/all?q=%s&max-results=10","rules":["content"],"keyRules":{},"node":"media:content","attr":"url"},
		"flickr":{"refUrl":"http://www.flickr.com/search/?q=%s&f=hp","rules":["span","photo_container"],"keyRules":{},"node":"img","attr":"src"},
		"gettyimages":{"refUrl":"http://www.gettyimages.in/Search/Search.aspx?contractUrl=2&language=en-GB&family=editorial&assetType=image&ep=3&mt=photography&p=%s","rules":["div","imgInner"],"keyRules":{},"node":"img","attr":"src"},
		"fotosearch":{"refUrl":"http://www.fotosearch.com/photos-images/%s.html","rules":["div","ori"],"keyRules":{},"node":"img","attr":"src"},
		"ask":{"refUrl":"http://www.ask.com/pictures?qsrc=1&o=102140&l=dir&q=%s","rules":["div","rowresult"],"keyRules":{},"node":"img","attr":"src"},
		"photobucket":{"refUrl":"http://photobucket.com/images/%s/","rules":["div","thumbnail"],"keyRules":{},"node":"img","attr":"src"},
		"google":{"refUrl":"http://www.google.co.in/search?tbm=isch&hl=en&source=hp&biw=1280&bih=699&q=%s&gbv=2&oq=&aq=0&aqi=g5g-m2g-S3&aql=&gs_l=img.3.0.0l5j0i5l2j0i24l3.1999.3688.0.4767.10.8.0.2.2.0.144.776.3j5.8.0...0.0.kzNmYXEyt2Q","rules":["td"],"keyRules":{"style":"width:25%;word-wrap:break-word"},"node":"img","attr":"src"},

}

class homePage(webapp2.RequestHandler):#(templateServeHandler):
	def get(self):

		self.renderTemplate(templateName="",templateVales={})

class MainHandler2(webapp2.RequestHandler):
	def get(self):
		template_value = {}
		template_value["moniterKey"] = "CSVimport-"+strftime("%d-%b-%Y-%Hh%Mm%Ss-", gmtime()) 
		template_value["moniterKeyChannel"] = channel.create_channel(template_value["moniterKey"])

class MainHandler(webapp2.RequestHandler):
	def get(self):
#		self.response.out.write('Hello world!')
		sites=self.request.get_all("domains")
		keyWord= self.request.get("keyword")
		for domain in sites:
			self.response.out.write( "<br/><br/><H2>"+domain +"</H2>   --start------------------------------------------------------------<br/><br/>")
#			self.response.out.write( domain)
			if domain in resources:
#				self.response.out.write('Hello world!')
				siteData = urlfetch.fetch(resources[domain]["refUrl"]%(keyWord))
#				self.response.out.write(siteData.status_code)
				if siteData.status_code==200:
#					print siteData.content,"inside6555"
					
					#print 
					#print siteData.content
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
						nodeX = link.find(resources[domain]['node'])
						if nodeX:
							for attr, value in nodeX.attrs:
								if attr==resources[domain]['attr']:
									self.response.out.write( "<img src='%s' style='max-height:200px;'/>"%(value) +domain)
							#print link.find("img"),"stupi"

#					for row in xx.soup('li', {'class' : 'ld'}):
#					  tds = row('img')
#					  print tds[0].string, tds[1].string
					pass#self.perocessData(siteData.content)
	def perocessData(self,searchData="",domainInfo=""):
		self.response.out.write(searchData)

app = webapp2.WSGIApplication([('/', homePage),('/homePage', MainHandler)],
                              debug=True)
