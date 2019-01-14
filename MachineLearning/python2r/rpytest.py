# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc : python 调用 R

'''
import rpy2.robjects as robjects
import rpy2

print(rpy2.__path__)

rcode='''f<-function(r){pi*r}
         f(3)
      '''
print(robjects.r(rcode))


from rpy2.robjects.packages import  importr

base = importr("base")
print(base.letters[0])

stats = importr('stats')
graphics = importr('graphics')

plot = graphics.plot
rnorm = stats.rnorm
plot(rnorm(100),ylab="random")

