# -*- coding:utf-8 -*-
# find the indexs of max 10 values
import numpy as np
import cv2
import math
import os
#from skimage import measure, color
#os.environ["CUDA_VISIBLE_DEVICES"] = "1"
#from os import listdir
#from skimage.io import imread, imsave
#from matplotlib import pyplot as plt
from collections import Counter
#
#from skimage import data, util
'''
                                                       ver 1
'''
# maxN = []
# m = np.array([[1,2,3],[4,6,6],[7,6,9]])
# a = m.flatten()
# print(a)
# n = np.argmax(m)
# print(n)
# max = a[n]
# index = np.argwhere(m == max)
# print(index)
# maxN.append(index)
# m[index[0][0],index[0][1]] = 0
# print(m)
#
# n2 = np.argmax(m)
# print(n2)
# max = a[n2]
# index = np.argwhere(m == max)
# print(index)
# maxN.append(index)
# m[index[0][0],index[0][1]] = 0
# print(m)
# print('--------')
# print(maxN)


'''
                                                        ver 2
'''
# Predict = '/home/ydf/Hehao/Post_process/test_0716/GF2_PMS1__20160327_L1A0001491484-MSS1_label.tif'
# Edge = '/media/ydf/disk1/data/rssrai2019_semantic_segmentation/test/edge_results_test/process1/GF2_PMS1__20160327_L1A0001491484-MSS1 (2).tif'
#
# imgP = imread(Predict)
# imgE = imread(Edge)
# imgQuarter = imgP[0:3500,0:3500]
#
#
#
# #
# # label = measure.label(imgE)
# # props = measure.regionprops(label)
# # c = props[25].bbox
# # print(c)
# # cv2.rectangle(imgE,(c[0],c[1]),(c[2],c[3]),(255, 255, 255), 20)
# #
# #
# # pic = cv2.resize(imgE, (960, 960), interpolation=cv2.INTER_CUBIC)
# # cv2.imshow('d',pic)
# # cv2.waitKey()
#
# label = measure.label(imgE, connectivity=2)
# print(label)
# maxN = []
# # label = np.array([[1,2,3],[4,6,6],[6,7,7]])
# flatLabel = label.flatten()
# counts = Counter(flatLabel)
# topN = counts.most_common(10)
# print(topN)
#
# # if max 10,all max have only one value,which means each value is different with others
# for i in range(10):
#     # record the locations  of all max locations that share one value,
#     # for example,array([[3499, 3402], [3499, 3403], [3499, 3404],[3499, 3405]]),four locations share one value.
#     index = np.argwhere(label == topN[i][0])
#     # collect the max locations
#     maxN.append(index)
#
# # print(label)
#
# print(maxN)
# print(maxN[0])
#
#
#
# # operation on predict img
# first = [tuple(imgQuarter[coord[0]][coord[1]]) for coord in maxN[0]]# collect the color infomation according to locations
# countColor = Counter(first)
# topColor = countColor.most_common(3)# top 1 color will be used,in this case (0,0,0)
# print(topColor)
#
# for coord in maxN[0]:
#     imgQuarter[coord[0]][coord[1]] = topColor[0][0]
#     # print('topColor[0][0]:',topColor[0][0])
#
#
#
#
# plt.imshow(imgQuarter)
# plt.show()

