from src.plot import HysteresisPlot, prep_data
from src.genetic import Parameter, Chromosome
from src.optimization import SelectionFunction


graphNumber = "graph4"


target_plot = HysteresisPlot(prep_data(graphNumber, is_degrees=False))
target_displacement = target_plot.get_plot()["Displacement"]
target_force = target_plot.get_plot()["Moment"]
target_plot.plot()

boundaries = target_plot.boundaries

chromosome = {
    "ePf1" : Parameter(nature="variable", value=50.52697032120241, lower_bound=49, upper_bound=54),
    "ePf2" : Parameter(nature="variable", value=90.14339556423617, lower_bound=90, upper_bound=97),
    "ePf3": Parameter(nature="variable", value=114.78401391686505, lower_bound=114, upper_bound=115.5),
    "ePf4": Parameter(nature="variable", value=115.64619891964476, lower_bound=115, upper_bound=117),
    "ePd1": Parameter(nature="variable", value=0.012, lower_bound=0.007, upper_bound=0.012),
    "ePd2": Parameter(nature="variable", value=0.04285714285714286, lower_bound=0.03, upper_bound=0.06),
    "ePd3": Parameter(nature="variable", value=0.08917808219178082, lower_bound=0.06, upper_bound=0.09),
    "ePd4": Parameter(nature="variable", value=0.10105882352941176, lower_bound=0.09, upper_bound=0.11),
    "eNf1": Parameter(nature="variable", value=-49.46021210040436, lower_bound=-54, upper_bound=-49),
    "eNf2": Parameter(nature="variable", value=-90.89643017906326, lower_bound=-95, upper_bound=-88),
    "eNf3": Parameter(nature="variable", value=-113.95196386608478, lower_bound=-114.5, upper_bound=-112),
    "eNf4": Parameter(nature="variable", value=-115.05694753868221, lower_bound=-117, upper_bound=-115),
    "eNd1": Parameter(nature="variable", value=-0.011761904761904762, lower_bound=-0.012, upper_bound=-0.007),
    "eNd2": Parameter(nature="variable", value=-0.05759295499021526, lower_bound=-0.06, upper_bound=-0.03),
    "eNd3": Parameter(nature="variable", value=-0.09, lower_bound=-0.09, upper_bound=-0.06),
    "eNd4": Parameter(nature="variable", value=-0.09141176470588235, lower_bound=-0.11, upper_bound=-0.09),
    "rDispP": Parameter(nature="variable", value=0.08344422700587084, lower_bound=0.04, upper_bound=0.15),
    "rForceP": Parameter(nature="variable", value=0.09385518590998043, lower_bound=0.08, upper_bound=0.12),
    "uForceP": Parameter(nature="variable", value=0.008931301587301588, lower_bound=0.008096, upper_bound=0.012144),
    "rDispN": Parameter(nature="variable", value=0.0785518590998043, lower_bound=0.04, upper_bound=0.09),
    "rForceN": Parameter(nature="variable", value=0.1253816046966732, lower_bound=0.12, upper_bound=0.17),
    "uForceN": Parameter(nature="variable", value=0.008931301587301588, lower_bound=0.008096, upper_bound=0.012144),
    "gK1": Parameter(nature="constant", value=1.000001),
    "gK2": Parameter(nature="constant", value=0.500001),
    "gK3": Parameter(nature="constant", value=0.5),
    "gK4": Parameter(nature="constant", value=0.500001),
    "gKLim": Parameter(nature="constant", value=0.01),
    "gD1": Parameter(nature="constant", value=0.5),
    "gD2": Parameter(nature="constant", value=0.5),
    "gD3": Parameter(nature="constant", value=1.0),
    "gD4": Parameter(nature="constant", value=0.8),
    "gDLim": Parameter(nature="constant", value=0.200001),
    "gF1": Parameter(nature="constant", value=1.000001),
    "gF2": Parameter(nature="constant", value=0),
    "gF3": Parameter(nature="constant", value=1.0),
    "gF4": Parameter(nature="constant", value=1.000001),
    "gFLim": Parameter(nature="constant", value=0.01),
    "gE": Parameter(nature="constant", value=10.000001)
    }

