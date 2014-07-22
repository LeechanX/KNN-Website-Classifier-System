#-*- encoding=utf-8 -*-
import csv

def preteat(result_set):
	dataset=[]
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
	for web,cateno in result_set:
		dataset.append((web,cate_name[cateno]))
	return dataset

def export2csv(filepath,dataset):
	#dataset: [(..,..),(..,..),..]
	dataset=preteat(dataset)
	with open(filepath,'wb') as csvfile:
		writer=csv.writer(csvfile)
		writer.writerow(['URL','类别'])
		writer.writerows(dataset)

def __importcsv(filepath):
	urls=[]
	with open(filepath,'rb') as csvfile:
		reader=csv.reader(csvfile)
		for line in reader:
			url=line[0].split('\t')[0]
			urls.append(url)
	return urls

def importcsv(filepath):
	urls=[];retmsg=None;retval=True
	try:
		urls=__importcsv(filepath)
	except:
		retmsg='Error when import CSV...'
		retval=False
	else:
		retmsg=urls
	finally:
		return retval,retmsg