# -*- coding: utf-8 -*-


import numpy as  np
import math
from Optimizer import *

def func1(p:[float])->float:

    if p[0] == 0:
        p[0] = 0.01
    return 10 + math.sin(1.0/p[0])/(pow(p[0]-0.16,2) + 0.1)
def func3(p:[float])->float:
    x = p[0]
    y = p[1]
    return -(pow(x,2) + pow(y,2)-0.3 * math.cos(3 * math.pi * x)+ 0.3 * math.cos(4 * np.pi * y) + 0.3)
def getTestFun()->[OPInputParam]:
    testFunc:[OPInputParam] = []
    #函数1
    testFunc.append(OPInputParam(aimFunc=func1,
                                 numberOfVar=1,
                                 minArray=[-0.5],
                                 maxArray=[0.5]))
    #函数3
    testFunc.append(OPInputParam(aimFunc=func3,numberOfVar=2,minArray=[-1,-1],maxArray=[1,1]))


    return testFunc

def aimFunc1(p:[float]):
    p = np.array(p)
    # y = 0
    p = p * np.sin(np.sqrt(np.abs(p)))
    # for i in range(len(p)):
    #     y += p[i] * math.sin(math.sqrt(abs(p[i])))
    return np.squeeze(np.sum(p))


def getFunc()->OPInputParam:
    n = 20
    minArray = []
    maxArray = []
    for _ in range(n):
        minArray.append(-500.0)
        maxArray.append(500.0)


    ret = OPInputParam(aimFunc=aimFunc1,
                       numberOfVar=n,
                       minArray=minArray,
                       maxArray=maxArray)
    return ret