#-*- encoding=utf-8 -*-
import MySQLdb as db
from Settings.settings import Setting
class DBOP(object):
	def __init__(self):
		self.conn=None
		setting=Setting()
		args=setting.dbset
		self.conn=db.connect(charset='utf8',**args)
	def movehead(self,web):
		if web.startswith('http://'):web=web[7:]
		if web.startswith('https://'):web=web[8:]
		if web.startswith('www.'):web=web[4:]
		return web
	def checkifexist(self,url):
		cursor=self.conn.cursor()
		url=self.movehead(url)
		sql='select id from results where url = \'%s\'' % url
		num=cursor.execute(sql)
		retval=True if num else False
		cursor.close()
		return retval
	def getcate(self,urls):
		retval=[]
		cursor=self.conn.cursor()
		for url in urls:
			url=self.movehead(url)
			sql='select cate from results where url = \'%s\'' % url
			num=cursor.execute(sql)
			if num:
				result=cursor.fetchall()
				cateno=result[0][0]
				retval.append((url,int(cateno)))
		cursor.close()
		return retval
	def insertres(self,result_set):
		cursor=self.conn.cursor()
		for web,cateno in result_set:
			web=self.movehead(web)
			sql="insert into results(url,cate) values('%s','%d')" % (web,cateno)
			cursor.execute(sql)
		self.conn.commit()
		cursor.close()
	def filterurl(self,urls):
		unknown_urls=[url for url in urls if not self.checkifexist(url)]
		urls_known=[url for url in urls if url not in unknown_urls]
		return (unknown_urls,urls_known)
	def domain(self,urls):
		(unknown_urls,urls_known)=self.filterurl(urls)
		urls_known_cate=self.getcate(urls_known)
		return (unknown_urls,urls_known_cate)
	def byebye(self):
		self.conn.close()