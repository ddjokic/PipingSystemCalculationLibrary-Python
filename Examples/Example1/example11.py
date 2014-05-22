#!/usr/bin/env python
# calculation file - your calculation code coming below line approx. 45
# Copyright (c) D.Djokic, 2013
# This code is released under GNU General Public Licence, Version 2
# No Warranties, whatsoever

''' List of functions in "Building Blocks file":
flow(H,A,B) - calculates flow for given Headloss
par_lines(A1, B1,A2, B2) - calculates resultant of parallel connected pipes
ser_lines(A1,B1, A2,B2) - calculates resultant of pipes connected in series
eq_pump (APump,BPump,ASuction,BSuction) - calculates curve of equivalent pump - pump curve minus suction pipe curve
curve_intersection(APump, BPump, APipe, BPipe) - calcultes intersection of two curves - used system curve 
												and pump curve, result is working point of the system
												Q=Intersection[0], Headloss=Intersection[1], Error=Intersection[2]
decomp_serial(Flow, AS1,BS1, AS2,BS2) - calculates Headloss in each of pipes in serial connestion, based on given Headloss
decomp_parallel(Headloss, AP1,BP1, AP2,BP2) - calculates Flow in each of pipes in serial connestion, based on given Headloss
Reynolds(flow, ARe) - calculates Reynolds number for a pipe, and given flow
velocity(flow, Avel) - calculates Velocity of fluid in pipe for given flow
write_res_head_csv(filename) - writes headers of result table in specified file
write_res_num_csv(filename, PipeTag, Flow, Headloss, Reynolds, Velocity)- writes results table to file - one pipe per row
par_flow(Flow, A1, B1, A2,B2)-calculates Flow and Headloss through each pipeline in parallel loop for given total Flow which entering loop
'''
## Note: difference between example1.py and example11.py is in line 86, where par_flow() is called in this script, while in example1.py is called decomp_parallel()
## Results are not the same. Function par_flow() gives correct flow and headloss
import numpy as np
import hydrobb as bb
# HeadlossCoef = A and B coefs in Headloss=A*FLow**2+B
# ReVelCoef = ARe and AVel coef in: Reynolds=ARe*Flow and Velocity=AVel*Flow
inpfilename=raw_input("Input Filename: ")
HeadlossCoef=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=1, usecols=(1,2), unpack=False, ndmin=0)
ReVelCoef=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=1, usecols=(3,4), unpack=False, ndmin=0)
outfilename=raw_input("Output Filename: ")

# creating empty arrays to store data
AH=[]
BH=[]
ARe=[]
Avel=[]
npt=len(HeadlossCoef)  # total number of pipelines in system

# store input data in python arrays
for element in range (0, npt):
	AH.append(HeadlossCoef[element, 0])
	BH.append(HeadlossCoef[element,1])
	ARe.append(ReVelCoef[element,0])
	Avel.append(ReVelCoef[element,1])

# your code/functions calls go below this line

# calculating paralel comp. line
res_par0_1=bb.par_lines(AH[0],BH[0],AH[1],BH[1])
# coefs of paralel comp. curve
AH0_1=res_par0_1[0]
BH0_1=res_par0_1[1]

# calculating serial comp.lines
res_ser2_3=bb.ser_lines(AH[2],BH[2], AH[3],BH[3])
# coef of serial lines
AH2_3=res_ser2_3[0]
BH2_3=res_ser2_3[1]

# calculating whole system curve
total_res=bb.ser_lines(AH0_1,BH0_1, AH2_3,BH2_3)
AHtot=total_res[0]
BHtot=total_res[1]

#calculating working point of the system - pump is curve 4
WP=bb.curve_intersection(AH[4],BH[4], AHtot,BHtot)
QSys=WP[0]
HSys=WP[1]
print(WP)
#rolling back!
# calculating headlosses in loop total_ser Flow=cal[0], HS1=cal[1], HS2=cal[2]
res_tot_ser=bb.decomp_serial(QSys, AH0_1,BH0_1, AH2_3,BH2_3)
Qres_tot=res_tot_ser[0]
H0_1=res_tot_ser[1]
H2_3=res_tot_ser[2]
Q=[]
H=[]
#calculating headlosses in loop res_ser2_3
loop_ser2_3=bb.decomp_serial(Qres_tot,AH[2],BH[2], AH[3],BH[3])
Q.append(loop_ser2_3[0])
H.append(loop_ser2_3[1])
Q.append(loop_ser2_3[0])
H.append(loop_ser2_3[2])
#calculating flows in loop res_par0_1
#loop_par0_1=bb.decomp_parallel(H0_1, AH[0],BH[0], AH[1],BH[1])
loop_par0_1=bb.par_flow(loop_ser2_3[0], AH[0],BH[0], AH[1],BH[1])
Q.append(loop_par0_1[0])
H.append(loop_par0_1[1])
Q.append(loop_par0_1[2])
H.append(loop_par0_1[3])
# writting results

bb.write_res_head_csv(outfilename)
for i in range(0,4):
	bb.write_res_num_csv(outfilename, str(i), Q[i], H[i], 0, 0)

