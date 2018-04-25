import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from functions import *
import sys

if len(sys.argv)<2:
	sys.exit("Error ingresar directorio con las corridas a todos los pHs")
else:
	data_dir = sys.argv[1]

#Making of ionizable residue list
#data_dir = os.path.dirname(__file__) #<-- Absolute directory
rel_path = "/../files/MC_params/MC.input.bk"
#dire = os.path.join(data_dir, rel_path)
dire = data_dir + rel_path
f = open(dire,'r')

#Skip first parameters
for i in range(5):
	next(f)

resList = []
resLett = []

for line in f:
	inter = [x for x in line.split(' ')]
	resList.append(inter[0])
	resLett.append(inter[1])

f.close()

print('resList Made')

totalSteps = 100000
meanInit = 500
decorrStep = 50

dataPoints = (totalSteps - meanInit)/decorrStep

#print('Data points per res: '+str(dataPoints))


pHs = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']
phsVal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
#pHs = ['1','2','3','4']
#phsVal = [1,2,3,4]
deprs = []

for ph in pHs:
	#MC.state file
	outDepr = {}
	rel_path = "/"+ph+"/MC_result/MC.state"
	stateDirec = data_dir + rel_path
	outDepr = deproto(stateDirec,meanInit,resList,decorrStep)
	deprs.append(outDepr)

print('states Analyzed')

#Write data in a file
rel_path = "/titrdata.txt"
director = data_dir + rel_path
g = open(director,'w')
pkas = []
g.write('{:<4s}'.format("Res")+"\t")
for pH in phsVal:
	g.write('{:.4f}'.format(pH)+"\t")
g.write("\n")
for idx,r in enumerate(resList):
	values = []
	for dictio in deprs:
		values.append(dictio[r][0])
	#------------
	#Write data
	g.write('{:<4d}'.format(int(r)+1)+"\t")
	for v in values:
		g.write('{:.5f}'.format(v)+"\t")
	g.write("\n")
	#---------------
	result = fitHenHass(phsVal,values,resLett[idx])
	pkas.append(result)
g.close()
plt.show()
print('pKas obtained')

for idx,r in enumerate(resList):
	print('Res: '+str(int(r)+1)+' , pKa: '+str(pkas[idx]))

'''
#BBL
expRes = ['4','16','17','20','36','37','39','41']
expPkas = [3.9,4.5,6.5,3.7,3.7,3.2,4.5,5.4]
expConte = [3.7,3.7,6.7,3.5,3.8,3.1,3.6,6.0]
'''
print('HEWL comparison')
#HEWL
expRes = ['7','15','18','35','48','52','66','87','101','119']
expPkas = [2.6,5.5,2.8,6.1,1.4,3.6,1.2,2.2,4.5,3.5]
expConte = [3.2,5.1,2.3,3.2,3.5,3.0,3.1,3.2,3.0,3.1]


x=[] #For linear fitting
y=[]
for i,pka in enumerate(pkas):
	for j,r in enumerate(expPkas):
		res = str(int(resList[i])+1)
		if(res == expRes[j] and pka > 0):
			print(resList[i])
			x.append(r)
			y.append(pka)
			plt.scatter(r,pka,label='Res: '+res)

xmin=1
xmax=7
ymin=1
ymax=7
plt.plot(expPkas,expConte,'g*')
plt.plot(range(8),range(8))
plt.xlim([xmin,xmax])
plt.ylim([ymin,ymax])
plt.xlabel('Experimental pKa')
plt.ylabel('Simulated pKa')
plt.legend()
plt.show()
