#-*- encoding=utf-8 -*-
import wx

def display_tips(tips):
	dlg = wx.MessageDialog(None,tips,'提示',wx.YES_NO)
	retCode = dlg.ShowModal()
	dlg.Destroy()