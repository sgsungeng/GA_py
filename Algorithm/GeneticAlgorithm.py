# -*- coding: utf-8 -*-
'''
遗传算法文件

'''

from Optimizer import *
import numpy as np
import copy

class GAIndividual(OPIndividual):
    stepArray:[] #步长数组
    genelengthes:[int] = [] #基因长度数组

    @staticmethod
    def setStepArray(value):
        GAIndividual.stepArray = value
        GAIndividual.genelengthes = []
        minArray, maxArray = OPIndividual.minAndMax
        for i in range(len(minArray)):
            c = 0
            count = int((maxArray[i]-minArray[i])/GAIndividual.stepArray[i])
            while count > 0:
                c += 1
                count = count // 2
            GAIndividual.genelengthes.append(c)


    def __init__(self):
        '''
        为了保证十进制和二进制参数相互转换后都是合法的，不使用父类初始化参数
        '''
        super(GAIndividual,self).__init__(isGenerateArgum=False)
        # self.argument:[float] = []  # 个体参数表示
        # self.fitness: float = 0.0
        minArray, maxArray = OPIndividual.minAndMax
        while True:
            for i in range(len(minArray)):
                gen = np.random.uniform(minArray[i],maxArray[i])
                self.argument.append(gen)
            self.decimal2binary()
            self.binary2decimal()
            if self.isFitRestrain():
                break
            else:
                self.gene_binary = []
                self.argument = []
        self.caculateFitness()


    def binary2decimal(self):
        '''
        二进制转十进制
        :return: 无
        '''
        indexOfGene = 0
        cureentGeneIndex = 0
        minArray, maxArray = OPIndividual.minAndMax
        for lenth in GAIndividual.genelengthes:
            l = 0.0
            for i in range(cureentGeneIndex,cureentGeneIndex + lenth):
                l = l * 2 + float(self.gene_binary[i])
            self.argument[indexOfGene] = minArray[indexOfGene] + l * GAIndividual.stepArray[indexOfGene]
            indexOfGene += 1
            cureentGeneIndex += lenth

    def decimal2binary(self):
        '''
        十进制转二进制
        :return: 无
        '''
        self.gene_binary = []
        currentGeneIndex = 0
        minArray, maxArray = OPIndividual.minAndMax
        for i in range(len(self.argument)):
            step = int((self.argument[i] - minArray[i])/GAIndividual.stepArray[i])
            length = GAIndividual.genelengthes[i]
            for _ in range(currentGeneIndex,currentGeneIndex + length):
                self.gene_binary.append(step % 2)
                step = step // 2
            currentGeneIndex = currentGeneIndex + length

class GAOption(OPOption):
    '''
    遗传算法进化参数
    '''
    def __init__(self,cycleTimes: int = 10000,parentNum: int = 200, sonNumMulti: int = 0,crossRate:float = 0.7,mutateRate:float= 0.1,selectType:int = 1):
        '''
        遗传算法进化参数
        :param cycleTimes: 循环次数
        :param parentNum: 种群个数
        :param sonNumMulti: 子代个数，该算法没有子代不需要
        :param crossRate: 交叉概率
        :param mutateRate: 变异概率
        :param selectType: 选择算法，1为轮盘赌，当前仅实现轮盘赌
        '''
        super(GAOption,self).__init__(cycleTimes=cycleTimes,parentNum = parentNum,sonNumMulti= sonNumMulti)

        self.crossRate = crossRate
        self.mutateRate = mutateRate
        self.selectType = selectType


