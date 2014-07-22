#-*- encoding=utf-8 -*-

import wx
from Settings.settings import Setting

class TextFrame(wx.Frame):
	def __init__(self):
		setting=Setting()
		setting.loadsettings()

		wx.Frame.__init__(self, None, -1, '参数设置',size=(260, 260))
		panel = wx.Panel(self, -1)
		sizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=5)
		
		label1=wx.StaticText(panel, -1, 'host:',size=(35, -1))
		self.host=wx.TextCtrl(panel, -1, '%s' % setting.dbset['host'],
			size=(100, -1))
		label2=wx.StaticText(panel, -1, 'password:')
		self.passwd=wx.TextCtrl(panel, -1, '%s' % setting.dbset['passwd'],
			size=(100, -1),style=wx.TE_PASSWORD)
		label3=wx.StaticText(panel, -1, 'user:')
		self.user=wx.TextCtrl(panel, -1, '%s' % setting.dbset['user'],
			size=(100, -1))
		label4=wx.StaticText(panel, -1, 'DB name:')
		self.db=wx.TextCtrl(panel, -1, '%s' % setting.dbset['db'],
			size=(100, -1))
		label5=wx.StaticText(panel, -1, 'DB port:')
		self.port=wx.TextCtrl(panel, -1, '%d' % setting.dbset['port'], 
			size=(100, -1))
		
		statisbtn=wx.Button(panel,-1,'更改',size=(80,30))
		self.Bind(wx.EVT_BUTTON,self.OnSetClick,statisbtn)

		sizer.AddMany([label1,self.host,
			label2,self.passwd,
			label3,self.user,
			label4,self.db,
			label5,self.port,
			statisbtn])
		panel.SetSizer(sizer)
	def OnSetClick(self,event):
		host=self.host.GetValue()
		passwd=self.passwd.GetValue()
		user=self.user.GetValue()
		db=self.db.GetValue()
		port=self.port.GetValue()
		setting=Setting()
		setting.updatesettings(host=host,passwd=passwd,user=user,db=db,port=port)
		del setting
def displaycfg():
	frame = TextFrame()
	frame.Show()