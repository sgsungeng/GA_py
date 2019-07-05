# -*- coding: utf-8 -*-

#蜂群算法

from Optimizer import *
import numpy as np
import copy


class ABCIndividual(OPIndividual):
    followers = [] #观察蜂仅做临时保存用
    maxFlag = 0
    def __init__(self):
        super(ABCIndividual,self).__init__(isGenerateArgum=True)
        self.flag = 0
        self.bestFitness = self.fitness
        self.bestFitness_info = self.argument
    def search(self, otherBee)->bool:
        if self.flag < ABCIndividual.maxFlag:
            while(True):
                self.argument = self.argument + np.random.uniform(-1, 1, size=OPIndividual.numberOfArgument).T * (
                            np.array(self.argument) - np.array(otherBee.argument))
                if self.isFitRestrain():
                    self.caculateFitness()
                    if self.fitness > self.bestFitness:
                        self.bestFitness = self.fitness
                        self.bestFitness_info = self.argument
                        self.flag = 0
                    else:
                        self.fitness = self.bestFitness
                        self.argument = self.bestFitness_info
                        self.flag += 1

                    break
                else:
                    self.argument = self.bestFitness_info
            return True
        else:
            return False
    def rerandom(self):
        min, max = OPIndividual.minAndMax
        self.argument = []
        while True:  # 保证能够生成符合约束的个体
            for i in range(OPIndividual.numberOfArgument):
                self.argument.append(np.random.uniform(min[i], max[i]))
            if self.isFitRestrain():
                break
            else:
                self.argument = []
        self.caculateFitness()
        self.bestFitness = self.fitness
        self.bestFitness_info = self.argument
        self.flag = 0

    def learnFromOther(self,other):
        while True:
            self.argument = other.argument + np.random.uniform(-1, 1, size=OPIndividual.numberOfArgument)
            if self.isFitRestrain():
                self.caculateFitness()
                self.bestFitness = self.fitness
                self.bestFitness_info = self.argument
                self.flag = 0
                break
            else:
                self.argument = []



class ABCOption(OPOption):
    def __init__(self,cycleTimes: int = 10000,parentNum: int = 200, sonNumMulti: int = 0,maxFlag: int = 5,numnberOfemploye:float = 0.7):
        super(ABCOption,self).__init__(cycleTimes=cycleTimes,parentNum=parentNum)
        self.maxFlag = maxFlag #最大停留时间
        self.numberOFemployer =numnberOfemploye

class ABCOptimizer(Optimizer):
    def optimiz(self, inputParam: OPInputParam, option: OPOption = ABCOption()) -> OPOutputParam:


        inputParam = self.convert(inputParam)
        OPIndividual.aimFunc = inputParam.aimFunc
        OPIndividual.restrain = inputParam.otherRestrain
        OPIndividual.numberOfArgument = inputParam.numberOfVar
        OPIndividual.minAndMax = (inputParam.minArray, inputParam.maxArray)
        self.option = option
        ABCIndividual.maxFlag = option.maxFlag
        self.initPopulation(self.option.parentNum)

        for _ in range(option.cycleTimes):
            self.update(self.option.numberOFemployer)
            self.population.sort(reverse=True) #排序
            self.fitness = self.population[0]
            self.optiHistory.append(self.fitness.fitness)
        return OPOutputParam(self.fitness, self.population, self.optiHistory)


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
            self.population.append(ABCIndividual())
    def update(self, rate:float):
        #将蜂群划分为采蜜蜂和跟随蜂
        ABCIndividual.followers = self.population[int(len(self.population) * rate):]
        self.population = self.population[0:int(len(self.population) * rate)]
        randoms = np.random.randint(len(self.population),size=len(self.population))
        # 采蜜蜂到附近寻优
        for i in range(len(self.population)):
            re = self.population[i].search(self.population[randoms[i]])
            if re == False:
            #采蜜蜂附近寻优失败，变为侦查蜂，重新找
                self.population[i].rerandom()
        #跟随蜂，依据概率跟随
        sum = 0
        for item in self.population:
            sum += item.fitness
        probBility = list(map(lambda x: x.fitness / sum, self.population))
        rans = np.random.ranf(size=len(ABCIndividual.followers))
        i = 0
        k = 0
        maxlen = len(probBility)
        newArray = []
        while ABCIndividual.followers.__len__() > k:
            le = 0
            while True:
                if i >= maxlen:
                    i = 0
                le += probBility[i]
                if le > rans[k]:
                    ABCIndividual.followers[k].learnFromOther(self.population[i])
                    self.population.append(ABCIndividual.followers[k])
                    k += 1
                    break
                i += 1

        # #为了避免早熟 ，将跟随蜂变为随机搜寻
        # for item in ABCIndividual.followers:
        #     item.rerandom()
        #     self.population.append(item)



