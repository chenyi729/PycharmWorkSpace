# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc :

'''

class Bag(object):

     def __init__(self,maxsize=10):
         self.maxsize = maxsize
         self._items = list()

     def add(self,item):
         if len(self) > self.maxsize:
             raise Exception("Bag is full")
         self._items.append(item)

     def remove(self,item):
         self._items.remove(item)

     def __len__(self):
         return len(self._items)

     def __iter__(self):
         for item in self._items:
             yield item




if __name__ == "__main__":
    bag = Bag()

    bag.add(1)
    bag.add(2)
    bag.add(3)
    bag.add(4)


    #断言
    assert  len(bag) == 4

    bag.remove(4)

    assert  len(bag) == 3

    for i in bag:
        print(i)

