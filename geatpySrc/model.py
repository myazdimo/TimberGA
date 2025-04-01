import numpy as np
from multiprocessing import Pool
import geatpy as ea
from numpy._typing import NDArray

from src.genetic import Chromosome
from src.optimization import SelectionFunction
from src.plot import HysteresisPlot, prep_data 
from src.data import parameters

class OptimizationProblem(ea.Problem):

    def __init__(self, M=2, processors=10):

        name = 'Pinching4'
        Dim = 30 #number of decision variables
        maxormins = [1] * M # Initialize maxormins (objective optimization flag list, 1: minimize the objective; -1: maximize the objective)
        varTypes = [0] * Dim # Initialize varTypes (types of decision variables, 0: real number; 1: integer) 
        lb = [ parameters[parameter].lower_bound for parameter in parameters] #lower bounds
        ub = [ parameters[parameter].upper_bound for parameter in parameters] #upper bounds
        lbin = [1] * Dim #lower bound inclusion
        ubin = [1] * Dim #upper bound inclusion
        self.processors = processors #number of processors used for computation

        self.target_plot = HysteresisPlot(prep_data("graph"))
        self.selection_function = SelectionFunction(self.target_plot)
        self.energy_rankings = [] #list of energy rankings in order
        self.force_rankings = [] #list of force rankings in order

        #parent class constructor called to complete instantiation
        ea.Problem.__init__(self,
                         name,
                         M,
                         maxormins,
                         Dim,
                         varTypes,
                         lb,
                         ub,
                         lbin,
                         ubin)
        self.curr_population = 0

    def evalVars(self, Vars): #objective function

        self.curr_population += 1
        print(f"evaluating population number {self.curr_population}")
        
        pool = Pool(processes=self.processors)
        rankings = pool.map(self._get_ranking, Vars) #Vars represents a single population

        f1 = [ranking[0] for ranking in rankings]
        f2 = [ranking[1] for ranking in rankings]

        best_force_ranking = min(f1) if (len(self.force_rankings) == 0 or self.force_rankings[-1] > min(f1)) else self.force_rankings[-1]
        best_energy_ranking = min(f2) if (len(self.energy_rankings) == 0 or self.energy_rankings[-1] > min(f2)) else self.energy_rankings[-1]

        self.force_rankings.append(best_force_ranking)
        self.energy_rankings.append(best_energy_ranking)

        f1 = np.array(f1).reshape(-1,1)
        f2 = np.array(f2).reshape(-1,1)
        f = np.hstack([f1, f2])

        CV = np.hstack([-f1])

        return f, CV 

    def _get_ranking(self, individual: NDArray):

        i=0
        chromosome = Chromosome(parameters, self.target_plot.boundaries)
        for parameter in chromosome:
            chromosome.change_parameter_value(parameter, individual[i])
            i += 1

        force_ranking, energy_ranking = self.selection_function.get_ranking(chromosome)

        return (force_ranking, energy_ranking)


