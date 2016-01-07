from simulation import *

def divideOr99(a,b):
	if b==0:
		return 99
	else:
		return a/b

class Evaluation:
	def __init__(self, nRuns):
		self.nRuns = nRuns
		self.nCorrect = [0.0 for i in range(nRuns)]
		self.nIC = [0.0 for i in range(nRuns)]
		self.nError = [0.0 for i in range(nRuns)]
	def printEvaluationSingle(self):
		self.nTotal = [self.nCorrect[i]+self.nIC[i]+self.nError[i] for i in range(self.nRuns)]
		self.pCorrect = [self.nCorrect[i]/self.nTotal[i] for i in range(self.nRuns)]
		self.pIC = [self.nIC[i]/self.nTotal[i] for i in range(self.nRuns)]
		self.pError = [self.nError[i]/self.nTotal[i] for i in range(self.nRuns)]
		self.cost = [round(np.power(.37/.49 - divideOr99(self.nIC[i],self.nCorrect[i]), 2), 2) for i in range(self.nRuns)]
		print("correct: ",self.pCorrect)
		print("IC:      ",self.pIC)
		print("error:   ",self.pError)
		print("distance:",self.cost)
	def printEvaluation(self, ratios):
		self.nTotal = [self.nCorrect[i]+self.nIC[i]+self.nError[i] for i in range(self.nRuns)]
		self.pCorrect = [self.nCorrect[i]/self.nTotal[i] for i in range(self.nRuns)]
		self.pIC = [self.nIC[i]/self.nTotal[i] for i in range(self.nRuns)]
		self.pError = [self.nError[i]/self.nTotal[i] for i in range(self.nRuns)]
		self.cost = [round(np.power(.49/.37 - divideOr99(self.nCorrect[i],self.nIC[i]), 2), 2) for i in range(self.nRuns)]
		print("correct: ",self.pCorrect)
		print("IC:      ",self.pIC)
		print("error:   ",self.pError)
		print("distance:",self.cost)
		iOptimal = np.argmin(self.cost)
		print("optimal ratio: ", round(ratios[iOptimal],2))
		print("optimal [correct, IC, error]:",[self.pCorrect[iOptimal], self.pIC[iOptimal], self.pError[iOptimal]])
		

#def evaluateRunsRandom(m, nIter, seedTrials, nRuns):
#	evaluation = Evaluation(nRuns)
#	evaluation.nIter = nIter
#	for iRun in range(nRuns):
#		evaluateRunRandom(m, evaluation, iRun, seedTrials)
#	return evaluation


def evaluateRunsModels(ms, nIter, seedTrials):
	nm = len(ms)
	evaluation = Evaluation(nm)
	evaluation.nIter = nIter
	for i in range(nm):
		evaluateRun(ms[i], evaluation, seedTrials, i)
	return evaluation

#def evaluateRunRandom(m, evaluation, seedTrials, iRun):
#	for i in range(len(seedTrials)):
#		np.random.seed(1000*iRun + seedTrials[i])
#		evaluateTrial(m, evaluation, iRun)

def evaluateRun(m, evaluation, seedTrials, iRun):
	for i in range(len(seedTrials)):
		np.random.seed(seedTrials[i])
		evaluateTrial(m, evaluation, iRun)

def evaluateTrial(m, evaluation, iRun):
	rsFinal = iterate(m, evaluation.nIter)
	# index of the winning position-invariant neuron in dimension 0
	wind0 = rsFinal[m.incd0].argmax()
	# index of the winning position-invariant neuron in dimension 1
	wind1 = rsFinal[m.incd1].argmax()
	
	# Suppose that the model is specified in a way that one object has
	# feature 1 (e.g. blue) in dimension 1 (e.g. color)
	# and feature 1 (e.g. square) in dimension 2 (e.g. shape);
	# whereas the other object has
	# feature 2 (eg green) in dim 1 (eg color)
	# and feature 2 (eg star) in dim 2 (eg shape)
	fvf = [0,1,2] # features present in the visual field (by chance the same for both dimensions)
	if (wind0 in fvf) & (wind1 in fvf):
		if wind0 == wind1 :
			evaluation.nCorrect[iRun] = evaluation.nCorrect[iRun]+1
		else:
			evaluation.nIC[iRun] = evaluation.nIC[iRun]+1
	else:
		evaluation.nError[iRun] = evaluation.nError[iRun]+1

##################

def evaluateAndPrintStimuli(m, nIter, seedTrial):
	rsFinal = iterate(m, nIter)
	np.random.seed(seedTrial)
	print("strong stimulus [dim0, dim1]: ", [round(rsFinal[m.incd0][0],4), round(rsFinal[m.incd1][0],4)])
	np.random.seed(seedTrial)
	print("poor stimulus [dim0, dim1]:   ", [round(rsFinal[m.incd0][1],4), round(rsFinal[m.incd1][1],4)])
