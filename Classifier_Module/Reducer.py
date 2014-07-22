#!/usr/bin/env python
#-*- encoding=utf-8 -*-
from __future__ import division
import math
from SimResult import SimResult

def pick_unknown():
	return (-1,'不知道哦')

def sort_by_value(dict_,reverse=False):
	return sorted(dict_.items(),lambda x,y: cmp(x[1],y[1]),reverse=reverse)
def Merge_Sort(sub_kNNs):
	"""merge every subkNN sim_sort results to allkNN topk"""
	get_topk=0
	kNNsets=[]
	while get_topk<30:
		max_one,which=0,-1
		for i,sub_kNN in enumerate(sub_kNNs):
			if not sub_kNN:continue
			if sub_kNN[0].sim>max_one:
				max_one,which=sub_kNN[0].sim,i
		if which==-1:#now all count ok!
			break
		chooseone=sub_kNNs[which].pop(0)
		kNNsets.append(chooseone)
		get_topk+=1
	return kNNsets

def kNN_handle(kNNsets,**candidate_cates_argv):
	"""find a category which has max weight value to be result"""
	words_tfidf,cateweight=candidate_cates_argv['tfidf'],candidate_cates_argv['cateweight']
	cate_statis={};attrsets={}
	for k in kNNsets:
		cate,sim=k.hiscate,k.sim
		if sim<=0:continue
		cate_statis[cate]=(cate_statis[cate][0]+sim,cate_statis[cate][1]+1) if cate in cate_statis\
		else (sim,1)
	for cate in cate_statis:
		simall,occurall=cate_statis[cate]
		cate_statis[cate]=(0.8*simall/occurall+0.2*math.log(occurall,2))
		aver_tfidf=sum(words_tfidf[cate].values())/len(words_tfidf[cate])
		aver_tfidf*=math.log(len(words_tfidf[cate])+1,2)
		cate_statis[cate]*=aver_tfidf*cateweight[cate]

	results=sort_by_value(cate_statis,True)
	return results[0][0]

def Reducer(candidate_cates,**candidate_cates_argv):
	"""get every subkNN results,
	then call function Merge_Sort to get allkNN topk result
	"""
	sub_files=['cache/subkNNs/subkNN%s.txt' % x for x in candidate_cates]
	if not sub_files:return pick_unknown()
	sub_kNNs=[]
	for sub_file in sub_files:
		sub_kNN=[]
		with open(sub_file,'r') as fi:
			for line in fi:
				item=line.strip().split('\t')
				simobj=SimResult(float(item[1]),int(item[0]),item[2])
				sub_kNN.append(simobj)
		sub_kNNs.append(sub_kNN)
	kNNsets=Merge_Sort(sub_kNNs)
	return kNN_handle(kNNsets,**candidate_cates_argv)

def main(**candidate_cates_argv):
	"""firstly,get candidate cates for this test item;
	secondly,call Reducer to get kNN topk
	"""
	candidate_cates=candidate_cates_argv['cateweight'].keys()
	return Reducer(candidate_cates,**candidate_cates_argv)