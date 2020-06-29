import numpy as np,sys
import cv2
from matplotlib import pyplot as plt
from time import sleep
import imutils
cap = cv2.VideoCapture(0)#0 1 represent camera in laptop
while(True):
    if(cap.isOpened()):
        #width and height
        #print(cap.get(3),cap.get(4))
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=min(400, frame.shape[1]))
        
        #adjust window size
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(r"write.png", frame)
            break
        #cv2.waitKey(0)
##    else:
##        cap.open()
