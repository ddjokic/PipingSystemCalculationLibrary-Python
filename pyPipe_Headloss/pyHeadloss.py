#!/usr/bin/env python

''' 
Copyright (c) 2013 D. Djokic <deki.djokic at gmail.com>
This code is released under the [GPL], version 2 or later

Calculates local and friction losses, using Serghides solution of Darcy-Weisbach equation. 
Pipe characteristics are given in "csv" file - see template file. Results are witten in 
inputfilename.out file and set of three graphs for each pipe - Headloss=f(Flow), Reynolds=f(flow)
and Velocity=f(flow).
In result file coefficients AH, BH, ARe and AVelo of following equations are written for each pipe:
1. Headloss=AH*Q**2+BH
2. Reynolds=ARe*Q
3. Velocity=AVelo*Q
4. Total local losses

Pipe  tags should be integers, starting with zero ("0") - 0, 1, 2, 3....
Requirements:
numpy
matplotlib
DWheadlos.py - put in python path
string

Local loss factors (k-factors) are given in file "k_factors.csv", which should be located in
same folder as this script. If you do not like predefined factors, feel free to change them, 
maintaining structure of the file.

k-factor for "user defined" loss is predefined as "1" - input number of user defined local losses
as you like - e.g 7.965, 0.222, 0,... It was done to avoid 0*0 operation, whithout "if-loop".
'''
import numpy as np
#from scipy.optimize import fsolve
from matplotlib import pyplot as plt
import DWheadloss as dw
import string

# reading input from csv file:
inpfilename=raw_input("Input Filename: ")
viscosity=dw.get_float("Input kinematic viscosity of fluid in cSt or '0' for fresh water@20degC(1.002): ", 1.002)
fittings=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26), unpack=False, ndmin=0)
chars=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(1,2,3,4,5), unpack=False, ndmin=0)
pipes_num=len(fittings)

# results in csv file
file_name=string.split(inpfilename, '.')
fname_out=file_name[0]+'.out'	
dw.write_res_head_csv(fname_out)
fn=open(fname_out, "a")
print("--")

# read local loss "k"-factors from "k_factors.csv" file, which must be in same folder as main script
k=np.loadtxt("k_factors.csv", dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(None), unpack=False, ndmin=0)

# calculate local loss in reducer and enlargement

for pipes in range(0, pipes_num):
# calculating local losses
	loss=fittings[pipes]
	dims=chars[pipes]
	
	# local losses due to elbows
	elbows=dw.elbow_loss(float(k[0]),float(loss[0]), float(k[1]),loss[1], float(k[2]),float(loss[2]), k[3],loss[3], float(k[4]),loss[4])
	
	# local losses in valves
	valves=dw.valve_loss(k[5],loss[5], k[6],loss[6], k[7],loss[7], k[8],loss[8], k[9],loss[9], k[10],loss[10], k[11],loss[11], k[12],loss[12])
	
	# local losses due to flow through tees - header and branch
	tee=dw.tee_loss(k[13],loss[13], k[14],loss[14])
	
	#local losses in reducer/contraction
	reducer=dw.red_loss(dims[0], dims[2], loss[18], loss[19])
	
	#miscellaneous local losses
	misc=dw.misc_loss(k[16],loss[16], k[15],loss[15], k[17],loss[17], k[20],loss[20])
	
	#total local losses
	total=dw.tot_loc_loss(elbows, valves, tee, misc, reducer)
	
	#calculating friction loss
	Reynolds=[]
	Velocity=[]
	Headloss=[]
	Flow=[]
	for flow in range (1,30):
		#ff=serghides(PipeID, flow, visco, roughness)
		ff=dw.serghides(float(dims[0]), float(flow), float(viscosity), float(dims[1]))
		
		frict=float(ff[0])
		rey=float(ff[1])
		velo=float(ff[2])
		Reynolds.append(rey)
		Velocity.append(velo)
		Flow.append(flow)
		
		hl=dw.headloss(float(frict), float(dims[3]), float(dims[0]), float(total), float(flow), float(dims[4]))
		Headloss.append(hl)
	headloss_a=np.array(Headloss)
	reynolds_a=np.array(Reynolds)
	velocity_a=np.array(Velocity)
	flow_a=np.array(Flow)
	
	headloss_f=np.polyfit(flow_a,headloss_a,2)
	print("----")
	
	reynolds_f=np.polyfit(flow_a, reynolds_a,1)
	print("--------")
	
	velocity_f=np.polyfit(flow_a, velocity_a,1)
	print("---------------")
	
	#graphs (ptag, AH, BH, ARe, AVel)
	pipetag=str(pipes)
	dw.graphs(pipetag, float(headloss_f[0]), float(headloss_f[2]), float(reynolds_f[0]), float(velocity_a[0]))
	print("-------------------")
	
	#writing results to file
	pipetag="Pipe "+ str(pipes)
	dw.write_table6(fn, pipetag, str(headloss_f[0]), str(headloss_f[2]), str(reynolds_f[0]), str(velocity_f[0]), str(total))

fn.close()
print("Job Done!")


	
