try:
	import numpy as np
	import scipy
	from scipy import stats
except:
	pass

class metapython():
	def __init__(self, val, llimit, ulimit, datatype = 1):
		'''
		Normal meta-analysis using python
		:param val: (list) list of the value
		:param llimit: (list) llimit
		:param ulimit: (list) ulimit
		:param datatype: (NOT totally defined) datatype = 1 means that there is the log value and log limits mostly presented in the studies
		'''
		val = np.array(val)
		llimit = np.array(llimit)
		ulimit = np.array(ulimit)

		if datatype == 1:
			self.es = np.log(val)
			self.var = (np.log(ulimit/llimit)/3.92)**2

		else: #todo: make other datatypes, later
			pass

		self.weight = 1 / self.var
		self.eswt = self.es * self.weight
		self.es2wt = (self.es ** 2) * self.weight
		self.wt2 = self.weight ** 2
		self.n = len(self.es)
		self.s1 = sum(self.weight)
		self.s2 = sum(self.eswt)
		self.s3 = sum(self.es2wt)
		self.s4 = sum(self.wt2)

		self.q = self.s3-(self.s2**2)/self.s1
		self.df = self.n-1
		self.numerator = max(self.q-self.df, 0)
		self.c = self.s1-self.s4/self.s1
		self.tau_sq = self.numerator/self.c

		self.var_total = self.var + self.tau_sq
		self.wt_random = 1/self.var_total
		self.eswt_random = self.es*self.wt_random

		self.s5 = sum(self.wt_random)
		self.s6 = sum(self.eswt_random)

	def meta_fixed(self):
		self.es_fixed_log = self.s2/self.s1
		self.var_fixed = 1/self.s1
		self.es_fixed = np.exp(self.es_fixed_log)
		self.lli_fixed = np.exp(self.es_fixed_log-1.96*np.sqrt(self.var_fixed))
		self.uli_fixed = np.exp(self.es_fixed_log+1.96*np.sqrt(self.var_fixed))
		self.pvalue_fixed = scipy.stats.norm.sf(abs((self.es_fixed_log)/(np.sqrt(self.var_fixed))))
		result = [self.es_fixed, self.lli_fixed, self.uli_fixed, self.pvalue_fixed]
		return result

	def meta_random(self):
		#todo: Make a meta_random function (random-effect meta-analysis)

		self.es_random_log = self.s6/self.s5
		self.var_random = 1/self.s5
		self.es_random = np.exp(self.es_random_log)
		self.lli_random = np.exp(self.es_random_log-1.96*np.sqrt(self.var_random))
		self.uli_random = np.exp(self.es_random_log+1.96*np.sqrt(self.var_random))
		self.pvalue_random = scipy.stats.norm.sf(abs(self.es_random_log)/(np.sqrt(self.var_random)))
		result = [self.es_random, self.lli_random, self.uli_random, self.pvalue_random]
		return result

	def meta_egger(self):
		'''
		Egger p-value
		:return: P-value (val)
		'''

		pass

	def print(self):
		print(self.s5, self.s6)

