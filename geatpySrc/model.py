import numpy as np

from src.data import parameters

from geatpy.geatpy.Problem import Problem

types = []

class OptimizationProblem(Problem):

    def __init__(self, M=2):

        name = 'Optimization'
        Dim = 38 #number of decision variables
        maxormins = [1] * M # Initialize maxormins (objective optimization flag list, 1: minimize the objective; -1: maximize the objective)
        varTypes = [0] * Dim # Initialize varTypes (types of decision variables, 0: real number; 1: integer) 
        lb = [ parameters[parameter].lower_bound for parameter in parameters]
        ub = [ parameters[parameter].upper_bound for parameter in parameters]
        lbin = [1] * Dim
        ubin = [1] * Dim

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
