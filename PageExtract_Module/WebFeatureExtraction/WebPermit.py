# -*- encoding=utf-8 -*-

import re

class WebPermit(object):
	webcurpattern=ur".*([\u4e00-\u9fa5]网文).*"
	curwebpattern=ur".*(文网游?[\u4e00-\u9fa5]字).*$"
	icppattern=ur".*[\u4e00-\u9fa5]*ICP[\u4e00-\u9fa5]*(\w*-?\w*).*"
	videopattern=ur".*(网络[\u4e00-\u9fa5]+视听[\u4e00-\u9fa5]+许可).*"
	def __init__(self):
		'icp:icp id;accesscode:4-wenwang,2-shiting,1-wangwen'
		self.icp=None
		self.accesscode=0
		self.webculture,self.cultureweb,self.visual=[0]*3
	def extract_permit(self,data):
		'match sentence'
		if not self.icp:
			m=re.match(self.icppattern,data)
			if m: self.icp=m.groups()[0]
		if not self.accesscode:
			m=re.match(self.webcurpattern,data)
			if m: self.accesscode+=1#self.webculture=m.groups()[0].encode("utf-8")
		if self.accesscode<2:
			m=re.match(self.videopattern,data)
			if m: self.accesscode+=2
		if  self.accesscode<4:
			m=re.match(self.curwebpattern,data)
			if m: self.cultureweb+=4#self.cultureweb=m.groups()[0].encode("utf-8")
	def display_permit(self):
		pass
		#permitresult=''
		#if self.icp:
		#	permitresult+="icpaccess:%s\n" % self.icp
			#print "icpaccess:",self.icp
		#if self.webculture:
		#	permitresult+=self.webculture+'\n'
			
		#if self.cultureweb:
		#	permitresult+=self.cultureweb+'\n'
			#print self.cultureweb
		#if self.visual:
		#	permitresult+="visualaccess:OK\n"
			#print "visualaccess:OK"
		#return permitresult