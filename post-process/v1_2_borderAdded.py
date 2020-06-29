'''
### Description:
###         Generate random direction each time creates a new pts,
###         draw it in 200x200.Border done. 
### Future Goal:
###         1.[Done]border detection
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
    '''
    spread all over the selected area
    '''
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
        '''
        show a 3x3 direction grid of a given coordinate
        '''
        allNextCoord = lambda i,j:[(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j),  (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)]
        for index,val in enumerate(allNextCoord(i, j)):
            if index%3 == 0:
                print('\n')      
            print(val,end=' ') 

    def direction(self, i,j):
        '''
        generate directions according to last direction
        '''
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
    print('\n-----------------------------')
    #print(t.direction(100, 100))
    # track of iter 10000 coords
    points = []
    # start point at (100,100):about the middle of an img np.ones(200,200) which is defined below
    newD = (100, 100)
    # init log level
    logging.basicConfig(level=logging.INFO)
    # i was going to print 10000 points but crashed,if not print,will B ok,maybe a memory cost problem
    while True: 
        newD = t.direction(*newD)# check the return value of function direction(),update newD each time newD`s alive time is the for loop
        # border detection
        if newD[0]>0 and newD[1]>0 and newD[0] < 200 and newD[1] < 200:
            points.append(newD)
        else:
            print(newD)# stop at this point
            break
        
    # logging.info('i = {}'.format(i)) # may not
    # if points is too large,print is not recommmended
    #print(points)
    # make us a canvas
    img = np.ones((200, 200))
    # draw points in img
    [cv2.circle(img, point, 1, (0,255,0), 1) for point in points]
    cv2.imshow('img',img)
    cv2.waitKey()


