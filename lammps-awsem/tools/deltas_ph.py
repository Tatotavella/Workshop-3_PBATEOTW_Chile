# -⁻- coding: UTF-8 -*-
#######################################################################
# 
#  Inputs:
#  - Path to directory with pH runs data.
#  Outputs:
#  - 
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

# Residue list from MC.input.bk
dire_backup = data_dir + '/files/MC_params/MC.input.bk'
file_backup = open(dire_backup, 'r')
for i in range(5):
	next(file_backup)
res_list = [] # Indexes
res_lett = [] # Types
for line in file_backup:
	inter = [x for x in line.split(' ')]
	res_list.append(inter[0])
	res_lett.append(inter[1])
file_backup.close()




#Data saving place. Lists for every mean at each pH
means = {}
for r in res_list:
    means.update({r:[[],[],[]]}) #meanpH , meanElec, meanSelf


for ph in pHs:
	# Reset values
	data = {}
	for r in res_list:
		data.update({r:[[],[],[]]}) #D_ph , D_elec, D_self

	#Logs analisys
	rel_path = "/"+ph+"/MC_result/MC.log"
	logDirec = data_dir + rel_path
	h = open(logDirec,'r')
	# Jump header
	next(h)
	# Fill values in lists
	for line in h:
		inter = [x for x in line.split('\t')]
		aa = str(int(inter[1]) - 1)
		lista = data[aa]
		#D_ph , D_elec, D_self | 0 , 1 , 2
		lista[0].append(float(inter[5]))
		lista[1].append(float(inter[6]))
		lista[2].append(float(inter[7]))
	h.close()
	# Mean values
	for r in res_list[:-2]:
		mpH = 0
		mElec = 0
		mSelf = 0

		lista = data[r]
		# pH list
		for v in lista[0]:
			mpH+=v
		mpH=mpH/(len(lista[0]))
		# Elec list 
		for v in lista[1]:
			mElec+=v
		mElec=mElec/(len(lista[1]))
		# Self list
		for v in lista[2]:
			mSelf+=v
		mSelf=mSelf/(len(lista[2]))
		#Save
		means[r][0].append(mpH)
		means[r][1].append(mElec)
		means[r][2].append(mSelf)


for r in res_list:
	dph = np.asarray(means[r][0])
	dele = np.asarray(means[r][1])
	dself = np.asarray(means[r][2])
	plt.figure(1)
	plt.plot(phsVal,dph,'bo',label='Res: '+r+' , '+'<DeltapH>')
	plt.legend()

	plt.figure(2)
	plt.plot(phsVal,dele,'ro',label='Res: '+r+' , '+'<DeltaElec>')
	plt.plot(phsVal,dself,'go',label='Res: '+r+' , '+'<DeltaSelf>')
	plt.legend()

	plt.show()

	'''
	curva = dself/np.max(dself)

	dg = dph/curva + dele/(curva*R*T) + dself/(curva*R*T)
	dg_b = dph/(curva*R*T) + dele/(curva*R*T) + 1.5*dself/(curva*R*T)
	henhas = []
	henhas_b = []
	for idx,g in enumerate(dg):
		x = np.exp(-g/(R*T))
		y = x/(1+x)
		henhas.append(y)

		x_b = np.exp(-dg_b[idx]/(R*T))
		y_b = x_b/(1+x_b)
		henhas_b.append(y_b)
	'''
	'''
	for idx,expr in enumerate(expRes):
		if r==expr:
		    if r=='15':
		        print(r)
		        xteo = np.linspace(1,14,100)
		        teorica = []
		        teorica = bases(xteo,expPkas[idx],1.0)
		        plt.plot(xteo,teorica)
		    else:
		        xteo = np.linspace(1,14,100)
		        teorica = acidos(xteo,expPkas[idx],1.0)
		        plt.plot(xteo,teorica)


	plt.figure(1)
	plt.plot(phsVal,dph,'bo',label='Res: '+r+' , '+'<DeltapH>')
	plt.legend()

	plt.figure(2)
	plt.plot(phsVal,dele,'ro',label='Res: '+r+' , '+'<DeltaElec>')
	plt.plot(phsVal,dself,'go',label='Res: '+r+' , '+'<DeltaSelf>')
	plt.legend()
	plt.figure(3)

	plt.plot(phsVal,henhas,'go',label='Res: '+r+' , '+'HenHas')
	plt.plot(phsVal,henhas_b,'b*',label='Res: '+r+' , '+'HenHas_b algo*self')
	plt.legend()

	plt.show()
	'''






















