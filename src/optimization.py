from src.openSees import Pinching4Model
import numpy as np
import matplotlib.pyplot as plt

from src.plot import HysteresisPlot
from src.data import parameters as params 
import random
from src.genetic import Chromosome, FitnessFunction, Parameter, Population
from typing import Dict, List, Tuple 

class SelectionFunction(FitnessFunction):

    def __init__(self, target_plot: HysteresisPlot):

        self.target_data = target_plot.get_plot()

    def get_ranking(self, chromosome: Chromosome) -> Tuple[float, float]:
        """returns the ranking of how close a chromosome
        fits the target plot. The better it fits, lower
        the ranking value
        returns res: (force ranking, energy ranking)""" 

        pinching4 = Pinching4Model(chromosome)
        
        disp = pinching4.get_displacement()
        force = pinching4.get_moment()

        # number of points is taken from the plot with the least number of points
        self.points_num = len(disp) if len(disp) <= len(self.target_data["Displacement"]) else len(self.target_data["Displacement"])

        force_ranking = self._calculate_force_ranking(force)
        energy_ranking = self._calculate_energy_ranking(disp, force)

        res = (force_ranking, energy_ranking)
        return res

    def _calculate_energy_ranking(self, disp: List[float], force: List[float]) -> float:
        
        numerator = 0
        denominator = 0

        for i in range(1, self.points_num):

            disp = np.array(disp[0:i+1])
            force = np.array(force[0:i+1])
            target_disp = np.array(self.target_data["Displacement"][0:i+1])
            target_force = np.array(self.target_data["Moment"][0:i+1])

            energy = np.trapz(abs(force), disp)
            target_energy = np.trapz(abs(target_force), target_disp)

            numerator += abs(target_energy - energy) 
            denominator += target_energy

        return (numerator/denominator)

    def _calculate_force_ranking(self, force: List) -> float:
        
        numerator = 0
        denominator = 0
        for i in range(self.points_num):
            numerator += abs(self.target_data["Moment"][i] - force[i])
            denominator += self.target_data["Moment"][i]

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

