#-*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :

'''
import matplotlib.pyplot as plt
import numpy as np

def loadDataSet(fileName):
    dataMat = [];
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():  # 逐行读取
        lineArr = line.strip().split('\t')  # 滤除空格
        dataMat.append([float(lineArr[0]), float(lineArr[1])])  # 添加数据
        labelMat.append(float(lineArr[2]))  # 添加标签
    return dataMat, labelMat


"""
    函数说明:随机选择alpha_j的索引值

    Parameters:
        i - alpha的下标
        m - alpha参数个数
    Returns:
        j - alpha_j的索引值
    """


def selectJrand(i, m):
    j = i  # 选择一个不等于i的j
    while (j == i):  # 只要函数值不等于输入值i，函数就会进行随机选择
        j = int(np.random.uniform(0, m))
    return j


"""
    调整大于H或小于L的alpha值
    Parameters：
        oS - 数据结构
        k - 标号为k的数据的索引值
    Returns:
        aj - 修剪后的alpah_j的值
    """


def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj
"""

def smoSimple(dataMatIn,classLabel,C,toler,maxIter):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabel)
    b = 0
    m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while(iter < maxIter):
        alphPairsChanged = 0  #更新次数
        for i in range(m):
            fXi = float(multiply(alphas,labelMat).T * (dataMatrix * dataMatrix[i,:].T)) + b
            Ei = fXi - float(labelMat[i])   #if checks if an example violates KKT conditions
            if (all(labelMat[i] * Ei < -toler) and all(alphas[i] < C)) or \
                    (all(labelMat[i] * Ei > toler) and all(alphas[i] > 0)):  # \ 表示换行符
                j = selectJrand(i,m)
                fXj = float(multiply(alphas,labelMat).T * (dataMatrix * dataMatrix[j,:].T))+b
                Ej = fXj - alphas[i].copy()
                alphaIold = alphas[j].copy()
                alphaJold = alphas[j].copy()
                if labelMat[i] != labelMat[j] :
                    L = max(0,alphas[j]-alphas[i])
                    H = min(C,C+alphas[j]-alphas[i])
                else:
                    L = max(0,alphas[j]+alphas[i]-C)
                    H = min(C,alphas[j]+alphas[i])

                if L == H:
                    print("L == H")
                    continue  #?
                eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].T - \
                      dataMatrix[i,:] * dataMatrix[i,:].T - \
                      dataMatrix[j,:] * dataMatrix[j,:].T

                if eta >= 0:
                    print("eta >= 0")
                    continue
                alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])
                # x1,y1=shape(b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i,:] * dataMatrix[i:,].T)
                # print(x1,",",y1)
                # x2,y2=shape(labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i,:] * dataMatrix[j,:].T)
                # print(x2, ",", y2)
                b1 = b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i,:] * dataMatrix[i:,].T - \
                     labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i,:] * dataMatrix[j,:].T

                b2 = b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i,:] * dataMatrix[i,:].T - \
                     labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j,:] * dataMatrix[j,:].T

                if (0<alphas[i]) and (C>alphas[i]):
                    b = b1
                elif (0<alphas[j]) and (C>alphas[j]):
                    b = b2
                else:
                    b = (b1+b2) / 2.0

                alphPairsChanged += 1
                print("iter:%d i:%d ,pairs changed  %d" %(iter,i,alphPairsChanged))
        if(alphPairsChanged == 0) :
            iter += 1
        else:
            iter = 0

        print("iteration number : %d" %iter)

    return b,alphas

"""
#简化版 SMO
#输入参数 数据集，类别标签，常数C，容错率，退出前最大的循环次数
def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    #转换为numpy的mat存储
    dataMatrix = np.mat(dataMatIn);
    labelMat = np.mat(classLabels).transpose() #将标签进行转置处理，降维为一维数组进行存储
    #初始化b参数，统计dataMatrix的维度
    b = 0;
    m,n = np.shape(dataMatrix)#m=100 n=2
    #初始化alpha参数，设为0  100行1列的0矩阵
    alphas = np.mat(np.zeros((m,1)))
    #初始化迭代次数，用来存储在没有任何alpha改变的情况下遍历数据集的次数
    iter_num = 0
    #最多迭代matIter次指没有任何alpha改变的情况下遍历数据集的次数
    #只有在所有数据集上遍历maxIter次，且不再发生任何alpha修改之后，程序才停止
    while (iter_num < maxIter):
        alphaPairsChanged = 0#每次循环alphaPairsChanged先设为0，用来记录alpha是否已经进行优化
        for i in range(m):#对整个集合顺序遍历
            #步骤1：计算误差Ei
            fXi = float(np.multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b #我们预测的类别
            Ei = fXi - float(labelMat[i])#基于该实例的预测结果和真实结果的比对，计算误差
            #优化alpha，更设定一定的容错率。toler=0.001 C=0.6
            #不管是正间隔还是负间隔都会被测试，并同时检查alpha值，以保证其不能等于0或C
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):
                #随机选择另一个与alpha_i成对优化的alpha_j
                j = selectJrand(i,m)#利用辅助函数来随机选择第二个alpha值
                #步骤1：计算误差Ej
                fXj = float(np.multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                #保存更新前的aplpha值，使用深拷贝 深拷贝即拷贝之后的对象不随原对象变化，即为新值分配内存
                alphaIold = alphas[i].copy();
                alphaJold = alphas[j].copy();
                #步骤2：计算上下界L和H用于把alpha[j]调整到0到C之间
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L==H: #不做任何改变
                    print("L==H");
                    continue#本次循环结束直接运行下一次for循环
                #步骤3：计算eta是alpha[j]的最优修改量
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0: #退出for循环的当前迭代过程
                    print("eta>=0");
                    continue
                #步骤4：计算新的alpha_j，并用辅助函数以及L与H值对其进行调整
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                #步骤5：修剪alpha_j
                alphas[j] = clipAlpha(alphas[j],H,L)
                #判断alphas[j]是否有轻微改变，若有退出for循环
                if (abs(alphas[j] - alphaJold) < 0.00001): print("alpha_j变化太小"); continue
                #步骤6：更新alpha_i，改变的方向和alphas[j]相反
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                #步骤7：更新b_1和b_2
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                #步骤8：根据b_1和b_2更新b
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2)/2.0
                #若执行到这一步都没有continue,说明成功改变了一对alpha
                #统计优化次数
                alphaPairsChanged += 1
                #打印统计信息
                print("第%d次迭代 样本:%d, alpha优化次数:%d" % (iter_num,i,alphaPairsChanged))
        #更新迭代次数，
        if (alphaPairsChanged == 0):
            iter_num += 1
        else: iter_num = 0#若有更新，将iter设为0后继续运行程序，
        #一直等到在所有数据集上遍历maxIter次且不再发生任何alpha修改之后程序停止并退出while()循环
        print("迭代次数: %d" % iter_num)
    return b,alphas


def kernelTrans(X,A,kTup):
    """
    #calc the kernel or transform data to a higher dimensional space
    :param X:
    :param A:
    :param kTup:
    :return:
    """
    m,n = np.shape(X)
    K = np.mat(np.zeros((m,1)))
    if kTup[0] == "lin":
        K = X * A.T
    elif kTup[0] == "rbf":
        for j in range(m):
            deltaRow = X[j,:] - A
            K[j] = deltaRow * deltaRow.T
        K = np.exp(K/(-1*kTup[1]**2))
    else:
        raise NameError("Houston We Have a Problems That kernel is not recognized")
    return K



# 完整版的SMO支持函数
class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler):
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = np.shape(dataMatIn)[0]
        self.alphas = np.mat(np.zeros(self.m,1))
        self.b = 0
        self.eCache = np.mat(np.zeros(self.m,1))

def calcEk(oS,k):
    fxk = float(np.multiply(oS.alphas,oS.labelMat).T * (oS.X * oS.X[k:].T) + oS.b)
    Ek = fxk - float(oS.labelMat[k])
    return Ek

def selectJ(i,oS,Ei):
    maxK = i
    maxDeltaE = 0
    Ej = 0
    oS.eCache[i] = [1,Ei]
    validEcacheList = np.nonzero(oS.eCache[:,0].A)[0]
    if (len(validEcacheList)) > 1 :
        for k in validEcacheList:
            if k == i:
                continue
            Ek = calcEk(oS,k)
            deltaE = abs(Ei -Ek)
            if(deltaE > maxDeltaE):
                maxK = k;
                maxDeltaE = deltaE
                Ej = Ek
        return maxK,Ej
    else:
        j = selectJrand(i,oS.m)
        Ej = calcEk(oS,j)
        return j,Ej

def updateEk(oS,k):
    Ek = calcEk(oS,k)
    oS.eCache[k] = [1,Ek]




def innerL(i,oS):
    Ei = calcEk(oS,i)
    if((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i]*Ei > oS.tol ) and (oS.alphas[i] >0)):
        j,Ej = selectJ(i,oS,Ei)
        alphaIOld = oS.alphas[i].copy()
        alphaJOld = oS.alphas[j].copy()
        if(oS.labelMat[i] != oS.labelMat[j]):
            L = max(0,oS.alphas[j] - oS.alphas[i])
            H = min(oS.C,oS.C+oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0,oS.alphas[j] +oS.alphas[i]-oS.C)
            H = min((oS.C,oS.alphas[j]+oS.alphas[i]))

        if L == H:
            print("L==H")
            return 0
        eta = 2.0 * oS.X[i,:] * oS.X[j,:].T - oS.X[i,:] * oS.X[i,:].T - os.X[j,:] * oS.X[j,:].T






if __name__  == "__main__":

    dataArr,labelArr = loadDataSet("testSet.txt")

    # print([label for label in labelArr])

    b,sample = smoSimple(dataArr, labelArr, 0.6, 0.001, 40)

    #b 的值
    print("b:")
    print(b)

    #sample
    print("sample:")
    for a in sample:
        if a>0:
            print(a)









