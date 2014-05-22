#!/usr/bin/env python
# # Copyright (c) D.Djokic, 2013
# This code is released under GNU General Public Licence, Version 2
# No Warranties, whatsoever!

import numpy as np 
from scipy.optimize import fsolve

''' acronyms used: H=Headloss, expressed in height of liquid column; Q=Flow
	Re = Reynold number; Vel=Velocity of fluid; P(ar)=Parallel; S(er)=Serial
'''

def flow(H,A,B):
# calculates Flow for given Headloss
	return (((abs(H-B))/A)**0.5)
# function call q=flow(h,a,b)

def par_lines(A1, B1,A2, B2):
# calculates result of parallel connected pipes
	head0=max(B1,B2) # eliminating error & sacrifises graph
	QPar=[]
	head=[]
	for headloss in np.arange(head0,70):
		QPar1=abs(flow(headloss, A1,B1)+flow(headloss, A2,B2))
		QPar.append(QPar1)
		head.append(headloss)
	#end of for loop
	p=np.polyfit(QPar, head, 2)
	# result in shape p[0]*Q**2+p[1]*Q+p[2]
	return p[0], p[2]
# function call p=par_lines(a1,b1, a2,b2); H=p[0]*Q**2+p[1] - tested

def ser_lines(A1,B1, A2,B2):
# calculates result of pipes connected in series
	QSer=[]
	HSer=[]
	for flow in np.arange(0,600):
		HSer1=(A1+A2)*flow**2+B1+B2
		QSer.append(flow)
		HSer.append(HSer1)
	#end of for loop
	h=np.polyfit(QSer, HSer, 2)
	return h[0], h[2]
# function call h=ser_lines(a1,b1,a2,b2); H=h[0]*Q**2+h[1] - tested

def eq_pump(APump,BPump,ASuction,BSuction):
# calculates equivalent pump headloss - difference between pump and suction line headloss
# pump coef., for cenrifugal pump, MUST be hegative number
	Qeqp=[]
	Heqp=[]
	for flow in np.arange (0,600):
		Hres=(APump*flow**2+BPump)-((ASuction*flow**2+BSuction))
		Qeqp.append(flow)
		Heqp.append(Hres)
	# end for loop
	eqp=np.polyfit(Qeqp, Heqp, 2)
	return eqp[0], eqp[2]
'''
 if there are more than one pump in the system, and are working simultaneusly, after calculating equivalent pump,
 depending of their configuration, use ser_lines or par_lines or both to combine them in the system
'''
# function call s=eq_pump(a,b1,a2,b2); H=s[0]*Q**2+s[1]

def curve_intersection(APump, BPump, APipe, BPipe):
# calculates intersection between two curves - work point of piping system
# APump and BPump are coefs. of equivalent pump; APump MUST BE NEGATIVE number
	Flow=(abs((BPipe-BPump)/(APump-APipe)))**.5
	HPump=APump*Flow**2+BPump
	Err=HPump-(APipe*Flow**2+BPipe)
	return Flow, HPump, Err
# function call Intersection=curve_intersection(a1,b1,a2,b2); Q=Intersection[0], Headloss=Intersection[1], Error=Intersection[2]

# "decomposition fuctions" - calculating Flow and Headloss in component pipes
# Re-Reynolds number related, Vel - velocity related

def decomp_serial(Flow, AS1,BS1, AS2,BS2):
# calculates Flow and Headloss in individual pipes in serial connection
	HS1=AS1*Flow**2+BS1
	HS2=AS2*Flow**2+BS2
	return Flow,HS1,HS2
# function call cal=decomp_serial(Q,a1,b1,a2,b2, a3,b3,a4,b4, a5,a6); Flow=cal[0], HS1=cal[1], HS2=cal[2];

def decomp_parallel(FlowQ,APRes,BPRes, AP1,BP1, AP2,BP2):
# calculates Flow and Headloss in individual pipes in parallel connection
# APRes, BPRes - coeff of curve to be decomposed
	HPar=APRes*FlowQ**2+BPRes
	QP1=flow(HPar, AP1,BP1)
	QP2=FlowQ-QP1 
	return QP1,QP2,HPar
# function call par=decomp_parallel(H, AP1,BP1, AP2,BP2); QP1=par[0], QP2=par[1], Headloss=par[2],

def par_flow(Flow, A1, B1, A2,B2):
# calculates Flow and Headloss through each pipeline in parallel loop for given total Flow which entering loop
# recomended usage!
	def equations(qp):
		Q1,Q2,H1,H2=qp
		return(A1*Q1**2+B1-H1, A2*Q2**2+B2-H2, Flow-Q1-Q2, H1-H2)  
	Q1,Q2,H1,H2=fsolve(equations,(Flow/4,Flow/4,0,0))
	return Q1,H1, Q2,H2

def reynolds(flow, ARe):
# calculates Reynolds number in individual pipe as function of flow
	Reynolds=ARe*Q
	return Reynolds
# function call rey=reynolds(Q,a); 

def velocity(flow, Avel):
# calculates fluid velocity in individual pipe as function of flow
	Vel=Avel*flow
	return Vel
# function call vel=velocity(Q,a);

def write_table5 (fn, v1, v2, v3, v4, v5):
# write table in previously opened file in "a" - mode	
	fn.write("\n")
	fn.write(v1)
	fn.write(",")
	fn.write(v2)
	fn.write(",")
	fn.write(v3)
	fn.write(",")
	fn.write(v4)
	fn.write(",")
	fn.write(v5)
	return

def write_res_head_csv(filename):
# write headers to "csv"- file
	fn=open(filename, "a")
	write_table5(fn, "PipeTag", "Flow [cum/h]" ,"Headloss[m]", "Reynolds [-]", "Velocity [m/s]")
	fn.close()
	return
# function call write_res_head_csv(filename_as_String) 

def write_res_num_csv(filename, PipeTag, Flow, Headloss, Reynolds, Velocity):
# write results rounded on 3 decimals to "csv"-file 
	fn=open(filename, "a")
	write_table5(fn, PipeTag, str(round(Flow,3)), str(round(Headloss,3)), str(round(Reynolds,3)), str(round(Velocity,3)))
	fn.close()
	return
# function call: filename and pipetag must be a string

# subloop routines
def sub_loop(AP1,BP1, AP2,BP2, AS1,BS1):
# calculates resultant of two parallel and one serial pipes - "fork" sub-loop
	if AP1==0 and BP1==0:
		res=ser_lines(AP2,BP2, AS1, BS1)
	elif AP2==0 and BP2==0:
		res=ser_lines(AP1,BP1,AS1,BS1)
	else:
		par=par_lines(AP1,BP1, AP2,BP2)
		res=ser_lines(par[0],par[1], AS1,BS1)
	# returns A and B coef. of resultant pipe	
	return res[0], res[1]

def res_sub_loop (Flow, ARes, BRes, AP1,BP1, AP2,BP2, AS,BS):
# calculates Flow and Headloss in component pipes of "fork" sub-loop
	par_tot=decomp_serial(Flow, ARes, BRes, AS,BS)
	#returns Flow, HRes, HSer
	loop_res=par_flow(Flow, AP1,BP1, AP2,BP2)
	#returns QP1,HP1,QP2,HP2
	return par_tot[0], par_tot[2], loop_res[0], loop_res[1], loop_res[2], loop_res[3]
	
