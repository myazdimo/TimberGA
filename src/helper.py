import numpy as np
from numpy._typing import NDArray

def integrate(y: NDArray, x: NDArray) -> float:

    x_subsets = []
    y_subsets = []
    temp_x = np.array([x[0]])
    temp_y = np.array([y[0]])
    area = 0
    trend = None #None by default

    for i in range(1, len(x)):
        temp_x = np.append(temp_x, x[i])
        temp_y = np.append(temp_y, y[i])

        if i+1 == len(x): 
            x_subsets.append(temp_x)
            y_subsets.append(temp_y)
            break

        if x[i] > x[i-1]:
            trend = True #increasing

        elif x[i] < x[i-1]:
            trend = False #decreasing

        if trend and x[i+1] < x[i]:
            x_subsets.append(temp_x)
            y_subsets.append(temp_y)
            temp_x = np.array([])
            temp_y = np.array([])

        if not trend and x[i+1] > x[i]:
            x_subsets.append(temp_x)
            y_subsets.append(temp_y)
            temp_x = np.array([])
            temp_y = np.array([])

    for i in range(len(x_subsets)):
        area += abs(np.trapz(y_subsets[i],x_subsets[i]))

    return area


