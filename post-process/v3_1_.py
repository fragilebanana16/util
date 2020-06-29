'''
Description:
            Get random pts` single direciton descriptor:a blue line for each point.
            This file test on real image
            
Note that:
            Test img is actually edged around with black color. 
            None type bug fixed,but float zero division is not added.
            This is a testing py file,many prints for test in the code may not be so elegant to read.
            Float zero division bug fixed,with a 0.0001 added to the divider.

Date:
            2019/10/08
'''
import cv2
import numpy as np
import random
import math
# concise number measure
from decimal import Decimal
# fraction used in equation
from fractions import Fraction
import heapq

def generateRandomPoints(number,img):
    """
    Description:
        Generate random points,if it is black collect it,already tested in a for range unit test,
    a maximum recursion depth would occur if depth is over 1000.

    Param:
        number:candidates for choosing,int
        
        img: a binary img
        
    Return:
        collectedPts: selected pts(if it is white),a list with tuple in it
    """
    assert number>0, "maybe a none-zero number?"
    # sample some random pts through the whole img
    randPts = random.sample([(i,j) for i in range(img.shape[0]) for j in range(img.shape[1])], number)
    collectedPts = []
    for i in randPts:
        if img[i[0]][i[1]] == 255:
            collectedPts.append(i)
##            print(img[i[0]][i[1]])
    # note that we cast some pts,then judge it if it is black,so casted could all be white
    if len(collectedPts) < 1:
        # use a self iteration to avoid collecting an empty pts list
        ret = generateRandomPoints(number,img)
        # remember to ret values,otherwise errs occur
        return ret
    else:
        # works fine get into this statement
        return collectedPts

def growthWithFixedPattern(img,startAt,pattern,color,thickness=2):
    """
    Description:
        Growth with a given pattern until edge(black)
    Param:
        img: a gray img
        
        startAt: initial pt:a random pt
        
        patternGrowth: growth action
        
        pattern: a pattern used for giving direction of growth
        
        color: (B,G,R)
        
        thickness: draw line thickness
   
    """
    start = startAt
    while True:
        coord = ptGrowth(start,pattern)
        start = coord
        
        if start[1]>=imgTestGray.shape[1] or start[0]>=imgTestGray.shape[0]:
##            print('[Info] index out of image.')
            return start
  
        if img[start[0]][start[1]] == 0:
##            print('[Info] reached the edge.')
##            cv2.line(imgTest,(startAt[1],startAt[0]),(start[1],start[0]),color,2)
            return start

##        print(start)

            
def distanceOfTwoPts(pt1,pt2):
    """
    Description:
        Distance of two pts
    Param:
        pt1:an array
        
        pt2:an array

    Return:
        distance:a int-likely number
    """
    diff = np.array(pt1) - np.array(pt2)
    distance = math.hypot(diff[0],diff[1])
    return distance


def calculateTwoEdgeDistance(a,b,pt):
    """
    Description:
        Calculate four edge growths` path length,we need max two to generate direction descriptor
    
    Param:
        a,b:pattern
        
    Return:
        pt1,pt2,distance
        
    """
    pt1 = growthWithFixedPattern(imgTestGray,pt,a,green,thickness=2)
    pt2 = growthWithFixedPattern(imgTestGray,pt,b,green,thickness=2)
    return pt1,pt2,distanceOfTwoPts(pt1,pt2)

def drawMiddlePt(pair1,pair2,color1,color2):
    """
    Description:
        With four coords,we get two centers of two pairs,visualize the pt and line
    
    Param:
        pair1,pair2:two growth paths` edge pts
        
    Return:
        equation ready-to-use coords 
        
    """
    middlePt = lambda a,b:((a[0]+b[0])/2,(a[1]+b[1])/2)
    pt1 = middlePt(pair1[0],pair2[0])
    pt2 = middlePt(pair1[1],pair2[1])
##    cv2.circle(imgTest,(int(pt1[1]),int(pt1[0])), 4, color1, -1)
##    cv2.circle(imgTest,(int(pt2[1]),int(pt2[0])), 4, color1, -1)
##    cv2.line(imgTest,(int(pt1[1]),int(pt1[0])),(int(pt2[1]),int(pt2[0])),color1,2)
    
    pt3 = middlePt(pair1[0],pair2[1])
    pt4 = middlePt(pair1[1],pair2[0])
