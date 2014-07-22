#-*- encoding=utf-8 -*-
class SortedDict(dict):
	def keys(self):
		return sorted(super(SortedDict,self).keys())
class Index(object):
	"""docstring for Index"""
	def __init__(self, clsname):
		super(Index, self).__init__()
		self.clsname=clsname
		self.reverseIndex=SortedDict()
	def create_Index(self,feature_pos,doc):
		"""input doc,append it"""
		if feature_pos not in self.reverseIndex:
			self.reverseIndex[feature_pos]=[]
		self.reverseIndex[feature_pos].append(doc)
	def record_Index(self):
		"""write to file"""
		with open('../../Attach/Index/index_%s.txt' % self.clsname,'w') as fi:
			for feature_pos in self.reverseIndex.keys():
				fi.write('%d:\t'% feature_pos)
				for doc_id in self.reverseIndex[feature_pos]:
					fi.write('%s\t' % doc_id)
				fi.write('\n')