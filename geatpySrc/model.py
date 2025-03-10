import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from genetic import Chromosome
import numpy as np

from optimization import SelectionFunction
from plot import HysteresisPlot
from data import parameters

from geatpy.geatpy.Problem import Problem
types = []

class OptimizationProblem(Problem):

    def __init__(self, M=1):

        name = 'Pinching4'
        Dim = 38 #number of decision variables
        maxormins = [1] * M # Initialize maxormins (objective optimization flag list, 1: minimize the objective; -1: maximize the objective)
        varTypes = [0] * Dim # Initialize varTypes (types of decision variables, 0: real number; 1: integer) 
        lb = [ parameters[parameter].lower_bound for parameter in parameters] #lower bounds
        ub = [ parameters[parameter].upper_bound for parameter in parameters] #upper bounds
        lbin = [1] * Dim #lower bound inclusion
        ubin = [1] * Dim #upper bound inclusion

        #parent class constructor called to complete instantiation

        Problem.__init__(self,
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
        
        target_plot = HysteresisPlot("graph")
        chromosome = Chromosome(parameters, target_plot.boundaries)

        i = 0
        for parameter in chromosome:
            chromosome.change_parameter_value(parameter, Vars[:, [i]])
            i += 1

        print("number of params:", i)

        selection_function = SelectionFunction(target_plot)    

        f1 = selection_function.get_ranking(chromosome)

        CV = np.hstack([])

        f = np.hstack([f1])

        return f, CV




        
