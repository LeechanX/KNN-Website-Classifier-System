#!/usr/bin/env python
#-*- encoding=utf-8 -*-
from __future__ import division
import heapq
from SimResult import SimResult
from Util import Util as myutil

def similarity_topk(simresults,k):
	"""get similarity_topk"""
	return heapq.nlargest(k,simresults,key=lambda x:x.sim)
def similarity_count(vector1,vector2,entroy_of_me):
	"""count for similarity between two vectors"""
	vectors_size_mul=sum(map(lambda x:x**2,vector1.values()))\
	*sum(map(lambda x:x**2,vector2.values()))
	pos_set1,pos_set2=frozenset(vector1.keys()),frozenset(vector2.keys())
	mix_attr=pos_set1 & pos_set2
	vector_mul=sum([vector1[x]*vector2[x]/entroy_of_me[x] for x in mix_attr])
	sim = 0 if not vectors_size_mul else vector_mul/vectors_size_mul**0.5
	pi=len(mix_attr)/min(len(pos_set1),len(pos_set2))
	sim*=pi
	return sim
def get_simresults(test_vector,doc_vectors,me_cate,entroy_of_me):
	"""get topk similarity in this category=me_cate
	we call the result 'subkNN'
	"""
	simresults=[]
	for doc_id in doc_vectors:
		sim=similarity_count(test_vector,doc_vectors[doc_id],entroy_of_me)
		result=SimResult(sim,me_cate,doc_id)
		simresults.append(result)
	kNNsets=similarity_topk(simresults,30)
	return kNNsets
def write_subkNN(kNNsets,fileno):
	"""write subkNN to file"""
	with open('cache/subkNNs/subkNN%s.txt' % fileno,'w') as out_file:
		for k in kNNsets:
			out_file.write(str(k)+'\n')
def get_samples_vectors(fileno,candidate_docs):
	doc_vectors={}
	with open('Attach/Train/train_t%s.txt' % fileno,'r') as fi:
		for line in fi:
			array=line.strip().split('\t')
			doc_id=array[0][:-1]
			if doc_id in candidate_docs:
				doc_vectors[doc_id]=myutil.read_posvectors_file(array[1:])
	return doc_vectors
def get_candidate_docs(test_vector,fileno):
	candidate_docs=[]
	with open('Attach/Index/index_t%s.txt' % fileno,'r') as fi:
		for line in fi:
			array=line.strip().split('\t')
			featureID=int(array[0][:-1])
			if featureID in test_vector: candidate_docs.extend(array[1:])
	if not all(candidate_docs):candidate_docs.remove('')
	candidate_docs=myutil.remove_duplicate(candidate_docs)
	return candidate_docs
def Maper_main(mycate,vectorOfme,entroy_of_me):
	candidate_docs=get_candidate_docs(vectorOfme,mycate)
	doc_vectors=get_samples_vectors(mycate,candidate_docs)
	kNNsets=get_simresults(vectorOfme,doc_vectors,mycate,entroy_of_me)
	write_subkNN(kNNsets,mycate)