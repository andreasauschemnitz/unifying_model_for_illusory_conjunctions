import numpy as np

from gui import *
from model import *
from evaluation import *

np.core.arrayprint._line_width = 160

##########

nIter = 50

#nTrials = 100
#seedTrials = [100000*i for i in range(nTrials)]
seedTrial=1000

noise = 0.01

###########

mFull = createModel(noise, alternative="full", nStimuli=2)
mDivBoth = createModel(noise, alternative="divided", nStimuli=2)
mDivSingle = createModel(noise, alternative="divided", nStimuli=1)

###########

print("full attention:")
evaluateAndPrintStimuli(mFull, nIter, seedTrial)

print("divided attention, single stimulus:")
evaluateAndPrintStimuli(mDivSingle, nIter, seedTrial)

print("divided attention, both stimuli:")
evaluateAndPrintStimuli(mDivBoth, nIter, seedTrial)

#setupGUI(mDividedAtt)

############

def plot5StimulusSets(ys):
	plt.xlabel("stimulus set")
	plt.ylabel("neuronal response rate")
	plt.xlim([0.5,5.5])
	xTicks = [1,2,3,4,5]
	xTicksLabels = ["i","ii","iii","iv","v"]
	xBars = [xt-0.4 for xt in xTicks]
	plt.bar(xBars, ys)
	plt.xticks(xTicks,xTicksLabels)
	plt.show()

# the following values are from evaluateAndPrintStimuli(...) above
ysModel = [
	0.1503,
	0.0001,
	0.1536,
	0.0941,
	0.0419
]
ysModelNormalized = [yM / max(ysModel) for yM in ysModel]
plt.title("B")
plt.ylim([-0.1,1.1])
plot5StimulusSets(ysModelNormalized)


plt.title("A")
plt.ylim([-0.1,2.1])
plt.yticks([0,1,2],["low","medium","high"])

ysReynolds = [2,0,2,1,0]

plot5StimulusSets(ysReynolds)

