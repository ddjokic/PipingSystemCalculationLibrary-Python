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
def par_flow(Flow, A1, B1, A2,B2)-calculates Flow and Headloss through each pipeline in parallel loop for given total Flow which entering loop
'''
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


