class SimResult(object):
	"""similarity of every sample in trainsamples"""
	def __init__(self,sim,hiscate,whom):
		super(SimResult,self).__init__()
		self.sim=sim
		self.hiscate=hiscate
		self.whom=whom
	def __str__(self):
		return '%s\t%f\t%s' % (self.hiscate,self.sim,self.whom)
	__repr__=__str__