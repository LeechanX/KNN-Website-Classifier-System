class Centroid(object):
	def CalcCentroid(self,posvecsets):
		vector={}#pos:v
		size=len(posvecsets)
		for posvecs in posvecsets:
			for pos in posvecs:
				if pos not in vector:vector[pos]=0.0
				vector[pos]+=posvecs[pos]
		return vector,size
	def __init__(self,trainsets):
		self.centroid,self.size=self.CalcCentroid(trainsets)
