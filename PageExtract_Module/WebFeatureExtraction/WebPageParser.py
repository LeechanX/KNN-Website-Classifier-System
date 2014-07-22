# -*- encoding=utf-8 -*-

from __future__ import division
from WebPermit import WebPermit
import matplotlib.pyplot as plt
from time import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class WebPageParser(object):
	def __init__(self):
		self.permit=WebPermit()
		self.content=None
		self.text=[]
		self.blocksets=[]
		self.thresold,self.blocksize=86,3
	def get_text(self,htmldoc):
		'get all words text in page'
		puretext=htmldoc.split('\n')
		textsize,nowline=len(puretext),0
		for text in puretext:
			realtext=re.sub('\s','',text)
			ituple=(text,len(realtext.strip()))
			self.text.append(ituple)
			if nowline>textsize//3:
				udata=realtext.strip().decode('utf-8')
				self.permit.extract_permit(udata)
			nowline+=1
	def get_blocksets(self):
		'count for block length'
		lines=len(self.text)
		for i in range(self.blocksize):
			self.blocksets.append(0)
		for i in range(self.blocksize,lines):
			blockcapacity=0
			for ib in range(self.blocksize):
				blockcapacity+=self.text[i-ib][1]
			self.blocksets.append(blockcapacity)
		self.get_content_coord()
	def get_content(self,start,end):
		'get real content'
		if self.content:
			self.content=''
			for i,ituple in enumerate(self.text[start:end+1]):
				self.content+=ituple[0]
	def get_content_coord(self):
		'get content position x,y'
		setsize=len(self.blocksets)
		maxvalue=max(self.blocksets)
		maxpos=self.blocksets.index(maxvalue)
		if maxpos>setsize*3//4: return
		if maxvalue<500:
			count=0
			devirate,maxset=[],[]
			for i in range(setsize-1):
				devirate.append(self.blocksets[i+1]-self.blocksets[i])
			for i in range(1,setsize-1):
				if devirate[i]<0 and devirate[i-1]>0:
					maxset.append(self.blocksets[i])
			for i in sorted(maxset):
				if 0<=maxvalue-i<maxvalue*0.4:
					count+=1
					if count==5: return
		start=end=-1
		for x,y in enumerate(self.blocksets[:maxpos+1]):
			if start==-1 and y>self.thresold:
				check=1
				if setsize<=x+self.blocksize: return
				for i in range(self.blocksize+1):
					check*=self.blocksets[x+i] 
				if not (x<=maxpos<=x+self.blocksize) and not check: continue
				start=x
		if start!=-1:
			if x+start+2>=setsize or x+start+1>=setsize: return
			for x,y in enumerate(self.blocksets[start+1:]):
				if x+start+2>=setsize or x+start+1>=setsize: break
				if not self.blocksets[x+start] and not self.blocksets[x+start+1] \
				and not self.blocksets[x+start+2]:
					end=1+start+x
					break
		start-=self.blocksize//2
		if start!=-1 and end!=-1 and maxvalue>200:
			if start<maxpos<=end:
				if maxvalue/(end-start)>6:
					self.content='ok'
			else:
				if maxvalue>200: self.content='ok'
		if self.content: self.get_content(start,end)
