import random
import numpy as np
import cv2
import math
import os
from collections import Counter
ImgE = cv2.imread('test.jpg', 1)
ImgEcopy = ImgE[:]
##ImgEcopy[100:120,400:470] = (0,0,0)
print(ImgEcopy is ImgE)
##cv2.imshow('L', ImgEcopy)
##cv2.waitKey()
