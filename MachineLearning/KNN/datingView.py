# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :  约会数据可视化

'''
from matplotlib.font_manager import  FontProperties
import  numpy as np
import  matplotlib.pyplot as plt
from knn import file2matrix
import matplotlib.lines as mlines


def showDatas(datingDataMats , datingLabels):

    # 设置字体
    font = FontProperties(fname=r'c:\windows\fonts\simsun.ttc')

    #函数返回一个figure图像 和一个子图ax的array列表
    fig , axs = plt.subplots(nrows=2,ncols=2,
                             sharex=False,sharey=False,
                             figsize=(13,8))


    numberOfLabels = len(datingLabels)
    labelColors = []
    for i in datingLabels:
        if i == 1:
            labelColors.append('black')
        if i == 2:
            labelColors.append('orange')
        if i == 3:
            labelColors.append('red')

    #散点图 以数据第一列（飞行常客历程） 第二列（玩游戏）数据散点图
    #散点大小15， 透明度0.5

    axs[0][0].scatter(x = datingDataMats[:,0],
                      y = datingDataMats[:,1],
                      color = labelColors,
                      s = 15,alpha = 0.5)

    axs0TitleText = axs[0][0].set_title(u"每年获得的飞行里程数与玩视频游戏消耗时间占比",
                                          FontProperties=font)
    axs0XLabelText = axs[0][0].set_xlabel("每面获得的飞行常客里程数",FontProperties=font)
    axs0YLabelText = axs[0][0].set_ylabel("玩游戏消耗时间",FontProperties=font)
    plt.setp(axs0TitleText,size=9,weight='bold',color='red')

    #散点图 以数据第一列（飞行常客历程） 第三列（冰激凌公斤数）数据散点图
    #散点大小15， 透明度0.5
    axs[0][1].scatter(x = datingDataMats[:,0],
                      y = datingDataMats[:,2],
                      color = labelColors,
                      s = 15,alpha = 0.5)

    axs0TitleText = axs[0][1].set_title(u"每年获得的飞行里程数与玩视频游戏消耗时间占比",
                                          FontProperties=font)
    axs0XLabelText = axs[0][1].set_xlabel("每面获得的飞行常客里程数",FontProperties=font)
    axs0YLabelText = axs[0][1].set_ylabel("所吃冰激淋公斤数",FontProperties=font)
    plt.setp(axs0TitleText,size=9,weight='bold',color='red')

   #散点图 以数据第二列（玩游戏） 第三列（冰激凌公斤数）数据散点图
    #散点大小15， 透明度0.5
    axs[1][0].scatter(x = datingDataMats[:,1],
                      y = datingDataMats[:,2],
                      color = labelColors,
                      s = 15,alpha = 0.5)

    axs0TitleText = axs[1][0].set_title(u"每年获得的飞行里程数与玩视频游戏消耗时间占比",
                                          FontProperties=font)
    axs0XLabelText = axs[1][0].set_xlabel("每面获得的飞行常客里程数",FontProperties=font)
    axs0YLabelText = axs[1][0].set_ylabel("所吃冰激淋公斤数",FontProperties=font)
    plt.setp(axs0TitleText,size=9,weight='bold',color='red')

    #设置图例
    didntLike = mlines.Line2D([],[],color='black',marker='.',markersize=6,label='didntLike')
    smallDose = mlines.Line2D([],[],color='orange',marker='.',markersize=6,label='smallDose')
    largeDose = mlines.Line2D([],[],color='black',marker='.',markersize=6,label='largeDose')

    #添加图例
    axs[0][0].legend(handles = [didntLike,smallDose,largeDose])
    axs[0][0].legend(handles=[didntLike, smallDose, largeDose])
    axs[0][0].legend(handles=[didntLike, smallDose, largeDose])

    plt.show()


#main
if __name__ == "__main__":
    fileName = "datingTestSet.txt"
    returnMat,classLabelVector = file2matrix(fileName)
    showDatas(returnMat,classLabelVector)
