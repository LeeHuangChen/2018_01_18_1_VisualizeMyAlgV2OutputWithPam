import os
import Configurations as conf
import util

import matplotlib
if os.environ.get('DISPLAY','') == '':
	print('no display found. Using non-interactive Agg backend')
	matplotlib.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import matplotlib.patches as mpatches

#Plot function
def timelines(y, xstart, xstop, color='b'):
	"""Plot timelines at y from xstart to xstop with given color."""   
	plt.hlines(y, xstart, xstop, color, lw=4)
	plt.vlines(xstart, y+0.03, y-0.03, color, lw=2)
	plt.vlines(xstop, y+0.03, y-0.03, color, lw=2)


def graphModuleandPamComparison(moduleDict,pamDict, family):
	pids=moduleDict.keys()

	for pid in pids:
		
		if pid in pamDict.keys():
			moduleSubDict=moduleDict[pid]
			pamBorders=pamDict[pid][0]



			for module in moduleSubDict.keys():
				ycounter=1
				#plot pam borders:
				for border in pamBorders:
					start=border[0]
					end=border[1]

					timelines(ycounter,start,end, "red")
					ycounter+=1

				#graph my module borders
				for border in moduleSubDict[module]:
					start=border[0]
					end=border[1]

					timelines(ycounter,start,end, "blue")
					ycounter+=1

				#create the legend
				red_patch = mpatches.Patch(color='red', label='PFam Mappings')
				blue_patch = mpatches.Patch(color='blue', label='My Module Borders')
				plt.legend(handles=[red_patch, blue_patch],loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)

				#save the figure:
				#generate the result folder
				outputFolder=os.path.join(conf.resultFolder,family,pid)
				util.generateDirectories(outputFolder)
				outdir=os.path.join(outputFolder,"Module"+str(module)+".png")
				plt.savefig(outdir,bbox_inches="tight")
				plt.close()
		else:
			print pid, "not found in PFam Mappings"




