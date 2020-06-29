'''
### Description:
###         Generate random direction each time creates a new pts,
###         draw it in 200x200.No border detection. 
### Future Goal:
###         1.border detection
###         2.river direction cluster
###         3.modify the direction to 7 
'''
import random
import numpy as np
import cv2
import math
import os
from collections import Counter
import logging
class Tantanle:
    '''tan yi xia'''
    def __init__(self):
        # relevant pattern would be used for generate the directions,note that lt and rd share one direction candidate(if u just draw a craft u will know it,only six directions are allowed)
        self.ltCandidates = self.rdCandidates = lambda i,j:[(i,j-1), (i+1,j-1), (i-1,j), (i-1,j+1), (i,j+1), (i+1,j)]
        self.ldCandidates = self.rtCandidates = lambda i,j:[(i-1,j-1), (i-1,j), (i,j-1), (i,j),  (i,j+1), (i+1,j), (i+1,j+1)]
        self.upCandidates = self.downCandidates = lambda i,j:[(i-1,j-1), (i-1,j+1), (i,j-1), (i,j),  (i,j+1), (i+1,j-1), (i+1,j+1)]
        self.leftCandidates  = self.rightCandidates = lambda i,j:[(i-1,j-1), (i-1,j), (i-1,j+1), (i,j), (i+1,j-1), (i+1,j), (i+1,j+1)]
        # begin with UpDown direction
        self.d = 'UpDown'
        # choices for different patterns
        self.choice = {'UpDown' : self.upCandidates, 'LeftRight' : self.leftCandidates, \
                  'LeftTopOrRightdown' : self.ltCandidates ,'RightTopOrLeftdown' : self.ldCandidates }
       
    def getGrid(self, i, j):
        '''show a 3x3 direction grid of a given coordinate'''
        allNextCoord = lambda i,j:[(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j),  (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)]
        for index,val in enumerate(allNextCoord(i, j)):
            if index%3 == 0:
                print('\n')      
            print(val,end=' ') 

    def direction(self, i,j):
        '''generate directions according to last direction'''
        oldD = (i,j)
        # sample a new direction
        newD = random.sample(self.choice[self.d](i,j), 1)
        # ways of judge last move pattern,record last direction
        if abs(oldD[0]-newD[0][0]) == 1 and abs(oldD[1]-newD[0][1]) == 0:
            self.d = 'UpDown'
        elif abs(oldD[0]-newD[0][0]) == 0 and abs(oldD[1]-newD[0][1]) == 1:
            self.d = 'LeftRight'
        elif oldD[0]-newD[0][0] == oldD[1]-newD[0][1]:
            self.d = 'LeftTopOrRightdown'
        elif oldD[0]-newD[0][0] == newD[0][1] - oldD[1]:
            self.d = 'RightTopOrLeftdown'
        # new position will be returned 
        return newD[0]
    
if __name__=='__main__':
    # create an object to realize the goal
    t = Tantanle()
    # get a selectable path of coordinate (100,100)
    t.getGrid(100, 100)
    # spilt the grid, too many prints may raise the memory cost
    print('\n---------------')
    print(t.direction(100, 100))
    # track of iter 10000 coords
    points = []
    # start point at (100,100):about the middle of an img np.ones(200,200) which is defined below
    newD = (100, 100)
    # init log level
    logging.basicConfig(level=logging.INFO)
    # i was going to print 10000 points but crashed,if not print,will B ok,maybe a memory cost problem
    for i in range(10000): 
        newD = t.direction(*newD)# check the return value of function direction(),update newD each time newD`s alive time is the for loop
        points.append(newD)
        # logging.info('i = {}'.format(i)) # may not
    # if points is too large,print is not recommmended
    #print(points)
    # make us a canvas
    img = np.ones((200, 200))
    # draw points in img
    [cv2.circle(img, point, 1, (0,255,0), 1) for point in points]
    cv2.imshow('img',img)
    cv2.waitKey()









### 资源浪费最少的读取文件方法
##for line in open('main.py'):
##    print(line.upper(),end='')

##a = [1,2,3,4]
##b = iter(a)
##print(b.__next__())
### same as
##print(next(b))
##print(b.next())

