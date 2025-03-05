import openseespy.opensees as ops
from genetic import Chromosome

class Pinching4Model():

    def __init__(self, chromosome: Chromosome):

        ops.wipe()

        self.chromosome = chromosome

        #parsing function to get parameter data
        self.parse = lambda key: self.chromosome.get_parameter(key).value  

        self.WBay = 1
        self.ndm = 2
        self.ndf = 3
        self.P_delta = 1
        self.load_model()

        self.R_F = 1.5  # Reinforced factor for force
        self.R_D = 2.0  # Reinforced factor for displacements
        self.DOF = [1,2]
        
        self.DL=0   #Uniform Dead Load
        self.GR=1
        self.Linear=1

        self.eleTags=[1, 2]

        self.Tol = 1.0e-6
        self.NstepGravity = 10
        self.DGravity = 1.0 / self.NstepGravity




    def load_model(self):

        ops.model('basic', '-ndm', self.ndm, '-ndf', self.ndf)
        ops.geomTransf('PDelta', self.P_delta)
        
        #define nodes
        ops.node(1, 0, 0)
        ops.fix(1, 1, 1, 1)
        ops.node(2, self.WBay, 0)
        ops.node(3, 0.01, 0)
        ops.node(4, 0.01, 0)

        ops.element('elasticBeamColumn', 1, 1,3,  0.0504, 12.800e6, 3.3e-4, 1)
        ops.element('elasticBeamColumn', 2, 4,2,  0.0504, 12.800e6, 3.3e-4, 1)

        parse = self.parse
        self.model = uniaxialMaterial('Pinching4', 100, 
                         parse("ePf1"), parse("ePd1"), parse("ePf2"), parse("ePd2"), parse("ePf3"), parse("ePd3"), parse("ePf4"), parse("ePd4"), 
                         parse("eNf1"), parse("eNd1"), parse("eNf2"), parse("eNd2"), parse("eNf3"), parse("eNd3"), parse("eNf4"), parse("eNd4"),
                         parse("rDispP"), parse("rForceP"), parse("uForceP"),
                         parse("rDispN"), parse("rForceN"), parse("uForceN"),
                         parse("gK1"), parse("gK2"), parse("gK3"), parse("gK4"), parse("gKLim"),
                         parse("gD1"), parse("gD2"), parse("gD3"), parse("gD4"), parse("gDLim"),
                         parse("gF1"), parse("gF2"), parse("gF3"), parse("gF4"), parse("gFLim"),
                         parse("gE"), "cycle") 


        element('zeroLength',10,3,4,'-mat',100,'-dir',6)
        equalDOF(3, 4, *DOF)


