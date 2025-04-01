from src.genetic import Parameter

#parameters used to model the pinching4 uniaxial material used in opensees
# refer to https://openseespydoc.readthedocs.io/en/latest/src/Pinching4.html for information on parameters
parameters = {
    "ePf1": Parameter("variable", 0.6, 0.85),
    "ePf2": Parameter("variable", 6, 8),
    "ePf3": Parameter("variable", 22, 24),
    "ePf4": Parameter("variable", 24, 25),
    "ePd1": Parameter("variable", 0.0001, 0.0003),
    "ePd2": Parameter("variable", 0.04, 0.06),
    "ePd3": Parameter("variable", 0.1, 0.25),
    "ePd4": Parameter("variable", 0.25, 0.4),
    "rDispP": Parameter("constant", 0.7, 0.71),
    "fFoceP": Parameter("constant", 0.155, 0.1551),
    "uForceP": Parameter("constant", 0.01012, 0.010121),
    "rDispN": Parameter("variable", 0.7, 0.71),
    "fFoceN": Parameter("variable", 0.155, 0.1551),
    "uForceN": Parameter("variable", 0.01012, 0.010121),
    "gK1": Parameter("constant", 1, 1.00001), 
    "gK2": Parameter("constant", 0.5, 0.51),
    "gK3": Parameter("constant", 0.5, 0.51),
    "gK4": Parameter("constant", 0.5, 0.51),
    "gKLim": Parameter("constant", 0.01, 0.011),
    "gD1": Parameter("constant", 0.5, 0.51),
    "gD2": Parameter("constant", 0.5, 0.51),
    "gD3": Parameter("constant", 1, 1.001),
    "gD4": Parameter("constant", 0.8, 0.81),
    "gDLim": Parameter("constant", 0.2, 0.21),
    "gF1": Parameter("constant", 1, 1.001),
    "gF2": Parameter("constant", 0, 0.0001),
    "gF3": Parameter("constant", 1, 1.001), 
    "gF4": Parameter("constant", 1, 1.00001),
    "gFLim": Parameter("constant", 0.01, 0.011),
    "gE": Parameter("constant", 10, 10.0001),
}

#parameters used to model the hysteretic uniaxial material used in opensees
# refer to https://openseespydoc.readthedocs.io/en/latest/src/Hysteretic.html for information on parameters
hysteretic_params = {
    "p1": Parameter("variable", 0.6, 0.85),
    "p2": Parameter("variable", 6, 8),
    "p3": Parameter("variable", 22, 24),
    "n1": Parameter("variable", 24, 25),
    "n2": Parameter("variable", 0.0001, 0.0003),
    "n3": Parameter("variable", 0.04, 0.06),
    "pinchx": Parameter("variable", 0.1, 0.25),
    "pinchy": Parameter("variable", 0.25, 0.4),
    "damage1": Parameter("constant", 0.7, 0.71),
    "damage2": Parameter("constant", 0.155, 0.1551),
    "beta": Parameter("constant", 0.01012, 0.010121),
}
