# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc : 朴素贝叶斯

'''
from numpy import *
import os

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problem', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]

    classVec=[0,1,0,1,0,1] #1代表侮辱性词汇，0代表正常文字

    return postingList,classVec

#创建一个空集
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document) #集合或运算 ，也是按位或运算（OR）

    return list(vocabSet)

#词集模型
#  只记录每个词是否出现，而不记录出现的次数
#输入文档 输出文档向量，1：出现，0：没有出现
def setOfWord2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] =1
        else:
            print('the word : %s is not in my vocabulary' %word)

    return returnVec


#朴素贝叶斯分类器训练函数
'''
p0Vect 词汇表中各个单词在正常言论中的条件概率密度
p1Vect 词汇表中各个单词在侮辱言论中的条件概率密度
pAbusive 词侮辱言论在整个数据集中的比例
'''
def trainNB0(trainMatrix,trainCategroy):

    #行数
    numTrianDocs = len(trainMatrix)
    #训练集中所有单词总数：词向量维度
    numWords = len(trainMatrix[0])

    #
    pAbusive = sum(trainCategroy)/float(numTrianDocs)

    # p0Num = zeros(numWords)
    # p1Num = zeros(numWords)

    #拉普拉斯平滑
    #初始化分子为1
    p0Num = ones(numWords)
    p1Num = ones(numWords)

    #初始化分母为2
    p0Denom=2.0
    p1Denom=2.0

    for i in range(numTrianDocs):
        #如果为侮辱类
        if trainCategroy[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    #数据取log ，单个单词的p取log，防止下溢出
    p0Vect = log(p0Num/p0Denom)
    p1Vect = log(p1Num/p1Denom)

    print("p0Vect",p0Vect)
    print("p1Vect",p1Vect)

    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0Vect,p1Vect,pClass1):

    #在对数空间进行计算，属于哪一类的概率比较大就判为那一类
    print("pClass1 : ",pClass1)

    p1 = sum(vec2Classify*p1Vect) + log(pClass1)
    print("p1 = %f" %p1)
    p0 = sum(vec2Classify*p0Vect) + log(1-pClass1)
    print("p0 = %f" % p0)

    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():

    listOfPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOfPosts)

    #存放数据集
    trainMat=[]

    for postinDoc in listOfPosts:
        #数据转换
        trainMat.append(setOfWord2Vec(myVocabList,postinDoc))

        #训练
    p0v,p1v,pAb = trainNB0(array(trainMat),array(listClasses))

    print("trainNB:p0v",p0v)
    print("trainNB:p1v", p1v)
    print("trainNB:pAb", pAb)

    #测试数据集1
    testEntry = ['love','my','dalmattion']

    thisDoc = array(setOfWord2Vec(myVocabList,testEntry))

    print(testEntry,"classify as :",classifyNB(thisDoc,p0v,p1v,pAb))


#词袋模型：考虑单词出现的次数
#vocabList ：词汇表
#inputSet : 某个文档向量

def bagOfWords2VecMN(vocabList,inputSet):

    returnVec = [0]*len(vocabList)

    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1

        else:
            print("the word : %s is not in my Vocabulary!" %word )

    return  returnVec

def textParese(bigString):
    import re
    listOfToken = re.split(r'\w*',bigString)
    #tok.lower() 大写转小写
    return [tok.lower() for tok in listOfToken if len(tok) >2 ]

def spamTest():

    #存放文章
    docList=[]

    #文章类别
    classList=[]

    #存放所有文章内容
    fullText=[]

    for i in  range(1,26):

        #读取垃圾邮件
        # dirText ="/email/spam/%d.txt"
        wordList = textParese(open(r'E:/PycharmWorkSpace/KNN/NaiveBayes/email/spam/%d.txt' %i,encoding='gbk',errors='ignore').read())

        #按篇存放文章
        docList.append(wordList)

        #full text 邮件放到一起
        fullText.extend(wordList)

        #垃圾邮件标记为1
        classList.append(1)

        #读取正常邮件
        # dirText2 = "/email/ham/%d.txt"
        wordList2 = textParese(open(r'E:/PycharmWorkSpace/KNN/NaiveBayes/email/ham/%d.txt' % i,encoding='gbk',errors='ignore').read())
        docList.append(wordList2)
        fullText.extend(wordList2)
        classList.append(0)

    #创建词典
    vocabLsit = createVocabList(docList)

    trainingSet = range(50)

    #测试集
    testSet=[]

    for i in range(10):
        rangeIndex = int(random.uniform(0,len(trainingSet)))

        testSet.append(trainingSet[rangeIndex])

        #删除对应文章
        del(trainingSet[rangeIndex])

    trainMat = []
    trainClasses = []

    for docIndex in trainingSet:

        trainMat.append(bagOfWords2VecMN(vocabLsit,docList[docIndex]))

        trainClasses.append(classList[docIndex])

    p0v,p1v,pSpam = trainNB0(array(trainMat),array(trainClasses))

    errorCount = 0

    for docIndex in testSet :

         wordVector = bagOfWords2VecMN(vocabLsit,docList)

         if classifyNB(array(wordVector),p0v,p1v,pSpam) != classList[docIndex]:
             errorCount += 1;

             print("classification error",docList[docIndex])

    print("the error rate is :",float(errorCount)/len(testSet))




if __name__=="__main__":

    print(os.path.abspath('.'))

    #获取数据
    listOfPosts , lisClass = loadDataSet()

    #创建词汇表

    myVocabList = createVocabList(listOfPosts)

    print("my vocabulary list is :",myVocabList)
    print("result:",setOfWord2Vec(myVocabList,listOfPosts[0]))

    trainMat = []

    for postinDoc in listOfPosts:
        #构建训练矩阵
        trainMat.append(setOfWord2Vec(myVocabList,postinDoc))

    p0Vect,p1Vect,pAbusive = trainNB0(trainMat,lisClass)

    print("p0Vect=",p0Vect)
    print("p0Vect=",p1Vect)
    print("pAbusive=",pAbusive)

    # print("--------------testing----------")
    # testingNB()
    # print("-----------spam filter---------")
    # spamTest()







