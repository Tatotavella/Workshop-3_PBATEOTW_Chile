# -⁻- coding: UTF-8 -*-
######################################################################
#
#  Inputs:
#  -
#  Outputs:
#  -
######################################################################
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#from functions import *
import sys
import StringIO

acid_list = ['D', 'E']
base_list = ['K', 'R', 'H']

if len(sys.argv)<2:
	sys.exit("Error. Enter file.seq to read sequence")
else:
	seq_file = sys.argv[1]

# Get residues as a list in seq variable
f = open(seq_file,'r')
seq = f.read()
seq = list(seq)
seq = seq[:-1]

# MC.input.bk and charge_on_residue.dat
output = StringIO.StringIO()
dat_out = StringIO.StringIO()
buffer_out = StringIO.StringIO()
chrg_on_res_out = StringIO.StringIO()
output.write('freqMC\n')
output.write('freqOUT\n')
output.write('TEMP\n')
output.write('pH\n')
tot_res_chrgd = 0
for idx,res in enumerate(seq):
    if res in acid_list:
        chrg = -1 * np.random.randint(2)
        buffer_out.write(str(idx)+' '+str(res)+' '+str(chrg)+'\n')
        chrg_on_res_out.write(str(idx)+' '+str(chrg)+'\n')
        tot_res_chrgd += 1
    elif res in base_list:
        chrg = 1 * np.random.randint(2)
        buffer_out.write(str(idx)+' '+str(res)+' '+str(chrg)+'\n')
        chrg_on_res_out.write(str(idx)+' '+str(chrg)+'\n')
        tot_res_chrgd += 1
output.write(str(tot_res_chrgd + 2)+'\n') # Two more for termials
content = buffer_out.getvalue()
output.write(content)
# Terminals
output.write(str(idx+1)+' '+'N'+' '+str(0)+'\n')
output.write(str(idx+2)+' '+'C'+' '+str(0)+'\n')

dat_out.write(str(tot_res_chrgd)+'\n')
dat_cont = chrg_on_res_out.getvalue()
dat_out.write(dat_cont)
# Terminals
dat_out.write(str(idx+1)+' '+str(0)+'\n')
dat_out.write(str(idx+2)+' '+str(0)+'\n')

write_input = output.getvalue()
write_charge = dat_out.getvalue()

mcinput = open('MC.input.bk','w')
charge_on = open('charge_on_residues.dat','w')

mcinput.write(write_input)
charge_on.write(write_charge)
