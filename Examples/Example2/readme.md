# Example 2: Working Point Calculation

I was challenged recently to pick the best *for the purpose* one out of four pumps. Challenge was that pump should work in two modes, giving above 300 cum/h @ some pressure and approx. 30 cum/h @ more than 7.5 barg. Fluid was **drilling mud**, 1620 kg/cum, with kinamatic viscosity of 0.0216 cSt.

I come with WP.py script, which takes output of pyHeadlosses.py, connects pipes in serial connection (as many pipes as there are in the system but min. 2) and plot system curve(s) against pump curves.

I slightly mdified results of pyHeadlosses, adding column status with values "1" for open and "0" for closed pipe - multiple working point. Flag status will not affect Reynolds number and Velocity calculation - it is handled through column "StatReVel". In a case of heving equation which is result of subloop calculation, one wants flow through subloop but there is no logic to calculate Reynolds and Velocity.

Slightly modified input and calculation results are given in folder results. In reality, I have not recomended any of those four pumps - only one which satisfied both services was big for the intended purpose.

Limitations:
Pipes - minimum two pipe lines.
Pumps - minimum two pumps
Discharge pressure (desired) - should be input as part of static head. 

Copyright © 2013-2014 D. Djokic <deki.djokic at gmail.com>

This code is released under the [GPL], version 2 or later:

   >This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   >This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   >You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

The GNU General Public License is available in the file "GNU_LICENSE.txt" in
the source distribution.  On Debian systems, the complete text of the
GPL can be found [here](http://www.gnu.org/copyleft/gpl.html).