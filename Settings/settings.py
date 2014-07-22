#-*- encoding=utf-8 -*-
import ConfigParser

class Setting(object):
	settingfile='settings.ini'
	def __init__(self):
		self.dbset={'host':'localhost','passwd':'210013','user':'root','db':'samplesetsdb','port':3306}
	def loadsettings(self):
		cfg=ConfigParser.ConfigParser()
		cfg.read(self.settingfile)
		sections=cfg.sections()
		if 'mysql' in sections:
			for attr in cfg.options('mysql'):
				attrvalue=cfg.get('mysql',attr)
				if attr in self.dbset and attrvalue:
					self.dbset[attr]=attrvalue
			if self.dbset['port']:
				try:
					self.dbset['port']=int(self.dbset['port'])
				except ValueError:
					self.dbset['port']=3306
	def updatesettings(self,**args):
		cfg=ConfigParser.ConfigParser()
		cfg.read(self.settingfile)
		for key in args:
			if key in cfg.options('mysql'):cfg.set('mysql',key,args[key])
		cfg.write(open(self.settingfile,'w'))