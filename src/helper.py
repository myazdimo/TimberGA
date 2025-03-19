from typing import Tuple, List
import numpy as np
from numpy._typing import NDArray

def splitter(y: NDArray, x: NDArray) -> Tuple[List[NDArray], List[NDArray], List[int]]:
    """splits y and x into subsets where each subset
    is monotonic. returns (x_subsets, y_subsets, order of monotonicity)
    order of monotonicity: 1 if increasing, -1 if decreasing"""

    order = []
    x_subsets = []
    y_subsets = []
    temp_x = np.array([x[0]])
    temp_y = np.array([y[0]])
    trend = None #None by default

    for i in range(1, len(x)):
        temp_x = np.append(temp_x, x[i])
        temp_y = np.append(temp_y, y[i])

        #stop loop and append to subset at last index
        if i+1 == len(x): 
            if len(temp_x) == 1:
                x_subsets[-1] = np.append(x_subsets[-1], temp_x[0])
                y_subsets[-1] = np.append(y_subsets[-1], temp_y[0])
                order.pop()
            else:
                x_subsets.append(temp_x)
                y_subsets.append(temp_y)
            break

        #Trend is increasing
        if x[i] > x[i-1]:
            trend = True #increasing
            if len(order) == 0 or order[-1] != 1:
                order.append(1)

        #Trend is decreasing
        elif x[i] < x[i-1]:
            trend = False #decreasing
            if len(order) == 0 or order[-1] != -1:
                order.append(-1)

        #change in trend from increasing to decreasing
        if trend and x[i+1] < x[i]:
            x_subsets.append(temp_x)
            y_subsets.append(temp_y)
            temp_x = np.array([])
            temp_y = np.array([])
            order.append(-1)

        #change in trend from decreasing to increasing
        if not trend and x[i+1] > x[i]:
            x_subsets.append(temp_x)
            y_subsets.append(temp_y)
            temp_x = np.array([])
            temp_y = np.array([])
            order.append(1)

    return (x_subsets, y_subsets, order)

def integrate(y: NDArray, x: NDArray) -> float:

    x_subsets, y_subsets, order = splitter(y, x)

    area = 0
    for i in range(len(x_subsets)):
        #calculate area for each subset
        area += abs(np.trapz(y_subsets[i],x_subsets[i]))

    return area


