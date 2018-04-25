# -⁻- coding: UTF-8 -*-
######################################################################
# Script for pKa calculation of ionizable residues. Path to directory
# with runs for every pH must be given and a separate files directory
# with the main data of the system. An output file is generated called
# titrdata.txt with protonated fraction per pH and residue pKa and n
# value with their corresponding estimation error.
#  Inputs:
#  - Path to directory with pH runs data and main files.
#  Outputs:
#  - File titrdata.txt with analysis of pKa, n value and protonated
#    fraction.
######################################################################
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


# Deprotonated fraction for every pH and residue
dcr_step = 70 # Decorrelation step
init_step = 70 # Starting point of data analysis


deprs = []

for ph in pHs:
	#MC.state file
	outDepr = {}
	rel_path = "/"+ph+"/MC_result/MC.state"
	stateDirec = data_dir + rel_path
	outDepr, totalStates = deproto(stateDirec,init_step,res_list,dcr_step)
	deprs.append(outDepr)

print('MC.state files analyzed with '+str(int(totalStates))+' data points per residue')

#Write data in a file

rel_path = "/titrdata.txt"
direc_titr = data_dir + rel_path
g = open(direc_titr,'w')

# File Header
g.write('{:<4s}'.format("Res")+"\t")
g.write('{:<4s}'.format("Let")+"\t")
for pH in phsVal:
	g.write('{:.4f}'.format(pH)+"\t")
g.write('{:<4s}'.format("pKa")+"\t")
g.write('{:<4s}'.format("errpKa")+"\t")
g.write('{:<4s}'.format("n")+"\t")
g.write('{:<4s}'.format("errn")+"\t")
g.write("\n")

# File Data
pkas = []
for idx,r in enumerate(res_list):
	values = []
	for dictio in deprs:
		values.append(dictio[r][0])
        pka, errpka, n,errn = fitHenHass(phsVal,values,res_lett[idx])
	pkas.append(pka)
	
	#Write data
	g.write('{:<4d}'.format(int(r)+1)+"\t")
        g.write('{:<4s}'.format(res_lett[idx])+"\t")
	for v in values:
		g.write('{:.5f}'.format(v)+"\t")
                
        g.write('{:.4f}'.format(pka)+"\t")
        g.write('{:.5f}'.format(errpka)+"\t")
        g.write('{:.5f}'.format(n)+"\t")
        g.write('{:.5f}'.format(errn)+"\t")
	g.write("\n")
g.close()
print('pKas obtained')
print('File titrdata.txt generated in '+ direc_titr)

'''
for idx,r in enumerate(res_list):
	print('Res: '+str(int(r)+1)+' , pKa: '+str(pkas[idx]))
'''
'''
#BBL
expRes = ['4','16','17','20','36','37','39','41']
expPkas = [3.9,4.5,6.5,3.7,3.7,3.2,4.5,5.4]
expConte = [3.7,3.7,6.7,3.5,3.8,3.1,3.6,6.0]
'''
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
'''
