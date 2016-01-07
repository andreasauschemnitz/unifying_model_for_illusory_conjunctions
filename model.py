import numpy as np

class Model:
	def printRates(self, rs):
		print("visual field:")
		print(rs[self.ivf])
		print("positions:")
		print(rs[self.inp])
		print("features/positions:")
		print(rs[self.inf])
		print("position invariant neurons:")
		print(rs[self.inc])
		print("position invariant neurons - dim 1:")
		print(rs[self.incd0])
		print("position invariant neurons - dim 2:")
		print(rs[self.incd1])
		print("winner - dim 1:")
		print(rs[self.incd0].argmax())
		print("winner - dim 2:")
		print(rs[self.incd1].argmax())

def nrange(start, n):
	return np.arange(start, start+n);

def createModel(wNoise, alternative, nStimuli):
	#wNoise = 0.04
	timeConst = 0.1
	
	#combinedRatio = 0.95
	
	cd = 2
	cp = 3
	cf = 5
	# dimension 0, feature 0: red
	# dimension 0, feature 1: green
	# dimension 1, feature 0: square
	# dimension 1, feature 1: star

	# visual field neurons
	ivf = nrange(0,cd*cf*cp)
	# location neurons
	inp = nrange(max(ivf)+1,cp)
	# feature neurons
	inf = nrange(max(inp)+1,cd*cf*cp)
	# position-invariant neurons
	inc = nrange(max(inf)+1,cd*cf)
	
	# position-invariant neurons, dimension 0
	incd0 = inc[range(0,int(len(inc)/2))]
	# position-invariant neurons, dimension 1
	incd1 = inc[range(int(len(inc)/2),len(inc))]

	iInput = np.append(ivf,inp)

	cn = max(inc)+1
	ns = range(cn)

	ws = np.zeros(cn*cn).reshape(cn,cn)

	###

	winh = -0.5
	wexc = 1

	for iDim in range(cd):
		for iFeature in range(cf):
			for iPos in range(cp):
				# VF --> feature
				ws[inf[iDim*cf*cp+iFeature*cp+iPos], ivf[iDim*cf*cp+iFeature*cp+iPos]] = wexc
				# pos --> feature
				ws[inf[iDim*cf*cp+iFeature*cp+iPos], inp[iPos]] = wexc
				# feature --> position invariant
				ws[inc[iDim*cf+iFeature], inf[iDim*cf*cp+iFeature*cp+iPos]] = wexc
				
				
				
				# feature --> feature (at same position) inhibition
				for iFeatureInhibit in range(cf):
					if iFeature != iFeatureInhibit:
						ws[inf[iDim*cf*cp+iFeature*cp+iPos], inf[iDim*cf*cp+iFeatureInhibit*cp+iPos]] = winh
			
			# inhibition between position-invariant neurons of the same dimension
			for iFeatureInhibit in range(cf):
				if iFeature != iFeatureInhibit:
					ws[inc[iDim*cf+iFeature], inc[iDim*cf+iFeatureInhibit]] = winh

	initOn = 0.1

	rsInit = np.zeros(cn)
	
	if nStimuli == 1: # Reynolds
		rsInit[[
			ivf[0*cf*cp+0*cp+0], # red, pos A
			ivf[1*cf*cp+0*cp+0] # square, pos A
		]] = initOn
	elif nStimuli == 2: # Reynolds
		rsInit[[
			ivf[0*cf*cp+0*cp+0], # red, pos A
			ivf[1*cf*cp+0*cp+0], # square, pos A
			ivf[0*cf*cp+1*cp+1], # green, pos B
			ivf[1*cf*cp+1*cp+1] # star, pos B
		]] = initOn
	else: # 3 objects (Treisman setup)
		rsInit[[
			ivf[0*cf*cp+0*cp+0], # red, pos A
			ivf[1*cf*cp+0*cp+0], # square, pos A
			ivf[0*cf*cp+1*cp+1], # green, pos B
			ivf[1*cf*cp+1*cp+1], # star, pos B
			ivf[0*cf*cp+2*cp+2], # dim 0, feature 2, pos C
			ivf[1*cf*cp+2*cp+2]  # dim 1, feature 2, pos C
		]] = initOn

	if alternative == "full":
		# FULL ATTENTION
		rsInit[inp[0]] = initOn
	elif alternative == "divided":
		# DIVIDED ATTENTION
		for i in range(cp):
			rsInit[inp[i]] = initOn / cp
	elif alternative == "random":
		# NO VISUAL FIELD INPUT
		rsInit[ivf] = 0
	else:
		#alternative == "combined"
		# COMBINED FULL AND DIVIDED ATTENTION
		#rsInit[inp[0]] = combinedRatio * initOn
		#initOnRest = (1-combinedRatio) * cp
		rsInit[inp[0]] = alternative * initOn
		initOnRest = (1-alternative) * cp
		for i in np.arange(1,cp):
			rsInit[inp[i]] = initOnRest / cp

	###

	locs = np.zeros((cn,),dtype=('f4,f4'))
	locs.dtype.names = ('x','y')

	distd = 5
	distf = 1
	distp = 2
	xcenter = (cf*cp-1)*distp+cp*distf+distd/2.0
	locs[inp] = [(xcenter-2,1), (xcenter,1), (xcenter+2,1)]
	locs[ivf] = [(i * distp + i // cp * distf + i // (cf*cp) * distd, 0) for i in range(cf*cp*cd)]
	locs[inf] = [(i, j+4) for (i,j) in locs[ivf]]
	locs[inc] = [(np.mean([locs[ivf][i*cp+iP]['x'] for iP in range(cp)]), 9) for i in range(cf*cd)]
	
	m = Model()
	m.ws = ws
	m.cn = cn
	m.locs = locs
	m.rsInit = rsInit
	m.iInput = iInput
	m.wNoise = wNoise
	m.timeConst = timeConst
	m.ivf=ivf
	m.inf=inf
	m.inp=inp
	m.inc=inc
	m.incd0=incd0
	m.incd1=incd1
	
	return m
