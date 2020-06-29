#import the necessary packages
import numpy as np
import cv2

def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
##    cv2.imshow("image", edged)
##    cv2.imwrite('edged.jpg', edged)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key = cv2.contourArea)
    #minAreaRect函数返回矩形的中心点坐标，长宽，旋转角度[-90,0)，当矩形水平或竖直时均返回-90
    # compute the bounding box of the of the paper region and return it
    return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth



def readFocal(firstImg, d, w):
    
    image = cv2.imread(firstImg)
    marker = find_marker(image)
    focalLength = (marker[1][0] * d) / w
    return marker[1][0],focalLength
if __name__=='__main__':
    # cm
    KNOWN_DISTANCE = 25*10
    # cm
    KNOWN_WIDTH = 18

    # 第一个放标定图
    IMAGE_PATHS = ["F1_10A4.jpg","F2_9A4.jpg","F3_8A4.jpg"]
    _, focalLength = readFocal(IMAGE_PATHS[0], KNOWN_DISTANCE, KNOWN_WIDTH)
    print("object width(cm):")
    print(_)
    print("focallength(pixel):")
    print(focalLength)
    #计算其他图像中物体与摄像头距离
    for imagePath in IMAGE_PATHS:
        image = cv2.imread(imagePath)
        marker = find_marker(image)
        inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        print("distance(cm):")
        print(inches)
        # draw a bounding box around the image and display it
        box = cv2.boxPoints(marker)
        box = np.int0(box)
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, "%.2fcm" % float(inches),
                (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)
        #cv2.namedWindow("enhanced",0);
        cv2.resizeWindow("enhanced", 640, 480);
        
        cv2.imshow("image", image)
        cv2.imwrite('distance.jpg', image)
        cv2.waitKey(0)
