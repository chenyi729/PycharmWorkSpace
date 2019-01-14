# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :

'''
from DataStructure.LinearStructure import linkedList as ll

class FullError(Exception):
    pass
class EmptyError(Exception):
    pass

class Queue(object):
    def __init__(self,maxsize=None):
        self.maxsize = maxsize
        self.__item_linked_list = ll.linkedList()

    def __len__(self):
        return len(self.__item_linked_list)

    def push(self,value):
        if self.maxsize is not None and len(self) >= self.maxsize:
            raise  FullError("queue full")
        return  self.__item_linked_list.append(value)

    def pop(self):
        if len(self) <= 0:
            raise EmptyError("queue empty")
        return self.__item_linked_list.popleft()


def testQueue():
    q = Queue()

    q.push(1)
    q.push(2)
    q.push(3)


    assert  len(q) ==3

    assert  q.pop()==1
    assert  q.pop()==2
    assert  q.pop()==3

