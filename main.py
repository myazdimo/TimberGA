from genetic import FitnessFunction, Chromosome
from optimization import OptimizationModel
from plot import HysteresisPlot

class Function(FitnessFunction):

    def get_ranking(self, chromosome: Chromosome) -> float:

        value = 0
        for parameter in chromosome:
            value += chromosome.get_parameter(parameter).value
        
        print("value: ", value)
        return value


plot = HysteresisPlot("graph") 

model = OptimizationModel(target_plot=plot,
                          population_size=100, generations=1,
                          fitness_function=Function())

model.load()
model.run()
