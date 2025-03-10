import numpy as np
from model import OptimizationProblem

from geatpy.geatpy.Problem import Problem
from geatpy.geatpy import optimize
from geatpy.geatpy.Population import Population 
from geatpy.geatpy.algorithms.moeas.nsga2 import moea_NSGA2_templet

if __name__ == "__main__":

    problem = OptimizationProblem()

    #construct the algorithm
    algorithm = moea_NSGA2_templet(
        problem,
        Population(Encoding='BG', NIND=50), #Binary encoding, Population size = 50
        MAXGEN=100, #maximum number of generations
        logTras=0) # Log recording interval (0 means no logging) 

    algorithm.mutOper.Pm = 0.2 #mutation probability
    algorithm.recOper.XOVR = 0.9 #crossover probability

    res = optimize(algorithm,
                   verbose=False, #disable detailed output
                   drawing=1, #Enable visualization
                   outputMsg=True, #display output messages
                   drawLog=False, #disable log plotting
                   saveFlag=False) #do not save results
    print(res)

