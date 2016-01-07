import math
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

nradius = 0.5
arrowRadius = 0.1

def transferPositive(r):
	if r<0:
		return 0
	else:
		return r

def transferSigmoid(r):
	return 1.0/(1+math.e**(-r))

def transferShiftedSigmoid(r):
	if r<0:
		return 0
	else:
		return 2.0/(1+math.e**(-r))-1

def transferExp(r):
	if r<0:
		return 0
	else:
		return (1-math.e**(-r*1))

def transferFct(m,rs):
	for r in np.nditer(rs,op_flags=['readwrite']):
		rNoisy = r + np.random.normal()*m.wNoise
		r[...] = transferPositive(rNoisy)
	return(rs)

def iterate(m,nIter):
	rs=m.rsInit
	for i in range(nIter):
		sumIn=m.ws.dot(rs)
		rs = (1-m.timeConst)*rs + m.timeConst*transferFct(m, sumIn)
		rs[m.iInput]=m.rsInit[m.iInput]
	return(rs)

def drawNeuron(loc,r,rMax,ax):
	if r<0:
		r = 0
	if r>rMax:
		r=rMax
	rNormalized = r/rMax
	facecolor = mpl.colors.rgb2hex([1,1-rNormalized,1-rNormalized])
	circle = plt.Circle((loc['x'], loc['y']), radius=nradius, facecolor=facecolor, edgecolor='black')
	ax.add_patch(circle)

def drawNeurons(m, nIter, ax):
	rs = iterate(m, nIter)
	rMax = max(rs)
	
	print("====================================")
	print("nIter = "+str(nIter))
	m.printRates(rs)
	
	for i in range(len(m.locs)):
		drawNeuron(m.locs[i],rs[i],rMax,ax)

def drawArrow(locTo, locFrom, w,ax):
	if w>0:
		ls='solid'
		col="blue"
	else:
		ls='solid' #'dashed' #'dotted'
		col="turquoise"
	if locFrom == locTo:
		arc = mpatches.Arc((locFrom['x']-1.5*nradius,locFrom['y']),2*nradius,nradius,0,45,-45, linestyle=ls,color=col)
		ax.add_patch(arc)
	elif locFrom['y'] == locTo['y'] :
		if locFrom['x']<locTo['x']:
			start=(locFrom['x']+nradius*0.9,locFrom['y']-nradius*0.2)
			end=(locTo['x']-nradius*0.9,locTo['y']-nradius*0.2)
			cstyle = 'arc3,rad=0.3'
		else:
			start=(locFrom['x']-nradius*0.8,locFrom['y']-nradius*0.2)
			end=(locTo['x']+nradius*0.8,locTo['y']-nradius*0.2)
			cstyle = 'arc3,rad=-0.3'
		arrow = mpatches.FancyArrowPatch(start, end, connectionstyle=cstyle, mutation_scale=20, arrowstyle='->', linestyle=ls,color=col)
		ax.add_patch(arrow)
	else:
		angle = math.atan((locTo['x'] - locFrom['x']) / float(locTo['y'] - locFrom['y']))
		xAdjustment = nradius * math.sin(angle)
		yAdjustment = nradius * math.cos(angle)
		if locTo['y'] > locFrom['y'] :
			start = (locFrom['x'] + xAdjustment, locFrom['y'] + yAdjustment)
			end = (locTo['x'] - xAdjustment, locTo['y'] - yAdjustment)
		else:
			start = (locFrom['x'] - xAdjustment, locFrom['y'] - yAdjustment)
			end = (locTo['x'] + xAdjustment, locTo['y'] + yAdjustment)
		arrow = mpatches.FancyArrowPatch(start, end, mutation_scale=20, arrowstyle='->', linestyle=ls,color=col)
		ax.add_patch(arrow)