##    cv2.circle(imgTest,(int(pt3[1]),int(pt3[0])), 4, color2, -1)
##    cv2.circle(imgTest,(int(pt4[1]),int(pt4[0])), 4, color2, -1)
##    cv2.line(imgTest,(int(pt3[1]),int(pt3[0])),(int(pt4[1]),int(pt4[0])),color2,2)

    return ((pt1,pt2),(pt3,pt4))

def growth(startPt,euqation,euqation_,color):
    """
    Description:
        Growth from origin pt to edge according to equation
    
    Param:
        startPt: start point
        equation: one of two option
        color: draw the growth path
        
    Return:
        Edge points pair
        
    """
    pair1 = startPt
    pair2 = startPt
    start = startPt[0]
    while True:
        start += 1#
##        print(euqation(start))
        # overflow switch
        if start < 0 or start > imgTestGray.shape[0]-1: 
##            print("[Info]index overflow",euqation(start) )
            break
        elif euqation(start) >imgTestGray.shape[1]-1:
            # y=x to x=y
            pair1 = (int(euqation_(imgTestGray.shape[1]-1)),imgTestGray.shape[1]-1)
            break
        elif euqation(start) < 0:
           pair1 = (int(euqation_(0)),0)
           break
##        print((start,euqation(start)),end=' ') # check the growth coords if u want to
##        imgTest[int(start)][int(euqation(start))] = color
        pair1 = (int(start),int(euqation(start)))
        if imgTestGray[int(start)][int(euqation(start))] == 0:
##            print("[Info]edge detected")
            break
        
    # back to start do it again,but another direction
    start = startPt[0]
    while True:
        start -= 1#
        if start < 0 or start > imgTestGray.shape[0]-1: 
##            print("[Info]index overflow2",euqation(start) )
            break
        elif euqation(start) >imgTestGray.shape[1]-1:
            pair2 = (int(euqation_(imgTestGray.shape[1]-1)),imgTestGray.shape[1]-1)
            break
        elif euqation(start) < 0:
            pair2 = (int(euqation_(0)),0)
            break
##        print((start,euqation(start)),end=' ') # check the growth coords if u want to
##        imgTest[int(start)][int(euqation(start))] = color
        pair2 = (int(start),int(euqation(start)))
        if imgTestGray[int(start)][int(euqation(start))] == 0:
##            print("[Info]edge2 detected")
            break
##    print("[Info]round finished") 
    return pair1,pair2
if __name__ == '__main__':
    green = (0,255,0)
    blue = (255,0,0)
    redyellow = (0,150,255)
    red = (0,0,255)
    # generate num random pts
    num = 50
    # pattern
    Down2Up = lambda i,j:(i-1,j)
    Up2Down = lambda i,j:(i+1,j)
    Right2Left = lambda i,j:(i,j-1)
    Left2Right = lambda i,j:(i,j+1)
    toLeftTop =lambda i,j:(i-1,j-1)
    toRightdown = lambda i,j:(i+1,j+1)
    toLeftdown = lambda i,j:(i+1,j-1)
    toRightTop = lambda i,j:(i-1,j+1)
    
    # from loc grow with a pattern
    ptGrowth = lambda loc, pattern:pattern(*loc)
    # ====================test with self made image====================
##    # get us a 400*300  arr,one channel,colored one is for visualize different growth
##    imgTest = np.zeros((400, 300, 3),np.uint8) # better generate a symmetrical shape,in case some coordinate err
##    imgTestGray = cv2.cvtColor(imgTest,cv2.COLOR_BGR2GRAY)
##
##    
##    
##    # pick a built-in rectangle draw it with black 
##    imgTest[111:200,66:299] = (255,255,255)
##    imgTestGray[111:200,66:299] = 255
    # ====================test with self made image====================
    
    imgTest = cv2.imread("1.jpg",1)
    imgTestGrayCvt = cv2.cvtColor(imgTest,cv2.COLOR_BGR2GRAY)
    ret,imgTestGray = cv2.threshold(imgTestGrayCvt,127,255,cv2.THRESH_BINARY)
##    cv2.imshow("11",imgTestGray)

        
    print(imgTestGray.shape)
    # some rand pts in white area,note that return numbers is not arg num,num is just a base number
    randPts = generateRandomPoints(num,imgTestGray)
    print("there are {} random pts ready!".format(len(randPts)))
    print(randPts)
    fullPattern = [(toLeftTop,toRightdown),(Right2Left,Left2Right),(Down2Up,Up2Down),(toRightTop,toLeftdown)]
