from src.genetic import Chromosome
import numpy as np

from src.optimization import SelectionFunction
from src.plot import HysteresisPlot, prep_data 
from src.data import parameters

import geatpy as ea
types = []

class OptimizationProblem(ea.Problem):

    def __init__(self, M=2):

        name = 'Pinching4'
        Dim = 30 #number of decision variables
        maxormins = [1] * M # Initialize maxormins (objective optimization flag list, 1: minimize the objective; -1: maximize the objective)
        varTypes = [0] * Dim # Initialize varTypes (types of decision variables, 0: real number; 1: integer) 
        lb = [ parameters[parameter].lower_bound for parameter in parameters] #lower bounds
        ub = [ parameters[parameter].upper_bound for parameter in parameters] #upper bounds
        lbin = [1] * Dim #lower bound inclusion
        ubin = [1] * Dim #upper bound inclusion
        self.target_plot = HysteresisPlot(prep_data("graph"))
        self.selection_function = SelectionFunction(self.target_plot)

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

    def evalVars(self, Vars): #objective function

        print("evaluating population...")
        
        f1 = []
        f2 = []
        
        #Vars contains a population
        for individual in Vars:
            i=0
            chromosome = Chromosome(parameters, self.target_plot.boundaries)
            for parameter in chromosome:
                chromosome.change_parameter_value(parameter, individual[i])
                i += 1

            force_ranking, energy_ranking = self.selection_function.get_ranking(chromosome)

            f1.append(force_ranking)
            f2.append(energy_ranking)

        f1 = np.array(f1).reshape(-1,1)
        f2 = np.array(f2).reshape(-1,1)
        f = np.hstack([f1, f2])

        CV = np.hstack([-f1])

        return f, CV 
