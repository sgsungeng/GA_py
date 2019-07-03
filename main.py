# -*- coding: utf-8 -*-

import TestFunc
import GeneticAlgorithm as ga
import DifferentialEvolution as de
import matplotlib.pyplot as plt
import EvolutionStrategy as es
import EvolutionaryProgramming as ep
import ParticleSwarmOptimization as pso
import ArtificalBeeColony as abc




testfunc = TestFunc.getFunc() #测试函数
# history = []
# for inputP in testfunc:
#     op = de.DEOptimize()
#     op = es.ESOPtimizer()
#     output = op.optimiz(inputParam=inputP)
#     plt.plot(output.history)
#     plt.show()
#     print(output.fitnessIndividual.fitness)
# op = ga.GAOptimizer()
# op = de.DEOptimize()
# op = es.ESOPtimizer()
op = ep.EPOptimizer()
op = pso.PSOOptimizer()
op = abc.ABCOptimizer()
output = op.optimiz(testfunc)
plt.plot(output.history)
plt.show()
print(output.fitnessIndividual.fitness)
