'''
### Description:
###         Random pts in edge with black value spread in black area with a shape
###         of 米, stop when reach the border and the value is white.
###
###         
### Future Goal:
###         1.river direction cluster

'''
import random
import numpy as np
import cv2
import math
import os
from collections import Counter
import logging   
class Sami:
    '''
    random one to end(edge),spread all over the inside area,no turning back,
    draw strategy:from one point to it`s selected direction`s edge.
         
    '''
    def __init__(self):
        '''
        relevant pattern would be used for generate the directions,
        note that lt and rd share one direction candidate(if u just draw a craft u will know it,
        only six directions are allowed).
        '''
        # chosse direction, no turning back direction and last direction
        self.Down2UpCandidates = self.Up2DownCandidates = lambda i,j:[(i-1,j-1), (i-1,j+1), (i,j-1), (i,j),  (i,j+1), (i+1,j-1), (i+1,j+1)]
        self.Right2LeftCandidates = self.Left2RightCandidates = lambda i,j:[(i-1,j-1), (i-1,j), (i-1,j+1), (i,j), (i+1,j-1), (i+1,j), (i+1,j+1)]
        self.toLeftTopCandidates = self.toRightdownCandidates = lambda i,j:[(i,j-1), (i+1,j-1), (i-1,j), (i-1,j+1), (i,j+1), (i+1,j)]
        self.toLeftdownCandidates = self.toRightTopCandidates = lambda i,j:[(i-1,j-1), (i-1,j), (i,j-1), (i,j),  (i,j+1), (i+1,j), (i+1,j+1)]
        # growth pattern
        self.Down2Up = lambda i,j:(i-1,j)
        self.Up2Down = lambda i,j:(i+1,j)
        self.Right2Left = lambda i,j:(i,j-1)
        self.Left2Right = lambda i,j:(i,j+1)
        self.toLeftTop =lambda i,j:(i-1,j-1)
        self.toRightdown = lambda i,j:(i+1,j+1)
        self.toLeftdown = lambda i,j:(i+1,j-1)
        self.toRightTop = lambda i,j:(i-1,j+1)
        # begin with UpDown direction
        self.d = 'Up2Down'
        # choices for different patterns
        self.choice = {'Down2Up' : self.Down2UpCandidates, 'Up2Down' : self.Up2DownCandidates, \
                       'Right2Left' : self.Right2LeftCandidates ,'Left2Right' : self.Left2RightCandidates, \
                       'toLeftTop' : self.toLeftTopCandidates ,'toRightdown' : self.toRightdownCandidates , \
                       'toLeftdown' : self.toLeftdownCandidates,'toRightTop' : self.toRightTopCandidates}
        self.growthPattern = {'Down2Up' : self.Down2Up, 'Up2Down' : self.Up2Down, \
                              'Right2Left' : self.Right2Left,'Left2Right' : self.Left2Right, \
                              'toLeftTop' : self.toLeftTop ,'toRightdown' : self.toRightdown , \
                              'toLeftdown' : self.toLeftdown,'toRightTop' : self.toRightTop}
        self.allds = self.growthPattern.keys()
    def __add__(self,other):
        '''
        ???
        '''
        return 'what r u doing?'
    def getGrid(self, i, j):
        '''
        show a 3x3 direction grid of a given coordinate
        '''
        allNextCoord = lambda i,j:[(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j),  (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)]
        for index,val in enumerate(allNextCoord(i, j)):
            if index%3 == 0:
                print('\n')      
            print(val,end=' ')
    def readImgs(self):
        '''
        read label and gray with ROI
        '''
        self.Predict = 'label.tif'
        self.Edge = 'gray.tif'
        self.imgP = cv2.imread(self.Predict, 1)
        self.imgE = cv2.imread(self.Edge, 1)
        self.imgQ = self.imgP[0:3500,0:3500]
        self.imgQResized = self.imgQ[1100:1900,1100:1900]
        self.imgEResized = self.imgE[1100:1900,1100:1900]

    def showImgs(self):
        '''
        show imgs
        '''
        cv2.imshow('E', self.imgEResized)
        cv2.imshow('Q', self.imgQResized)
        cv2.waitKey()
    def generateRandomPoints(self, number):
        '''
        from 200 x 200 generate random coords
        '''
        paths = random.sample([(i,j) for i in range(800) for j in range(800)], number)
        return paths
    def generateRandomPointsEdge(self, number):
        '''
        from 200 x 200 generate random coords according to edge img
        '''
        remained = []
        paths = random.sample([(i,j) for i in range(800) for j in range(800)], number)