##D = {'a':1,'b':2 }
##for key in D:
##    print(key,key[key])
##
##D = {'a':1,'b':2 }
##for key in D[key]:
##    print(key,key[key])
##
### 明确地获得键的列表
##D = {'a':1,'b':2 }
##for key in D.keys():
##    print(key,D[key])
##
##
##D = {'a':1,'b':2 }
##for key in D.keys():
##    print(key,key[key])
##
##D = {'a':1,'b':2 }
##I = iter(D)
##for key in I:
##    print(key,key[key])
##
##D = {'a':1,'b':2 }
##I = iter(D)
##for key in D:
##    print(key,I[key])
##
### 迭代获取键
##D = {'a':1,'b':2 }
##for key in D:
##    print(key,D[key])
##
### 迭代器只返回键
##D = {'a':1,'b':2 }
##I = iter(D)
##for key in I:
##    print(key)
##
##D = {'a':1,'b':2 }
##I = iter(D)
##for key in I:
##    print(key,I[key])

##res = []
##for i in range(10):
##    for j in range(5):
##        res.append((i,j))
##print(res)
##
##
### 列表解析的写法
##res2 = [(i,j) for j in range(5) for i in range(10) ]
##print(res2)

##r = range(5)
##print(iter(r) is r)

##items = [1,2,3,4]
##GT2 = [item for item in items if item > 2]
##print(GT2)

##seq1 = ['a','b','']
##a = map(bool,seq1)
##print(list(a))


##r = range(5)
##I1 = iter(r)
##I2 = iter(r)
##print(next(I1))# 两个迭代器分离进行哦
##print(next(I1))
##print(next(I2))


##a= [[(row,col)] for row in range(10) for col in range(5)]
##print(a)


##l = [[1,2,3],[4,5,6]]
####提取1 2 的方法
##collect = [x for (a,x,c) in l]
##print(collect)
##collect2 = list(map(lambda x:x[1],l))
##print(collect2)


##def mymap(func,*seqs):# 解包
##    print('seqs is:'+str(seqs)+',its type is:'+str(type(seqs)))
##    print('*seqs is:'+str(*seqs)+',its type is:'+str(type(*seqs)))
##    return [func(*args) for args in zip(*seqs)]
##print(mymap(abs,[-2,-1,0,1,2]))

##def mymap(func,*seqs):# 解包
##    return (func(*args) for args in zip(*seqs))
##print(list(mymap(abs,[-2,-1,0,1,2])))


##def mymap(func,*seqs):# 解包
##    for args in zip(*seqs):
##        yield func(*args)
##print(list(mymap(abs,[-2,-1,0,1,2])))

##def mymap(*seqs):# 解包
##    print(seqs)# ('1234','xy')解包后为(('1234', 'xy'),)，留了个逗号
##    print(type(seqs))
##    seqs = [list(S) for S in seqs]
##    print(seqs)
##s = ('1234','xy')
##print(*s)
##mymap(s)
#### 当s2为s时，应当与函数内部结果一致
##s2 = (('1234', 'xy'),)
##seqs = [list(S) for S in s2]# 进行了两次列表
##print(seqs)
##print('==============')# 结果不同的原因
##for S in s:
##    print(S)
##for S in s2:
##    print(S)
##
##def myzip(*seqs):# 解包
##    #('1234','xy')解包后为(('1234', 'xy'),)
##    print(seqs)
##    seqs = [list(S) for S in seqs]
##    #(('1234', 'xy'),)列表解析为 [['1', '2', '3', '4'], ['x', 'y']]
##    print(seqs)
##    res = []
##    while all(seqs):# 为什么不用while1就是因为两个串长度不一,pop将会pop空
##        res.append(tuple(S.pop(0) for S in seqs))
##    return res
##    
##
##s = ('1234','xy')
##print(myzip(*s))
####
####t = []
####p = [['1', '2', '3', '4'], ['x', 'y']]
####for p1 in p:
####    t.append([S.pop(0) for S in p])
####print(t)
##print('----------let the test begin--------------')
### 列表解析测试1
##seqs = (('1234', 'xy'))
##seqs = [list(S) for S in seqs]# 1234为最小单位,以最小单位迭代
##print(seqs)# [['1', '2', '3', '4'], ['x', 'y']]
### 列表解析测试2
##seqs = (('1234', 'xy'),)# 加个逗号
##seqs = [list(S) for S in seqs]# ('1234', 'xy')为最小单位
##print(seqs)# [['1234', 'xy']]
### 解包测试
##s = ('1234','xy')
##print(*seqs)# 解成了列表

### 几何解析
##print({x ** x for x in range(10)})
### 字典解析
##print(dict((x,x ** x) for x in range(10)))
### 表达式有两个项
##a = iter((x,x ** x) for x in range(10))
##print(a.__next__())
##print(a.__next__())


