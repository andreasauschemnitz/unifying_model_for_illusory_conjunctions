import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button, Slider
from matplotlib.text import Text

from simulation import *

nIterInit = 0

def updateSlider(m, val, ax):
	slider.set_val(val)
	drawNeurons(m, val, ax)

def keyPressed(event,slider):
	val = slider.val
	if (event.key == '+') | (event.key == '-') | (event.key == '*') :
		if event.key == '+':
			val = int(slider.val)+1
		if event.key == '-':
			val = int(slider.val)-1
		if event.key == '*':
			val = int(slider.val)
		slider.set_val(val)

def setupGUI(m):
	plt.ion()

	fig = plt.figure()
	fig.patch.set_facecolor('white')

	#mng = plt.get_current_fig_manager()
	#(maxsizeW,maxsizeH)=mng.window.maxsize()
	#mng.resize(maxsizeW+30,maxsizeH)

#	gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1]) 
#	ax0 = plt.subplot(gs[0])
#	ax1 = plt.subplot(gs[1])
#	ax0.axis('off')
#	ax1.axis('off')
	
	ax0 = plt.axes([0.1,0.2,0.8,0.7], axisbg="w")
	ax0.axis('off')
	
	axSlider = plt.axes([0.2, 0.1, 0.6, 0.05], axisbg="w")
	
	slider = Slider(axSlider, "iter", 0, 100, valinit=0, dragging=False)

	slider.on_changed(lambda event: drawNeurons(m, int(slider.val), ax0))
	
	#ax_b0 = plt.axes([0.8,0.05,0.1,0.05])
	#b0 = Button(ax_b0,'-')
	#ax_b1 = plt.axes([0.8,0.1,0.1,0.05])
	#b1 = Button(ax_b1,'o')
	#ax_b2 = plt.axes([0.8,0.15,0.1,0.05])
	#b2 = Button(ax_b2,'+')
	#b0.on_clicked(lambda event: updateSlider(m, slider.val-1, ax0))
	#b1.on_clicked(lambda event: updateSlider(m, slider.val, ax0))
	#b2.on_clicked(lambda event: updateSlider(m, slider.val+1, ax0))
	
	fig.canvas.mpl_connect('key_press_event',lambda event: keyPressed(event, slider))

	print(m.rsInit)
		
	# Draw all arrows only once
	for i in range(m.cn):
		for j in range(m.cn):
			w = m.ws[i,j]
			if w != 0:
				drawArrow(m.locs[i],m.locs[j], w, ax0)

	# Draw initial state of neurons
	drawNeurons(m, nIterInit, ax0)
	
	ax0.axis('scaled')

	plt.show()
