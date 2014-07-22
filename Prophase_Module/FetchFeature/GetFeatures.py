#!/usr/bin/env python
#-*- encoding=utf-8 -*-
from __future__ import division
import os
import math
import MySQLdb as db
from CateFeature import CateFeature
class SortedDict(dict):
	"""docstring for SortedDict"""
	def keys(self):
		return sorted(super(SortedDict,self).keys())
def write_feature(cate_name,feature,all_features):
	with open('../../Attach/Features/feature_%s.txt' % cate_name,'w') as fi:
		for i,word in enumerate(all_features.keys()):
			if word in feature:
				fi.write('%d---%f\n' % (i,all_features[word]))
def write_all_feature(all_features):
	with open('../../Attach/featureall.txt','w') as fi:
		for f in all_features.keys():
			fi.write('%s---%f\n' % (f,all_features[f]))
def get_allcates(conn):
	cur=conn.cursor()
	num=cur.execute('show tables')
	results=cur.fetchall()
	cur.close()
	for tablename in ['t%d' % i for i in range(1,34)]:#[table[0] for table in results if table[0] not in ['testsets','unknown','t41']]:
		yield tablename

def make_dir(*paths):
	for path in paths:
		if not os.path.exists(path):os.makedirs(path)
def main():
	try:
		conn=db.connect(host='localhost',user='root',passwd='210013',db='samplesetsDB',port=3306,charset='utf8')
		allcates=[tablename for tablename in get_allcates(conn)]
		allcates={}.fromkeys([tablename for tablename in get_allcates(conn)],None)
		samplebook_length=0
		category_length=len(allcates)
		for cate in allcates:
			allcates[cate]=CateFeature(cate)
			allcates[cate].set_docs(conn)
			samplebook_length+=allcates[cate].docnum
		CateFeature.all_docs_num=samplebook_length
		make_dir('../../Attach/Train','../../Attach/Index','../../Attach/Ft')
		all_features=SortedDict()
		cate_feat_chi={}
		for cate_name in allcates:
			cate_feat_chi[cate_name]={}
			print 'Now fetch for %s' % cate_name
			thresold=(samplebook_length-allcates[cate_name].docnum)**2/(samplebook_length-1)
			allcates_except_me=list(allcates.values())
			allcates_except_me.remove(allcates[cate_name])
			allcates[cate_name].set_word_chi(allcates_except_me,category_length)
			wordssize=len(allcates[cate_name].words)
			result=allcates[cate_name].feature_topk(k=wordssize,thresold=thresold+1)
			print 'Fetch for %s OK' % cate_name
			for r in result:
				all_features[r.name]=math.log(samplebook_length/(r.docnum_in_cate+r.docnum_in_others),10)
				cate_feat_chi[cate_name][r.name]=r.chi
		write_all_feature(all_features)
		for cate_name in allcates:
			print 'now write for %s' % cate_name
			allcates[cate_name].doc_to_vector_all('../../Attach/Train/train_%s.txt' % cate_name,'../../Attach/Ft/feat_%s.txt' % cate_name,all_features)
			print 'Write for %s OK' % cate_name
		conn.close()
	except db.Error,e:
		print 'MySQL error:%d:%s' % (e.args[0],e.args[1])
if __name__ == '__main__':
	main()