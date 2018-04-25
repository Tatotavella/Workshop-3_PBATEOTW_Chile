# -⁻- coding: UTF-8 -*-
######################################################################
# This script retrieves the changes in Energy for a single pH in a MC 
# run and plots the output. Also gets the data of neighbouring 
# residues.
#
#  Inputs:
#  - Specific residue index to look data from. Indexes as used
#    in MC.log
#  Outputs:
#  - Plot of deltas for every step.
#  - Plot of Polar and Non polar neighbours for every step.
######################################################################
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

if len(sys.argv)<3:
	sys.exit("Error, enter /MC_result path and residue index of interest")
else:
	data_dir = sys.argv[1]
        residue_interest = float(sys.argv[2])

# Residue list from MC.state
dire_state = data_dir + '/MC.state'
file_state = open(dire_state, 'r')
firstLine = file_state.readline()
aux = [x for x in firstLine.split('\t')]
res_list = aux[1:-1]
file_state.close()

# Deltas from MC.log
dire_log = data_dir + '/MC.log'
# Columns are Step | Res | Nu_pol | Nu_npol | DpH | DElec | DEself
step, resids, Nu_pol, Nu_npol, DpH, DElec, DSelf = np.loadtxt(dire_log, delimiter = '\t', skiprows = 1 , usecols = (0,1,3,4,5,6,7), unpack = True)
# Get data for residue of interest
data_len = len(step)
res_Nu_pol = []
res_Nu_npol = []
res_DpH = []
res_DElec = []
res_DSelf = []
for i in range(data_len):
        if resids[i] == residue_interest:
                res_Nu_pol.append(Nu_pol[i])
                res_Nu_npol.append(Nu_npol[i])
                res_DpH.append(DpH[i])
                res_DElec.append(DElec[i])
                res_DSelf.append(DSelf[i])
# Graphs            
plt.figure(1)
plt.plot(res_Nu_pol,'o', color = 'blue', label = 'Polar Neighbours')
plt.plot(res_Nu_npol,'o', color = 'red', label = 'Non Polar Neighbours')
plt.xlabel('Monte Carlo Step', fontsize = 20)
plt.ylabel('Neighbour Count', fontsize = 20)
plt.legend(loc = 'upper right', numpoints = 1, fontsize = 20)
plt.tick_params(axis='both', labelsize=20)
plt.figure(2)
plt.plot(res_DpH,'o', color = 'green', label = r'$\Delta pH$')
plt.plot(res_DElec,'o', color = 'blue', label = r'$\Delta Elec$')
plt.plot(res_DSelf,'o', color = 'red', label = r'$\Delta Self$')
plt.xlabel('Monte Carlo Step', fontsize = 20)
plt.ylabel('Energy', fontsize = 20)
plt.legend(loc = 'upper right', numpoints = 1, fontsize = 20)
plt.tick_params(axis='both', labelsize=20)
plt.show()
