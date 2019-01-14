# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :   1,单链表


'''

class Node(object):
    def __init__(self,value = None,next=None):
        self.value , self.next = value,next

class linkedList(object):

    def __init__(self,maxsize=None):
        self.maxsize = maxsize
        self.root = Node()
        self.length = 0
        self.tailNode = None   #最后一个node 尾节点

    def __len__(self):
        return self.length


    def append(self,value):
        """
        在列表的尾部添加
        :param value:
        :return:
        """

        if self.maxsize is not None and len(self) > self.maxsize:
            raise Exception("Full!")

        node = Node(value)
        tailNode = self.tailNode

        if tailNode is None:
            self.root.next = node
        else:
            tailNode.next = node

        self .tailNode = node  #更新尾节点
        self.length += 1

    def appendleft(self,value):
        """
        从左侧插入节点
        :param value:
        :return:
        """

        headNode =  self.root.next
        node = Node(value)
        self.root.next = node
        node.next = headNode
        self.length += 1


    def iterNode(self):
        currentNode = self.root.next

        while currentNode is not  self.tailNode:
            yield currentNode
            currentNode = currentNode.next

        yield currentNode

    def __iter__(self):
        for node in self.iterNode():
            yield node.value


    def remove(self,value):  #O(n)
        prevNode = self.root
        currentNode = self.root.next
        while currentNode is not None:
            if currentNode.value == value:
                prevNode.next = currentNode.next
                del currentNode
                self.length -= 1
                return 1    #删除成功
            else:
                prevNode = currentNode

        return -1  #删除失败


    def find(self,value):  #O(n)

        index = 0
        for node in self.iterNode():
            if node.value == value:
                return  index
            index += 1
        return  -1

    def popleft(self): #O(n)

        if self.root.next is None:
            raise Exception("pop form empty LinkedList")
        headNode = self.root.next
        self.root.next = headNode.next
        self.length -= 1
        value = headNode.value
        del headNode
        return value

    def clear(self):
        for node in self.iterNode():
            del node
        self.root.next = None
        self.length =0


# def testLinkedList():
#     ll = linkedList()
#
#     ll.append(0)
#     ll.append(1)
#     ll.append(2)
#
#     assert len(ll) == 3
#     assert ll.find(2) == 2
#     assert ll.find(3) == -1
#
#     ll.remove(0)
#     assert  len(ll) == 2
#     assert  ll.find(0) == -1
#
#
#     assert list(ll) == [1,2]
#
#     ll.appendleft(0)
#
#     assert  list(ll) == [0,1,2]
#     assert len(ll) == 3
#
#     headValue = ll.popleft()
#     assert headValue == 0
#     assert len(ll) == 2
#
#     ll.clear()
#     assert len(ll) == 0













