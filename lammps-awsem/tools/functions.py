import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

##
# Lists of acid bases. C is Cterminal, N is Nterminal and B is cysteine
##
acid_list = ['D', 'E', 'C', 'B', 'Y']
base_list = ['K', 'R', 'N', 'H']
##
# Autocorrelation value of a data set y in a given distance
# tau.
#
#  Inputs:
#  - y. Data values to be analyzed
#  - tau. Distance of auto-correlation to compute
#  Outputs:
#  - z. Autocorrelation value at a distance tau
##
def autocorr(y,tau):
    mean = np.mean(y)
    var = np.var(y)
    partsum = 0.0
    for t in range(len(y)-tau):
        partsum += (y[t] - mean)*(y[t+tau] - mean)
    corr = partsum/(len(y)-tau)
    z = corr/var
    return z

##
# This function calculates the times a residue is charged
# in the ensemble of a given pH. Starts from meanInit and
# decorrelates the data each decorrStep. This is done for
# every residue in resList. The data is loaded from
# stateDirec using MC.state files.
#
#  Inputs:
#  - stateDirec. Directory containing MC.state file
#  - meanInit. Starting data Point from which data is
#              collected
#  - resList. List of residues' indexes to be analyzed
#  - decorrStep. Step to decorrelate data in the ensemble
#
#  Outputs:
#  - outputDepr. Dictionary with indexes as keys containing
#                protonated fraction mean values for each
#                residue.
#  - totalStates. Number of points per residue used for
#                 mean calculations.
##
def deproto(stateDirec,meanInit,resList,decorrStep):
	g = open(stateDirec,'r')
        # Deprotonated fraction - Initialization for auxiliary mean calculator
        outputDepr = {}
        resMeans = []
	for r in resList:
		outputDepr.update({r:[]})
                resMeans.append(0)
	totalStates = 0.0
        # Jump header
	next(g)
        # Jump meanInit Steps
        k = 0
        for a in range(meanInit):
            next(g)
            k += 1
        # Mean calculations
	for line in g:
            # Decorrelated states
            if((k-meanInit)%decorrStep == 0):
		inter = [x for x in line.split('\t')]
                for idx,q in enumerate(inter[1:-1]):
                    # Times charged
	            resMeans[idx] += abs(float(q))
                totalStates += 1
            k += 1
	g.close()
    	for idx in range(len(resMeans)):
		resMeans[idx] = resMeans[idx]/totalStates
                outputDepr[resList[idx]].append(resMeans[idx])
        return [outputDepr, totalStates]
##
# Function to obtain for a single pH the mean value
# and variance of the total charge in the system.
# Data is taken next to meanInit and it's
# decorrelated every decorrSteps. The path to
# MC.state is stateDirec.
#
#  Inputs:
#  - stateDirec. Path to MC.state file
#  - meanInit. Starting data Point from which data is
#              collected
#  - decorrStep. Step to decorrelate data in the ensemble
#  Outputs:
#  - chargeMean. Mean value of the total charge in the
#                system over the ensemble
#  - chargeVar. Variance of the total charge in the
#               system over the ensemble
#  - totalStates. Number of points per residue used for
#                 calculations.
##
def qTot(stateDirec,meanInit,decorrStep):
	g = open(stateDirec,'r')
	chargeMean = 0
	csqrtMean = 0
        # Jump Header
	next(g)
        # Jump meanInit Steps
        k = 0
        for a in range(meanInit):
            next(g)
            k += 1 
        totalStates = 0
        # Mean-Var calculations
	for line in g:
            # Decorrelated states
	    if((k-meanInit)%decorrStep == 0):
		inter = [x for x in line.split('\t')]
		q = inter[-1]
		chargeMean += float(q)
		csqrtMean += float(q)*float(q)
		totalStates += 1
	    k+=1
	g.close()
	chargeMean = chargeMean/totalStates
	csqrtMean = csqrtMean/totalStates
	chargeVar = csqrtMean - chargeMean**2
	return [chargeMean,chargeVar,totalStates]
##
# Function to obtain for a single pH the mean value
# and variance of the total electrostatic energy
# in the system.
# Data is taken next to meanInit and it's
# decorrelated every decorrSteps. The path to
# MC.log is logDirec.
#
#  Inputs:
#  - logDirec. Path to MC.log file
#  - meanInit. Starting data Point from which data is
#              collected
#  - decorrStep. Step to decorrelate data in the ensemble
#  Outputs:
#  - energyMean. Mean value of the total charge in the
#                system over the ensemble
#  - energyVar. Variance of the total charge in the
#               system over the ensemble
#  - totalStates. Number of points per residue used for
#                 mean calculations.
##
def eTot(logDirec,meanInit,decorrStep):
	g = open(logDirec,'r')
	energyMean = 0
	esqrtMean = 0
        # Jump Header
	next(g)
        # Jump meanInit Steps
        k = 0
        for a in range(meanInit):
            next(g)
            k += 1     
        totalStates = 0
        # Mean-Var calculations
	for line in g:
            # Decorrelated States
            if((k-meanInit)%decorrStep == 0):
		inter = [x for x in line.split('\t')]
		e = inter[-1]
		energyMean += float(e)
		esqrtMean += float(e)*float(e)
		totalStates += 1
	    k+=1
	g.close()
	energyMean = energyMean/totalStates
	esqrtMean = esqrtMean/totalStates
	energyVar = esqrtMean - energyMean**2
	return [energyMean,energyVar,totalStates]


##
# Henderson - Hasselbalch functions to fit acid
# and bases
#
#  Inputs:
#  - x. Actual pH
#  - a. pKa Value
#  - b. n Value
#  Outputs:
#  - y. Henderson - Hasselbalch Value
##
def acidos(x, a, b):
	y = 1.0/(1.0+10.0**(-1.0*b*(x-a)))
	return y
def bases(x, a, b):
	y = 1.0/(1.0+10.0**(b*(x-a)))
	return y
##
# Fitting function of Henderson - Hasselbalch curve.
# Numpy's curve_fit method is used. pKa and n values
# are obtained with its errors. If all variables
# returned are -1 there is a fitting error.
#
#  Inputs:
#  - phs. A list of phs used
#  - deprot. A list with protonated fractions
#  - let. Residue type in single letter code
#  Outputs:
#  - pka. pKa value from fit
#  - errpka. pka error from fit estimation
#  - n. n value from fit
#  - errn. n error from fit estimation
##
def fitHenHass(phs,prot,let):
    # Error if all values are -1
    pka = -1
    errpka = -1
    n = -1
    errn = -1
    # Fit
    x = np.linspace(phs[0], phs[-1], 100)
    if let in acid_list:
        try:
            popt, pcov = curve_fit(acidos, phs, prot,p0=[5,1])
            perr = np.sqrt(np.diag(pcov))
	    pka = popt[0]
            errpka = perr[0]
            n = popt[1]
            errn = perr[1]
        except RuntimeError:
            pass
    elif let in base_list:
        try:
            popt, pcov = curve_fit(bases, phs, prot,p0=[10,1])
            perr = np.sqrt(np.diag(pcov))
	    pka = popt[0]
            errpka = perr[0]
            n = popt[1]
            errn = perr[1]
        except RuntimeError:
            pass
    return [pka,errpka,n,errn]
