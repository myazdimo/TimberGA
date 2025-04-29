import matplotlib.pyplot as plt
import geatpy as ea
import sys

sys.path.append('C:/Users/myazdimo/Downloads/TMRF_PLATFORM')

from src.openSees import Pinching4Model
from src.data import parameters
from src.genetic import Chromosome

from model import OptimizationProblem

if __name__ == "__main__":

    problem = OptimizationProblem()
    pop_size = 200 #Population size
    generations = 20

    #construct the algorithm
    algorithm = ea.moea_NSGA2_templet( 
        problem,
        ea.Population(Encoding='BG', NIND=pop_size), #Binary encoding
        MAXGEN=generations, #maximum number of generations
        logTras=0) # Log recording interval (0 means no logging) 

    print(f"Initializing algorithm with {pop_size} Population size and {generations} generations")
    
    algorithm.mutOper.Pm = 0.2   
    algorithm.recOper.XOVR = 0.9

    try:
        res = ea.optimize(algorithm,
                    verbose=False, #disable detailed output
                    drawing=1, #Enable visualization
                    outputMsg=True, #display output messages
                    drawLog=True, #disable log plotting
                    saveFlag=False) #do not save results

    except KeyboardInterrupt:
        print("Optimization interrupted by user")

    plt.figure()
    plt.plot(problem.force_rankings)
    plt.xlabel("Iterations")
    plt.ylabel("CFE")
    plt.show()

    plt.figure()
    plt.plot(problem.energy_rankings)
    plt.xlabel("Iterations")
    plt.ylabel("CEE")
    plt.show()

    result = Chromosome(parameters, problem.target_plot.boundaries) #result initialization

    print("Results:-")
    i = 0
    for parameter in result:

        result.change_parameter_value(parameter, res["Vars"][0][i])
        print(parameter+": ", res["Vars"][0][i])
        i += 1

    force_ranking, energy_ranking = problem.selection_function.get_ranking(result)
    print("CFE: ", force_ranking)
    print("CEE: ", energy_ranking)
    plt.figure()
    problem.target_plot.plot() #plot target graph
    res_model = Pinching4Model(result)
    res_model.plot() #plot pinching4 solution model
    plt.show()
