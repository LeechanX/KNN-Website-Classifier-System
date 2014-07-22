#-*- encoding=utf-8 -*-
class TestObj(object):
	"""Test class"""
	def __init__(self,url):
		super(TestObj,self).__init__()
		self.url=url
		self.text=[]
		self.thinkbe=0
	def setText(self,title,keyword,description):
		self.text=title.encode('utf-8').split('+')\
			+keyword.encode('utf-8').split('+')\
			+description.encode('utf-8').split('+')