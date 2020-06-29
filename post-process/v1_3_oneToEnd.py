'''
### Description:
###         Generate one direction each time when it comes to
###         one pt which is random genrated, one way to the edge,
###         and draw it on 200*200
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
class Tantanle:
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
    def getGrid(self, i, j):
        '''
        show a 3x3 direction grid of a given coordinate
        '''
        allNextCoord = lambda i,j:[(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j),  (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)]
        for index,val in enumerate(allNextCoord(i, j)):
            if index%3 == 0:
                print('\n')      
            print(val,end=' ') 
    def generateRandomPoints(self, number):
        '''
        from 200 x 200 generate random coords
        '''
        paths = random.sample([(i,j) for i in range(200) for j in range(200)], number)
        return paths
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
        from one coord to the edge of the canvas
        '''
        points = []
        newD = t.getDirection(*newD) # generate one time
        while True: 
            # border detection
            if newD[0]>0 and newD[1]>0 and newD[0] < 200 and newD[1] < 200:
                points.append(newD)
                # keeps growing
                newD = t.growthPattern[t.d](newD[0],newD[1])
            else:
                #print(newD)# stop at this point
                break# edge detected
        return points # return the path of one start coord
            

    
if __name__=='__main__':
    # start rolling
    t = Tantanle()
    # create an object to realize the goal
    t = Tantanle()
    # generate 100 random points
    paths = t.generateRandomPoints(100)
    # collect all paths of each point
    pointsAll = [t.oneToEndGrowth(path) for path in paths]
    # make us a canvas
    img = np.ones((200, 200))
    # draw all paths
    [[cv2.circle(img, point, 1, (0,255,0), 1) for point in points] for points in pointsAll]
    cv2.imshow('img',img)
    cv2.waitKey()


