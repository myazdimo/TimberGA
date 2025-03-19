from typing import Dict, List

from src.plot import HysteresisPlot
from src.pinching4 import openseesModel
from src.genetic import Chromosome

class Pinching4Model():
    """Class that takes a chromosome and models a pinching4 
    uniaxial material based on it"""

    def __init__(self, chromosome: Chromosome):
        
        self.chromosome = chromosome

        #parsing function to get parameter data
        self.parse = lambda key: self.chromosome.get_parameter(key).value  
        
        self.hysteresis = HysteresisPlot()
        data = openseesModel(self.parse, self.chromosome.boundaries)      
        self._prep_hysteresis(data)

    def _prep_hysteresis(self, data: Dict[str, List[float]]):
        """splits the model data into cycles and adds them to
        the hysteresis object"""

        disp = data["Displacement"]
        force = data["Moment"]
        points = len(disp)
        disp_cycle = []
        force_cycle = []
        switch = False #default state of the graph

        for point in range(points):
            if force[point] < 0:
                switch = True #flip state as soon as force is negative

            #reset cycle when point hits first quadrant again or if at last point
            if (switch and disp[point] >= 0 and force[point] > 0) or point == points-1:
                self.hysteresis.add_cycle(disp_cycle, force_cycle)
                #reset force and displacement values
                #start of new cycle
                disp_cycle = []
                force_cycle = []
                switch = False #flip state to default when point is in first quadrant again

            disp_cycle.append(disp[point])
            force_cycle.append(force[point])

    def plot(self):

        #plot using pinching4 function
        openseesModel(self.parse, self.chromosome.boundaries, plotting=True)
