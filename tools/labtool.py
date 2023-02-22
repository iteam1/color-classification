'''
LAB parser
Support function horizontal stack same size image
CMD: python3 tools/labtool.py imgs/profile/image_detect_profile_682.jpg
'''
import numpy as np
import cv2
import sys

def empty(i):
    pass

def on_trackbar(val):
    global img,lab,res
    # get ,S,V value from trackbar
    L_min = cv2.getTrackbarPos("L Min", "TrackedBars")
    L_max = cv2.getTrackbarPos("L Max", "TrackedBars")
    A_min = cv2.getTrackbarPos("A Min", "TrackedBars")
    A_max = cv2.getTrackbarPos("A Max", "TrackedBars")
    B_min = cv2.getTrackbarPos("B Min", "TrackedBars")
    B_max = cv2.getTrackbarPos("B Max", "TrackedBars")
    scale   = cv2.getTrackbarPos("Scale", "TrackedBars")
    # get current mask of HSV range
    lower = np.array([L_min, A_min, B_min])
    upper = np.array([L_max, A_max, B_max])
    mask = cv2.inRange(lab, lower, upper)
    res = cv2.bitwise_and(img,img,mask=mask)
    # reshape the image
    h,w,c = res.shape
    h = int(h*scale/100)
    w = int(w*scale/100)
    resized = cv2.resize(res,(0,0),fx=scale/100,fy=scale/100)
    # display result
    cv2.imshow("LAB",resized)

# read input the images
img_paths = sys.argv[1:] # the argument after program's name
print(f"Reading {len(img_paths)} images")
imgs = [] # list of input image
for img_path in img_paths:
    img = cv2.imread(img_path)
    imgs.append(img)
    
# stack the images
img = cv2.hconcat(imgs)
    
# convert to hsv space
lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)

# create window
cv2.namedWindow("TrackedBars")
cv2.resizeWindow("TrackedBars", 640, 240)
# create trackbars
cv2.createTrackbar("L Min", "TrackedBars", 0,255, on_trackbar)
cv2.createTrackbar("L Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("A Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("A Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("B Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("B Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("Scale", "TrackedBars",10, 100, on_trackbar)

# show some stuff
on_trackbar(0)

# wait until user press any key
k = cv2.waitKey()
if k:
    cv2.imwrite("hsv.jpg",res)