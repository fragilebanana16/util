'''
Description:
            angel growth in white, init two angles ↑ and →,choose a middle angel one
            direction:clockwise,
    
            # this function calculates ↑ and →,and then return the final two directions
            def funcIter(up,right,iterationTimes):
            
                if iterationTimes < 1:
                    return up,right
                    
                calculate two distancesToWhite(up ,right)
                
                if upDistance > rightDistance:
                    right = middleDistanceOfUpandRight(up ,right)
                else upDistance < rightDistance:
                    up = middleDistanceOfUpandRight(up ,right)
                    
                funcIter(up,right,iterationTimes-1)
            # then we need to calculate the middle one,then get its vertical vector,
            # if middel of middle one and the vertical one is shorter,then the fore-middle one
            # is selected as the final direction of this point growth,if not,then funcIter is used again




            returnedUp ,returnedRight = funcIter(up(random`s),right(random`s),iterationTimes=5)
            calculate distancesToWhite(returnedRight)
            getTheMiddleDistanceOneOfTheRets = middleDistanceOfUpandRight(up ,right)
            if getTheMiddleDistanceOneOfTheRets < returnedUp:
                final = getTheMiddleDistanceOneOfTheRets
            else:
                funcIter(up,right,iterationTimes)
            
Note that:
         
Date:
            2019/09/24
'''
import cv2
import numpy as np
import random
import math
# concise number measure
from decimal import Decimal
# fraction used in equation
from fractions import Fraction

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

def growthWithFixedPattern(img,startAt,patternGrowth,pattern,color,thickness=2):
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
        try:
            if imgTestGray[start[0]][start[1]] == 0:
##                print('[Info] reached the edge.')
                cv2.line(imgTest,(startAt[1],startAt[0]),(start[1],start[0]),color,2)
                return start
        except Exception:
            print('[Warning] something wrong happened!Can not find the edge!')
            
def growth(img,startAt,equation):
    x = list(startAt)
##    print(x)
    while True:
##        print(equation(x[0]))
        y = int(equation(x[1]))

##        print(x)
        
##        temp = y
       
##        try:
        if imgTestGray[y][x[1]] == 0:
            break
##        except Exception:
##            return y,x[1]
            



        x[1] += 1

  
    return y,x[1]
            
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

def binaryDivide(origin,a,b,distanceA,distanceB,iterTimes,Right2Left=lambda i,j:(i,j-1)):
    """
    Description:
        Divide a rect angle with a binary method
        
        Note that i did not switch the call in main
    Param:
        a,b:pt coordinates
        
        distanceA,distanceB: pt a to zero origin pt distance,pt b to zero origin pt distance
        
        iterTimes: iter the binary divide for that much times
        
        Right2Left: third if case,reverse the axis
    Return:

        c: final direction end pt
    """
    
    for i in range(iterTimes):
        a,b = np.array(a),np.array(b)
        c = ((a+b)/2).astype(int)
##        cv2.line(imgTest,(origin[1],origin[0]),tuple((c[1],c[0])),(255,0,0),2)
        # coordinates are already too close
        if abs(c[0]-origin[0]) > 0.1:
            # apply fraction to avoid unneccessary float convert,decimal more accurate also avoid some issues
            euqation=lambda x:Decimal(float((Fraction((x-origin[0])*(c[1]-origin[1]),(c[0]-origin[0]))+origin[1]))) 
            c = growth(imgTest,origin,euqation)
            distanceC = distanceOfTwoPts(c,randPts[0])
            if distanceC >= distanceA and distanceC <= distanceB:
                a = c
                distanceA = distanceOfTwoPts(a,origin)
            elif distanceC >= distanceB and distanceC <= distanceA:
                b = c
                distanceB = distanceOfTwoPts(b,origin)
            elif distanceC <= distanceA and distanceC <= distanceB:
                # aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                d = np.array(growthWithFixedPattern(imgTestGray,origin,ptGrowth,Right2Left,redyellow))
                b = d
                a = c
                distanceA = distanceOfTwoPts(a,origin)
                distanceB = distanceOfTwoPts(b,origin)
##            elif distanceC >= distanceB and distanceC <= distanceA:
##                b = c
##                distanceB = distanceOfTwoPts(b,origin)

                
            
            cv2.line(imgTest,(origin[1],origin[0]),tuple((c[1],c[0])),(255,0,0),2)
##            cv2.line(imgTest,origin,tuple(ret),(255,0,0),2)
        else:
            print("close enough!")
            break
##    cv2.line(imgTest,(origin[1],origin[0]),tuple((ret[1],ret[0])),(0,255,255),4)
    return c
        
if __name__ == '__main__':
    green = (0,255,0)
    blue = (0,0,255)
    redyellow = (0,150,255)
    # generate num random pts
    num = 20
    # pattern
    Down2Up = lambda i,j:(i-1,j) # note different with 2d-coord,starts at left up corner
    Left2Right = lambda i,j:(i,j+1) # vertical is i
    
    # from loc grow with a pattern
    ptGrowth = lambda loc, pattern:pattern(*loc)
    
    # get us a 400*300  arr,one channel
    imgTest = np.zeros((400, 300, 3),np.uint8) # better choose a non-mirror shape,in case some coordinate err
    imgTestGray = cv2.cvtColor(imgTest,cv2.COLOR_BGR2GRAY)

    
    
    # pick a built-in rectangle draw it with black 
    imgTest[111:200,66:299] = (255,255,255)
    imgTestGray[111:200,66:299] = 255
    
    ##cv2.imshow('imgTest',imgTestGray)
## =================================================================================
    randPts = generateRandomPoints(num,imgTestGray)
##    cv2.circle(imgTest,(randPts[0][1],randPts[0][0]), 5, (255,0,0), -1)
##    print(randPts)
##    for i in randPts:
##        # circle really sucks,arg center is converse with normal one
##        cv2.circle(imgTest,(i[1],i[0]), 2, (0,0,255), -1)

    # we need two initial growth margins,only inital once
    a = np.array(growthWithFixedPattern(imgTestGray,randPts[0],ptGrowth,Down2Up,blue))
    distanceA = distanceOfTwoPts(a,randPts[0])
    
    b = np.array(growthWithFixedPattern(imgTestGray,randPts[0],ptGrowth,Left2Right,green))
    distanceB = distanceOfTwoPts(b,randPts[0])
    
    print('distanceA,distanceB:')
    print(distanceA,distanceB)
    # iter 5 times find the final pt`s end
    c = binaryDivide(randPts[0],a,b,distanceA,distanceB,4)
##    print(c)
##    for i in range(5):
##        # this pt needs to be int in image index
##        c = ((a+b)/2).astype(int)
##        if distanceA > distanceB:
##            b = c
##            distanceA = distanceOfTwoPts(b,randPts[0])
##        else:
##            a = c
##            distanceB = distanceOfTwoPts(a,randPts[0])
##        cv2.line(imgTest,(randPts[0][1],randPts[0][0]),tuple((c[1],c[0])),(0,255,0),2)
    
    cv2.imshow('imgTest',imgTest)


##def middlePoint(head,tail,iterTimes):
##    if iterTimes < 1:
##        return head,tail
    










### raw img in gray mode,note that we donot need to cvtColor to fit function findContour()`s first para,which need 8bit single channel
##img = cv2.imread('1.jpg',1)
##
##imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##
### just to make sure
##ret,thresh = cv2.threshold(imgGray,25,255,0)
##
##cv2.imshow('thresh',thresh)

