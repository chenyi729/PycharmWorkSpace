# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :C4.5

'''
from numpy import *
from scipy import *
from math import log
import operator

#计算给定数据的香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCount = {}     #类别字典
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel] = 0

        labelCount[currentLabel] += 1

    shannonEnt = 0.0

    for key in labelCount:
        prob = float(labelCount[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

#按照给定的特征划分数据集
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatureVec = featVec[:axis]
            reducedFeatureVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatureVec)
    return  retDataSet #返回分类后的新矩阵

#选择最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet):
    numFeature = len(dataSet[0])-1 #求属性个数
    baseEntryopy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1

    for i in range(numFeature):
        featList = [example[i] for example in dataSet]
        uniqueValues = set(featList)
        newEntropy = 0.0
        splitInfo = 0.0
        for value in uniqueValues:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob* calcShannonEnt(subDataSet)
            splitInfo -= prob * log(prob,2)

        infoGain = (baseEntryopy - newEntropy) /splitInfo; #求出第i列属性的信息增益率
        print(infoGain)
        if (infoGain >bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i

    return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter,
                              reverse=True)

#创建树
def createTreeByC45(dataSet,labels):
    classLsit = [example[-1] for example in dataSet]
    if classLsit.count(classLsit[0]) == len(classLsit):
        return classLsit[0]

    if len(dataSet[0]) == 1: #只有类别属性，而没有值
        return majorityCnt(classLsit)

    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    # del(labels[bestFeat])
    featValue = [example[bestFeat] for example in dataSet]
    uniqueValue = set(featValue)
    for value in uniqueValue:
        subLabel = labels[:]
        myTree[bestFeatLabel][value] = createTreeByC45(splitDataSet(dataSet,bestFeat,value),
                                                  subLabel)

    return myTree


def classify(inputTree,featLabel,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabel.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == "dict":
                classLabel = classify(secondDict[key],featLabel,testVec)
            else:
                classLabel = secondDict[key]

    return classLabel

# def createTrainData():
#     lineSet = open().readlines()
#     lineSet = lineSet[15:22]

if __name__=="__main__":
    pass












