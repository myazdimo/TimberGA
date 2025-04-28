from typing import Dict
from src.genetic import Parameter
import json

#parameters used to model the pinching4 uniaxial material used in opensees
# refer to https://openseespydoc.readthedocs.io/en/latest/src/Pinching4.html for information on parameters
# parameters = {
#     "ePf1": Parameter("variable", lower_bound=0.6, upper_bound=0.85),
#     "ePf2": Parameter("variable", lower_bound=6, upper_bound=8),
#     "ePf3": Parameter("variable", lower_bound=22, upper_bound=24),
#     "ePf4": Parameter("variable", lower_bound=24, upper_bound=25),
#     "ePd1": Parameter("variable", lower_bound=0.0001, upper_bound=0.0003),
#     "ePd2": Parameter("variable", lower_bound=0.04, upper_bound=0.06),
#     "ePd3": Parameter("variable", lower_bound=0.1, upper_bound=0.25),
#     "ePd4": Parameter("variable", lower_bound=0.25, upper_bound=0.4),
#
#     "eNf1": Parameter("variable", lower_bound=-0.85, upper_bound=-0.6),
#     "eNf2": Parameter("variable", lower_bound=-8, upper_bound=-6),
#     "eNf3": Parameter("variable", lower_bound=-24, upper_bound=-22),
#     "eNf4": Parameter("variable", lower_bound=-25, upper_bound=-24),
#     "eNd1": Parameter("variable", lower_bound=-0.0003, upper_bound=-0.0001),
#     "eNd2": Parameter("variable", lower_bound=-0.06, upper_bound=-0.04),
#     "eNd3": Parameter("variable", lower_bound=-0.25, upper_bound=-0.1),
#     "eNd4": Parameter("variable", lower_bound=-0.4, upper_bound=-0.25),
#
#     "rDispP": Parameter("constant", value=0.7),
#     "rForceP": Parameter("constant", value=0.155),
#     "uForceP": Parameter("constant", value=0.01012),
#     "rDispN": Parameter("constant", value=0.7),
#     "rForceN": Parameter("constant", value=0.155),
#     "uForceN": Parameter("constant", value=0.01012),
#     "gK1": Parameter("constant", value=1), 
#     "gK2": Parameter("constant", value=0.5),
#     "gK3": Parameter("constant", value=0.5),
#     "gK4": Parameter("constant", value=0.5),
#     "gKLim": Parameter("constant", value=0.01),
#     "gD1": Parameter("constant", value=0.5),
#     "gD2": Parameter("constant", value=0.5),
#     "gD3": Parameter("constant", value=1),
#     "gD4": Parameter("constant", value=0.8),
#     "gDLim": Parameter("constant", value=0.2),
#     "gF1": Parameter("constant", value=1),
#     "gF2": Parameter("constant", value=0),
#     "gF3": Parameter("constant", value=1), 
#     "gF4": Parameter("constant", value=1),
#     "gFLim": Parameter("constant", value=0.01),
#     "gE": Parameter("constant", value=10),
# }

parameters: Dict[str, Parameter] = {}

# Load JSON file
with open("../parameters.json", "r") as file:
    data = json.load(file)

for name, details in data["parameters"].items():
    if details["nature"] == "constant":
        # Create a constant parameter
        parameters[name] = Parameter(nature="constant", value=details["value"])

    else:
        # Create a variable parameter
        parameters[name] = Parameter(
            nature="variable",
            lower_bound=details["lower_bound"],
            upper_bound=details["upper_bound"]
        )
