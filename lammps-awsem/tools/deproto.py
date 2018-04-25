import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data_dir = os.path.dirname(__file__) #<-- Absolute directory
rel_path = "MC.state"
dire = os.path.join(data_dir, rel_path)
g = open(dire,'r')

res = []
data = {}

for line in g:
	inter = [x for x in line.split('\t')]
	for r in inter[1:len(inter)-1]:
		res.append(r)
		data.update({r:[]}) #Charge over steps
	break

for line in g:
	inter = [x for x in line.split('\t')]
	step = inter[0]
	for idx,c in enumerate(inter[1:len(inter)-1]):
		data[res[idx]].append(float(c))
		
		
g.close()

plt.plot(data[res[2]],'bo')
plt.show()



