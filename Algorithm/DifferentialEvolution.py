# -*- coding: utf-8 -*-
# 差分进化
from Optimizer import *
import numpy as np
import copy

class DEIndividual(OPIndividual):
    cachePool = [] # 缓存池
    def productChildWith(self,individual1, individual2):
        neIndividual:DEIndividual = None
        if len(DEIndividual.cachePool) == 0:
            neIndividual = DEIndividual()
        else:
            neIndividual = DEIndividual.cachePool.pop()

        while True:
            neIndividual.argument =  []
            random = np.random.normal()
            count = np.random.randint(len(self.argument))
            di = np.random.randint(len(self.argument),size=count)
            for item in self.argument:
                neIndividual.argument.append(item)
            for item in di:
                neIndividual.argument[item] = self.argument[item] + random * (individual1.argument[item] - individual2.argument[item])
            if neIndividual.isFitRestrain():
                neIndividual.caculateFitness()
                break
        if(self.fitness > neIndividual.fitness):
            DEIndividual.cachePool.append(neIndividual)
            return self
        else:
            DEIndividual.cachePool.append(self)
            return neIndividual

class DEOptimize(Optimizer):

    def optimiz(self, inputParam: OPInputParam, option: OPOption = OPOption()) -> OPOutputParam:
        self.option = option

        inputParam = self.convert(inputParam)
        OPIndividual.aimFunc = inputParam.aimFunc
        OPIndividual.restrain = inputParam.otherRestrain
        OPIndividual.numberOfArgument = inputParam.numberOfVar
        print(OPIndividual.restrain)
        OPIndividual.minAndMax = (inputParam.minArray, inputParam.maxArray)
        self.initPopulation(self.option.parentNum)
        for _ in range(self.option.cycleTimes):
            self.mutation(self.option.parentNum)
            so = sorted(self.population,reverse=True)
            fi = so[0]
            if self.fitness is None:
                self.fitness = fi
            elif self.fitness < fi:
                self.fitness = fi
            self.optiHistory.append(self.fitness.fitness)
        return OPOutputParam(fitnessIndividual=self.fitness,population=self.population,history=self.optiHistory)

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
            self.population.append(DEIndividual(isGenerateArgum=True))

    def mutation(self,count: int):
        '''
        进化
        :param count: 种群规模
        :return:
        '''
        for i in range(count):
            newIndex = np.random.randint(len(self.population),size=2)
            i1 = self.population[newIndex[0]]
            i2 = self.population[newIndex[1]]
            self.population[i] = self.population[i].productChildWith(i1,i2)
