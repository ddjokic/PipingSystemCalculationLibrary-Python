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
'''
import numpy as np
import hydrobb as bb
import matplotlib.pyplot as plt

#input pipe lines data
# HeadlossCoef = A and B coefs in Headloss=A*FLow**2+B
# ReVelCoef = ARe and AVel coef in: Reynolds=ARe*Flow and Velocity=AVel*Flow
inpfilename=raw_input("Input Piping Filename: ")
HeadlossCoef=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=1, usecols=(1,2), unpack=False, ndmin=0)
ReVelCoef=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=1, usecols=(3,4), unpack=False, ndmin=0)
stat=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=1, usecols=(6, 7), unpack=False, ndmin=0)
pump_fn = raw_input ("Input Pumps Filename: ")
pumpCoeff = np.loadtxt(pump_fn, dtype=float, comments="#", delimiter=',', converters=None, skiprows=1, usecols=(1,2), unpack=False, ndmin=0)

case = raw_input ("Enter Case identifier - exapmple: pipe276 closed: ")
outfilename=raw_input("Output Filename: ")
ofn=outfilename+".csv"


# pipes block:
# creating empty arrays to store pipes data
AH1=[]
BH1=[]
ARe1=[]
Avel1=[]
status = []
statReVel = []
AH=[]
BH=[]
ARe=[]
Avel=[]
npt=len(HeadlossCoef)  # total number of pipelines in system

# store pipes input data in python arrays
for element in range (0, npt):
	status.append (stat[element, 0])
	statReVel.append(stat[element, 1])
	AH1.append(HeadlossCoef[element, 0])
	BH1.append(HeadlossCoef[element,1])
	ARe1.append(ReVelCoef[element,0])
	Avel1.append(ReVelCoef[element,1])
	
	# pipe is open (status=1) or closed (status=0):
	
	AH.append (AH1[element]*status[element])
	BH.append (BH1[element]*status[element])
	ARe.append (ARe1[element]*statReVel[element])
	Avel.append (Avel1[element]*statReVel[element])
	# calculating A & B coeffs for pipe system - pipes in serial connection
	AHpl = sum(AH)
	BHpl = sum(BH)
# end pipe block

#pumps block:
# creating empty arrays to store pumps data

AP=[]
BP=[]
Err = []
pnt = len(pumpCoeff)
Flowres=[]
Lossres=[]


# creating empty array to store WP results
Working_point = []

# preparing output file - headders
fn=open(ofn, "a")
fn.write("\n")
fn.write("Case: " +case)
fn.write ("\n")
fn.write ("Working Points of the pumps: ")
fn.write ("\n")
fn.write("Pump ID, Flow[cum/h], Headloss[m], Error")
fn.write("\n")
fn.close()

# store pump data in python arrays
for pump in range (0,pnt):
	AP.append(pumpCoeff[pump,0])
	BP.append(pumpCoeff[pump,1])
	
# end pump block
	
	# calculating system curve and pump curve intersection - working point
	wp=bb.curve_intersection(AP[pump], BP[pump], AHpl, BHpl)
	Working_point.append(wp)
	
	Flowres.append(wp[0])
	Lossres.append(wp[1])
	Err.append(wp[2])
	
	#setting boundaries for graph
	step_bound = Flowres[pump]/3
	low_bound = int(Flowres[pump]-step_bound)
	high_bound = int(Flowres[pump]+step_bound)
	
	
	#constructing graphs:
	out_fn = case+"Pump"+str(pump)+".png"
	Q=np.linspace(low_bound, high_bound)
	# H,Re,Vel=AH*Q**2+BH, ARe*Q, AVel*Q
	Pump, Pipe = AP[pump]*Q**2+BP[pump], AHpl*Q**2+BHpl
	
	plt.plot(Q,Pump, color="red")
	plt.plot(Q, Pipe, color = "green")
	plt.title("Pump: "+str(pump)+", Case: "+ case)
	plt.xlabel("Flow [cum/hr]")
	plt.ylabel("Headloss [m]")
	plt.grid(True)
	plt.savefig(out_fn)
	plt.close()
	
#writing working point into file
fn=open(ofn, "a")
for pump in range(0, pnt):
	fn.write(str(pump))
	fn.write(",")
	fn.write(str(Flowres[pump]))
	fn.write(",")
	fn.write(str(Lossres[pump]))
	fn.write(",")
	fn.write(str(Err[pump]))
	fn.write("\n")
	
for pump in range(0,pnt):
	fn.write("\n")
	fn.write("Pipe data for Pump-")
	fn.write(str(pump))
	fn.write("\n")
	fn.write("PipeLoss[m], Reynolds[-], Velocity[m/s]")
	
	QP=Flowres[pump]
	
	for element in range (0, npt):
		#print(pipe)#
		PipeLoss=AH[element]*QP**2+BH[element]
		PipeRe=ARe[element]*QP
		PipeVel=Avel[element]*QP
		
		
		fn.write("\n")
		fn.write(str(PipeLoss))
		fn.write(",")
		fn.write(str(PipeRe))
		fn.write(",")
		fn.write(str(PipeVel))
	
fn.close()
print("DONE!")
	

	
	


	