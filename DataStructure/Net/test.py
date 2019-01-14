# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :

'''
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import math
import numpy as np

n=100

def aloha(p):
    res = []
    for i in p :
       y = n*p*(1-p)**((n-1))
       res.append(y)
    return res

def pAloha(p):
    res =[]
    for i in p:
        y = n*p*(1-p)**(2*(n-1))
        res.append(y)
    return res



if __name__ == "__main__":

    x1 = np.linspace(0,1/math.exp(1),100)
    x2 = np.linspace(0, 1/(math.exp(1)*2),100)
    y1 = [n*p*(1-p)**((n-1)) for p in x1]
    y2 = [n*p*(1-p)**(2*(n-1)) for p in x2]

    fig = plt.figure(figsize=(6,6))
    plt.plot(x1,y1,label="gapALOHA",color="red")
    plt.plot(x2,y2,label="pureALOHA",color="blue")
    plt.grid(True)
    plt.show()
