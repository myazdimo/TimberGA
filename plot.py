import os
from typing import List, Dict

class HysteresisPlot:

    """ a class that represents a hysteresis plot"""

    def __init__(self, dir_path: str):
        
        self.cycle_number = len(os.listdir(dir_path)) #number of cycles in the plot 
        self.data = self._prep_data(dir_path, self.cycle_number)
        
    def _prep_data(self, path: str, num: int) -> Dict[int, List[List[float]]]:

        """returns a dictionary with key = cycle index
        and value = list of data points where each element is
        in the form of [x, y]"""

        data = {}
        for i in range(1, num+1):
            
            data[i] = self._extract(f"{path}/{i}.txt")

        return data

    def __iter__(self):

        return iter(self.data)

    def get_cycle(self, cycle_num: int) -> List[List[float]]:

        """return a specific cycle"""

        return self.data[cycle_num]

    def get_point(self, cycle_num: int, point_num: int) -> List[float]:

        """returns a data point in a specific cycle at a specific index
        in the form of [x, y]"""

        return self.data[cycle_num][point_num]

    def _extract(self, path) -> List:
        
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


