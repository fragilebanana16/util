from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import readFocal as rf

D = []
pix_person_height = 0
focalLength = 880
KNOW_PERSON_HEIGHT = 170

# cm
KNOWN_DISTANCE = 25*9
# cm
KNOWN_WIDTH = 18
#_, focalLength = rf.readFocal("F1_10A4.jpg", KNOWN_DISTANCE, KNOWN_WIDTH)

cap = cv2.VideoCapture(0)
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
#　使用opencv默认的SVM分类器
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



while(1):
    # get a frame
    ret, frame = cap.read()
    
    frame = imutils.resize(frame, width=min(400, frame.shape[1]))


    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),
         padding=(8, 8), scale=1.05)
    
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    #　非极大抑制 消除多余的框 找到最佳人体
    marker = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for (xA, yA, xB, yB) in marker:
    	cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    	ya_max = yA
    	yb_max = yB
    	pix_person_height = yb_max - ya_max
    #初始为0，防止除零异常
    if(pix_person_height == 0 ):
        #pix_person_height = 1
        distance = 0
    else:
    #print (pix_person_height)

        distance = (KNOW_PERSON_HEIGHT * focalLength) / pix_person_height
        print(distance)
        D.append(distance)
        pix_person_height = 0
    cv2.putText(frame, "%.2fcm" % float(distance),
                 (frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                 1.0, (0, 255, 0), 2)
    
   

 
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(D)
        break
cap.release()
cv2.destroyAllWindows()
 