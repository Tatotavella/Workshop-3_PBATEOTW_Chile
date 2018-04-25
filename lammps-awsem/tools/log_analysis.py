# -⁻- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from functions import *

f = open('asd','r')
next(f)
E_electro = []
for line in f:
	inter = [x for x in line.split('\t')]
	V = inter[8]
	E_electro.append(float(V))
plt.ylabel('Electrostatic Energy')
plt.xlabel('Monte Carlo Step')
plt.plot(E_electro,'b*')
plt.show()

descorr = []
for e in range(len(E_electro)):
	if(e%100 == 0):
		descorr.append(E_electro[e])
plt.plot(descorr,'*')
plt.show()

taus = range(1,500)
corr = []
for tau in taus:
	asd = autocorr(E_electro,tau)
	corr.append(asd)
plt.plot(taus,corr,'r*')
plt.show()