##    randPt = randPts[0]
    
    for randPt in randPts:
        ret3elements = [calculateTwoEdgeDistance(i,j,randPt) for i,j in fullPattern]

        # stores four couples of coords
        coords = [i[:2] for i in ret3elements]
    ##        print("[Info]Four couples of coords:\n",coords)
        # four directions` distances
        d = [i[2] for i in ret3elements]
    ##        print("[Info]Four distances:\n",d)     
        # find max 2`s index
        index = map(d.index, heapq.nlargest(2, d)) 
        # find max 2
        max2 = heapq.nlargest(2, d) 
        # better use a temp copy
        temp = list(index)
        # get max 2`s coords 
        pair1 = coords[temp[0]]
        pair2 = coords[temp[1]]
    ##    print(pair1,pair2)
    ##    print(pair1[0],pair2[0])
        # =================the first binary divide=========================
        coord1,coord2 = drawMiddlePt(pair1,pair2,red,redyellow)
    ##    print("[Info]check coords...")
    ##    print("coord1:{}\ncoord2:{}".format(coord1,coord2))
        
        # the first equation,0.0001 is for the case that the divider is zero
        euqation1 = lambda x:float((x-coord1[0][0])*(coord1[1][1]-coord1[0][1])/\
                                                (coord1[1][0]-coord1[0][0]+0.0001)+coord1[0][1])
        # get x
        euqation1_1 = lambda y:float((y-coord1[0][1])*(coord1[1][0]-coord1[0][0])/\
                                                    (coord1[1][1]-coord1[0][1]+0.0001)+coord1[0][0])
    ##    print("[Info]this is correction")
    ##    print(coord1[0][0],euqation1(coord1[0][0]))
        # the second equation
        euqation2 = lambda x:float((x-coord2[0][0])*(coord2[1][1]-coord2[0][1])/\
                                                    (coord2[1][0]-coord2[0][0]+0.0001)+coord2[0][1])
        # get x
        euqation2_2 = lambda y:float((y-coord2[0][1])*(coord2[1][0]-coord2[0][0])/\
                                                    (coord2[1][1]-coord2[0][1]+0.0001)+coord2[0][0])
    ##    print("[Info]this is correction2")
    ##    print(coord2[0][0],euqation2(coord2[0][0]))
    ##    print("[Info]correction done")
        
        # left growth
        p1,p2 = growth(coord1[0],euqation1,euqation1_1,red)
        # right growth
        p3,p4 = growth(coord1[0],euqation2,euqation2_2,redyellow) 


      ##    print(pair1,pair2)
    ##    print(pair1[0],pair2[0])

        # edge point
    ##        [cv2.circle(imgTest,(i[1],i[0]), 4, (150,150,0), -1) for i in [p1,p2,p3,p4]]
    ##        print("[Info]first divide done")
    ##    # =================the second binary divide=========================
    ##    coord11,coord22 = drawMiddlePt((p1,p2),(p3,p4),blue,green)            
    ####        print(coord11,coord22)
    ##    # the first equation
    ##    euqation11 = lambda x:float((x-coord11[0][0])*(coord11[1][1]-coord11[0][1])/\
    ##                                                (coord11[1][0]-coord11[0][0])+coord11[0][1])
    ##    # get x
    ##    euqation11_1 = lambda y:float((y-coord11[0][1])*(coord11[1][0]-coord11[0][0])/\
    ##                                                (coord11[1][1]-coord11[0][1])+coord11[0][0])
    ##    rcle(imgTest,(i[1],i[0]), 4, (150,150,0), -1) for i in [p11,p22,p33,p44]]
    ##    # =================the second binary divide=========================

        # =================output final descriptor:a couple coords============
        whoIsLonger = lambda a,b:a if distanceOfTwoPts(*a)>distanceOfTwoPts(*b) else b
        getItsCoords = whoIsLonger((p1,p2),(p3,p4))
        # print("[Info]chosen one:\n",getItsCoords)
        # final direction
        cv2.line(imgTest,(int(getItsCoords[1][1]),int(getItsCoords[1][0])),\
                 (int(getItsCoords[0][1]),int(getItsCoords[0][0])),blue,2)
        
        # center of each with red colored
    ##        cv2.circle(imgTest,(randPt[1],randPt[0]), 3, red, -1)
    cv2.imshow('imgTest',imgTest)
    cv2.imshow('imgGray',imgTestGray)





