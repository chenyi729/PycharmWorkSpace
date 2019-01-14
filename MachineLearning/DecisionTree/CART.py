# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :  CART

'''
import pickle
import numpy as np
from DecisionTree.treePlotter import treePlotter

def loadDataSet(filename):

    """

    :param filename: 文件路径
    :return:  dataMat
    """
    fr  = open(filename)
    dataMat = []
    for line in fr.readlines():
        cutLine = line.strip().split('\t')
        floatLine = map(float,cutLine)
        dataMat.append(floatLine)
    return dataMat

def binarySplitData(dataSet,feature,value):
    """

    :param dataSet:
    :param feature:
    :param value:
    :return:  左右子数据集
    """
    matLeft = dataSet[np.nonzero(dataSet[:feature] <= value)[0]:]
    matRight = dataSet[np.nonzero(dataSet[:,feature] > value)[0]:]

    return matLeft,matRight


#-------------------------------回归树所需子函数---------------------------------#
def regressLeaf(dataSet):
    """

    :param dataSet:
    :return:  对应数据集的叶节点
    """
    return np.mean(dataSet[:-1])


def regressErr(dataSet):
    """
    求数据集划分左右子数据集的误差平方和
    :param dataSet: 数据集
    :return: 划分后的误差平方和
    """
    # 由于回归树中输出的均值作为叶节点，所以在这里求误差平方和实质上就是方差
    return np.var(dataSet[:,-1]) * np.shape(dataSet)[0]


def regressData(fileName):
    """
    将数据序列化
    :param fileName:
    :return:
    """
    fr = open(fileName)
    return pickle.load(fr)


def choosBestSplit(dataSet ,leafType = regressLeaf,errType=regressErr
                   ,threshold=(1,4)):
    """

    :param dataSet:
    :param leafType:
    :param errType:
    :param threshold:
    :return:
    """
    thresholdErr = threshold[0]
    thresholdSamples = threshold[1]
    #当数据中输出值都相等的时候，feature = None，value = 输出值的均值（叶子节点）
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
        return None,leafType(dataSet)
    m,n = np.shape(dataSet)
    err = errType(dataSet)
    bestErr = np.inf
    bestFeatureIndex = 0
    bestFeatureValue = 0

    for featureIndex in range(n-1):
        for featureValue in dataSet[:,featureIndex]:
            matLeft,matRight = binarySplitData(dataSet,featureIndex,featureValue)

            if((np.shape(matLeft)[0] < thresholdSamples) or
               (np.shape(matRight)[0] <thresholdSamples)):
                continue
            tempErr = errType(matLeft) + errType(matRight)

            if tempErr <bestErr:
                bestErr = tempErr
                bestFeatureIndex = featureIndex
                bestFeatureValue = featureValue

    #在所选出的最优化分的划特征及其取值下，检验误差平方和与未划分时候的差是否小于阈值 若是，则划分不合适
    if(err-bestErr) < thresholdErr:
        return  None,leafType(dataSet)
    matLeft,matRight = binarySplitData(dataSet,bestFeatureIndex,bestFeatureValue)

    #检验 所选的最优划分特征及其取值下，划分的左右数据集的样本数是否小于阈值 如果是，则不合适划分
    if((np.shape(matLeft)[0] <thresholdSamples) or
       (np.shape(matRight)[0] < thresholdSamples)):
        return None,leafType(dataSet)

    return bestFeatureIndex,bestFeatureValue


def creatCARTTree(dataSet,leafType=regressLeaf,errType=regressErr,threshold=(1,4)):
    """
    :param dataSet: 数据集
    :param leafType: regressLeaf（回归树）、modelLeaf（模型树）
    :param errType: 差平方和
    :param threshold:用户自定义阈值参数
    :return: 以字典嵌套数据形式返回子回归树或子模型树或叶结点
    """
    feature,value = choosBestSplit(dataSet,leafType,errType,threshold)
    #当不满足阈值或者某一子数据集下输出全相等时，返回叶子节点
    if feature == None:
        return  value

    returnTree = {}
    returnTree['bestSplitFeature'] = feature
    returnTree['bestSplitFeatValue'] = value

    leftSet,right = binarySplitData(dataSet,feature,value)
    returnTree['left'] = creatCARTTree(leftSet,leafType,errType,threshold)
    returnTree['right'] = creatCARTTree(leftSet,leafType,errType,threshold)

    return returnTree

#--------------------------------回归树剪枝函数------------------------------------------

def isTree(obj):
    return (type(obj).__name__ == 'dict')

def getMean(tree):
    """

    :param tree:
    :return:
    """

    if isTree(tree['left']):
        tree['left'] = getMean(tree['left'])

    if isTree(tree['right']):
        tree['right'] = getMean(tree['right'])

    return (tree['left']+tree['right'])/2.0

def prune(tree,testData):
    """
    剪枝
    :param tree:
    :param testData:
    :return:
    """

    #存在测试集中没有训练数据的情况
    if np.shape(testData)[0] == 0:
        return getMean(tree)

    if isTree(tree['left']) or isTree(tree['right']):
        leftTestData,rightTestData = binarySplitData(testData,tree['right'])

    #递归调用prune函数对左右子树，注意与左右子树对应的测试数据集
    if isTree(tree['left']):
        tree['left'] = prune(tree['left'],leftTestData)

    if isTree(tree['right']):
        tree['right'] = prune(tree['right'],rightTestData)

    #当递归搜索到左右子树均为节点，计算测试数据集的误差平方和
    if not isTree(tree['left']) and not isTree(tree['right']):
        leftTestData,rightTestData = binarySplitData(testData,
                                                     tree['bestSplitFeature'],
                                                     tree['bestFeatureValue'])

        errNoMerge = sum(np.power(leftTestData[:,-1] - tree['left'],2))+sum(np.power(rightTestData[:,-1] - tree['right'],2))
        errorMerge = sum(np.power(testData[:,1] - getMean(tree),2))

        if errorMerge <errNoMerge:
            print("merging")
            return getMean(tree)
        else:
            return tree
    else:
        return tree

#--------------------------------回归树剪枝函数 END-----------------------------------------


#--------------------------------模型树子函数------------------------------------------
def linearSolve(dataSet):
    m,n = np.shape(dataSet)
    X = np.mat(np.ones((m,n)))
    Y = np.mat(np.ones(m,1))
    X[:,1:n] = dataSet[:,0:(n-1)]
    Y = dataSet[:,-1]
    xTx = X.T * X
    if np.linalg.det(xTx) == 0:
        raise NameError('This matrix is singular ,cannot do inverse, try increasing the second value of threashold')
        ws = xTx.I * (X.T * Y)
        return ws,X,Y

def modelLeaf(dataSet):
    ws,X,Y = linearSolve(dataSet)
    return ws

def modelErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(np.power(Y - yHat,2))

#-------------------------------------------模型树子函数END-------------------------------------------------------


#-------------------------------------------CART预测子函数-------------------------------------------------------
def regressEvaluation(tree,inputData):
    #只有当tree为叶节点的时候，才会输出
    return float(tree)

def modelTreeEvaluation(model , inputData):
    n = np.shape(inputData)
    X = np.mat(np.ones((1,n+1)))
    X[:,1:1+n] = inputData
    return float(X * model)


def treeForceCast(tree,inputData,modelEval = regressEvaluation):
    if not isTree(tree):
        return modelEval(tree,inputData)
    if inputData[tree['bestSplitFeature']] <= tree['bestSplitFeatureValue']:
        if isTree(tree['left']):
            return treeForceCast(tree['left'],inputData,modelEval)
        else:
            return modelEval(tree['left'],inputData)

    else:
        if isTree(tree['right']):
            return treeForceCast(tree['right'],inputData,modelEval)
        else:
            return modelEval(tree['right'],inputData)

def createForceCast(tree,testData,modelEval=regressEvaluation):
    m = len(testData)
    yHat = np.mat(np.zeros((m,1)))
    for i  in range(m):
        yHat = treeForceCast(tree,testData[i],modelEval)
    return yHat

#--------------------------------------CART预测子函数END-------------------------------------------------------


if __name__ == '__main__':
    pass







    




















