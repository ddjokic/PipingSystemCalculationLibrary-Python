#!/usr/bin/env python

'''
Copyright (c) 2013 D. Djokic <deki.djokic at gmail.com>
This code is released under the [GPL], version 2 or later

Collection of functions to calculate headlosses in pipes and present results.

Note: not all functions had been carefully tested - used only functions used in pyHeadloss.py"
'''

import numpy as np
from scipy.optimize import fsolve
from matplotlib import pyplot as plt

def red_loss(PipeIDmm, OtherIDmm, num_red,num_el):
	'''Calculate local loss in reducer and enlargement.
	Input: Pipe inner dia [mm], Reducer/Enlargement Dia, number of reducers and number of enlargements.'''
	IDFact=float(PipeIDmm/OtherIDmm)
	Kred=(1-(IDFact**2))**2
	Kenl=(1-(1/(IDFact**2)))**2
	red_loss=Kred*num_red+Kenl*num_el
	return float(red_loss)
	

	
def calc_re_vel (Flow, PipeIDmm, Viscosity_cSt):
	'''Calculate Reynolds number and Velocity of fluid in meters per second.
   Call: Flow [cum/h], Pipe ID[mm] and Viscosity of fluid [cSt]'''
	velocity_mps=(4*Flow/3600)/(3.14*(PipeIDmm/1000)**2); #units m/s;
  	reynolds=velocity_mps*(PipeIDmm/1000)/(Viscosity_cSt*0.000001); #no units
  	return velocity_mps, reynolds
  	
def elbow_loss(k90deg,num90deg,kLR,numLR,kSR,numSR,kRet,numRet,k45deg,num45deg):
	''' Calculate local losses due to elbows and bends.
	Call: k-factors for different elbows, number of elbows by type
	'''
	elb_loss=k90deg*num90deg+kLR*numLR+kSR*numSR+kRet*numRet+k45deg*num45deg
	return elb_loss
	
def valve_loss(kButt,numButt, kGate,numGate, kAngle,numAngle, kGlobe,numGlobe, kDuoChk, numDuoChk, kSwingChk,numSwingChk, kFoot, numFoot, kPop,numPop):
	''' Calculate local losses in valves.
	Call: k-factors for different types of valves and number of valves'''
	vlve_loss=kButt*numButt+kGate*numGate+kAngle*numAngle+kGlobe*numGlobe+kDuoChk*numDuoChk+kSwingChk*numSwingChk+kFoot*numFoot+kPop*numPop
	return vlve_loss
	
def tee_loss(kHeader,numHeader, kBranch,numBranch):
	'''Calculate local losses in tees - through header and through branch.
	Call: k-factors for flow through header and brunch, number of headers and branches.'''
	t_loss=kHeader*numHeader+kBranch*numBranch
	return t_loss
	
def misc_loss(kEntrance,num_Entrance, kExit,num_Exit, kStrainer,num_Strainer,kUser,num_User):
	''' calculate losses in Pipe Entrance, Pipe Exit, Strainer and User defined losses'''
	m_loss=kEntrance*num_Entrance+kExit*num_Exit+kStrainer*num_Strainer+kUser*num_User
	return m_loss 
	
def tot_loc_loss (elb_loss, vve_loss, t_loss, mis_loss, red_loss):
	''' calculate total local losses'''
	loc_loss=elb_loss+vve_loss+t_loss+mis_loss+red_loss
	return loc_loss

		
def frict_loss(PipeID, flow, visco, rough):
# calculate friction loss using Darcy-Weisbach equations
	'''NOT TESTED'''
	#Rey=[]
	#firct=[]
	s=calc_re_vel (flow, PipeID, visco)
	rey=s[1]
	if rey<=4000:
		fcoef=64/rey
	elif rey==0:
		fcoef=0
	else:
		def darcy (fcoef):
			return 1.14-2*np.log10(rough/PipeID+9.35/(rey*fcoef**0.5))-1/(fcoef**.5)	
	#initial guess, fi:	
		fi=1/((1.8*np.log10(6.9/rey + ((rough/PipeID)/3.7)**1.11))**2)
		fcoef=fsolve(darcy, fi)  
	return fcoef

