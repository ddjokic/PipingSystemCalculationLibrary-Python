<h4>pyPiping System Calculation</h4>
</p>
Copyright © 2013 D. Djokic <deki.djokic at gmail.com></p>
**Work in progress- experimental, so far!!**</p>

Main file is function file, hydrobb.py, around which you have to build script for problem in hands.

List of functions in "Building Blocks file":
flow(H,A,B) - calculates flow for given Headloss
par_lines(A1, B1,A2, B2) - calculates resultant of parallel connected pipes
ser_lines(A1,B1, A2,B2) - calculates resultant of pipes connected in series
eq_pump (APump,BPump,ASuction,BSuction) - calculates curve of equivalent pump - pump curve minus suction pipe curve
curve_intersection(APump, BPump, APipe, BPipe) - calcultes intersection of two curves - used system curve and pump curve, result is working point of the system
decomp_serial(Flow, AS1,BS1, AS2,BS2) - calculates Headloss in each of pipes in serial connestion, based on given Headloss
decomp_parallel(Headloss, AP1,BP1, AP2,BP2) - calculates Flow in each of pipes in serial connestion, based on given Headloss
Reynolds(flow, ARe) - calculates Reynolds number for a pipe, and given flow
velocity(flow, Avel) - calculates Velocity of fluid in pipe for given flow
write_res_head_csv(filename) - writes headers of result table in specified file
write_res_num_csv(filename, PipeTag, Flow, Headloss, Reynolds, Velocity)- writes results table to file - one pipe per row
par_flow(Flow, A1, B1, A2,B2)-calculates Flow and Headloss through each pipeline in parallel loop for given total Flow which entering loop