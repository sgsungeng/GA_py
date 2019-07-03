# -*- coding: utf-8 -*-

#进化规划
from Optimizer import *
import numpy as np
import copy

class ESIndividual(OPIndividual):
    cachePool = []

    def __init__(self, isGenerateArgum=False):
        super(ESIndividual,self).__init__(isGenerateArgum =False)
        self.standardDeviation:[float] =[]
        self.p1:float = 200
        min, max = OPIndividual.minAndMax
        if isGenerateArgum:
            while True:
                for i in range(OPIndividual.numberOfArgument):
                    self.argument.append(np.random.uniform(min[i],max[i]))
                if self.isFitRestrain():
                    break
                else:
                    self.argument = []
            self.standardDeviation = np.random.ranf(size=len(self.argument))+1

            self.caculateFitness()
    def productChild(self,count: int,success: float):
        re = []
        for _ in range(count):
            if len(ESIndividual.cachePool) != 0:
                item = ESIndividual.cachePool.pop()
            else:
                item = ESIndividual()
            item.standardDeviation = []
            item.argument = []
            for i in range(OPIndividual.numberOfArgument):
                sigma = self.standardDeviation[i]
                if success - 0.2 > 0.00001:
                    sigma *= 1.22
                elif success - 0.2 < 0.00001:
                    sigma *= 0.82
                item.standardDeviation.append(sigma)

            while True:
                for i in range((OPIndividual.numberOfArgument)):
                    newValue = self.argument[i] + np.random.normal(item.standardDeviation[i])
                    item.argument.append(newValue)
                if item.isFitRestrain():
                    break
                else:
                    item.argument = []
            re.append(item)
        for item in re:
            item.caculateFitness()
        return re

class ESOption(OPOption):
    def __init__(self,cycleTimes: int = 300,parentNum: int = 80, sonNumMulti: int = 7,c_i = 1.22, c_d = 0.81):
        super(ESOption,self).__init__(cycleTimes=cycleTimes,parentNum=parentNum, sonNumMulti= sonNumMulti)
        self.c_i = c_i
        self.c_d = c_d

class ESOPtimizer(Optimizer):
    def optimiz(self,inputParam:OPInputParam,option:OPOption = ESOption())->OPOutputParam:
        '''
        优化类通用方法，需要子类实现
        :param inputParam: 输入参数
        :param option: 优化参数
        :return: 输出参数
        '''
        self.option = option
        inputParam = self.convert(inputParam)
        OPIndividual.numberOfArgument = inputParam.numberOfVar
        OPIndividual.aimFunc = inputParam.aimFunc
        OPIndividual.restrain = inputParam.otherRestrain
        OPIndividual.minAndMax = (inputParam.minArray, inputParam.maxArray)
        self.initPopulation(self.option.parentNum)
        for index in range(self.option.cycleTimes):
            ss = 0.2
            if index > 50:
                ss = self.sucssTime / index + 0.1
            self.mutating(self.option.sonNumMulti,ss)
            self.select(self.option.parentNum)
            self.optiHistory.append(self.fitness.fitness)
        return OPOutputParam(self.fitness,self.population,self.optiHistory)
    def initPopulation(self,populationSize:int):
        '''
        初始化种群
        :param populationSize: 种群大小
        :return: 无
        '''
        self.fitness = None
        self.sucssTime = 0
        self.sonPoulation = []
        self.population = []
        self.optiHistory = []
        for _ in range(populationSize):
            self.population.append(ESIndividual(isGenerateArgum=True))

    def mutating(self,multi: int,success: float):
        ESIndividual.cachePool = self.sonPoulation
        self.sonPoulation = []
        for item in self.population:
            self.sonPoulation += item.productChild(count=multi,success= success)

    def select(self,count):
        self.sonPoulation += self.population
        self.sonPoulation.sort(reverse=True)
        self.population = self.sonPoulation[:count]
        self.sonPoulation = self.sonPoulation[count:]
        if self.fitness is None:
            self.sucssTime += 1
        else:
            if self.population[0].fitness > self.fitness.fitness:
                self.sucssTime += 1
        self.fitness = self.population[0]