optimizedParameters = Chromosome(chromosome=chromosome, boundaries=boundaries)
selectionFunction = SelectionFunction(target_plot)
x = selectionFunction.get_ranking(optimizedParameters)
print("CFE:", x[0]*100)
print("CEE:", x[1]*100)


# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 16:20:54 2024

@author: myazdimo
"""

from openseespy.opensees import *
import opsvis as opsv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


boundaries = [boundary * 400 for boundary in boundaries]

wipe()

WBay=1     #Width of Bay in cm




ndm=2
ndf=3
model('basic', '-ndm', ndm, '-ndf', ndf)
P_delta=1
geomTransf('PDelta', P_delta)


#Define nodes

node(1,0,0)
fix(1, 1, 1,1) 

    

node(2,WBay,0)


    

node(3,0.01,0)
node(4,0.01,0)





element('elasticBeamColumn', 1, 1,3,  0.0504, 12.800e6, 3.3e-4, 1)
element('elasticBeamColumn', 2, 4,2,  0.0504, 12.800e6, 3.3e-4, 1)




# uniaxialMaterial('Pinching4', 100, ePf1, ePd1, ePf2, ePd2, ePf3, ePd3, ePf4, ePd4, <eNf1, eNd1, eNf2, eNd2, eNf3, eNd3, eNf4, eNd4>, rDispP, rForceP, uForceP, <rDispN, rForceN, uForceN>, gK1, gK2, gK3, gK4, gKLim, gD1, gD2, gD3, gD4, gDLim, gF1, gF2, gF3, gF4, gFLim, gE, dmgType)
###########################
#Beam TO Column
###########################

R_F=1.0  # Reinforced factor for force
R_D=1.0  # Reinforced factor for displacements

#Unreinforced
# ePf1 =0.7852
# ePd1 =0.000241
# ePf2 =7.3124074
# ePd2 =0.0521
# ePf3 =23.432
# ePd3 =0.1822
# ePf4 =24.691
# ePd4 =0.2901

#Reinforced with STS
# ePf1 =0.7852
# ePd1 =0.000241
# ePf2 =7.3124074
# ePd2 =0.0521
# ePf3 =23.432
# ePd3 =0.1822
# ePf4 =24.691
# ePd4 =0.2901
#

###########################
#Column to Base
###########################

#Unreinforced
# ePf1 =0.7865
# ePd1 =0.000137
# ePf2 =61.2074
# ePd2 =0.0416
# ePf3 =63.224
# ePd3 =0.1709
# ePf4 =54.712
# ePd4 =0.2595

#Reinforced with STS

ePf1 =52
ePd1 =0.01
ePf2 =92
ePd2 =0.05
ePf3 =114.5
ePd3 =0.08
ePf4 =115.8
ePd4 =0.108

eNf1 =-ePf1
eNd1 =-ePd1
eNf2 =-ePf2
eNd2 =-ePd2
eNf3 =-ePf3
eNd3 =-ePd3
eNf4 =-ePf4
eNd4 =-ePd4

rDispP =0.1
rForceP =0.1
uForceP =0.01012
rDispN =0.07
rForceN =0.15
uForceN =0.01012
gK1 =1.0
gK2 =0.5
gK3 =0.5
gK4 =0.5
gKLim =0.01
gD1 =0.5
gD2 =0.5
gD3 =1.0
gD4 =0.8
gDLim =0.2
gF1 =1.0
gF2 =0
gF3 =1.0
gF4 =1.0
gFLim =0.01
gE =10
dmgType ='cycle'


uniaxialMaterial('Pinching4', 100, ePf1, ePd1, ePf2, ePd2, ePf3, ePd3, ePf4, ePd4, eNf1, eNd1, eNf2, eNd2, eNf3, eNd3, eNf4, eNd4, rDispP, rForceP, uForceP, rDispN, rForceN, uForceN, gK1, gK2, gK3, gK4, gKLim, gD1, gD2, gD3, gD4, gDLim, gF1, gF2, gF3, gF4, gFLim, gE, dmgType)




# element('zeroLength',eleTag,nodeR,nodeC,'-mat',matTag,'-dir',6)

element('zeroLength',10,3,4,'-mat',100,'-dir',6)



DOF=[1,2]
equalDOF(3,4,*DOF) 



DL=0   #Uniform Dead Load


Linear=1   #Linear load
timeSeries('Linear', Linear)

GR=1   #Gravity Load
pattern('Plain', GR, Linear)

eleTags=[1,2]

eleLoad('-ele', *eleTags, '-type', '-beamUniform', DL)


Tol = 1.0e-6
NstepGravity = 10
DGravity = 1.0 / NstepGravity

# Convergence settings
test('NormDispIncr', Tol, 6)
algorithm('Newton')

# Constraints and system settings
constraints('Plain')
numberer('RCM')
system('BandGeneral')

# Load control and analysis type
integrator('LoadControl', DGravity)
analysis('Static')
analyze(NstepGravity)

# Maintain constant gravity loads and reset time to zero
loadConst('-time', 0.0)

#Analysis

st1_force=100


push=2

timeSeries('Linear', push)

pattern('Plain', push, push)

load(2, 0,st1_force,0)


num_push_step=int(boundaries[0])  #number of pushover steps
push_inc_step=0.0025 #increment of pushover steps
# push_data=np.zeros((1001,2))


#recorder
# ops.recorder('Node', '-file', 'Rotations.txt', '-time', '-node', 107,10701, '-dof', 3, 'disp')

# ops.recorder('Element', '-file', 'EndI111_force.txt','-time', '-ele', 111, 'force')

Disp=[]
Force=[]
Env_F=[]
Env_D=[]
Env_F_N=[]
Env_D_N=[]

wipeAnalysis()
constraints('Transformation')
numberer('RCM')
system('BandGen')
test('NormUnbalance', 1e-4, 1000)
algorithm('Newton')
integrator('DisplacementControl', 2, 2, push_inc_step)
analysis('Static')


for i in range (1,num_push_step+1):
    Force_1=[]
    Disp_1=[]

    analyze(1)
    Disp.append(nodeDisp(2, 2))
    Disp_1.append(nodeDisp(2, 2))
    reactions()
    Force.append(nodeReaction(1, 2))
    Force_1.append(nodeReaction(1, 2))
max_force = max(Force_1)
max_force_index = Force_1.index(max_force)
corresponding_disp = Disp_1[max_force_index]
# Add to Env_F and Env_D
Env_F.append(max_force)
Env_D.append(corresponding_disp)


integrator('DisplacementControl', 2, 2, -2*push_inc_step)
for i in range (1,num_push_step+1):
    Force_1=[]
    Disp_1=[]
    
    analyze(1)
    Disp.append(nodeDisp(2, 2))
    Disp_1.append(nodeDisp(2, 2))
    reactions()
    Force.append(nodeReaction(1, 2))
    Force_1.append(nodeReaction(1, 2))
min_force = min(Force_1)
min_force_index = Force_1.index(min_force)
corresponding_disp = Disp_1[min_force_index]
# Add to Env_F and Env_D
Env_F_N.append(min_force)
Env_D_N.append(corresponding_disp)

integrator('DisplacementControl', 2, 2, push_inc_step)
for i in range (1,num_push_step+1):
    analyze(1)
    Disp.append(nodeDisp(2,2))
    reactions()
    Force.append(nodeReaction(1,2))


def run_pushover(num_push_steps, push_inc_step):

    integrator('DisplacementControl', 2, 2, push_inc_step)
    for i in range(num_push_steps):
        Force_1=[]
        Disp_1=[]

        analyze(1)
        Disp.append(nodeDisp(2, 2))
        Disp_1.append(nodeDisp(2, 2))
        reactions()
        Force.append(nodeReaction(1, 2))
        Force_1.append(nodeReaction(1, 2))
    max_force = max(Force_1)
    max_force_index = Force_1.index(max_force)
    corresponding_disp = Disp_1[max_force_index]
    # Add to Env_F and Env_D
    Env_F.append(max_force)
    Env_D.append(corresponding_disp)
    
    integrator('DisplacementControl', 2, 2, -2 * push_inc_step)
    for i in range(num_push_steps):
        Force_1=[]
        Disp_1=[]
        
        analyze(1)
        Disp.append(nodeDisp(2, 2))
        Disp_1.append(nodeDisp(2, 2))
        reactions()
        Force.append(nodeReaction(1, 2))
        Force_1.append(nodeReaction(1, 2))
    min_force = min(Force_1)
    min_force_index = Force_1.index(min_force)
    corresponding_disp = Disp_1[min_force_index]
    # Add to Env_F and Env_D
    Env_F_N.append(min_force)
    Env_D_N.append(corresponding_disp)
    
    integrator('DisplacementControl', 2, 2, push_inc_step)
    for i in range(num_push_steps):
        analyze(1)
        Disp.append(nodeDisp(2, 2))

        reactions()
        Force.append(nodeReaction(1, 2))

    

# List of (num_push_steps, push_inc_step) tuples for each iteration
parameters = [
    (50, 0.001),
    (75, 0.001),
    (100, 0.001),
    (125, 0.001),
    (150, 0.001),
    (200, 0.001),
    (250, 0.001),
    (300, 0.001),
    (350, 0.001),
    (400, 0.001),
    (450, 0.001),
    (500, 0.001), 
    (550, 0.001),
    (600, 0.001),
]

parameters = [(int(boundary), 0.0025) for boundary in boundaries[1:]]

# Run the pushover analysis for each set of parameters
for num_push_steps, push_inc_step in parameters:
    run_pushover(num_push_steps, push_inc_step)

    

for i in range(len(Force)):
    Force[i] = -Force[i]
    
for i in range(len(Env_D)):
    Env_D[i] = -Env_D[i]

for i in range(len(Env_D_N)):
    Env_D_N[i] = -Env_D_N[i]  
    
Disp.insert(0, 0)
Force.insert(0, 0)
Env_F.insert(0, 0)
Env_D.insert(0, 0)
Env_F_N.insert(0, 0)
Env_D_N.insert(0, 0)    
# for i in range(1,num_push_step+1):    
#     analyze(1)
#     push_data[i,0]=nodeDisp(2,2)
#     reactions()
#     push_data[i,1]=nodeReaction(1,2)
    

# plt.plot(push_data[:,0],abs( push_data[:,1]))
# plt.xlabel('Horizontal Displacement(mm)')
# plt.ylabel('Horizontal Load(kN)')

#eliminating faulty points in envelope curve
def elimination(Env_D, Env_F):
    New_Env_D = []
    New_Env_F = []

    for i in range(len(Env_D)):
        if (i==0 or abs(Env_F[i]) > abs(Env_F[i-1])):
            New_Env_D.append(Env_D[i])
            New_Env_F.append(Env_F[i])

    return New_Env_D, New_Env_F

New_Env_D, New_Env_F = elimination(Env_D, Env_F)
New_Env_D_N, New_Env_F_N = elimination(Env_D_N, Env_F_N)



plt.plot(Disp, Force)

# Plotting the force vs. displacement
plt.figure(1)
plt.plot(Disp, Force,color='black',linestyle='--',linewidth=1)
plt.plot(New_Env_D,New_Env_F,'r.-',markersize=8,linewidth=1.5)
plt.plot(New_Env_D_N,New_Env_F_N,'r.-',markersize=8,linewidth=1.5)
plt.xlabel('Rotation (rad)')
plt.ylabel('Moment (kN.m)')
plt.title('Moment vs. Rotation of Pinching4')
plt.grid(True)


# opsv.plot_model()
# opsv.plot_defo()

data = {
    "Displacement": Disp,
    "Moment": Force}


plt.plot(data['Displacement'], data['Moment'])
plt.show()
