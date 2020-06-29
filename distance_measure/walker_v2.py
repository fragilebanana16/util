from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
D = []
pix_person_height = 0
focalLength = 880
KNOW_PERSON_HEIGHT = 170
x = 0
# cm
KNOWN_DISTANCE = 25*9
# cm
KNOWN_WIDTH = 18
#_, focalLength = rf.readFocal("F1_10A4.jpg", KNOWN_DISTANCE, KNOWN_WIDTH)
height = 160


cap = cv2.VideoCapture(0)
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
#　使用opencv默认的SVM分类器
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



while(1):
    # get a frame 480x640
    ret, frame = cap.read()
    
    #300x400
    frame = imutils.resize(frame, width=min(400, frame.shape[1]))
    centerX = frame.shape[0]/2
    centerY = frame.shape[1]/2
    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),
         padding=(8, 8), scale=1.05)
    
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    #　非极大抑制 消除多余的框 找到最佳人体
    marker = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for (xA, yA, xB, yB) in marker:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        pv = 0
        x = 0
        pointX = xA
        pointY = yB
        #p = ((xA-centerX)**2 + (xY-centerY)**2)**0.5
        pv = abs(centerY - yB)#vertical length 
        print("yB:")
        print(yB)
        if(pv != 0):
            x = focalLength * height /pv
        else:
            print("zero")
        print(x)
   
        
    cv2.putText(frame, "%.2fcm" % float(x),
                 (frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                 1.0, (0, 255, 0), 2)
    
   

 
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(D)
        break
cap.release()
cv2.destroyAllWindows()
 
