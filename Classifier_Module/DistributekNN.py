#!/usr/bin/env python
#-*- encoding=utf-8 -*-
from __future__ import division
import threading
import Reducer
from Maper import similarity_count,Maper_main
from Util import Util as myutil

def collect_cates():
	"""get the features of every cate in system"""
	cates_feature={};
	for i in range(1,34):
		cates_feature[i]=[]
		with open('Attach/Ft/feat_t%d.txt' % i,'r') as fi:
			for line in fi:
				word=line.strip()
				cates_feature[i].append(word)
	return cates_feature
def loadFeatures():
	all_features={}
	with open('Attach/featureall.txt','r') as fi:
		lineno=0
		for line in fi:
			lineArr=line.strip().split('---')
			feature,idf=lineArr[0],float(lineArr[1])
			all_features[feature]=(lineno,idf)
			lineno+=1
	return all_features
def loadIndex():
	filename='Attach/roindex.txt'
	return myutil.cpickleload(filename)
def loadEntroy():
	filename='Attach/entroy.txt'
	return myutil.cpickleload(filename)
def createVector(test_entry,all_features):
	words,features=frozenset(test_entry.text),frozenset(all_features.keys())
	mixed=words&features
	vectorOfme={}
	for word in mixed:
		pos,tfidf=all_features[word]
		tfidf*=test_entry.text.count(word)/len(test_entry.text)
		vectorOfme[pos]=tfidf
	return vectorOfme
def isEmptyVector(vector):
	return True if sum(vector.values()) else False
def choose_candidate_cate(vector,indexes,entroy_of_me):
	cate_sim={};aver_sim=0.0
	for i,index in enumerate(indexes):
		sim=similarity_count(vector,index,entroy_of_me)
		if sim:cate_sim[i+1]=sim
	if len(cate_sim):
		aver_sim=sum([x for x in cate_sim.values()])/len(cate_sim)
	candidate_cate={k:v for k,v in cate_sim.items() if v>aver_sim}
	return candidate_cate
def further_choose_candidate_cate(test_entry,cates_feature,first_candidate,all_feature):
	cates_tfidf={};final_candidate={}
	words_set_in_test=frozenset(test_entry.text)
	for cate in first_candidate:
		words_set_in_train=frozenset(cates_feature[cate])
		mixed = words_set_in_test & words_set_in_train
		if mixed:
			cates_tfidf[cate]={}
			final_candidate[cate]=first_candidate[cate]
			for w in mixed:
				fid=all_feature[w][0]
				tf=test_entry.text.count(w)
				tfidf=tf*all_feature[w][1]
				cates_tfidf[cate][w]=tfidf
	weightsum=sum(final_candidate.values())
	for cate in final_candidate:
		final_candidate[cate]/=weightsum
	return final_candidate,cates_tfidf

def exec_Maper(cate,vectorOfme,entroy_of_me):
	Maper_main(cate,vectorOfme,entroy_of_me)
def main():
	cates_feature=collect_cates()
	all_features=loadFeatures()
	rocchioIndex=loadIndex()
	totalentroy=loadEntroy()
	myutil.makedirectory('cache/subkNNs/')
	while True:
		test_entry=(yield)
		print 'Yo,I am check %s Yo!' % test_entry.url###
		vectorOfme=createVector(test_entry,all_features)
		entroy_of_me={k:v for k,v in totalentroy.items() if k in vectorOfme}
		if not isEmptyVector(vectorOfme):
			yield (test_entry.url,-1)
			continue
		first_candidate=choose_candidate_cate(vectorOfme,rocchioIndex,entroy_of_me)
		if not first_candidate:
			yield (test_entry.url,-1)
			continue
		candidate_cates,cates_tfidf=\
		further_choose_candidate_cate(test_entry,cates_feature,first_candidate,all_features)
		
		threads=[]
		for cate in candidate_cates:
			t=threading.Thread(target=exec_Maper,args=(cate,vectorOfme,entroy_of_me,))
			threads.append(t)
		for t in threads:t.start()
		for t in threads:t.join()
		
		result=Reducer.main(tfidf=cates_tfidf,cateweight=candidate_cates)
		test_entry.thinkbe=result
		
		yield (test_entry.url,test_entry.thinkbe)