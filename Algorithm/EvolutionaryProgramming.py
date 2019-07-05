# -*- coding: utf-8 -*-

#进化规划
from Optimizer import *
import numpy as np
import copy
import math

class EPIndividual(OPIndividual):
    cachePool = []

    def __init__(self, isGenerateArgum=False):
        super(EPIndividual, self).__init__(isGenerateArgum=False)
        self.standardDeviation:[float] = []
        self.p1: float = 200
        self.winTime = 0
        min, max = OPIndividual.minAndMax
        if isGenerateArgum:
            while True:
                for i in range(OPIndividual.numberOfArgument):
                    self.argument.append(np.random.uniform(min[i], max[i]))
                if self.isFitRestrain():
                    break
                else:
                    self.argument = []
            self.standardDeviation = np.random.ranf(size=len(self.argument))
            self.caculateFitness()

    def productChild(self,count: int):
        re:[EPIndividual] = []
        for _ in range(count):
            if EPIndividual.cachePool.__len__():
                item = EPIndividual.cachePool.pop()
            else:
                item = EPIndividual()
            item.standardDeviation = []
            item.argument = []
            while True:
                for i in range(OPIndividual.numberOfArgument):
                    newValue = self.argument[i] + math.sqrt(math.fabs(self.fitness))* np.random.normal()
                    item.argument.append(newValue)
                if item.isFitRestrain():
                    item.caculateFitness()
                    for i in range(OPIndividual.numberOfArgument):
                        sigma = self.standardDeviation[i] + np.random.normal()
                        item.standardDeviation.append(sigma)
                    break
                else:
                    item.argument = []

            re.append(item)
        return re


class EPOption(OPOption):
    def __init__(self,cycleTimes: int = 10000,parentNum: int = 100, sonNumMulti: int = 7,Q = 0.2):
        super(EPOption,self).__init__(cycleTimes=cycleTimes,parentNum=parentNum, sonNumMulti= sonNumMulti)
        self.Q = Q
class EPOptimizer(Optimizer):
    def optimiz(self,inputParam:OPInputParam,option:OPOption = EPOption())->OPOutputParam:
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
            self.mutating(self.option.sonNumMulti)
            self.select(self.option.parentNum,Q=self.option.Q)
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
            self.population.append(EPIndividual(isGenerateArgum=True))

    def mutating(self,multi: int):
        EPIndividual.cachePool = self.sonPoulation
        self.sonPoulation = []
        for item in self.population:
            self.sonPoulation += item.productChild(count=multi)

    def select(self,count,Q: float):#Q竞争法
        trails = [] #裁判
        self.sonPoulation += self.population
        r = np.random.randint(self.sonPoulation.__len__(),size=int(self.sonPoulation.__len__()* Q))
        trails = list(map(lambda x: self.sonPoulation[x],r))
        # trails = self.sonPoulation[r]
        for item in self.sonPoulation:
            item.winTime = 0
            for tr in trails:
                if item > tr:
                    item.winTime += 1
        self.sonPoulation.sort(key=lambda l:l.winTime,reverse=True)
        self.population = self.sonPoulation[:count]
        self.sonPoulation = self.sonPoulation[count:]
        if self.fitness is None or self.fitness < self.population[0]:
            self.fitness = self.population[0]


