#!/usr/bin/env python
#-*- encoding=utf-8 -*-
from __future__ import division
import math

class LoadIndex(object):
	def __init__(self,clsid):
		self.clsid=clsid
		self.occurence={}
		self.readIndex()
	def readIndex(self):
		with open('../../Attach/Index/index_t%d.txt' % self.clsid) as fi:
			for line in fi:
				lineArr=line.strip().split('\t')
				attrID=int(lineArr[0][:-1])
				self.occurence[attrID]=len(lineArr[1:])
	def CalcsubEntroy(self,attrID,times):
		probability=self.occurence[attrID]/times if attrID in self.occurence else 0
		if not probability:return 0
		return (-1)*math.log(probability)*probability if probability<1 else 0.5
def createIndexSet():
	indexset=[]
	for i in range(1,34):
		index=LoadIndex(i)
		indexset.append(index)
	return indexset
def calcAttrOccurs(attrID,bigindex):
	times=0
	for index in bigindex:
		if attrID in index.occurence:
			times+=index.occurence[attrID]
	return times
def calcEntroy(attrID,bigindex,times):
	entroy=0
	for index in bigindex:
		entroy+=index.CalcsubEntroy(attrID,times)
	return entroy
def calcTotalEntroy(bigindex):
	attr_entroy={}
	for i in range(33):
		curindex=bigindex[i]
		for attrID in curindex.occurence:
			if attrID not in attr_entroy:
				times=calcAttrOccurs(attrID,bigindex)
				attr_entroy[attrID]=calcEntroy(attrID,bigindex,times)
	return attr_entroy

def writeEntroy(attr_entroy):
	import cPickle
	with open('../../Attach/entroy.txt','w') as efile:
		bytes=cPickle.dumps(attr_entroy,2)
		cPickle.dump(bytes,efile)

if __name__ == '__main__':
	indexset=createIndexSet()
	attr_entroy=calcTotalEntroy(indexset)
	writeEntroy(attr_entroy)