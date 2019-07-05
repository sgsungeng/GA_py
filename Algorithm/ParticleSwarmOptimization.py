# -*- coding: utf-8 -*-

from Optimizer import *
import numpy as np
import copy

class PSOIndividual(OPIndividual):
    instant = None
    def __init__(self):
        super(PSOIndividual,self).__init__(isGenerateArgum=False)
        self.currentSpeed = []
        min, max = OPIndividual.minAndMax
        while True:
            for i in range(OPIndividual.numberOfArgument):
                self.argument.append(np.random.uniform(min[i], max[i]))
            if self.isFitRestrain():
                break
            else:
                self.argument = []

        self.argument = np.array(self.argument)
        self.caculateFitness()
        self.pBest = self.argument
        self.pBest_fitness = self.fitness
        self.currentSpeed = np.random.uniform(-1,1,size=OPIndividual.numberOfArgument)

    def update(self,w:float,c1:float,c2:float,gBest:[float]):
        min, max = OPIndividual.minAndMax
        if PSOIndividual.instant is None:
            PSOIndividual.instant = PSOIndividual()
        while True:
            PSOIndividual.instant.argument = self.argument
            arg = np.array(self.argument)
            PSOIndividual.instant.currentSpeed = w * self.currentSpeed + c1 * np.random.normal(size=len(self.currentSpeed)) \
                                * (self.pBest - arg) + c2 * np.random.normal(size=len(self.currentSpeed)) \
                                * (gBest.argument - arg)
            PSOIndividual.instant.currentSpeed = PSOIndividual.instant.currentSpeed / 10
            PSOIndividual.instant.argument = arg + PSOIndividual.instant.currentSpeed
            for i in range(OPIndividual.numberOfArgument):
                if PSOIndividual.instant.argument[i] > max[i]:
                    PSOIndividual.instant.argument[i] = max[i]- 0.1
                if PSOIndividual.instant.argument[i] < min[i]:
                    PSOIndividual.instant.argument[i] = min[i] + 0.1
            if PSOIndividual.instant.isFitRestrain():
                self.argument = PSOIndividual.instant.argument
                self.currentSpeed = PSOIndividual.instant.currentSpeed
                self.caculateFitness()
                if self.fitness > self.pBest_fitness:
                    self.pBest_fitness = self.fitness
                    self.pBest = self.argument
                break
class PSOOption(OPOption):
    def __init__(self, cycleTimes: int = 10000, parentNum: int = 200, sonNumMulti: int = 7,w:float = 1,c1:float = 1,c2:float=0.5 ):
        '''
        粒子群优化参数
        :param cycleTimes:
        :param parentNum:
        :param sonNumMulti:
        :param w: 1-w>=0
        :param c1:2w + 2>= c1 + c2
        :param c2:
        '''
        super(PSOOption,self).__init__(cycleTimes=cycleTimes,parentNum=parentNum,sonNumMulti=0)
        self.w = w
        self.c1 = c1
        self.c2 = c2


class PSOOptimizer(Optimizer):
    def optimiz(self,inputParam:OPInputParam,option:OPOption =PSOOption()):
        self.option = option
        inputParam = self.convert(inputParam)
        OPIndividual.aimFunc = inputParam.aimFunc
        OPIndividual.restrain = inputParam.otherRestrain
        OPIndividual.numberOfArgument = inputParam.numberOfVar
        print(OPIndividual.restrain)
        OPIndividual.minAndMax = (inputParam.minArray, inputParam.maxArray)
        self.initPopulation(self.option.parentNum)
        po = sorted(self.population,reverse=True)
        self.fitness = po[0]
        for _ in range(self.option.cycleTimes):
            for item in self.population:
                item.update(option.w,option.c1,option.c2,self.fitness)
            so = sorted(self.population, reverse=True)
            fi = so[0]
            if self.fitness is None:
                self.fitness = fi
            elif self.fitness < fi:
                self.fitness = fi
            self.optiHistory.append(self.fitness.fitness)
        return OPOutputParam(fitnessIndividual=self.fitness, population=self.population, history=self.optiHistory)
    def initPopulation(self,populationSize:int):
        '''
        初始化种群
        :param populationSize: 种群大小
        :return: 无
        '''
        self.fitness = None
        self.population = []
        self.optiHistory = []
        for _ in range(populationSize):
            self.population.append(PSOIndividual())