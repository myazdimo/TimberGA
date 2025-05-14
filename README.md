# Genetic Algorithm-Based Optimization for Pinching4 Material
## Introduction
The program is designed to assist engineers and researchers in calibrating the Pinching4 model to fit their test data.

The program begins by receiving a user-provided hysteresis plot (the “test data”), which is then decomposed into individual loading cycles. Additionally, the user specifies the upper and lower bounds for the parameters to optimizate while also defining which parameters remain constant. For constant parameters, the user must explicitly provide their values.

Library `geatpy` (https://github.com/geatpy-dev/geatpy) is used as the toolbox for the genetic algortihm

Once the parameters are configured, the user determines the population size and the number of generations for the genetic algorithm. The program employs multiprocessing capabilities, utilizing 10 CPU cores to process 10 individuals in each generation simultaneously, significantly reducing computation time.

For parameter descriptions, refer to OpenSees documentation: https://opensees.berkeley.edu/wiki/index.php/Pinching4_Material

## Optimization
The optimization process is driven by two objective functions:
- Cumulative Force Error (CFE) – Measures the deviation between the simulated and experimental force response.
- Cumulative Energy Error (CEE) – Measures the difference in energy dissipation between the model and experimental data.

## Results
Upon completion, the program outputs a set of optimized parameters along with two visualization plots:
- Plot of the best force ranking achieved as a function of iterations.
- Plot of the best energy ranking achieved as a function of iterations.
- A comparison plot of test data and model data, where the model data is generated using the optimal parameter set.

## Requirements
All library dependencies can be installed by running the command:

```sh
pip install -r requirements.txt
```

Note: If you run into an issue while installing `geatpy`, directly downloading the 2.7.0 version from their [website](https://pypi.org/project/geatpy/#files), and pip install it using that wheel.


## Usage
To achieve a set of optimized parameters, follow these steps: -

**Step 1: Modify the `parameters.json` file**:

Each parameter is classified as either a variable or a constant.

**Variable**: The format for modifying the boundaries of a variable is as below.

`"ePf1": { "nature": "variable", "lower_bound": 0.6, "upper_bound": 0.85 }`

In this example, `ePf1` is the name of the parameter, `nature` is set to “variable”, `lower_bound` is 0.6 and `upper_bound` is 0.85.
To adjust the boundaries, simply update the corresponding values. Both the lower and upper bounds values must be specified as floating-point numbers.

**Constant**: The format for modifying the boundaries of a constant is as below.

`"rDispP": { "nature": "constant", “value”: 0.7 }`

In this example, `rDispP` is the name of the parameter, `nature` is set to “constant”, and `value` is 0.7.
To adjust the constant, simply update the value. The value must be specified as floating-point number.

**Note**: A _constant_ can be changed to a _variable_ and vice versa, provided that the format is strictly maintained.
A _constant_ cannot have the fields `lower_bound` and `upper_bound`, similarly a _variable_ cannot have the field `value`.

**Step 2: Select the test data**:

select the data set by changing the `path` of the dataset ("graph1", "graph2", etc) passed into class `HysteresisPlot()` which is assigned to `self.target_plot` in file `geatpy/model.py`

**Step 3: Run**:

Run the `geatpy/main.py` file