'''
                                                   ver 3 
'''
# from skimage.color import rgb2gray
# from skimage.draw import circle
# Predict = '/home/ydf/Hehao/Post_process/test_0716/GF2_PMS1__20160327_L1A0001491484-MSS1_label.tif'
# Edge = '/media/ydf/disk1/data/rssrai2019_semantic_segmentation/test/edge_results_test/0-3500---0-3500/GF2_PMS1__20160327_L1A0001491484-MSS1 (2).tif'
# imgP = imread(Predict)
# imgE = imread(Edge)
# imgQ = imgP[0:3500,0:3500]
# imgQResized = imgQ#[1100:1900,1100:1900]
# imgEResized = imgE#[1100:1900,1100:1900]
# img_gray = rgb2gray(imgEResized) # needs only one channel
# label = measure.label(img_gray, connectivity=2)
# for region in measure.regionprops(label):# label 0 will be ignored
#     if region.area > 200000:
#         print(region.centroid)
#
# maxN = []
# flatLabel = label.flatten()
# counts = Counter(flatLabel)
# topN = counts.most_common(10)
# print(topN)
# print(topN[0][0])
# for i in range(10):
#     index = np.argwhere(label == topN[i][0])
#     print(index)
#     maxN.append(index)
# print(maxN)
# print(maxN[0])
# # print(maxN[0])
# print('?')
# for coord in maxN[0]:
#     # print('?')
#     # print(imgEResized[coord[0]][coord[1]])
#     imgEResized[coord[0]][coord[1]] = 0
# for coord in maxN[1]:
#     imgEResized[coord[0]][coord[1]] = 100
# for coord in maxN[2]:
#     imgEResized[coord[0]][coord[1]] = 150
# for coord in maxN[3]:
#     imgEResized[coord[0]][coord[1]] = 200
# for coord in maxN[4]:
#     imgEResized[coord[0]][coord[1]] = 220
# for coord in maxN[5]:
#     imgEResized[coord[0]][coord[1]] = 255
#
#
# first = [tuple(imgQResized[coord[0]][coord[1]]) for coord in maxN[0]]# collect the color infomation according to locations
# countColor = Counter(first)
# topColor = countColor.most_common(6)
# print(topColor)
# for coord in maxN[0]:
#     imgQResized[coord[0]][coord[1]] = topColor[0][0]
# for coord in maxN[1]:
#     imgQResized[coord[0]][coord[1]] = topColor[1][0]
# for coord in maxN[2]:
#     imgQResized[coord[0]][coord[1]] = topColor[2][0]
# for coord in maxN[3]:
#     imgQResized[coord[0]][coord[1]] = topColor[3][0]
#
# plt.imshow(imgEResized)
# plt.show()

#
# Predict = '/home/ydf/Hehao/Post_process/test_0716/GF2_PMS1__20160327_L1A0001491484-MSS1_label.tif'
# Edge = '/media/ydf/disk1/data/rssrai2019_semantic_segmentation/test/edge_results_test/process1/GF2_PMS1__20160327_L1A0001491484-MSS1 (2).tif'
# imgP = cv2.imread(Predict,1)
# imgE = cv2.imread(Edge,0)
# imgQ = imgP[0:3500,0:3500]
# imgQResized = imgQ[1100:1900,1100:1900]
# imgEResized = imgE[1100:1900,1100:1900]
# # cv2.imshow('d', imgQResized)
# # cv2.waitKey()
# _, label = cv2.connectedComponents(imgEResized)
# # print(label)
# maxN = []
# flatLabel = label.flatten()
# counts = Counter(flatLabel)
# topN = counts.most_common(10)
# print(topN)
# for i in range(10):
#     index = np.argwhere(label == topN[i][0])
#     print(index)
#     maxN.append(index)
# print(maxN)
# first = [tuple(imgQResized[coord[0]][coord[1]]) for coord in maxN[0]]# collect the color infomation according to locations
# countColor = Counter(first)
# topColor = countColor.most_common(3)
# print(topColor)
# for coord in maxN[1]:
#     imgQResized[coord[0]][coord[1]] = topColor[1][0]
#
# cv2.imshow('m', imgQResized)
# cv2.waitKey()

'''
                                             check the lables
'''
# image = np.zeros((600, 600))
# image[200:300,200:300] = np.ones((100, 100))
# image[100:150,100:150] = np.ones((50, 50))
# # print(image.ndim)
# # plt.imshow(image)
# # plt.show()
# labelTest = measure.label(image, connectivity=2)
# flatLabel = labelTest.flatten()
# counts = Counter(flatLabel)
# topN = counts.most_common(4)
# maxN = []
# # for i in range(3):
# #     index = np.argwhere(labelTest == topN[i][0])
# #     maxN.append(index)
# # for region in measure.regionprops(label):
# #
# #     #take regions with large enough areas
# #     if region.area >= 1000:
# #         # # draw rectangle around segmented coins
# #         # minr, minc, _, maxr, maxc, _ = region.bbox
# #         print(region.bbox)
# #         # cv2.rectangle(imgEResized, (minr+2, minc+2), (maxr-2, maxc-2), (255, 0, 0), 2)
#
# print(topN)
# plt.imshow(image)
# plt.show()

# from skimage.draw import circle, set_color
# # img = np.zeros((10, 10), dtype=np.uint8)
# rr, cc = circle(415.9693368127071, 615.7684222712079, 7)
# imgEResized[rr, cc] = 1
# set_color(imgEResized, (rr, cc), (255,0,0))
# plt.imshow(imgEResized)
# plt.show()




