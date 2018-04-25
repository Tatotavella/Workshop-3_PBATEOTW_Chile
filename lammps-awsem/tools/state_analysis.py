# -⁻- coding: UTF-8 -*-
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

ph = 1
if len(sys.argv)>1:
	ph = sys.argv[1]

data_dir = os.path.dirname(__file__) #<-- Absolute directory
rel_path = "../"+ph+"/MC_result/MC.state"
dire = os.path.join(data_dir, rel_path)
f = open(dire,'r')
next(f)
Q_total = []
for line in f:
        inter = [x for x in line.split('\t')]
        q = 0.0
	for charge in inter[1:]:
		q += float(charge)
        Q_total.append(q)
plt.xlabel('Monte Carlo Step')
plt.ylabel('Total charge')
plt.plot(Q_total,'b*')
plt.show()
