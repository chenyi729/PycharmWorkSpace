# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc : knn 算法改进之 kd树

'''
from collections import namedtuple
from math import sqrt
from random import random



# kd - tree 每个节点包含的主要数据结构：（定义kdTree的Node）
class kdNode(object):
    def __init__(self , dom_elt , split , left , right):
        self.dom_elt = dom_elt  # 一个节点（k维空间的一个样本点）
        self.split = split      # int,进行分割维度的序号
        self.left = left        # 当前节点分割超平面左子空间的kdTree
        self.right = right      # 当前节点分割超平面右子空间的kdTree


#kd树
class kdTree(object):
    def __init__(self,data):
        k = len(data[0]) #数据维度

        def createNode(split , data_Set):#按照split维度划分数据集exset创建kdNode

            if not data_Set :
                return None
            '''
               key 参数的值为一个函数，此函数只有一个参数且返回一个值用来进行比较
               operator模块提供的itemgetter函数用于获取对象的哪些维属性
               dataSet.sort 按照要进行分割的那一维数据排序
            '''
            data_Set.sort(key = lambda x:x[split])  #排序
            splitPos = len(data_Set) //2            #整除  二分
            print("splitPos : %d" %splitPos)
            median = data_Set[splitPos]             #中位数分割点
            splitNext = (split + 1) % k             #cycle coordinates

            #递归创建kd树
            return kdNode(median ,split,
                          createNode(splitNext,data_Set[:splitPos]),
                          createNode(splitNext,data_Set[splitPos+1:]))

        self.root= createNode(0,data)         #返回根节点


#kdTree 前序遍历
def preorderKdTree(root):
    print(root.dom_elt)

    if root.left:          #节点不为空
        preorderKdTree(root.left)
    if root.right:
        preorderKdTree(root.right)


#kd树搜索
'''
 算法步骤 ：
  1，先从根节点出发，向下访问，如果目标点的x小于当前的节点的下，则访问左子节点，否则访问右子节点，如此反复，一直到叶节点
  2，假设1中获取的叶子结点为最近点
  3，从2中的最近节点开始向上回溯：
     3.1 ，先计算2中的节点和目标点的欧式距离，
     3.2 ，在计算2节点的父节点和目标点的欧式距离
     3.3 ，再计算父节点的另一个子节点和目标点的欧式距离
'''
#namedtuple 存放最近坐标点，最近距离 和 访问过的节点
result = namedtuple("resultTulpe",["nearestPoint","nearestDist", "nodesVisit"])

def kdTreeSearch(tree,targePoint):
    k = len(targePoint)

    def travel(kdNode , target , maxDist):

        if kdNode is None:
            return  result([0]*k , float("inf"),0)  #python中用float("inf")和float("-inf")表示正副无穷

        nodesVisit = 1

        s=kdNode.split                   #进行分割的维度
        pivot = kdNode.dom_elt           #进行分割的轴

        if target[s] <= pivot[s]:        #如果目标s小于分割轴的对应值(走左边)

            nearerNode = kdNode.left
            furtherNode = kdNode.right

        else:                            #走右边
            nearerNode = kdNode.right
            furtherNode = kdNode.left

        temp1 = travel(nearerNode,target,maxDist)

        nearest = temp1.nearestPoint
        dist = temp1. nearestDist

        nodesVisit += temp1.nodesVisit

        if dist < maxDist:
            maxDist=dist  #最近点将在以目标点为球心，maxDist为半径的超球体内

        tempDist = abs(pivot[s] - target[s]) #第s维上目标点于分割平面的距离

        if maxDist < tempDist:   #判断球体是否与超平面相交
            return result(nearest,dist,nodesVisit)  #不相交则可以直接返回

        #计算目标点与分割点的欧式距离
        tempDist =sqrt(sum((p1 - p2 ) ** 2 for p1,p2 in zip(pivot,target)))

        if tempDist <dist:
            nearest = pivot   #更新最近点
            dist = tempDist   #更新最近距离
            maxDist = dist    #更新半径

        #检查另一个子节点对应的区域是否有更近的点
        temp2 = travel(furtherNode,target,maxDist)

        nodesVisit += temp2.nodesVisit
        if temp2.nearestDist < dist:     #另一个子节点内存在更近的距离
            nearest = temp2.nearestDist  #更新最近点
            dist = temp2.nearestDist     #更新最近距离

        return  result(nearest,dist,nodesVisit)

    return travel(kdTree.root,targePoint,float("inf"))



def randomPoint(k):
    return [random()]

def randomPoints(k,n):
    return  [randomPoints(k) for _ in range(n)]






#main
if __name__ == "__main__":
    data = [[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]]
    kd = kdTree(data)
    preorderKdTree(kd.root)

