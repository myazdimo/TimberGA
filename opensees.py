import copy
from typing import List
from pinching4 import openseesModel
from genetic import Chromosome

class Pinching4Model():
    """Class that takes a chromosome a models a pinching4 
    uniaxial material based on it"""

    def __init__(self, chromosome: Chromosome, plotting=False):

        self.chromosome = chromosome

        #parsing function to get parameter data
        self.parse = lambda key: self.chromosome.get_parameter(key).value  
        
        self.data = openseesModel(self.parse, plotting)

    def get_displacement(self) -> List:

        return copy.deepcopy(self.data["Displacement"])

    def get_moment(self) -> List:

        return copy.deepcopy(self.data["Moment"])
