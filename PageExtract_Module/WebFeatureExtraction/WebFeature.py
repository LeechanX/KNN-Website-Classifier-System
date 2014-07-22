# -*- encoding=utf-8 -*-

from WebPermit import WebPermit
from WebPageParser import WebPageParser
from bs4 import BeautifulSoup as beautifulsoup
from bs4 import Comment
from time import time
from ParticipleTool import *
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')

class WebFeature(object):
	def __init__(self,url):
		self.url=url
		self.title,self.content,self.permit=None,None,None
		self.meta={}
	def set_title(self,soup):
		'set title'
		if soup.title: self.title=str(soup.title.string)
	def set_meta(self,soup):
		'set meta'
		for meta in soup.findAll('meta'):
			if str(meta.get('name')).lower() in ['description','keywords']:
				self.meta[meta.get('name').lower()]=meta.get('content')
			elif str(meta.get('http-equiv')).lower() in ['description','keywords']:
				self.meta[meta.get('http-equiv').lower()]=meta.get('content')
	def set_permit_and_content(self,htmldoc):
		'set permit and real content'
		if not htmldoc: return
		page_parser=WebPageParser()
		page_parser.get_text(htmldoc)
		page_parser.get_blocksets()
		self.permit=page_parser.permit
		self.content=page_parser.content
	def set_title_and_meta(self,htmltext):
		'before fetch feature,clear the html file'
		soup=beautifulsoup(htmltext.decode('utf-8'))
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		[comment.extract() for comment in comments]
		[style.extract() for style in soup.findAll('style')]
		[script.extract() for script in soup.findAll('script')]
		[form.extract() for form in soup.findAll('form')]
		[table.extract() for table in soup.findAll('table')]
		self.set_title(soup)
		self.set_meta(soup)
		htmldoc=re.sub('<[^>]*>','',soup.body.prettify()).encode('utf-8') if soup.body else None
		self.set_permit_and_content(htmldoc)
	def display_feature(self):
		if self.title: print 'title=',self.title
		if self.permit: self.permit.display_permit()
		if self.meta:
			for key in self.meta:
				print 'meta,',key,':',self.meta[key]
		if self.content: print 'has content!'
		else: print 'has no content!'
	def show_page_content(self):
		if self.content: print self.content
	def participle_words(self):
		if self.title: self.title=participle_title(self.title)
		if self.meta:
			if 'keywords' in self.meta and self.meta['keywords']:
				self.meta['keywords']=participle_keywords(self.meta['keywords'])
			if 'description' in self.meta and self.meta['description']:
				self.meta['description']=participle_description(self.meta['description'])
		if self.content: self.content=participle_content(self.content)