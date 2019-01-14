# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :logistic Regression


    #note：
    # transpose 矩阵转置
    # mat ：list转化为矩阵

'''
from numpy import *
import matplotlib.pyplot as plt

def loadDataSet():
    """

    :return:
    """
    dataMatrix = []
    dataLabel = []

    #读取文件
    f = open('testSet.txt')
    for line in f.readlines():
        # print(line)
        lineList = line.strip().split()
        dataMatrix.append([1,float(lineList[0]),float(lineList[1])])
        dataLabel.append(int(lineList[2]))

    # for i in range(len(dataMatrix)):
    #     print(dataMatrix[i])
    # print(dataLabel)
    # print(mat(dataLabel).transpose())

    matLabel = mat(dataLabel).transpose()
    return dataMatrix,matLabel


def sigmoid(inX):
    """
    sigmoid函数
    :param inX:
    :return:
    """
    return  1/(1+exp(-inX))

def graAscent(dataMatrix,matLabel):
    """
    梯度上升发，每次参数迭代，都需要遍历整个数据集
    :param dataMatrix: 数据集
    :param matLabel: 标签
    :return:
    """
    m ,n = shape(dataMatrix)
    matMatrix = mat(dataMatrix)

    w = ones((n,1))

    alpha = 0.001
    num = 500

    for i in range(num):
        error = sigmoid(matMatrix*w) - matLabel
        w = w -alpha * matMatrix.transpose() * error

    return w

def stoGraAscent(dataMatrix,matLabel):
    """
    随机梯度上升法
    :param dataMatrix:
    :param matLabel:
    :return:
    """
    m,n = shape(dataMatrix)
    matMatrix = mat(dataMatrix)

    w = ones((n,1))
    alpha = 0.001
    num = 20

    for i in range(num):
        for j in range(m):
            error = sigmoid(matMatrix[j]*w)-matLabel[j]
            w = w - alpha * matMatrix[j].transpose() * error

    return w


def stocGraAscent1(dataMatrix,matLabel):
    """
    改进后的随机梯度上升法
    改进 1 ：对于学习率 α 采用非线性下降的方式使得每次都不一样
    改进 2 ：每次使用一个数据，但是每次随机选择的数据，选过的不再进行选择
    :param dataMatrix:
    :param matLabel:
    :return:
    """
    m,n = shape(dataMatrix)
    matMatrix = mat(dataMatrix)

    w = ones((n,1))
    num = 200
    setIndex = set([])
    for i in range(num):
        for j in range(m):
            alpha = 4/(i+j+1) +0.01

            dataIndex = random.randint(0,100)
            while dataIndex in setIndex:
                setIndex.add(dataIndex)
                dataIndex = random.randint(0,100)
            error = sigmoid(matMatrix[dataIndex]*w) - matLabel[dataIndex]
            w = w - alpha * matMatrix[dataIndex].transpose()*error

    return w

def  draw(weight):
    """
    绘制图像
    :param weight:
    :return:
    """

    x0List = []
    y0List = []

    x1List = []
    y1List = []

    f = open('testSet.txt','r')

    for line in f.readlines():
        lineList = line.strip().split()
        if lineList[2] == '0':
            x0List.append(float(lineList[0]))
            y0List.append(float(lineList[1]))
        else:
            x1List.append(float(lineList[0]))
            y1List.append(float(lineList[1]))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x0List,y0List,s=10,c='red')
    ax.scatter(x1List,y1List,s=10,c='green')

    xList=[]
    yList=[]
    x = arange(-3,3,0.1)
    for i  in arange(len(x)):
        xList.append(x[i])
    y = (-weight[0] - weight[1] * x) / weight[2]

    for j in arange(y.shape[1]):
        yList.append(y[0,j])

    ax.plot(xList,yList)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.show()


if __name__ == '__main__':
    dataMatrix ,matLabel = loadDataSet()
    weight = stocGraAscent1(dataMatrix,matLabel)
    print(weight)
    draw(weight)



 









    