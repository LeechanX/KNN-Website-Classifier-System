#-*- encoding=utf-8 -*-

def cpickleload(filepath):
	import pickle,cPickle
	retobj=None
	with open(filepath,'rb') as pfile:
		bytes=pickle.load(pfile)
		retobj=cPickle.loads(bytes)
	return retobj
def dictsort(yourdict,reverse=False):
	return sorted(yourdict.items(),key=lambda x:x[1],reverse=reverse)
def read_posvectors_file(file_line_array):
	"""file_line_array except cate_id"""
	import re
	my_posvector={}
	for x in file_line_array:
		m=re.match('<(\d+),(\d+.\d+)>',x)
		if m:
			pos,v=int(m.groups()[0]),float(m.groups()[1])
			my_posvector[pos]=v
	return my_posvector
def remove_duplicate(obj):
	obj=set(obj)
	return list(obj)
def makedirectory(filepath):
	import os
	if not os.path.exists(filepath):
		os.makedirs(filepath)
def code2catename(cateno):
	cate_name=['',
	'餐饮烟酒副食','电邮','房产家居','交友','体育',
	'政法军事','宗教','时尚美容','影视','百货购物',#10
	'文化','工业行业网','新闻论坛','游戏动漫','旅行住店',#15
	'阅读','社会科学','音乐','交通物流','广告营销',#20
	'休闲娱乐','农林牧渔','金融保险','卫生保健',#24
	'人力与招聘','咨询服务','教育与培训','计算机技术',#28
	'家政礼仪','网络资源下载','门户网站与搜索引擎',#31
	'博彩','色情','无法识别'#33
	]
	return cate_name[cateno]