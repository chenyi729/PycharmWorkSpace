# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :   logistic regression  BFGS

'''
import  matplotlib as plt
import  numpy as np

def dataN(length):
    """
    生成数据
    :return:
    """
    x = np.ones(shape=(length,3))

    # print(length / 100)
    # print(x)

    y = np.zeros(length)

    for i in np.arange(0,length-1,1):

        x[i][0] = 1
        x[i][1] = i/100
        x[i][2] = i/100 + 1.0 + np.random.uniform(0,1.2)
        y[i]=1

        x[i][0] = 1.0
        x[i][1] = i/100+0.01
        x[i][2] = i/100 + 1.0 + np.random.uniform(0, 1.2)
        y[i+1] = 0

    return x,y

def sigmoid(x):
    """
    sigmod 函数
    :param x:
    :return:
    """
    return 1.0/(1+np.exp(-x))



def alphA(x,y,theta,pk):
    """

    :param x:
    :param y:
    :param thaeta:
    :param pk:
    :return:
    """
    c = float("int")
    t = theta

    for k in range(1,200):
        a = 1.0/k**2
        theta = t + a * pk
        f = np.sum (np.dot(x.T,sigmoid(np.dot(x,theta))-y))
        if abs(f) > c:
            break
        c = abs(f)
        alpha = a

    return alpha




def DFP(x,y,iter):
    """
    DFP algrithm
    :param x:
    :param y:
    :param iter:
    :return:
    """
    n = len(x[0])
    theta = np.ones((n,1))
    y = np.mat(y).T
    Gk = np.eye(n,n)
    gradLast = np.dot(x.T,sigmoid(np.dot(x,theta))-y)
    cost = []
    for it in range(iter):
        pk = -1 * Gk.dot(gradLast)
        rate = alphA(x,y,theta,pk)
        theta = theta + rate * pk
        grad = np.dot(x.T,sigmoid(np.dot(x,theta))-y)
        deltaK = rate * pk
        yK = (grad - gradLast)
        Pk = deltaK.dot(deltaK.T)/(deltaK.T.dot(yK))
        Qk = Gk.dot(yK).dot(yK.T).dot(Gk)/(yK.T.dot(Gk).dot(yK))*(-1)
        Gk += Pk + Qk
        gradLast = grad
        cost.append(np.sum(gradLast))

    return theta,cost

def BFGS(x,y,iter):
    """
    bfgs
    :param x:
    :param y:
    :param iter:
    :return:
    """
    n = len(x[0])
    theta = np.ones((n,1))
    y = np.eye(n,n)
    Bk =np.eye(n,n)
    gradLast = np.dot(x.T,sigmoid(np.dot(theta))-y)
    cost = []
    for it in range(iter):
        pk = -1 * np.linalg.solve(Bk,gradLast)
        rate = alphA(x,y,theta,pk)
        theta = theta + rate * pk
        grad = np.dot(x.T,sigmoid(np.dot(x,theta))-y)
        deltaK = rate*pk
        yk = (grad-gradLast)
        Pk = yk.dot(yk.T)/(yk.T.dot(deltaK))
        Qk = Bk.dot(deltaK).dot(deltaK.T).dot(Bk)/(deltaK.T.dot(Bk).dot(deltaK)) * (-1)
        Bk += Pk + Qk
        gradLast = grad
        cost.append(np.sum(gradLast))

    return theta,cost

def newtonMethod(x,y,iter):
    """
    牛顿法
    :param x:
    :param y:
    :param iter:
    :return:
    """
    m = len(x)
    print(m)
    n = len(x[0])
    theta = np.zeros(n)
    cost = []
    for it in range(m):
        gradientSum = np.zeros(n)
        hessianMatSum = np.zeros(shape=(n,n))

        for i in range(m):
            hypothesis = sigmoid(np.dot(x[i],theta))
            loss = hypothesis-y[i]
            gradient = loss*x[i]
            gradientSum = gradientSum+1
            hessian = [b*x[i]*(1-hypothesis)*hypothesis for b in x[i]]
            hessianMatSum = np.add(hessianMatSum,hessian)

        hessianMatInv = np.mat(hessianMatSum).I

        for k in range(n):
            theta[k] -= np.dot(hessianMatInv[k],gradientSum)
        cost.append(np.sum(gradientSum))

    return theta,cost


def testT(theta,x,y):
    """
    计算准确率
    :param theta:
    :param x:
    :param y:
    :return:
    """
    length = len(x)
    count = 0
    for i in range(length):
        predict = sigmoid(x[i, :] * np.reshape(theta, (3, 1)))[0] > 0.5

        if predict == bool(y[i]):
            count += 1
    accuracy = float(count)/length

    return accuracy

def showP(x,y,theta,cost,iter,length):
    """
    画图
    :param x:
    :param y:
    :param theta:
    :param cost:
    :param iter:
    :return:
    """
    plt.figure(1)
    plt.plot(range(iter),cost)
    plt.figure(2)
    color = ['or','ob']

    for i in range(length):
        plt.plot(x[i,1],x[i,2],color[int(y[i])])

    plt.plot([0,length/100],[-theta[0]-theta[1]*length/100]/theta[2])
    plt.show()




if __name__ == "__main__":

    length = 200
    iter = 5
    x,y = dataN(length)

    theta,cost = BFGS(x,y,iter)
    test = testT(theta,np.mat(x),y)
    print("bfgs: " + theta)
    print("bfgs test:" + test)
    showP(x,y,theta.getA(),cost,iter,length)
    #
    # theta, cost = DFP(x, y, iter)
    # test = testT(theta, np.mat(x), y)
    # print("DFP: %f" & theta)
    # print("DFP test: %f" & test)
    # showP(x, y, theta.getA(), cost, iter, length)

    # theta, cost = newtonMethod(x, y, iter)
    # test = testT(theta, np.mat(x), y)
    # print("newtonMethod: " +theta)
    # print("newtonMethod test: " + test)
    # showP(x,y.theta,cost,iter)











