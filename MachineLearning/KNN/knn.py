# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :

'''
import numpy as np
import operator
import os



#创建dataset
def createDataSet():
    group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']

#k-nn
def classify0(inX ,dataSet,lables,k):

    dataSetSize =dataSet.shape[0] #shape 返回一个矩阵的行数和列数

    diffMat =np.tile(inX,(dataSetSize,1)) -dataSet

    sqDiffMat = diffMat**2

    #当axis为0时,是压缩行,即将每一列的元素相加,将矩阵压缩为一行
    #当axis为1时,是压缩列,即将每一行的元素相加,将矩阵压缩为一列

    sqDistances = sqDiffMat.sum(axis=1)#行相加，变成列向量


    distances =sqDistances**0.5  #开根号

    sortedDistIndicies = distances.argsort()
    classCount = {}

    for i in range(k):
        voteLabel = lables[sortedDistIndicies[i]]
        classCount[voteLabel] = classCount.get(voteLabel,0)+1

    #原来的代码里是classCount.iteritems() ，运行会报错，改成items() 就好了
    #key=operator.itemgetter(0) 以字典的key排序
    #key=operator.itemgetter(1) 以字典的value排序
    sortedClassCount = sorted(classCount.items(),
                              key=operator.itemgetter(1),
                              reverse=True)               #降序排列
    return sortedClassCount[0][0]

#文件转换
def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = np.zeros((numberOfLines,3)) #返回的矩阵
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]           #取前三列
        # classLabelVector.append(int(listFromLine[-1]))

        if listFromLine[-1] == 'didntLike':
            classLabelVector.append(1)
        elif listFromLine[-1] == 'smallDoses':
            classLabelVector.append(2)
        else:
            classLabelVector.append(3)

        index += 1
    return returnMat,classLabelVector

#归一化 : 将数字特征转化到0-1之间
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - np.tile(minVals,(m,1))
    normDataSet = normDataSet/np.tile(ranges,(m,1))
    return normDataSet, ranges, minVals

#约会测试
def datingClassTest():
    hoRatio = 0.10
    datingDataMat , datingLables = file2matrix("datingTestSet.txt")
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat .shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],
                                     normMat[numTestVecs:m,:],
                                     datingLables[numTestVecs:m],3)
        print("the classifier came back with : %d the real answer is %d "
              %(classifierResult, datingLables[i]))
        if(classifierResult != datingLables[i]):
            errorCount += 1.0

    print("the total error rate is : %f" %(errorCount/float(numTestVecs)))


if __name__ == '__main__':
    print("running ...")
    datingClassTest()
    print("end...")