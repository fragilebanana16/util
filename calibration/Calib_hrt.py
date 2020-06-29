import numpy as np
import cv2
import glob
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
#for i in range(4,15):
i=11
#    for j in range(5,15):
j=7
#chess board 9*12
objp = np.zeros((i*j, 3), np.float32)
#points in 3D world(no width added)
objp[:,:2] = np.mgrid[0:i, 0:j].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob(r'myImgs2/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (i,j),None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (i,j), corners2,ret)
        print("i ,j:")
        print(i,j)
        
        cv2.imshow('img',img)
        cv2.waitKey(100)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
##                try:
##                    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
##                except:
##                    continue
##                continue

np.savez('dataMatrix.npz', r=ret, m=mtx, d=dist, rv=rvecs, t=tvecs)
with np.load('dataMatrix.npz') as X:
    mtx2, dist2, rvecs2, tvecs2 = [X[i] for i in ('m','d','rv','t')]
##npzfile = np.load('dataMatrix.npz')
##print(npzfile.files)

print(mtx2)
#cv2.destroyAllWindows()


##def draw(img, corners, imgpts):
##    corner = tuple(corners[0].ravel())
##    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
##    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
##    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
##    return img
##def draw2(img, corners, imgpts):
##    imgpts = np.int32(imgpts).reshape(-1,2)
##
##    # draw ground floor in green
##    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
##
##    # draw pillars in blue color
##    for i,j in zip(range(4),range(4,8)):
##        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
##
##    # draw top layer in red color
##    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
##
##    return img



##axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
##axis2 = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],
##                   [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])
##
##for fname in glob.glob(r'myImgs/*.jpg'):
##    img = cv2.imread(fname)
##    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##    ret, corners = cv2.findChessboardCorners(gray, (9,12),None)
##
##    if ret == True:
##        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
##        print("-----------------------------------------------------")
##        print(len(objp))
##        print("-----------------------------------------------------")
##        print(len(corners2))
##        print("-----------------------------------------------------")
##        print(mtx)
##        print("-----------------------------------------------------")
##        print(dist)
##        # Find the rotation and translation vectors.
##        a = np.reshape(corners2,(-1,2))
##        print("-----------------------------------------------------")
##        print(len(a))
##        
##       
##    
##        retval, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
##        
##
##        # project 3D points to image plane
##        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
##
##        img = draw(img,corners2,imgpts)
##        cv2.imshow('img',img)
##        
##        cv2.imwrite(fname[7:9]+'Cube.png',img)




























