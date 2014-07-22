#!/usr/bin/env python
import re
import os

def spiderweb(start_url,filepath):
	os.system('scrapy crawl superspider -a start_url=\'%s\' -a output_file=\'%s\'' % (start_url,filepath))
def main(webset):
	standard_webset=[]
	for url in webset:
		url=re.sub('\s','',url)
		if not url.startswith('http://') and not url.startswith('https://'):
			url='http://'+url
		standard_webset.append(url)
	download_path={};noconnet_web=[]
	for numb,web in enumerate(standard_webset):
		filepath='../Download/%d.html' % numb
		spiderweb(web,filepath)
		if os.path.exists(filepath):
			print 'filepath=%s' % filepath
			download_path[web]=filepath[3:]
		else:noconnet_web.append(web)
	return download_path,noconnet_web
def check_linked():
	return False if os.system('ping -c1 www.baidu.com') else True
def clear_download():
	dirpath='Download/'
	for fil in os.listdir(dirpath):
		filepath=os.path.join(dirpath,fil)
		if os.path.isfile(filepath):os.remove(filepath)