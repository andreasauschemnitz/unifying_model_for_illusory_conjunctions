import numpy as np

from gui import *
from model import *
from evaluation import *

np.core.arrayprint._line_width = 160

##########

nIter = 50

nTrials = 100
seedTrials = [100000*i for i in range(nTrials)]
nRuns = 11

#ratios = np.arange(0.5,0.7,0.01)
ratios = np.arange(0.5,0.7,0.01)
noise = 0.01
msCombinedAtt = [createModel(noise, ratio, nStimuli=3) for ratio in ratios]

print("noise",noise)
print("ratios",ratios)

###########

mFullAtt = createModel(noise, alternative="full", nStimuli=3)
mDividedAtt = createModel(noise, alternative="divided", nStimuli=3)
mRand = createModel(noise, alternative="random", nStimuli=3)

###########

print("Full Attention:")
evFullAtt = evaluateRunsModels([mFullAtt], nIter, seedTrials)
evFullAtt.printEvaluationSingle()

print("Divided Attention:")
evDividedAtt = evaluateRunsModels([mDividedAtt], nIter, seedTrials)
evDividedAtt.printEvaluationSingle()

print("Random:")
evRand = evaluateRunsModels([mRand], nIter, seedTrials)
evRand.printEvaluationSingle()

print("Combined Attention:")
evCombinedAtt = evaluateRunsModels(msCombinedAtt, nIter, seedTrials)
evCombinedAtt.printEvaluation(ratios)

#setupGUI(mDividedAtt)

