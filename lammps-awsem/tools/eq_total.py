# -⁻- coding: UTF-8 -*-
#######################################################################
# Script to analyze the total charge and electrostatic energy on the
# system. The path to the pHs runs must be given and the data is
# displayed in plots.
#  Inputs:
#  - Path to directory with pH runs data.
#  Outputs:
#  - Plot of mean value of total charge and electrostatic energy. Also
#   the variances are plotted.
#######################################################################
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from functions import *
import sys

if len(sys.argv)<2:
	sys.exit("Error. Enter path to directory with runs for every pH")
else:
	data_dir = sys.argv[1]

# pH List
pHs = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']
phsVal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

# Total charge and electrostatic energy of the system
dcr_step = 70 # Decorrelation step
init_step = 70 # Starting point of data analysis

charges = []
chargesVar = []
energies = []
energiesVar = []

for ph in pHs:
	#MC.state file
	state_path = "/"+ph+"/MC_result/MC.state"
	stateDirec = data_dir + state_path
	q = qTot(stateDirec, init_step, dcr_step)
	charges.append(q[0])
	chargesVar.append(q[1])

        #MC.log file
	log_path = "/"+ph+"/MC_result/MC.log"
	logDirec = data_dir + log_path
	e = eTot(logDirec, init_step, dcr_step)
	energies.append(e[0])
	energiesVar.append(e[1])

        totalStates = e[2]
        
print('Files analyzed with '+str(int(totalStates))+' data points per residue')


# Graphs
# Mean Values
f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)
# Charge
ax1.errorbar(phsVal, charges, yerr=chargesVar, fmt='bo')
ax1.plot(phsVal, charges,'b')
ax1.plot([0,15],[0,0],'g', linewidth = 3 , linestyle = 'dashed')
ax1.set_xlim([1,14])
ax1.set_ylabel(r'$<Q_{tot}>$', fontsize = 20)
# Energy
ax2.errorbar(phsVal,energies,energiesVar,fmt='ro')
ax2.plot(phsVal,energies,'r')
ax2.plot([0,15],[0,0],'g', linewidth = 3 , linestyle = 'dashed')
ax2.set_xlim([1,14])
ax2.set_xlabel('pH', fontsize = 20)
ax2.set_ylabel(r'$<V_{elec}>$', fontsize = 20)

# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=0.2)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

# Variances
f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)
ax1.plot(phsVal,chargesVar,'bo')
ax1.plot(phsVal,chargesVar,'b')
ax1.set_xlim([1,14])
ax1.set_ylabel(r'$Var(Q_{tot})$', fontsize = 20)

ax2.plot(phsVal,energiesVar,'ro')
ax2.plot(phsVal,energiesVar,'r')
ax2.set_xlim([1,14])
ax2.set_xlabel('pH', fontsize = 20)
ax2.set_ylabel(r'$Var(V_{elec})$', fontsize = 20)

# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=0.2)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

plt.show()



