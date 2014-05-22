<h4> Some Local Losses (K-factors)</h4>


Fitting| k-factor | 
:----------- | :-----------: 
Standard 90 deg Elbow | 0.54
LR Elbow | 0.6
SR Elbow | 0.9
Return bend | 2.2
Standard 45 deg Elbow | 0.29
Butterfly Valve | 0.8
Gate Valve | 0.15
Angle Valve | 5
Globe Valve | 6.5
Duo Check Valve | 0.8
Swing Check | 1
Footvalve Standard | 1.4
Footvalve Poppet Type | 8
Tee Flow through | 0.4
Tee Flow branch | 1.1
Pipe exit | 1
Pipe entrance | 0.8
Sudden contraction | formula
Sudden enlargement | formula
Strainer | 8.43

From Octave Script k-factor for reducer/enlargement:</p>
IDFact=PipeIDmm/OtherIDmm</p>
Contraction/reducer=(1-(IDFact^2))^2</p>
Enlargent=(1-(1/(IDFact^)))^2 </p>

If you do not like provided Local (Minor) Losses factors, good references can be found [here](http://www.thermexcel.com/english/ressourc/pdclocal.htm) and [here](http://www.engineeringtoolbox.com/minor-loss-coefficients-pipes-d_626.html). </p>
"Must have" literature related to Minor Losses are Crane Technical Paper 410 and Idelchick's Handbook of Hydraulic Resistance (1994).

