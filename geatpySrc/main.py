import numpy as np
from src.openSees import Pinching4Model
from src.data import parameters
from src.genetic import Chromosome
from model import OptimizationProblem

import geatpy as ea

if __name__ == "__main__":

    problem = OptimizationProblem()

    #construct the algorithm
    algorithm = ea.moea_NSGA2_templet( 
        problem,
        ea.Population(Encoding='BG', NIND=5000), #Binary encoding, Population size = 100
        MAXGEN=10, #maximum number of generations
        logTras=0) # Log recording interval (0 means no logging) 

    print("Initializing algorithm with 5000 Population size and 10 generations")
    
    algorithm.mutOper.Pm = 0.2   
    algorithm.recOper.XOVR = 0.9

    res = ea.optimize(algorithm,
                   verbose=False, #disable detailed output
                   drawing=1, #Enable visualization
                   outputMsg=True, #display output messages
                   drawLog=True, #disable log plotting
                   saveFlag=False) #do not save results


    result = Chromosome(parameters, problem.target_plot.boundaries) #result initialization

    print("Results:-")
    i = 0
    for parameter in result:

        result.change_parameter_value(parameter, res["Vars"][0][i])
        print(parameter+": ", res["Vars"][0][i])
        i += 1

    problem.target_plot.plot()
    Pinching4Model(result, plotting=True)