### 集合无序
##
##a={x*x for x in range(20) if x%2 == 0}
##print(a)

##
##def forLoop():
##    res = []
##    for x in range(10):
##        res.append(abs(x))
##    return
##def listComp():
##    return [abs(x) for x in range(10)]
##def mapCall():
##    return list(map(abs,range(10)))
##def genExpr():
##    return list(abs(x) for x in range(10))
##def genFunc():
##    for x in range(10):
##        yield(abs(x))
##print(list(genFunc()))
##def genFunc():
##    def gen():
##        for x in range(10):
##            yield(abs(x))
##    return list(gen())
##print(genFunc())
##a,b,c = 1,2,3
##print('{0},{1}'.format(a,b))# recommended method
##print('%d,%d'% (a,b))

##def func(x=[]):# 默认参数像全局变量一般存在，但并不是全局，且重复运行代码不重新初始化
##    x.append(1)
##    print(x)
##    
##func()# [1]  默认[]append一个1
##func([2])# [2, 1]  此处初始化x了，参数[2]append一个1
##func()# [1, 1]  如果没有初始化x，将一直增长
##func()# [1, 1, 1]
##func()# [1, 1, 1, 1]

##def func(x=None):
##    if x is None:# 可以写成 x = x or []
##        x = []
##    x.append(1)
##    print(x)
##func([2])# x非None []append 一个1  [2, 1]
##func()# x为None，None append一个1  [1]
##func()# [1] 可以看到每次默认参数不再增加

##import modTest
##if __name__ == '__main__':
##    print('2')

##import pdb
##for i in range(5):
##    i +=1
##    pdb.set_trace() # 运行到这里会自动暂停,调试的话p i应该是1
##    print(i)


### import the necessary packages
##import argparse
## 
### construct the argument parse and parse the arguments
##ap = argparse.ArgumentParser()
##ap.add_argument("-n", "--name", required=False,
##	help="name of the user")# this arg is required
##args = vars(ap.parse_args())
##print(args)# a dict
## 
### display a friendly message to the user
##print("Hi there {}, it's nice to meet you!".format(args["name"]))

##l1 = [1,2,3]
##l2 =l1.copy() # same to l1[:]
##l1[0] = 4
##print(l1,l2,end=' ')
import copy
##origin = [1, 2, [3, 4]]
##cp1 = copy.copy(origin)#浅拷贝嵌套部分共享
##cp2 = copy.deepcopy(origin)
##origin[1] = "hey!"# 试图改变origin来改变cp1，然并卵，外层已经拷贝了，如果改变内层，cp1才变
##print(cp1)
##print(cp2)

##list1 = [1, 2, [3, 4]]
##list2 = list1.copy()# 浅拷贝改list1内层嵌套的数据，应该list2会变
##list1[2][0] = 5
##print(list2)


##x = 2
##y = 2
##print(x==y)
##print(x is y)
##
##x = 2
##y = x
##print(x==y)
##print(x is y)

##import sys 
####s = 'this'
####a = sys.getrefcount('this')
####print(a)
####x = 'this'
####a = sys.getrefcount('this')
####print(a)
####x = 'this'
####a = sys.getrefcount('this')
####print(a)
##
##import numpy
##print(sys.modules)



##class intresting():
##    def __init__(self, value):
##        self.data = value
##    def __add__(self, other):
##        return intresting(self.data+other)# sao operation
##    def __str__(self):
##        return '{}'.format(self.data)
##a = intresting('25')
##print(a)
##b = a + '5'
##print(b)

### empty class
##class Empty:pass # do nothing but pass, no inside stuff
##Empty.name = 'dicken' # an empty class with no attributes,
##Empty.age = 24 # but can have one outside cause a class is also a object
##x = Empty() # create a empty class object
##y = Empty() # create another empty class object
##print(x.name,y.name) # this two should be using the same name 'dicken'
##x.name = 'jone' # this time a new name is assigned to the object, however class Empty does not have that attributes
##print(x.name)# jone
##print(Empty.__dict__.keys()) # a namespace dictionary:dict_keys(['__module__', '__dict__', '__weakref__', '__doc__', 'name', 'age'])
##print(x.__dict__.keys()) # x only have name
##print(y.__dict__.keys()) # y does not have any object namespace dictionary
##print(x.__class__) # check out object x`s class,Empty
##print(Empty.__bases__) # check out class Empty`s base class
