from abc import abstractmethod
import copy
from typing import Callable, Iterator, List, Dict

class Parameter:
    """Restrictions and value associated with a parameter"""

    def __init__(self, value: float, lower_bound: float, upper_bound: float):
        self.value = value
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def set_value(self, value) -> None:

        self.value = value

    def set_lower_bound(self, bound: float) -> None:

        self.lower_bound = bound

    def set_upper_bound(self, bound: float) -> None:

        self.upper_bound = bound


class Chromosome:
    """Class that represents a set of parameters.
    each chromose represents a possible uniaxial material model"""

    def __init__(self, chromosome: Dict[str, Parameter]):

        self.chromosome = copy.deepcopy(chromosome)
        self.length = len(chromosome)

    def change_parameter_value(self, key:str, value: float) -> None:

        if key in self.chromosome:
            self.chromosome[key].set_value(value)
        else:
            raise KeyError(f"Parameter {key} does not exist")

    def get_parameter(self, key: str) -> Parameter:
        """returns the copy of a parameter"""

        if key in self.chromosome:
            return copy.deepcopy(self.chromosome[key])
        else:
            raise KeyError(f"Parameter {key} does not exist")

    def __iter__(self) -> Iterator:
        """Returns an iterator over chromosome"""

        return iter(self.chromosome)
    
    def __str__(self) -> str:
        """string representation of Chromose"""

        return f"{self.chromosome}"

class Population:
    """Class that represents a collection of chromosomes.
    Each population represents a single generation"""

    def __init__(self, population: List[Chromosome] = []):

        self.population_size = len(population)
        self.population = copy.deepcopy(population)

    def get_chromosome(self, index: int) -> Chromosome:
        """get chromosome data at a given index"""

        if index < self.population_size and index >= 0:
            return copy.deepcopy(self.population[index])
        else:
            raise IndexError("Invalid index")

    def pop(self) -> None:
        """remove chromosome at index -1"""

        self.population.pop()
        self.population_size -= 1

    def add_chromosome(self, chromosome: Chromosome) -> None:
        """add a chromosome at index -1"""

        self.population.append(chromosome)
        self.population_size += 1
    
    def replace(self, index: int, chromosome: Chromosome):
        """replace chromosome at a given index"""

        self.population[index] = chromosome

    def __iter__(self) -> Iterator:

        return iter(self.population)

    def sort(self, sorting_key: Callable) -> None:
        """sort the population based on the sorting key"""

        self.population = sorted(self.population, key=sorting_key)

    def __str__(self) -> str:
        """string representation of Population"""

        return f"{[str(chromosome) for chromosome in self.population]}"

class FitnessFunction:
    """Interface class for a selection function"""    

    @abstractmethod
    def get_ranking(self, chromosome: Chromosome) -> float:
        pass



