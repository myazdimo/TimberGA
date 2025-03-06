from optimization import OptimizationModel
from plot import HysteresisPlot

plot = HysteresisPlot("graph") 

model = OptimizationModel(target_plot=plot,
                          population_size=200, generations=10)
model.load()
model.run()
