from abc import abstractmethod
import copy
from typing import Callable, List, Dict

class Parameter:
    """restrictions associated with a parameter"""

    def __init__(self, value: float, lower_bound: float, upper_bound: float):
        self.value = value
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def set_value(self, value):

        self.value = value

    def set_lower_bound(self, bound: float):

        self.lower_bound = bound

    def set_upper_bound(self, bound: float):

        self.upper_bound = bound


class Chromosome:

    def __init__(self, chromosome: Dict[str, Parameter]):

        self.chromosome = copy.deepcopy(chromosome)
        self.length = len(chromosome)

    def change_parameter_value(self, key:str, value: float):

        if key in self.chromosome:
            self.chromosome[key].set_value(value)
        else:
            raise KeyError(f"Parameter {key} does not exist")

    def get_parameter(self, key: str) -> Parameter:

        if key in self.chromosome:
            return copy.deepcopy(self.chromosome[key])
        else:
            raise KeyError(f"Parameter {key} does not exist")

    def __iter__(self):
        """Returns an iterator over chromosome"""

        return iter(self.chromosome)
    
    def __str__(self) -> str:

        return f"{self.chromosome}"

class Population:

    def __init__(self, population: List[Chromosome] = []):

        self.population_size = len(population)
        self.population = copy.deepcopy(population)

    def get_chromosome(self, index: int) -> Chromosome:

        """get chromosome data at a given index"""

        if index < self.population_size and index >= 0:
            return copy.deepcopy(self.population[index])
        else:
            raise IndexError("Invalid index")

    def pop(self):

        """remove chromosome at index -1"""

        self.population.pop()
        self.population_size -= 1

    def add_chromosome(self, chromosome: Chromosome) -> None:

        """add a chromosome at index -1"""

        self.population.append(chromosome)
        self.population_size += 1
    
    def replace(self, index: int, chromosome: Chromosome):

        self.population[index] = chromosome

    def __iter__(self):

        return iter(self.population)

    def sort(self, sorting_key: Callable):

        self.population = sorted(self.population, key=sorting_key,  reverse=True)

    def __str__(self) -> str:
        return f"{[str(chromosome) for chromosome in self.population]}"

class FitnessFunction:
    
    @abstractmethod
    def get_ranking(self, chromosome: Chromosome) -> float:
        pass



