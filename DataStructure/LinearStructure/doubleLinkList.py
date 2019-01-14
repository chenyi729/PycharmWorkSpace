# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :

'''
class doubleNode(object):
    def __init__(self,value=None,prev=None,next=None):
        self.value,self.prev,self.next = value,prev,next

class circualDoubleLinkedList(object):
    def __init__(self,maxsize=None):
        self.maxsize = maxsize
        node = doubleNode()
        node.next,node.prev = node,node
        self.root = node
        self.length = 0

    def headNode(self):
        return self.root.next

    def tailNode(self):
        return self.root.prev

    def __len__(self):
        return self.length

    def append(self,value):
        if self.maxsize is not None and  len(self)>=self.maxsize:
            raise Exception("Full")
        node = doubleNode(value=value)
        tailNode = self.tailNode()

        tailNode.next = node
        node.prev = tailNode
        node.next = self.root
        self.root.prev = node

        self.length += 1

    def appendLeft(self,value):

        if self.maxsize is not None and  len(self)>=self.maxsize:
            raise Exception("Full")
        node = doubleNode(value=value)

        if self.root.next is self.root :
            # 判断是否为空 ,如果为空
            node.next = self.root
            node.prev = self.root
            self.root.next = node
            self.root.prev = node
        else:
            node.prev = self.root
            headNode = self.root.next
            node.next = headNode
            headNode.prev = node
            self.root.next = node

        self.length += 1

    def remove(self,node):
        """
        参数是node，而不是value
        O(1)
        :param node:
        :return:
        """

        if node is self.root:
            return
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        self.length -=1
        return node

    def iterNode(self):
        """

        :return:
        """
        if self.root.next is self.root:
            return
        currentNode = self.root.next
        while currentNode.next is not self.root:
            yield currentNode
            currentNode = currentNode.next
        yield currentNode

    def __iter__(self):
        for node in self.iterNode():
            yield node.value

    def iterNodeReverse(self):
        if self.root.prev is self.root:
            return

        currentNode = self.root.prev

        while currentNode is not self.root:
            yield currentNode
            currentNode = currentNode.prev

        yield currentNode


# def testDoublelinkedlist():
#     dll = circualDoubleLinkedList()
#     assert len(dll) == 0
#
#     dll.append(0)
#     dll.append(1)
#     dll.append(2)
#     print(node.value for node in dll.iterNodeReverse())
#
#     assert list(dll) == [0,1,2]
#
#     assert [node.value for node in dll.iterNode()] == [0,1,2]
#     # print(node.value for node in dll.iterNodeReverse())
#     # assert [node.value for node in dll.iterNodeReverse()] == [2,1,0]
#
#
#     headNode = dll.headNode()
#     assert headNode.value == 0
#     dll.remove(headNode)
#     assert len(dll) == 2
#     assert [node.value for node in dll.iterNode()] == [1, 2]
#
#     dll.appendLeft(0)
#     assert [node.value for node in dll.iterNode()] == [0, 1, 2]


if __name__ == "__main__":
    dll = circualDoubleLinkedList()

    dll.append(0)
    dll.append(1)
    dll.append(2)
    print([node.value for node in dll.iterNodeReverse()])
    print([node.value for node in dll.iterNode()])
