#-*- encoding=utf-8 -*-
from __future__ import division
import math
import heapq
from WordClass import WordClass
from Index import Index

class CateFeature(object):
	def __init__(self,name):
		"""docs :all doc in this type,docs=>words
		words :all word in this type,class(WordAttribute)
		feature :we need it as result,word=>weight
		"""
		self.name,self.docs,self.docnum=name,[],0
		self.words={}
		self.words_count={}
		self.feature={}
	def set_docs(self,conn):
		"""get every entry from db table
		entry[0]=id,entry[1]=keyword,entry[2]=description
		"""
		cur=conn.cursor()
		self.docnum=cur.execute('select id,title,keyword,description from %s' % self.name)
		if self.docnum:
			results=cur.fetchall()
			for entry in results:
				doc_id=entry[0]
				self.docs.append(doc_id)
				title=[word for word in entry[1].encode('utf-8').split('+') if word!='uk']
				keywords=[word for word in entry[2].encode('utf-8').split('+') if word!='uk']
				description=[word for word in entry[3].encode('utf-8').split('+') if word!='uk']
				self.words_count[doc_id]=len(title)+len(keywords)+len(description)
				for word in title+keywords+description:
					self.set_words(word,doc_id)
		cur.close()
	def set_words(self,word,doc_id):
		"""get all word (no repo)"""
		if word=='uk' or not word: return
		if word not in self.words:self.words[word]=WordClass(word,doc_id)
		else:self.words[word].updateRf(doc_id)
		self.words[word].setDocnum_in_cate()
	def counter_word_in_me(self,word):
		"""count for the number of document includes the word in this type"""
		return self.words[word].docnum_in_cate if word in self.words else 0
	def counter_word_in_others(self,word,other_cates):
		"""count for the number of document includes the word in one other type"""
		retval=0
		for other_cate in other_cates:
			num_in_other=other_cate.counter_word_in_me(word)
			if num_in_other: self.words[word].updateCatenum()
			retval+=num_in_other
		return retval
	def set_word_chi(self,other_cates,totaltype):
		"""count the for every word in words"""
		if not self.words: return
		for word in self.words:
			self.words[word].docnum_in_others=self.counter_word_in_others(word,other_cates)
			self.words[word].getCHI(totaltype,\
				cate_docsnum=self.docnum,othersdocs_num=self.all_docs_num-self.docnum)
	def feature_topk(self,k=100,thresold=6000):
		"""get top k of word chi,to be features"""
		topk=heapq.nlargest(k,self.words.values(),key=lambda x:x.chi) if self.words else None
		if not topk: return
		topk=[t for t in topk if t.chi>=thresold]
		for item in topk:
			self.feature[item.name]=item.chi
		return topk
	def count_tfidf(self):
		"""count tf*idf for every word"""
		if 'all_docs_num' not in dir(self):
			print 'just set all_docs_num to class attr firstly'
			return
		docsvector={}
		save_idf={}
		for doc_id in self.docs:
			docsvector[doc_id]=[]
			for word in sorted(self.feature):
				tf=0 
				if (doc_id in self.words[word].rf) and (self.words_count[doc_id]): 
					tf=self.words[word].rf[doc_id]
					tf/=self.words_count[doc_id]
				df=self.words[word].docnum_in_cate+self.words[word].docnum_in_others
				idf=math.log(self.all_docs_num/df,10.0)
				save_idf[word]=idf
				tfidf=tf*idf
				docsvector[doc_id].append(tfidf)
		return docsvector,save_idf
	def show(self):
		print 'feature'
		for word in self.feature:
			print word,':',self.feature[word]
	def get_words(self): return self.words
	def get_docs(self): return self.docs
	def get_feature(self): return self.feature
	def doc_to_vector_all(self,filename,feature_filename,all_feature):
		"""use features to make doc to vector"""
		docsvector=self.count_tfidf_all(all_feature)

		with open(feature_filename,'w') as featurefile:
			for word in sorted(self.feature):
				featurefile.write('%s\n' % word)

		my_index=Index(self.name)
		with open(filename,'w') as traintext:
			for doc in self.docs:
				traintext.write('%d:' % doc)
				feature_pos=0
				for tfidf in docsvector[doc]:
					if tfidf:
						my_index.create_Index(feature_pos,doc)
						traintext.write('\t<%d,%f>' % (feature_pos,tfidf))
					feature_pos+=1
				traintext.write('\n')
		my_index.record_Index()
	def count_tfidf_all(self,all_feature):
		"""count tf*idf for every word in every doc"""
		docsvector={}
		for doc_id in self.docs:
			docsvector[doc_id]=[]
			for word in all_feature.keys():
				tf=0
				if word in self.words and doc_id in self.words[word].rf and self.words_count[doc_id]:
					tf=self.words[word].rf[doc_id]
					tf/=self.words_count[doc_id]
				tfidf=tf*all_feature[word]
				docsvector[doc_id].append(tfidf)
		return docsvector