'''
                                                tantanle
'''
import random
red = (0, 0, 255)
blue = (255, 0, 0)
Predict = 'GF2_PMS1__20160327_L1A0001491484-MSS1_label.tif'
Edge = 'GF2_PMS1__20160327_L1A0001491484-MSS1 (2).tif'
imgP = cv2.imread(Predict, 1)
imgE = cv2.imread(Edge, 1)
imgQ = imgP[0:3500,0:3500]
imgQResized = imgQ[1100:1900,1100:1900]
imgEResized = imgE[1100:1900,1100:1900]

# cv2.imshow('d', imgQResized)
# cv2.waitKey()
# a = np.array((150, 250, 0))
# b = np.array((120, 250, 0))
# c = (a == b).all()
# print(c)
count = 0
'''
blue np.array((250, 200, 0))
'''
# all blue coords
coordsQ = [(i, j) for i in range(imgQResized.shape[1]) for j in range(imgQResized.shape[0])\
          if ((imgQResized[i][j] == np.array((250, 200, 0)))).all()]
print(len(coordsQ))
# Return a k length list of unique elements chosen from the population sequence or set. Used for random sampling without replacement.
randBalls = random.sample(coordsQ, 10000) # set the number of coords

drawPoint = lambda img, ball, rad, red, thickness:cv2.circle(img, ball, rad, red, thickness)
[drawPoint(imgQResized, (randBall[1],randBall[0]), 3, red, 5) for randBall in randBalls] # random balls

coordsE = [randBall for randBall in randBalls \
           if imgEResized[randBall[0]][randBall[1]][0] == 0]# find corresponding points in edge img
[drawPoint(imgQResized, (coord[1],coord[0]), 1, blue, 2) for coord in coordsE]# random legal in edge img

#for coord in coordsE:   
#    track = []
#    x, y = coord[1], coord[0]
#    cv2.circle(imgEResized, (x, y), 3, red, 2)
    

startBall = [(coord[1], coord[0]) for coord in coordsE if imgEResized[coord[1]][coord[0]][0] == 0]      
#for coord in coordsE:         
for (y,x) in startBall:
    while True:
        if imgEResized[x][y][0] == 255:
            break    
        imgQResized[x][y] = (0, 250, 0)
        x -= 1 # direction
        y -= 1
ltCandidates = lambda i,j:[(i,j-1), (i+1,j-1), (i-1,j), (i-1,j+1), (i,j+1), (i+1,j)]


def direction(i,j):
#    if d is leftTop:
    newD = random.sample(ltCandidates(i,j), 1)
    print(newD)
            
#    cv2.circle(imgEResized, (x, y), 3, red, 2)
#    cv2.circle(imgEResized, (x+10, y+10), 2, (255,0,0), 2)
#    while imgEResized[x][y][0] != 255:
##        track.append((x, y))
#        x += 1 # direction
#        y += 1
#        if x == 800 or y == 800:
#            break
#        imgEResized[x][y] = (0, 250, 0)
#    print(track)
#    for trackPoint in track:
#        imgEResized[trackPoint[0]][trackPoint[1]] = (250, 0, 0)
        
        
#print(random.sample([-1,1],1))
#def nextPos(i, j):
#    '''
#    generate direction
#    '''
#    (i+random.sample([-1,1],1)[0],j+random.sample([-1,1],1)[0])
#    while directionLast() == newDirection or directionLast() == -newDirection :
#        get nextPos
#        
#        
#    return 
#def direction():
#    '''
#    record last direction
#    '''
#    if lastStep[1]-nextPos[1] == -1:
#        lastDirection = right
#    elif lastStep[1]-nextPos[1] == 1:
#        lastDirection = left
#    elif lastStep[0]-nextPos[0] == 1:
#        lastDirection = up
#    elif lastStep[0]-nextPos[0] == -1:
#        lastDirection = down
#    elif lastStep[0]-nextPos[0] == -1 and lastStep[1]-nextPos[1] == -1:
#        lastDirection = rd
#    elif lastStep[0]-nextPos[0] == -1 and lastStep[1]-nextPos[1] == -1:
#        lastDirection = lr
#    else:
#        pass
#    return lastDirection
#    
#movingTrace = []
#for (i,j) in coordsE:
#    if imgEResized[nextPos(i, j)[0]][nextPos(i, j)[1]][0] == 0:
        
        


cv2.circle(imgEResized, (100,100), 3, red, 2)
cv2.imshow('E', imgEResized)
cv2.imshow('Q', imgQResized)
cv2.waitKey()
