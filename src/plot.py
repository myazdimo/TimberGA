import copy
import os
import matplotlib.pyplot as plt
from typing import List, Dict 

def prep_data(dir_path: str) -> Dict[int, List[List[float]]]:
    """returns a dictionary with key = cycle index
    and value = list of data points where each element is
    in the form of [x, y]"""
    
    data = {}
    num = len(os.listdir(dir_path))
    for i in range(1, num+1):
        
        data[i] = extract(f"{dir_path}/{i}.txt")

    return data

def extract(path) -> List:
    """returns the collection of points associated
    with a cycle"""
    
    points = []

    with open(path, 'r') as file:
        lines = file.readlines()

    for line in lines[1:]:
        point = line.strip().split(',')
        point = [ float(number.strip()) for number in point]
        points.append(point) 

    return points

class HysteresisPlot:
    """ a class that represents a hysteresis plot

    data: a dictionary with key = cycle index
    and value = list of data points where each element is
    in the form of [x, y]"""

    def __init__(self, data: Dict[int, List[List[float]]] = {}):
        
        self.data = copy.deepcopy(data)
        self.cycle_number = len(data) #number of cycles in the plot 
        self.boundaries = self._extract_boundaries()
        
    def _extract_boundaries(self) -> List[float]:

        boundaries = []

        for cycle_num in range(1, self.cycle_number+1):
            cycle = self.get_cycle(cycle_num)
            force = [point[1] for point in cycle]
            disp = [point[0] for point in cycle]

            force_peak = max(force)
            disp_peak = disp[force.index(force_peak)] 
            boundaries.append(disp_peak)

        return boundaries

    def add_cycle(self, disp: List[float], force: List[float]):

        disp = copy.deepcopy(disp)
        force = copy.deepcopy(force)

        if len(disp) != len(force):
            raise Exception("displacement and force dont have the same length")

        self.data[self.cycle_number+1] = []
        self.data[self.cycle_number + 1] = [[d, f] for d, f in zip(disp, force)]
        
        self.cycle_number += 1

    def __iter__(self):

        return iter(self.data)

    def get_cycle(self, cycle_num: int) -> List[List[float]]:
        """return a specific cycle, cycle number starts from 1"""

        return copy.deepcopy(self.data[cycle_num])

    def get_point(self, cycle_num: int, point_num: int) -> List[float]:

        """returns a data point in a specific cycle at a specific index
        in the form of [x, y]"""

        return copy.deepcopy(self.data[cycle_num][point_num])

    def get_plot(self) -> Dict[str, List[float]]:
        """returns a dictionary with keys diplacement and moment
        where their value is a list of points"""

        data = {
            "Displacement": [],
            "Moment": []
        }
        for cycle in range(1, self.cycle_number+1):

            data["Displacement"] += [ point[0] for point in self.get_cycle(cycle)]
            data["Moment"] += [ point[1] for point in self.get_cycle(cycle)]

        return copy.deepcopy(data)

    def plot(self) -> None:

        data = self.get_plot()
        plt.plot(data["Displacement"], data["Moment"])
            
