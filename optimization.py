from openseespy.opensees import uniaxialMaterial

from plot import HysteresisPlot
from data import parameters as params 
import random
from genetic import Chromosome, FitnessFunction, Parameter, Population
from typing import Dict 

class SelectionFunction(FitnessFunction):

    def get_ranking(self, chromosome: Chromosome) -> float:

        """returns the ranking of how close a chromosome
        fits the target plot. The better it fits, higher
        the ranking value""" 

        func = lambda key: chromosome.get_parameter(key).value

        self.model = uniaxialMaterial('Pinching4', 100, 
                         func("ePf1"), func("ePd1"), func("ePf2"), func("ePd2"), func("ePf3"), func("ePd3"), func("ePf4"), func("ePd4"), 
                         func("eNf1"), func("eNd1"), func("eNf2"), func("eNd2"), func("eNf3"), func("eNd3"), func("eNf4"), func("eNd4"),
                         func("rDispP"), func("rForceP"), func("uForceP"),
                         func("rDispN"), func("rForceN"), func("uForceN"),
                         func("gK1"), func("gK2"), func("gK3"), func("gK4"), func("gKLim"),
                         func("gD1"), func("gD2"), func("gD3"), func("gD4"), func("gDLim"),
                         func("gF1"), func("gF2"), func("gF3"), func("gF4"), func("gFLim"),
                         func("gE"), "cycle") 

        return 0



class OptimizationModel:

    """A model based on the Genetic Algortihm. 
    Used to find the parameters required to
    fit a pinching4 hysteresis curve"""

    def __init__(self, target_plot: HysteresisPlot, 
                 population_size: int, generations: int,
                 fitness_function: FitnessFunction):

        self.target_plot = target_plot
        self.population_size = population_size
        self.generations = generations
        self.fitness_function = fitness_function
        self.population: Population
        self.parameters: Dict[str, Parameter]

        self.isLoaded = False
        
    def load(self):

        """load the model"""

        self.parameters = params
        self.population = self.initPopulation(Population())
        self.population.sort(self.selection)

        self.isLoaded = True

    def run(self):

        """run the algorithm"""

        if self.isLoaded:
            for _ in range(self.generations):
                parent1 = self.population.get_chromosome(0)
                parent2 = self.population.get_chromosome(1)
                self.crossover(parent1, parent2)
                self.population.sort(self.selection)

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

            chromosome = self.initChromosome(Chromosome(self.parameters))
            population.add_chromosome(chromosome)
        
        return population

    def crossover(self, parent1: Chromosome, parent2: Chromosome):

        child_num = int(self.population_size*(3/4)) #number of children to be added to the population

        for i in range(child_num):

            child = Chromosome(self.parameters) 
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

