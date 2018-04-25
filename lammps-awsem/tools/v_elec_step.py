# -⁻- coding: UTF-8 -*-
######################################################################
# This script retrieves the Electrostatic Energy for a single pH
# and plots the output. Also an autocorrelation analysis is used 
# to filter the data from Monte Carlo steps. Decorrelation step
# can be changed to get desired results.
#
#  Inputs:
#  - Path to MC_result directory where MC.log file is placed
#  Outputs:
#  - Plots of Electrostatic energy with all steps and decorrelated
#    ones.
#  - Plot of Autocorrelation function of Electrostatic Energy
######################################################################
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from functions import *
import sys

if len(sys.argv)<2:
	sys.exit("Error, enter /MC_result path")
else:
	data_dir = sys.argv[1]

dire_log = data_dir + '/MC.log'
dire_state = data_dir + '/MC.state'

# Data loading
E_electro = np.loadtxt(dire_log, delimiter = '\t', skiprows = 1, usecols = (8,))

# Autocorrelation
taus = range(1,250)
corr = []
for tau in taus:
	tmp = autocorr(E_electro,tau)
	corr.append(tmp)

# Decorrelation step used. Extracted in reference to autocorrelation plot.
dcr_step = 70
descorr = []
for e in range(len(E_electro)):
	if(e%dcr_step == 0):
		descorr.append(E_electro[e])
mean_E = np.mean(descorr)
std_E = np.std(descorr)

#Graphs
plt.figure(1)
plt.title('Electrostatic Energy over MC steps')
plt.ylabel('Electrostatic Energy', fontsize = 20)
plt.xlabel('Monte Carlo Step', fontsize = 20)
plt.plot(E_electro, 'o', markersize = 5, color = 'blue')
plt.figure(2)
plt.title('Autocorrelation function of Elec Energy')
plt.plot(taus, corr, '*', markersize = 5, color = 'red')
plt.plot([1,len(taus)], [0,0], linewidth = 4, color = 'green', linestyle = 'dashed')
plt.xlabel('Tau', fontsize = 20)
plt.ylabel('Autocorrelation', fontsize = 20)
plt.figure(3)
plt.title('Decorrelated states of Elec Energy and mean value')
plt.plot(descorr,'o',markersize=5,color='blue')
plt.plot([1,len(descorr)],[mean_E,mean_E], linewidth = 4, color = 'red')
plt.xlim([1,len(descorr)])
plt.xlabel('Monte Carlo Step', fontsize = 20)
plt.ylabel('Decorrelated Elec Energy', fontsize = 20)

plt.show()

'''
#Extra stuff

x = range(0,len(descorr))
y = np.full(len(descorr),mean_E)
error = std_E
print(len(x))
print(len(y))
plt.fill_between(x, y-error, y+error)
plt.show()

plt.hist(descorr,bins=10)
plt.show()
'''
