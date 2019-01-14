# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc : 决策树 生成算法 ID3

'''
from math import log
import operator
from DecisionTree.treePlotter import treePlotter
from DecisionTree import C45


def createDataSet():
    dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfacing','flippers']
    return  dataSet , labels

#计算香农熵
def calcShannonEnt(dataSet):
    numEnt = len(dataSet)
    #为所有可能的分类创建字典
    labelCount = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel] = 0
        labelCount[currentLabel] += 1

    #计算香农熵
    shannonEnt = 0.0
    for key in  labelCount:
        prob = float(labelCount[key]) / numEnt
        shannonEnt -= prob*log(prob,2)
    return shannonEnt

#按照最大信息增益划分数据集
#输入三个变量（带划分数据集，特征，分类值）
def splitDataSet(DataSet,axis,value):
    retDataSet = []
    for featVec in DataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    #返回不含划分特征的子集
    return retDataSet


#定义按照最大信息增益划分数据的函数
def chooseBestFeatureToSplit(dataSet):
    numFeature = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)  #香农熵
    bestInfoGain = 0
    bestFeature = -1

    for i in range(numFeature):
        featList = [number[i] for number in dataSet] #得到某个特征下所有的值（列）
        uniqualValue = set(featList) #set 没有重复的特征属性
        newEntropy = 0
        for value in uniqualValue:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy #计算信息增益

        #最大信息增益
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i

    #返回特征值
    return bestFeature

#构造决策树
  #投票表决代码
def majorityCnt(classList):
    classCount = {}

    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1

    sortedClassCount = sorted(classCount.items(),
                              key = operator.itemgetter(1),
                              reverse=True)
    return sortedClassCount[0][0]

def createDecTreeByID3(dataSet,labels):

    classLsit = [example[-1] for example in dataSet]

    #如果类别相同，停止划分
    if classLsit.count(classLsit[-1]) == len(classLsit):
        return classLsit[-1]

    if len(classLsit[-1]) == 1:
        return  majorityCnt(classLsit)

    #按照信息增益最高选取分类的特征属性
    bestFeat = chooseBestFeatureToSplit(dataSet) #返回特征序号
    bestFeatLabel = labels[bestFeat]

    #构建树的字典
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])

    featValues = [example[bestFeat] for example in dataSet]

    uniqueValues = set(featValues)

    for value in uniqueValues:
        subLables = labels[:] #子集合
        #构建数据的子集合，并递归
        myTree[bestFeatLabel][value] = createDecTreeByID3(splitDataSet(dataSet,bestFeat,value),
                                                          subLables)
    return myTree


#分类
def classify(inputTree,featLabel,testVec):

    firstStr = list(inputTree.keys())[0] #获取树的第一个特性
    print(featLabel)
    secondDict = inputTree[firstStr] #树的分支，子集合Dict
    featIndex = featLabel.index(firstStr) #获取决策树第一层在featLables中的位置

    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key],featLabel,testVec)
            else:
                classLabel = secondDict[key]

    return classLabel









if __name__ == "__main__":
    myData,labels = createDataSet()
    # print(myData)
    # print(labels)

    # #测试 ： 计算香农熵
    # print(calcShannonEnt(myData))

    # #测试按照特征划分数据集的函数
    # print(splitDataSet(myData,0,0))
    # print(splitDataSet(myData, 0, 1))

    # #测试生成树
    # print(createDecTreeByID3(myData,labels))

    #测试分类
    # myTree = createDecTreeByID3(myData,labels)
    myTree = C45.createTreeByC45(myData, labels)
    print(C45.createTreeByC45(myData, labels))
    # myTree = treePlotter.retrieveTree(1)

    treePlotter.creatPlot(myTree)
    # print(classify(myTree,labels,[1,0]))

