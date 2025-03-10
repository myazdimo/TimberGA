# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 16:20:54 2024

@author: myazdimo
"""

import copy
from openseespy.opensees import *
import opsvis as opsv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def openseesModel(parse, plotting, boundaries):
    boundaries = [boundary * 1000 for boundary in boundaries]
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

    R_F=1.5  # Reinforced factor for force
    R_D=2.0  # Reinforced factor for displacements

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
    ePf1 =0.7852*R_F
    ePd1 =0.000241*R_D
    ePf2 =7.3124074*R_F
    ePd2 =0.0521*R_D
    ePf3 =23.432*R_F
    ePd3 =0.1822*R_D
    ePf4 =24.691*R_F
    ePd4 =0.2901*R_D


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

    # ePf1 =0.7865*R_F
    # ePd1 =0.000137*R_D
    # ePf2 =61.2074*R_F
    # ePd2 =0.0416*R_D
    # ePf3 =63.224*R_F
    # ePd3 =0.1709*R_D
    # ePf4 =54.712*R_F
    # ePd4 =0.2595*R_D

    eNf1 =-ePf1
    eNd1 =-ePd1
    eNf2 =-ePf2
    eNd2 =-ePd2
    eNf3 =-ePf3
    eNd3 =-ePd3
    eNf4 =-ePf4
    eNd4 =-ePd4

    rDispP =0.7
    rForceP =0.155
    uForceP =0.01012
    rDispN =0.7
    rForceN =0.155
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



    uniaxialMaterial('Pinching4', 100, 
                        parse("ePf1"), parse("ePd1"), parse("ePf2"), parse("ePd2"), parse("ePf3"), parse("ePd3"), parse("ePf4"), parse("ePd4"), 
                        -(parse("ePf1")), -(parse("ePd1")), -(parse("ePf2")), -(parse("ePd2")), -(parse("ePf3")), -(parse("ePd3")), -(parse("ePf4")), -(parse("ePd4")),
                        parse("rDispP"), parse("fFoceP"), parse("uForceP"),
                        parse("rDispN"), parse("fFoceN"), parse("uForceN"),
                        parse("gK1"), parse("gK2"), parse("gK3"), parse("gK4"), parse("gKLim"),
                        parse("gD1"), parse("gD2"), parse("gD3"), parse("gD4"), parse("gDLim"),
                        parse("gF1"), parse("gF2"), parse("gF3"), parse("gF4"), parse("gFLim"),
                        parse("gE"), "cycle") 




    # element('zeroLength',eleTag,nodeR,nodeC,'-mat',matTag,'-dir',6)

    element('zeroLength',10,3,4,'-mat',100,'-dir',6)



    DOF=[1,2]
    equalDOF(3,4,*DOF) 


    #########################
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
    ############################
    # Maintain constant gravity loads and reset time to zero
    loadConst('-time', 0.0)

    #Analysis

    st1_force=100


    push=2

    timeSeries('Linear', push)

    pattern('Plain', push, push)

    load(2, 0,st1_force,0)


    num_push_step=int(boundaries[0])  #number of pushover steps
    push_inc_step=0.001     #increment of pushover steps
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
    ###########
    wipeAnalysis()
    constraints('Transformation')
    numberer('RCM')
    system('BandGen')
    test('NormUnbalance', 1e-4, 1000)
    algorithm('Newton')
    integrator('DisplacementControl', 2, 2, push_inc_step)
    analysis('Static')
    #################
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

    parameters = [(int(boundary), 0.001) for boundary in boundaries]

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

    if plotting == True:
        # Plotting the force vs. displacement
        plt.figure(1)
        plt.plot(Disp, Force,color='black',linestyle='--',linewidth=1)
        plt.plot(New_Env_D,New_Env_F,'r.-',markersize=8,linewidth=1.5)
        plt.plot(New_Env_D_N,New_Env_F_N,'r.-',markersize=8,linewidth=1.5)
        plt.xlabel('Rotation (rad)')
        plt.ylabel('Moment (kN.m)')
        plt.title('Moment vs. Rotation of Pinching4 for Bolted Connection')
        plt.grid(True)

        plt.show()

    # opsv.plot_model()
    # opsv.plot_defo()

    data = {
        "Displacement": Disp,
        "Moment": Force}

    return data



