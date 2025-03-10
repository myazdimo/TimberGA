import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from openSees import Pinching4Model
import matplotlib.pyplot as plt

from plot import HysteresisPlot
from data import parameters as params 
import random
from genetic import Chromosome, FitnessFunction, Parameter, Population
from typing import Dict, List 

class SelectionFunction(FitnessFunction):

    def __init__(self, target_plot: HysteresisPlot):

        self.target_plot = target_plot

    def get_ranking(self, chromosome: Chromosome) -> float:
        """returns the ranking of how close a chromosome
        fits the target plot. The better it fits, lower
        the ranking value""" 

        pinching4 = Pinching4Model(chromosome)
        
        ranking = self._calculate_ranking(pinching4.get_displacement(), pinching4.get_moment())

        return ranking

    def _calculate_ranking(self, disp: List, force: List) -> float:
        
        target_data = self.target_plot.get_plot()
        
        # number of points is taken from the plot with the least number of points
        points_num = len(disp) if len(disp) <= len(target_data["Displacement"]) else len(target_data["Displacement"])

        numerator = 0
        denominator = 0
        for i in range(points_num):
            numerator += target_data["Moment"][i] - force[i]
            denominator += target_data["Moment"][i]

        return (numerator/denominator)

class OptimizationModel:
    """A model based on the Genetic Algortihm. 
    Used to find the parameters required to
    fit a pinching4 hysteresis curve"""

    def __init__(self, target_plot: HysteresisPlot, 
                 population_size: int, generations: int):

        print(f"Initializing a model with populations size:{population_size} and {generations} generations")

        self.target_plot = target_plot
        self.population_size = population_size
        self.generations = generations
        self.fitness_function: FitnessFunction
        self.population: Population
        self.parameters: Dict[str, Parameter]

        self.isLoaded = False
        
    def load(self):
        """load the model"""
        print("Model loading...")

        self.fitness_function = SelectionFunction(self.target_plot)
        self.parameters = params
        self.population = self.initPopulation(Population())
        self.population.sort(self.selection)

        self.isLoaded = True

        print("Done loading")

    def run(self):
        """run the algorithm"""

        print("Model running...")

        if self.isLoaded:
            for generation in range(self.generations):
                parent1 = self.population.get_chromosome(0)
                parent2 = self.population.get_chromosome(1)
                self.crossover(parent1, parent2)
                self.population.sort(self.selection)
                print(f"Generation number:{generation+1} done...")

            print("Done running. Now plotting solution")

            #plot the best matching chromosome
            solution = self.population.get_chromosome(0)
            self.target_plot.plot()
            Pinching4Model(solution, plotting=True)

            self.isLoaded = False

        else:
            raise Exception("Load the model before running: OptimizationModel.load()")

    def initChromosome(self, chromosome: Chromosome) -> Chromosome:
        """initializes a chromosome that already has parameters
        with default values stored in it""" 

        for parameter in chromosome:

            lower_bound = chromosome.get_parameter(parameter).lower_bound
            upper_bound = chromosome.get_parameter(parameter).upper_bound

            value = random.uniform(lower_bound, upper_bound)
            chromosome.change_parameter_value(parameter, value)
        
        return chromosome


    def initPopulation(self, population: Population) -> Population:
         
        for _ in range(self.population_size):

            chromosome = self.initChromosome(Chromosome(self.parameters, self.target_plot.boundaries))
            population.add_chromosome(chromosome)
        
        return population

    def crossover(self, parent1: Chromosome, parent2: Chromosome):

        child_num = int(self.population_size*(3/4)) #number of children to be added to the population

        for i in range(child_num):

            child = Chromosome(self.parameters, self.target_plot.boundaries) 
            alpha = random.random() #random value between 0 and 1

            for parameter in child:

                parent1_param = parent1.get_parameter(parameter).value
                parent2_param = parent2.get_parameter(parameter).value

                value = parent1_param*alpha + parent2_param*(1-alpha)
                child.change_parameter_value(parameter, value)

            self.mutation(child)

            self.population.replace(index=(-1-i), chromosome=child)

    def mutation(self, child: Chromosome):

        """muatation in chromosomes done by changing
        parameter values by 5%"""

        for parameter in child:

            param_value = child.get_parameter(parameter).value 
            value = param_value + random.uniform(-0.05*param_value, 0.05*param_value)
            child.change_parameter_value(parameter, value)
        
    def selection(self, chromosome: Chromosome):

        return self.fitness_function.get_ranking(chromosome)

