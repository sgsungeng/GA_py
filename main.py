# -*- coding: utf-8 -*-

import TestFunc
import GeneticAlgorithm as ga
import DifferentialEvolution as de
import matplotlib.pyplot as plt
import EvolutionStrategy as es
import EvolutionaryProgramming as ep
import ParticleSwarmOptimization as pso
import ArtificalBeeColony as abc
import time




testfunc = TestFunc.getFunc() #测试函数
ops = []
# ops.appe nd(ga.GAOptimizer())
# ops.append(de.DEOptimize())
# ops.append(es.ESOPtimizer())
ops.append(ep.EPOptimizer())
# ops.append(pso.PSOOptimizer())
# ops.append(abc.ABCOptimizer())
for op in ops:
    for _ in range(10):
        output = op.optimiz(testfunc)
        plt.plot(output.history)
        ti = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
        file = open('/Users/gengsun/Desktop/img/' + ti + '.txt', 'w');
        file.write(str(output.history));
        file.close();
        plt.savefig("/Users/gengsun/Desktop/img/" + ti + '.png')
        plt.show()
        print(output.fitnessIndividual.fitness)
