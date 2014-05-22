***NOTE***

Difference between scripts in /Examples/Example1 folder, example1.py and example11.py is that later is calling function "bb.par_flow()", while former "bb.decomp_parallel()" - line 86 in script example11.py.</p>
Unfortunatelly, decomp_parallel() not return correct results in all cases; par_flow is returning correct results in all <b>TESTED</b> cases. Hence, use par_flow() for time being. Function "decomp_parallel()" is fixable - in a future.</p>