class GAOptimizer(Optimizer):
    def __init__(self):
        super(GAOptimizer,self).__init__()
        self.fitness:GAIndividual = None # 最好的个体
        self.option:GAOption = None


    def optimiz(self,inputParam:OPInputParam,option:GAOption = GAOption(), stepArray:[float] = []):
        '''
        优化主方法
        :param inputParam:输入参数
        :param option: 优化选项
        :param stepArray: 步长默认为0。01
        :return: 优化结果OPOutputParam对象
        '''
        self.option = option
        inputParam = self.convert(inputParam)
        OPIndividual.aimFunc = inputParam.aimFunc
        OPIndividual.restrain = inputParam.otherRestrain

        OPIndividual.minAndMax = (inputParam.minArray,inputParam.maxArray)
        if len(stepArray) == 0:
            stepArray = [0.01 for _ in range(inputParam.numberOfVar)]
        GAIndividual.setStepArray(stepArray)

        if inputParam.numberOfVar >= 5:
            self.option.parentNum = max(self.option.parentNum,200)

        self.initPopulation(self.option.parentNum)
        self.population.sort(reverse=True)
        pop = sorted(self.population)
        self.fitness = pop[0]
        self.optiHistory.append(self.fitness.fitness)
        for _ in range(self.option.cycleTimes):
            self.across()
            self.mutation()
            self.select()
            pop = sorted(self.population,reverse=True)
            fit = pop[0]
            if self.fitness > fit:
                random = np.random.randint(len(self.population))
                self.population[random] = self.fitness # 使用随机位置替换为最优值
            else:
                self.fitness = fit
            # self.printPopulation()
            self.optiHistory.append(self.fitness.fitness)
            # print(self.fitness.fitness)
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
            self.population.append(GAIndividual())

    def across(self):
        '''
        交叉操作
        :return:无
        '''
        for i in range(0,len(self.population) // 2):
            # 只交叉一半的个体
            random = np.random.uniform(0,1)
            if random > self.option.crossRate: #看是否需要交叉
                continue

            p1p = np.random.randint(len(self.population))
            p2p = np.random.randint(len(self.population))
            p1 = self.population[p1p] # 第一个个体
            p2 = self.population[p2p] # 第二个个体
            position = np.random.randint(0,len(GAIndividual.genelengthes))
            # 单点交叉
            a = p1.gene_binary[position]
            p1.gene_binary[position] = p2.gene_binary[position]
            p2.gene_binary[position] = a
            p1.binary2decimal()
            p2.binary2decimal()
            if p1.isFitRestrain() and p2.isFitRestrain():
                p1.caculateFitness()
                p2.caculateFitness()
            else: #当交叉不满足约束则不交叉
                a = p1.gene_binary[position]
                p1.gene_binary[position] = p2.gene_binary[position]
                p2.gene_binary[position] = a
                p1.binary2decimal()
                p2.binary2decimal()

    def mutation(self):
        '''
        变异操作
        :return:无
        '''
        for i in range(len(self.population)):
            random = np.random.uniform(0,1)
            if random > self.option.mutateRate:
                continue
            postion = np.random.randint(len(self.population[i].gene_binary))
            gene = 0 if self.population[i].gene_binary[postion] == 1 else 1
            self.population[i].gene_binary[postion] = gene
            self.population[i].binary2decimal()
            if self.population[i].isFitRestrain():
                self.population[i].caculateFitness()
            else:
                self.population[i].gene_binary[postion] = 0 if gene == 1 else 1

    def select(self):
        '''
        选择操作 当前仅实现轮盘赌
        :return:无
        '''
        if self.option.selectType == 1:
            so = sorted(self.population)
            if so[0].fitness - so[len(so)-1].fitness != 0:
                min = min = so[0].fitness
            else:
                return
            sum = 0.0
            for ind in self.population:
                sum += ind.fitness - min
            probability:[float] = [(ind.fitness - min) / sum for ind in self.population]

            qe:[float] = np.random.uniform(0,1,len(self.population))
            newPopulation = []
            cur = 0.0
            for q in qe:
                for index in range(len(probability)):
                    cur += probability[index]
                    if cur >= q:
                        newPopulation.append(copy.deepcopy(self.population[index]))
                        cur = 0
                        break
            self.population = newPopulation