import wx
import os
def display_filedialog():
	filepath=None
	wildcard = "Python source (*.py)|*.py|" "Compiled Python (*.pyc)|*.pyc|" "All files (*.*)|*.*"
	dialog = wx.FileDialog(None, "Choose a file", os.getcwd(),"", wildcard, wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK:
		filepath = dialog.GetPath()
	dialog.Destroy()
	return filepath