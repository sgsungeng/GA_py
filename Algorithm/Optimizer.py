# -*- coding: utf-8 -*-
'''
优化基本类文件，包含优化个体基本类 优化输入类，优化输出类，优化功能实现的基本类（没有实现，需要子类覆盖）
'''

from typing import List
import numpy as np

class OPIndividual:
    '''
    优化器的个体
    '''
    # 类变量
    numberOfArgument: int = 0 # 个体的实型参数个数
    restrain: List = []  # 约束函数数组 类型为[([float])->bool] 不等式，等式，以及其他约束都可以包含在其中
    minAndMax: (List[float], List[float]) = ([], []) #最大值，最小值数组
    aimFunc = None # 所求的目标函数
    def __init__(self, isGenerateArgum=False):
        # 对象变量
        self.argument:[float] = [] # 个体参数表示
        self.fitness: float = 0.0 # 适应度

    #
        if isGenerateArgum:
            min,max = OPIndividual.minAndMax
            while True: # 保证能够生成符合约束的个体
                for i in range(OPIndividual.numberOfArgument):
                    self.argument.append(np.random.uniform(min[i],max[i]))
                if self.isFitRestrain():
                    break
                else:
                    self.argument = []
            self.caculateFitness()

    def caculateFitness(self):
        '''
        计算个体适应度
        :return: 无
        '''
        self.fitness = OPIndividual.aimFunc(self.argument)

    def isFitRestrain(self) -> bool:
        '''
        检查所有参数是否合法函数
        :return:
        '''
        a = True
        for func in OPIndividual.restrain:
            if func(self.argument) == False:
                a = False
        return a


    def __str__(self):
        '''
        自定义描述方法
        :return: string
        '''
        restr = "适应度："
        restr += str(self.fitness)
        restr += "\n参数："
        li = list(map(str,[fit for fit in self.argument]))
        restr += "["
        for s in li:
            restr += s
            restr += ","
        restr += "]"
        restr.join(li)
        return restr

    def __cmp__(self, other):
        '''
        比较运算符自定义
        :param other:
        :return:
        '''
        if self.__eq__(other):
            return 0
        elif self.__lt__(other):
            return -1
        elif self.__gt__(other):
            return 1

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness


class OPOption:
    '''
    优化选项
    '''
    def __init__(self,cycleTimes: int = 2000,parentNum: int = 20, sonNumMulti: int = 7):
        self.cycleTimes = cycleTimes
        self.parentNum = parentNum
        self.sonNumMulti = sonNumMulti

class OPInputParam:
    '''
    优化参数，主要是为了快速构建优化输入参数
    '''
    def __init__(self,aimFunc,numberOfVar:int = 0,minArray: List[float] = [],maxArray: List[float] = [],otherRestrain:[] = []):
        self.aimFunc = aimFunc
        self.numberOfVar = numberOfVar
        self.minArray = minArray
        self.maxArray = maxArray
        self.otherRestrain = otherRestrain

class OPOutputParam:
    '''
    优化器输出类
    '''
    def __init__(self,fitnessIndividual: OPIndividual,population: List[OPIndividual],history: List[float]):
        self.fitnessIndividual = fitnessIndividual
        self.population = population
        self.history = history

class Optimizer:
    '''
    优化器类
    '''
    def __init__(self):
        self.optiHistory:[float] = [] # 每一代最优个体的适应度，给予保留
        self.population = [] # 种群
        self.fitness = None
    def optimiz(self,inputParam:OPInputParam,option:OPOption)->OPOutputParam:
        '''
        优化类通用方法，ju需要子类实现
        :param inputParam: 输入参数
        :param option: 优化参数
        :return: 输出参数
        '''

        pass

    def convert(self,inputParam:OPInputParam)->OPInputParam:
        '''
        将参数范围添加到约束中
        :param inputParam:
        :return:
        '''
        input = inputParam
        restrain = inputParam.otherRestrain
        restrain.append(lambda x: self.minAndMaxRestrin(x,inputParam.minArray,inputParam.maxArray))
        input.otherRestrain = restrain
        return input
    def printPopulation(self):
        for indi in self.population:
            print(indi)
    def minAndMaxRestrin(self, p:[float],minArray:[float],maxArray:[float])->bool:
        '''
        最大值最小值约束函数，辅助lambad表达式
        :param p: 传入参数
        :param minArray: 最小值数组
        :param maxArray: 最大值数组
        :return:
        '''
        a = True
        for i in range(len(p)):
            if p[i] > minArray[i] and p[i] < maxArray[i]:
                pass
            else:
                a = False
        return a