##        for path in paths:
##            print(str(path)+':'+str(self.imgEResized[path[0],path[1]]))

        for path in paths:
            if self.imgEResized[path[0],path[1]][0] == 255:# if white remove
                paths.remove(path)
##                print(str(path)+'removed')
            else:
                remained.append(path)

##        print('-------------')
##        for path in remained:
##            print(str(path)+':'+str(self.imgEResized[path[0],path[1]]))
        return remained
    def getDirection(self, i,j):
        '''
        generate directions according to last direction
        '''
        oldD = (i,j)
        # sample a new direction
        newD = random.sample(self.choice[self.d](i,j), 1)
        # ways of judge last move pattern,record last direction
        if oldD[0]-newD[0][0] == 1 and oldD[1]-newD[0][1] == 0:
            self.d = 'Down2Up'# create another pattern and raw d is needed
        elif oldD[0]-newD[0][0] == -1 and oldD[1]-newD[0][1] == 0:
            self.d = 'Up2Down'
        elif oldD[0]-newD[0][0] == 0 and oldD[1]-newD[0][1] == 1:
            self.d = 'Right2Left'
        elif oldD[0]-newD[0][0] == 0 and oldD[1]-newD[0][1] == -1:
            self.d = 'Left2Right'
        elif oldD[0]-newD[0][0] == oldD[1]-newD[0][1] == 1:
            self.d = 'toLeftTop'
        elif oldD[0]-newD[0][0] == oldD[1]-newD[0][1] == -1:
            self.d = 'toRightdown'
        elif oldD[0]-newD[0][0] == newD[0][1] - oldD[1] and oldD[0]-newD[0][0]<0:
            self.d = 'toLeftdown'
        else:
            self.d = 'toRightTop'
        
        # new position will be returned 
        return newD[0]
    def oneToEndGrowth(self,newD):
        '''
        from one coord to the edge of the canvas,in this file retired but still got
        reference value.
        '''
        newDsrc = t.getDirection(*newD) # generate one time
        pointsAll = []
        for alld in self.allds:
            newD = newDsrc
            points = []
            while True:
                if newD[0]>0 and newD[1]>0 and newD[0] < 200 and newD[1] < 200:
                    points.append(newD)
                    newD = t.growthPattern[alld](newD[0],newD[1])
                else:
                    pointsAll.append(points)
                    break
   

                #print(newD)# stop at this point

        return pointsAll # return the path of one start coord
    
    def miToEndGrowth(self,newD):
        '''
        mi shape spread
        '''
        newDsrc = t.getDirection(*newD) # generate one time
        pointsAll = [] # all directions collection of only one pt
        # 8 directions
        for alld in self.allds:
            newD = newDsrc # record the center of mi in each loop,refresh it in order to start in 8 directions with the same center
            points = [] # 
            while True:
                if self.imgEResized[newD[0],newD[1]][0] != 255 and newD[0]>0 and newD[0]<800-1 and newD[1]>0 and newD[1]<800-1:
                    points.append(newD) # collect 
                    newD = t.growthPattern[alld](newD[0],newD[1])# growth in one direction
                else:
                    pointsAll.append(points)# 8 directions package 
                    break
        return pointsAll # return the path of one start coord
    
if __name__=='__main__':
    t = Sami()
    t.readImgs()
    pts = t.generateRandomPointsEdge(1000)
    #print(pts)# (y,x) so reverse it in draw
    pointsAlls = [t.miToEndGrowth(path) for path in pts]
    [[[cv2.circle(t.imgEResized, (point[1],point[0]), 1, (0,255,0), 1)\
       for point in points] for points in pointsAll] for pointsAll in pointsAlls]
    t.showImgs()
  



