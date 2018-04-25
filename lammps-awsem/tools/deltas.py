import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

ph = 1
if len(sys.argv)>1:
	ph = sys.argv[2]

data_dir = os.path.dirname(__file__) #<-- Absolute directory
rel_path = "../"+ph+"/MC_result/MC.state"
dire = os.path.join(data_dir, rel_path)
g = open(dire,'r')

res = []
data = {}

for line in g:
	inter = [x for x in line.split('\t')]
	for r in inter[1:len(inter)-1]:
		res.append(r)
		data.update({r:[[],[],[]]}) #D_ph , D_elec, D_self
	break

g.close()

data_dir = os.path.dirname(__file__) #<-- Absolute directory
rel_path = "../"+ph+"/MC_result/MC.log"
dire = os.path.join(data_dir, rel_path)
f = open(dire,'r')

next(f)#Jump header

for line in f:
	inter = [x for x in line.split('\t')]
	aa = inter[1]
	lista = data[aa]
	lista[0].append(float(inter[5]))
	lista[1].append(float(inter[6]))
	lista[2].append(float(inter[7]))
	
		
f.close()

if len(sys.argv)>1:
	resid = sys.argv[1]
	for idx,value in enumerate(res):
		if value==resid:
			residx=idx
			break
	plt.plot(data[res[residx]][0],'bo',label=r'$\Delta \ E_{pH}$')
	plt.plot(data[res[residx]][1],'ro',label=r'$\Delta \ E_{elec}$')
	plt.plot(data[res[residx]][2],'go',label=r'$\Delta \ E_{self}$')
	plt.xlabel('Step',fontsize=15)
	plt.ylabel(r'$\Delta \ E$',fontsize=15)
	plt.title('Residue: '+resid)
	plt.legend(prop={'size':12})
	plt.show()

else:
	plt.plot(data[res[0]][0],'bo',label='D_pH')
	plt.plot(data[res[0]][1],'ro',label='D_elec')
	plt.plot(data[res[0]][2],'go',label='D_self')
	plt.xlabel('Step',fontsize=15)
	plt.ylabel(r'$\Delta \ E$',fontsize=15)
	plt.title('Residue: '+res[0])
	plt.legend()
	plt.show()



