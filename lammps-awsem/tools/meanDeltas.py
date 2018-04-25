import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from functions import *

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
	resList.append(str(int(inter[0])+1))
	resLett.append(inter[1])

f.close()

print('resList Made')

pHs = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']
phsVal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

#Data saving place
means = {}
for r in resList:
    means.update({r:[[],[],[]]}) #meanpH , meanElec, meanSelf

for ph in pHs:
    #MC.state file
    outDepr = {}
    rel_path = "/"+ph+"/MC_result/MC.state"
    stateDirec = data_dir + rel_path
    g = open(stateDirec,'r')

    res = []
    data = {}

    for line in g:
    	inter = [x for x in line.split('\t')]
    	for r in inter[1:len(inter)-1]:
    		res.append(r)
    		data.update({r:[[],[],[]]}) #D_ph , D_elec, D_self
    	break

    g.close()

    #Logs analisys
    rel_path = "/"+ph+"/MC_result/MC.log"
    logDirec = data_dir + rel_path
    h = open(logDirec,'r')

    next(h)#Jump header


    for line in h:
    	inter = [x for x in line.split('\t')]
        #if inter[2]=='1':
        aa = inter[1]
        lista = data[aa]
        #D_ph , D_elec, D_self ; 0 , 1 , 2
        lista[0].append(float(inter[5]))
        lista[1].append(float(inter[6]))
        lista[2].append(float(inter[7]))
    h.close()



    for r in res:
        mpH = 0
        mElec = 0
        mSelf = 0

        lista = data[r]
        #Lista pH
        for v in lista[0]:
            mpH+=v
        mpH=mpH/(len(lista[0]))
        #Lista Elec
        for v in lista[1]:
            mElec+=v
        mElec=mElec/(len(lista[1]))
        #Lista Self
        for v in lista[2]:
            mSelf+=v
        mSelf=mSelf/(len(lista[2]))
        #Save in list
        means[r][0].append(mpH)
        means[r][1].append(mElec)
        means[r][2].append(mSelf)

print('logs Analyzed')
R = 0.0019872041
T = 300

#HEWL
expRes = ['7','15','18','35','48','52','66','87','101','119']
expPkas = [2.6,5.5,2.8,6.1,1.4,3.6,1.2,2.2,4.5,3.5]
let = ['R','K','D','E','H']
pkas = [12.0,10.6,4.0,4.5,6.3]
kas = [1,13,33,96,97,116]
erres = [5,14,21,45,61,68,73,112,114,125,128]
des = [18,48,52,66,87,101,119]
es = [7,35]
haches = [15]

for r in resList:
    dph = np.asarray(means[r][0])
    dele = np.asarray(means[r][1])
    dself = np.asarray(means[r][2])
    '''
    if int(r) in kas:
        for i,p in enumerate(dph):
            if phsVal[i]>=10.6:
                dph[i]=-1*dph[i]
                dele[i]=-1*dele[i]
                dself[i]=-1*dself[i]
    elif int(r) in erres:
        for i,p in enumerate(dph):
            if phsVal[i]>=12:
                dph[i]=-1*dph[i]
                dele[i]=-1*dele[i]
                dself[i]=-1*dself[i]
    elif int(r) in des:
        for i,p in enumerate(dph):
            if phsVal[i]<=4:
                dph[i]=-1*dph[i]
                dele[i]=-1*dele[i]
                dself[i]=-1*dself[i]
    elif int(r) in es:
        for i,p in enumerate(dph):
            if phsVal[i]<=4.5:
                dph[i]=-1*dph[i]
                dele[i]=-1*dele[i]
                dself[i]=-1*dself[i]
    elif int(r) in haches:
        for i,p in enumerate(dph):
            if phsVal[i]>=6.3:
                dph[i]=-1*dph[i]
                dele[i]=-1*dele[i]
                dself[i]=-1*dself[i]
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

    '''
    plt.figure(1)
    plt.plot(phsVal,dph,'bo',label='Res: '+r+' , '+'<DeltapH>')
    plt.legend()
    '''
    plt.figure(2)
    plt.plot(phsVal,dele,'ro',label='Res: '+r+' , '+'<DeltaElec>')
    plt.plot(phsVal,dself,'go',label='Res: '+r+' , '+'<DeltaSelf>')
    plt.legend()
    plt.figure(3)

    plt.plot(phsVal,henhas,'go',label='Res: '+r+' , '+'HenHas')
    plt.plot(phsVal,henhas_b,'b*',label='Res: '+r+' , '+'HenHas_b algo*self')
    plt.legend()
    '''
    plt.show()











'''
if len(sys.argv)<2:
	sys.exit("Error ingresar directorio con las corridas a todos los pHs")
else:
	data_dir = sys.argv[1]

#Making of ionizable residue list
rel_path = "/../files/MC_params/MC.input.bk"
dire = data_dir + rel_path
f = open(dire,'r')

ph = 1
if len(sys.argv)>1:
	ph = sys.argv[2]

data_dir = os.path.dirname(__file__) #<-- Absolute directory
rel_path = "../"+ph+"/MC_result/MC.state"
dire = os.path.join(data_dir, rel_path)
g = open(dire,'r')

res = []
data = {}
#Dict initialization
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
'''
