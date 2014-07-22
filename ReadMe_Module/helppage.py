#-*- encoding=utf-8 -*-
import wx
import wx.wizard
class TitledPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent, title):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title) 
        titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0,
            wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0,
            wx.EXPAND | wx.ALL, 5)
def displayhelp():
    wizard = wx.wizard.Wizard(None, -1, '使用帮助')
    page1 = TitledPage(wizard, '基本操作') 
    page2 = TitledPage(wizard, '基本配置') 
    page3 = TitledPage(wizard, '类别说明') 
    page4 = TitledPage(wizard, '软件说明')
    page1.sizer.Add(wx.StaticText(page1, -1, '操作流程和键位介绍'))
    loadInfo(1,page1)
    loadInfo(2,page2)
    loadInfo(3,page3)
    loadInfo(4,page4)
    wx.wizard.WizardPageSimple_Chain(page1, page2) 
    wx.wizard.WizardPageSimple_Chain(page2, page3) 
    wx.wizard.WizardPageSimple_Chain(page3, page4)
    wizard.FitToPage(page1)
    if wizard.RunWizard(page1):
        pass 
    wizard.Destroy()
def loadInfo(no,page):
    filepath='ReadMe_Module/doc/page%d.txt' % no
    with open(filepath,'r') as readmefile:
        for line in readmefile:
            page.sizer.Add(wx.StaticText(page, -1, line))