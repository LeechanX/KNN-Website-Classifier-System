#-*- encoding=utf-8 -*-
from __future__ import division
import math
class WordClass(object):
	"""docstring for WordClass"""
	def __init__(self, name, doc_id):
		super(WordClass, self).__init__()
		self.name=name
		self.docnum_in_cate,self.docnum_in_others=0,0
		self.catenum,self.chi=1,0
		self.rf={}
		self.rf[doc_id]=1
	def updateCatenum(self):
		self.catenum+=1
	def updateRf(self,doc_id):
		self.rf[doc_id]=1 if doc_id not in self.rf else self.rf[doc_id]+1
	def setDocnum_in_cate(self):
		self.docnum_in_cate=len(self.rf)
	def getCHI(self,types_num,cate_docsnum,othersdocs_num):
		"""the type number of the training,
		docnum of 
		ao: docnumber of term in this type,
		bo: docnumber of term not in this type,
		co: docnumber of this type not include term,
		do: docnumber of not this type not include term
		"""
		if not types_num: return
		ao=self.docnum_in_cate
		bo=self.docnum_in_others
		co,do=cate_docsnum-ao,othersdocs_num-bo
		relate_pn=ao*do-bo*co
		self.chi=0 if relate_pn<0 else \
		relate_pn**2/((ao+bo)*(co+do))*(math.log(types_num/self.catenum)+1)
		alf=0
		for doc_id in self.rf:
			alf+=self.rf[doc_id]
		rf_avr_in_cate=alf/cate_docsnum
		self.chi*=alf
		alf=ao/bo if bo!=0 else ao
		self.chi*=alf