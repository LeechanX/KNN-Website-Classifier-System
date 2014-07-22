#!/usr/bin/env python
#-*- encoding=utf-8 -*-
import re
import os
import wx
from copy import deepcopy
import UI_Module.filedialog as filedialog
import UI_Module.cfgdialog as cfgdialog
import UI_Module.tipsdialog as tipsdialog
import CSVop_Module.CSVstream as CSVstream
from DB_Module.DBop import DBOP
from Util import Util as myutil

class ProjectFrame(wx.Frame):
	"""docstring for ProjectFrame"""
	mesghead=['[INFO]:','[ERROR]:','[WARNNING]:']
	color=['GREEN','RED','BLUE']
	pattern=re.compile('((https?://)?[^\/\.]+\.[^\/]+)\w*')
	def __init__(self):
		super(ProjectFrame, self).__init__(None,-1,'网站智能识别系统',
			size=(530,410))
		panel=wx.Panel(self,-1)
		#panel.SetBackgroundColour('#FFFFCC')
		rev=wx.StaticText(panel,-1,'网站智能识别系统v0.1',
			pos=(183,8),size=(100,30),style=wx.ALIGN_CENTER)
		font=wx.Font(18,wx.DECORATIVE,wx.ITALIC,wx.NORMAL)
		rev.SetFont(font)

		author=wx.StaticText(panel,-1,'By:李琛轩',
			pos=(350,12),size=(100,30),style=wx.ALIGN_CENTER)
		font=wx.Font(14,wx.DECORATIVE,wx.ITALIC,wx.NORMAL)
		author.SetFont(font)
		author.SetForegroundColour('GRAY')
		self.textarea=wx.TextCtrl(panel,-1,'输入网站URL，一行一个',
			pos=(143,45),size=(350,320),style=wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_RICH2)
		self.textarea.SetInsertionPoint(0)
		f = wx.Font(3, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
	
		logo=wx.Image('logo.jpg',wx.BITMAP_TYPE_ANY)
		logo=logo.Scale(30,28)
		bm=wx.StaticBitmap(panel,-1,wx.BitmapFromImage(logo),
			pos=(143,8))

		self.importbtn=wx.Button(panel,-1,'导入CSV',
			pos=(20,35),size=(80,30))
		self.Bind(wx.EVT_BUTTON,self.OnImportClick,self.importbtn)
		self.startbtn=wx.Button(panel,-1,'开始分析',
			pos=(20,95),size=(80,30))
		self.Bind(wx.EVT_BUTTON,self.OnStartClick,self.startbtn)

		self.statisbtn=wx.Button(panel,-1,'参数配置',
			pos=(20,155),size=(80,30))
		self.Bind(wx.EVT_BUTTON,self.OnConfigClick,self.statisbtn)

		self.statisbtn=wx.Button(panel,-1,'清空栏目',
			pos=(20,215),size=(80,30))
		self.Bind(wx.EVT_BUTTON,self.OnClearClick,self.statisbtn)

		self.outbtn=wx.Button(panel,-1,'导出结果',
			pos=(20,275),size=(80,30))
		self.Bind(wx.EVT_BUTTON,self.OnOutClick,self.outbtn)

		self.helpbtn=wx.Button(panel,-1,'使用帮助',
			pos=(20,335),size=(80,30))
		self.Bind(wx.EVT_BUTTON,self.OnHelpClick,self.helpbtn)

		self.result_set=[]

	def loadclassifier(self,dialog):
		import Spider_Module.startspider as startspider
		dialog.Update(1)
		import PageExtract_Module.startextractor as startextractor
		dialog.Update(7)
		import Classifier_Module.Filter as cfilter
		dialog.Update(8)
		import Classifier_Module.DistributekNN as knnclassifier
		dialog.Update(14)
		self.classifier=knnclassifier.main()
		self.classifier.next()
		dialog.Update(21)

	def OnStartClick(self,event):
		linesize=self.textarea.GetNumberOfLines()
		urls=[]
		for i in xrange(linesize):
			url=self.textarea.GetLineText(i)
			urls.append(url)
		self.textarea.Clear()
		
		urls=myutil.remove_duplicate(urls)
		self.process_programmer(urls)
	def display_result(self):
		if not self.result_set:return
		self.textarea.Clear()
		self.textarea.SetDefaultStyle(wx.TextAttr('BLACK'))
		for web,cateno in self.result_set:
			self.WritetoFront('%s:%s' % (web,myutil.code2catename(cateno)))
		self.statis_result()
	def process_programmer(self,urls):
		self.result_set=[];domainurls=[]
		for url in urls:
			match=self.pattern.match(url)
			if match:
				url=match.group()
				domainurls.append(url)
				self.WritetoFront('目标 %d url : %s .' % (len(domainurls),url))
			else:
				self.WritetoFront(\
					'忽略%s,因为不是url...' % url,level=2)
		if not len(domainurls):
			self.WritetoFront('没有有效URL输入!',True,1)
			return
		self.WritetoFront('开始下载网页...')
		#check if has existed
		dbapi=None
		try:
			dbapi=DBOP()
		except:
			self.WritetoFront('无法连接数据库，请检查数据库设置!',True,1)
			return
		unknown_urls,urls_known_cate=dbapi.domain(domainurls)
		noconnet_web=[]
		if unknown_urls:
			import Spider_Module.startspider as startspider
			if not startspider.check_linked():
				self.WritetoFront('无法连接网络，请检查网络库设置!',True,1)
				return
			import PageExtract_Module.startextractor as startextractor
			import Classifier_Module.Filter as cfilter
			import Classifier_Module.DistributekNN as knnclassifier
			os.chdir('Spider_Module')
			(download_path,noconnet_web)=startspider.main(unknown_urls)
			self.WritetoFront('下载成功!')
			os.chdir('../')
			parser_results=startextractor.main(download_path)
			self.WritetoFront('页面处理成功!')
			classifier_inputs,unaccess_entity=cfilter.main(parser_results)
			self.WritetoFront('页面过滤成功!')
			#startspider.clear_download()
			for test_entry in classifier_inputs:
				result=self.classifier.send(test_entry)
				self.result_set.append(result)
				self.classifier.send(None)
			self.WritetoFront('分类结束!')
		inserts=deepcopy(self.result_set)
		self.result_set.extend(urls_known_cate)
		self.display_result()
		for web in noconnet_web:
			self.WritetoFront('%s无法连接!' % web)
		dbapi.insertres(inserts)
		dbapi.byebye()
	def OnConfigClick(self,evnet):
		cfgdialog.displaycfg()	
	def OnClearClick(self,event):
		self.textarea.SetDefaultStyle(wx.TextAttr('BLACK'))
		self.textarea.Clear()
	def OnOutClick(self,event):
		filepath=filedialog.display_filedialog()
		if not filepath:return
		if filepath.endswith('.csv'):
			CSVstream.export2csv(filepath,self.result_set)
			self.WritetoFront('导出结果成功!')
		else:
			self.WritetoFront('not CSV file!')
	def OnImportClick(self,event):
		filepath=filedialog.display_filedialog()
		if not filepath:return
		if not filepath.endswith('.csv'):
			tipsdialog.display_tips('注意导入的文件必须是CSV格式')
			return
		sign,urls=CSVstream.importcsv(filepath)
		if sign:
			self.CSVtoBoard(urls)
		else:
			msg=urls
			self.WritetoFront('%s' % msg,True,1)
	def WritetoFront(self,text,clear=False,level=0):
		self.textarea.SetDefaultStyle(wx.TextAttr(self.color[level]))
		if clear:self.textarea.Clear()
		self.textarea.AppendText('%s%s\n' % (self.mesghead[level],text))
	def CSVtoBoard(self,urls):
		self.textarea.SetDefaultStyle(wx.TextAttr('BLACK'))
		self.textarea.Clear()
		for url in urls:
			self.textarea.AppendText('%s\n' % url)
	def OnHelpClick(self,event):
		import ReadMe_Module.helppage as helppage
		helppage.displayhelp()
	def statis_result(self):
		if not self.result_set:return
		results={};results_sum=len(self.result_set)
		for web,cateno in self.result_set:
			if cateno not in results:results[cateno]=0
			results[cateno]+=1
		splitline='*'*10
		self.textarea.AppendText('%s\n' % splitline)
		self.textarea.AppendText('共分析了%d个网址,其中:\n' % results_sum)
		for cateno in results:
			self.textarea.AppendText('%s:%d个\n' % (myutil.code2catename(cateno),results[cateno]))
def main():
	app=wx.PySimpleApp()
	frame=ProjectFrame()
	progressMax=21
	dialog=wx.ProgressDialog('网站智能识别系统', '加载配置...', progressMax,
		style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
	frame.loadclassifier(dialog)
	dialog.Destroy()
	frame.Show()
	app.MainLoop()

if __name__ == '__main__':
	main()