#!/usr/bin/env python
#-*- encoding=utf-8 -*-
from __future__ import division
from Centroid import Centroid
class Rocchio(object):
	def __init__(self):
		self.centcls=[]
		for i in xrange(1,34):
			trainsets=self.loadTrainData(i)
			cen=Centroid(trainsets)
			self.centcls.append(cen)
	def loadTrainData(self,i):
		data_file=open('../../Attach/Train/train_t%d.txt' % i,'r')
		dataSet=[]
		with open('../../Attach/Train/train_t%d.txt' % i,'r') as data_file:
			for line in data_file:
				lineArr=line.strip().split('\t')
				posvec=read_posvectors_file(lineArr[1:])
				dataSet.append(posvec)
		return dataSet
	def CalcRepresentV(self,who,vd):
		alph,beta=16,4
		posv,size=self.centcls[who-1].centroid,self.centcls[who-1].size
		positiveV={}
		for pos in posv:
			positiveV[pos]=posv[pos]/size
		negativeSets=self.centcls[:who-1]+self.centcls[who:]
		negSize=sum([x.size for x in negativeSets])
		negativeV={}
		for neg in negativeSets:
			for pos in neg.centroid:
				if pos not in negativeV:
					negativeV[pos]=0
				negativeV[pos]+=neg.centroid[pos]
		for pos in negativeV.keys():
			negativeV[pos]/=negSize
		representV={}
		for pos in xrange(vd):
			positive,negative=0.0,0.0
			if pos in positiveV:
				positive=positiveV[pos]
			if pos in negativeV:
				negative=negativeV[pos]
			if alph*positive-beta*negative:
				representV[pos]=alph*positive-beta*negative
		return representV
def read_posvectors_file(file_line_array):
	import re
	"""file_line_array except cate_id"""
	my_posvector={}
	for x in file_line_array:
		m=re.match('<(\d+),(\d+.\d+)>',x)
		if m:
			pos,v=int(m.groups()[0]),float(m.groups()[1])
			my_posvector[pos]=v
	return my_posvector
def getfeaturelength():
	counts=0
	with open('../../Attach/featureall.txt','rb') as ffile:
		while True:
			bytes=ffile.read(1024*8192)
			if not bytes:
				break
			counts+=bytes.count('\n')
	return counts
def dump_rocchioindex(rocchioIndex):
	import cPickle
	with open('../../Attach/roindex.txt','w') as rfile:
		bytes=cPickle.dumps(rocchioIndex,2)
		cPickle.dump(bytes,rfile)
if __name__ == '__main__':
	rocchio=Rocchio()
	rocchioIndex=[]
	flength=getfeaturelength()
	for i in xrange(1,34):
		rv=rocchio.CalcRepresentV(i,flength)
		rocchioIndex.append(rv)
	print 'Rocchio index calculate OK.'
	dump_rocchioindex(rocchioIndex)
	print 'Rocchio index dump OK.'