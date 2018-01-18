import os
import Configurations as conf
import util

import matplotlib
if os.environ.get('DISPLAY','') == '':
	print('no display found. Using non-interactive Agg backend')
	matplotlib.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#Plot function
def timelines(y, xstart, xstop, color='b'):
	"""Plot timelines at y from xstart to xstop with given color."""   
	plt.hlines(y, xstart, xstop, color, lw=4)
	plt.vlines(xstart, y+0.03, y-0.03, color, lw=2)
	plt.vlines(xstop, y+0.03, y-0.03, color, lw=2)


def graphModuleandPamComparison(moduleDict,pamDict):
	pass

