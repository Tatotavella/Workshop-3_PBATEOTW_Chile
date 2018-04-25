import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from functions import *
import sys

if len(sys.argv)<5:
	sys.exit("Error ingresar directorio con las corridas a todos los pHs y las k_electro")
else:
	data_dir = sys.argv[1]
	kpp = float(sys.argv[2])
	kmm = float(sys.argv[3])
	kpm = float(sys.argv[4])


direc = data_dir + '/titrdata.txt'
'''
#BBL
expRes = ['4','16','17','20','36','37','39','41']
expPkas = [3.9,4.5,6.5,3.7,3.7,3.2,4.5,5.4]
'''
#HEWL
expRes = ['7','15','18','35','48','52','66','87','101','119']
expPkas=[2.6,5.5,2.8,6.1,1.4,3.6,1.2,2.2,4.5,3.5]

expCurvas = []
phsVal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
for idx,r in enumerate(expRes):
	if r=='15':
		aux=[]
		pka=expPkas[idx]
		for p in phsVal:
			aux.append(bases(p,pka,1))
		expCurvas.append(aux)
	else:
		aux=[]
		pka=expPkas[idx]
		for p in phsVal:
			aux.append(acidos(p,pka,1))
		expCurvas.append(aux)

#Read titration simulation data
resList=[]
resTitr=[]
f = open(direc,'r')
next(f)
for line in f:
	inter = [x for x in line.split('\t')]
	resList.append(inter[0])
	titration=inter[1:len(inter)-1]
	resTitr.append(titration)
f.close()
#Select only the ones with experimental data
simCurvas=[]
for j,expr in enumerate(expRes):
	for i,r in enumerate(resList):
		if int(r)==int(expr):
			simCurvas.append(resTitr[i])

#RMSD for each residue
'''
for r in expRes:
	sys.stdout.write('{:<4s}\t'.format(r))
sys.stdout.write('{:<4s}\t'.format("mean"))
sys.stdout.write("\n")
'''
sys.stdout.write('{:.4f}\t'.format(kpp))
sys.stdout.write('{:.4f}\t'.format(kmm))
sys.stdout.write('{:.4f}\t'.format(kpm))

meanrmsd=0
for idx,curva in enumerate(expCurvas):
	rmsd=0
	for j,val in enumerate(curva):
		rmsd+=(val-float(simCurvas[idx][j]))**2
	rmsd=rmsd/len(phsVal)
	rmsd=np.sqrt(rmsd)
	meanrmsd+=rmsd
	#print(expRes[idx],rmsd)	
	sys.stdout.write('{:.4f}\t'.format(rmsd))	

	
meanrmsd=meanrmsd/len(expRes)		
sys.stdout.write('{:.4f}\t'.format(meanrmsd))
sys.stdout.write("\n")
#print("\n")


for i,c in enumerate(expCurvas):
	p = plt.plot(phsVal,c,label=expRes[i])
	col = p[0].get_color()
	plt.plot(phsVal,simCurvas[i],col,linestyle='--')


plt.legend()
plt.show()
		


		
