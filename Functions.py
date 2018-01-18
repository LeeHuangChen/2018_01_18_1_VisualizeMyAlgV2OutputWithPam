import os
import Configurations as conf
import util
from macros import *

import Graph as graph

#adding values to a dictionary according to the follwoing format:
#Dict:
	#key: Protein PDB ID
	#val: Dictionary of modules and borders:
		# i.e. Dict:
			#key: modules
			#val: list of borders
				# i.e. list:
					#val: (start,end)

def addToModuleDict(pid, module, start, end, moduleDict):
	if pid in moduleDict.keys():
		subdict=moduleDict[pid]
	else:
		subdict={}
		moduleDict[pid]=subdict

	if module in subdict.keys():
		subdict[module].append((start,end))
	else:
		subdict[module]=[(start,end)]

#read the output from my algorithm and convert it to a moduleDict
def readModules(moduledir):

	#moduleDict
	#format:
	#Dict:
		#key: Protein PDB ID
		#val: Dictionary of modules and borders:
			# i.e. Dict:
				#key: modules
				#val: list of borders
					# i.e. list:
						#val: (start,end)
	moduleDict={}

	with open(moduledir,"r") as f:
		for i, line in enumerate(f):
			#first 3 lines are header
			if i>=3 and len(line)>0:
				#format of lines:
				#protName						borders
				#1DXZ:sp|P02710.1|ACHA_TETCF	M_0(302,325)	M_1(235,326)	M_2(393,461)	M_3(1,461)
				tabArr=line.split("\t")
				protName=tabArr[0]

				pid=protName.split(":")[0].strip()
				#read the borders
				for j in range(1,len(tabArr)):
					rawborder=tabArr[j]
					split1=rawborder.split("(")
					module=int(split1[0].split("_")[1])
					split2=split1[1].split(",")
					start=int(split2[0].strip())
					end=int(split2[1].replace(")","").strip())

					addToModuleDict(pid, module, start, end, moduleDict)
	return moduleDict

#read the pam mappings and covert it to a dict based on the same format as moduledict
def readPamMappings(pamdir):
	#for convienence, we will use the same format as moduleDict
	#format:
	#Dict:
		#key: Protein PDB ID
		#val: Dictionary of modules and borders:
			# i.e. Dict:
				#key: modules
				#val: list of borders
					# i.e. list:
						#val: (start,end)
	pamDict={}

	with open(pamdir,"r") as f:
		for i, line in enumerate(f):
			#first line is header
			if i>=1 and len(line)>0:
				#format of lines:
					#0      1               2               3       4
					#PDB_ID	PdbResNumStart	PdbResNumEnd	eValue	PFAM_ACC
					#1A2V	114	215	8.9E-31	PF02728.12
				tabArr=line.split("\t")
				pid=tabArr[0].strip()
				start=int(tabArr[1].strip())
				end=int(tabArr[2].strip())

				#assign a dummy module since all of the mappings are for the same family
				dummyModule=0

				addToModuleDict(pid, dummyModule, start, end, pamDict)

	return pamDict
			

def graphModuleAndPam(fileInfo):
	inputFolder=fileInfo[1]
	inputfile=fileInfo[2]

	moduledir=os.path.join(inputFolder, inputfile)
	pamdir=os.path.join(conf.pamFolder, inputfile)

	moduleDict=readModules(moduledir)
	pamDict=readPamMappings(pamdir)


	family=inputfile.replace(".txt","")
	graph.graphModuleandPamComparison(moduleDict,pamDict,family)


def main():
	forAllFiles(graphModuleAndPam, conf.moduleFolder)

if __name__ == '__main__':
	main()