def headloss(fric_loss,pipeLen_m, PipeIDmm, Klocal, flow, statHead_m):
	''' calculate Headloss in meters as function of Flow in cub. meters per second (cum/s)'''
	velocity_mps=(4*flow/3600)/(3.14*(PipeIDmm/1000)**2)
	HLQ=(fric_loss*(pipeLen_m*1000/PipeIDmm)+Klocal)*(velocity_mps**2)/(2*9.81)+statHead_m	
	return HLQ
	
def inp_k():
	''' read local loss "k"-factors from "k_factors.csv" file, which must be in same folder as main script'''
	k_fact=np.loadtxt("k_factors.csv", dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(None), unpack=False, ndmin=0)
	return k_fact

def graphs (ptag, AH, BH, ARe, AVel):
	''' plot Headloss, Reynolds Number and Velocity in pipe as functions of Flow'''
	fnameH=ptag+"_QH.png"
	fnameRe=ptag+"_QRe.png"
	fnameVel=ptag+"_QVel.png"
	Q=np.linspace(0,600)
	H,Re,Vel=AH*Q**2+BH, ARe*Q, AVel*Q
	plt.plot(Q,H, color="red")
	plt.title("Pipe: "+ptag)
	plt.xlabel("Flow [cum/hr]")
	plt.ylabel("Headloss [m]")
	plt.grid(True)
	plt.savefig(fnameH)
	#plt.show()	# not practical for multiple pipes - slow execution
	plt.close()
	plt.plot(Q,Re, color="blue")
	plt.title("Pipe: "+ptag)
	plt.xlabel("Flow [cum/hr]")
	plt.ylabel("Reynolds Number")
	plt.grid(True)
	plt.savefig(fnameRe)
	#plt.show()	# not practical for multiple pipes - slow execution
	plt.close()
	plt.plot(Q,Vel, color="green")
	plt.title("Pipe: "+ptag)
	plt.xlabel("Flow [cum/hr]")
	plt.ylabel("Velocity [m/s]")
	plt.grid(True)
	plt.savefig(fnameVel)
	#plt.show()	# not practical for multiple pipes - slow execution
	plt.close()
	
def get_float(message, default):
	'''get float number - error check included'''
	try:
		f=input (message)
		st=type(f)
		if f==0:
			f=default
			return float(f) ##dodo
		elif f==" ":
			f=default
			return float(f)  ##dodo
		else:
			return float(f)
	except:
		print("Wrong Input! Try again")
		return(get_float(message, default))
		
def serghides(PipeID, flow, visco, roughness):
	''' calculate friction flow using Serghides's 1984 solution of Darcy-Weisbach equation'''
	#Rey=[]
	#firct=[]
	s=calc_re_vel (flow, PipeID, visco)
	rey=float(s[1])
	vel=float(s[0])
	
	if rey==0:
		fcoef=0
	elif rey<=2500:
		fcoef=64/float(rey)
	else:
		A=-2*np.log10(float(roughness)/(3.7*float(PipeID))+12/float(rey))
		B=-2*np.log10(float(roughness)/(3.7*float(PipeID))+2.51*float(A)/float(rey))
		C=-2*np.log10(float(roughness)/(3.7*float(PipeID))+2.51*float(B)/float(rey))
		fcoef=float((A-(B-A))**2.0/float(C-2*B+A))**-2
	return fcoef, rey, vel
	
def write_table6 (fn, v1, v2, v3, v4, v5, v6):
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
	fn.write(",")
	fn.write(v6)
	return
	
def write_res_head_csv(filename):
# write headers to "csv"- file
	fn=open(filename, "a")
	write_table6(fn, "PipeTag,", "AH," ,"BH,", "ARe,", "AVelo,", "k")
	fn.close()
	return
		


