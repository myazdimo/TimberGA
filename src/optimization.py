from numpy._typing import NDArray
from src.helper import integrate, splitter
from src.openSees import Pinching4Model
import numpy as np

from src.plot import HysteresisPlot
from src.data import parameters as params 
import random
from src.genetic import Chromosome, FitnessFunction, Parameter, Population
from typing import Dict, Tuple 

class SelectionFunction(FitnessFunction):

    def __init__(self, target_plot: HysteresisPlot):

        self.target_plot = target_plot

    def _interpolate(self, x: NDArray, y: NDArray, 
                     x_target: NDArray, y_target: NDArray) -> Tuple[NDArray, NDArray]:

        x_subsets, y_subsets, order = splitter(y, x)
        x_target_subsets, y_target_subsets, target_order = splitter(y_target, x_target)
        y_interp = np.array([])
        x_interp = np.array([])

        assert len(x_subsets) == len(y_subsets) and len(x_target_subsets) == len(y_target_subsets)
        assert len(order) == 3 and len(target_order) == 3

        for i in range(len(x_subsets)):
            assert len(x_target_subsets[i]) == len(y_target_subsets[i])

            if order[i] == -1:
                disp_dense = np.linspace(x_subsets[i].max(), x_subsets[i].min(), len(x_target_subsets[i]))
                force_dense = np.interp(disp_dense, np.flip(x_subsets[i]), np.flip(y_subsets[i]))
            else:
                disp_dense = np.linspace(x_subsets[i].min(), x_subsets[i].max(), len(x_target_subsets[i]))
                force_dense = np.interp(disp_dense, x_subsets[i], y_subsets[i])

            x_interp = np.concatenate((x_interp, disp_dense))
            y_interp = np.concatenate((y_interp, force_dense))

        return (x_interp, y_interp)

    def get_ranking(self, chromosome: Chromosome) -> Tuple[float, float]:
        """returns the ranking of how close a chromosome
        fits the target plot. The better it fits, lower
        the ranking value
        returns res: (force ranking, energy ranking)""" 

        avg_force = 0
        avg_energy = 0
        pinching4 = Pinching4Model(chromosome) #generate a pinching4 model with chromosome

        cycles = pinching4.hysteresis.cycle_number
        assert cycles == self.target_plot.cycle_number #assert number of model cycles match test cycles

        for cycle in range(cycles):
            #model data
            data = pinching4.hysteresis.get_cycle(cycle+1) #cycle index starts from 1
            force = np.array([point[1] for point in data])
            disp = np.array([point[0] for point in data])

            #test data
            target_data = self.target_plot.get_cycle(cycle+1)
            target_disp = np.array([point[0] for point in target_data])
            target_force = np.array([point[1] for point in target_data])

            # number of points is taken from the plot with the most number of points
            if len(disp) > len(target_disp):
                #interpolate test data to match number of points with model data
                target_disp, target_force = self._interpolate(target_disp, target_force, disp, force)
                self.points_num = len(disp)

            elif len(disp) < len(target_disp):
                #interpolate model data to match number of points with test data
                disp, force = self._interpolate(disp, force, target_disp, target_force) 
                self.points_num = len(target_disp) 

            else:
                self.points_num = len(disp)

            #assert x matches y
            assert len(target_force) == len(target_disp)
            assert len(force) == len(disp)

            assert len(target_disp) == len(disp) #assert interpolation worked

            # print(f"test points: {len(target_disp)}, model points: {len(disp)}, {self.points_num}")

            force_ranking = self._calculate_force_ranking(target_force, force)
            energy_ranking = self._calculate_energy_ranking(target_disp, target_force, disp, force)

            avg_force += force_ranking
            avg_energy += energy_ranking

        res = (avg_force/cycles, avg_energy/cycles)

        return res

    def _calculate_energy_ranking(self, target_disp: NDArray, target_force: NDArray,
                                  disp: NDArray, force: NDArray) -> float:
        numerator = 0
        denominator = 0

        for i in range(1, self.points_num):

            disp_array = disp[0:i+1]
            force_array = force[0:i+1]
            energy = integrate(abs(force_array), disp_array) #calculate energy upto ith point

            target_disp_array = target_disp[0:i+1]
            target_force_array = target_force[0:i+1]
            target_energy = integrate(abs(target_force_array), target_disp_array) #calculate energy upto ith point

            numerator += abs(target_energy - energy) 
            denominator += target_energy 

        return (numerator/denominator)

    def _calculate_force_ranking(self, target_force: NDArray, force: NDArray)-> float:
        
        numerator = 0
        denominator = 0
        for i in range(self.points_num):
            numerator += abs(target_force[i] - force[i])
            denominator += target_force[i]

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

