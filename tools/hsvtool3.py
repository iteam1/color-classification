'''
HSV parser
Support function stack all images in folder and display
CMD: python3 tools/hsvtool3.py crop/red
*Note*
    - The images must be the same size and h = w
    - The output image also the square image
'''
import os
import sys
import cv2
import random
import numpy as np

def empty(i):
    pass

def on_trackbar(val):
    global output,hsv,res
    # get H,S,V value from trackbar
    hue_min = cv2.getTrackbarPos("Hue Min", "TrackedBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackedBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackedBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackedBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackedBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackedBars")
    scale   = cv2.getTrackbarPos("Scale", "TrackedBars")
    # get current mask of HSV range
    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(output,output,mask=mask)
    # reshape the image
    h,w,c = res.shape
    h = int(h*scale/100)
    w = int(w*scale/100)
    resized = cv2.resize(res,(0,0),fx=scale/100,fy=scale/100)
    # display result
    cv2.imshow("output",resized)


# init
src = sys.argv[1] # source images
D  = 990 # dimension of output image

# read all images
imgs = os.listdir(src)
print("total image:",(len(imgs)))

# create ouput image
output = np.zeros((D,D,3),np.uint8)

# check one image
path = os.path.join(src,imgs[0])
img = cv2.imread(path)
d = img.shape[0]
# find number of image each row follow the rescaled dimension
d2 = D
print('output dimension=',D)
n = int(D/d2)
# loop until the capability of row * column > total images
while n*n < len(imgs):
    d2 -=1 # reduce rescaled image
    n = int(D/d2)
# re calculate image dimension
d2 = int(D/n)
r = n*n-len(imgs) # the redundant image
print("rol=colum=",n)
print("d2=",d2)
print("redundant number:",r)
# create blank image
blank = np.zeros((d2,d2,3))

outputs = [] # list of output images

# loop over the images
for i in imgs:
    path = os.path.join(src,i)
    img = cv2.imread(path)
    # resize image
    img = cv2.resize(img,(d2,d2),interpolation=cv2.INTER_AREA)
    outputs.append(img)
    
# append blank images
for i in range(r):
    outputs.append(blank)

j =0 # first row
for i in range(len(outputs)):
    k = i%n
    # calculate top left point
    x1 = d2 * k
    y1 = d2 * j
    # calculate right bottom point
    x2 = x1+d2
    y2 = y1+d2
    #print(i,(j,k),(x1,y1),(x2,y2))
    #cv2.imshow(str(i),outputs[i])
    # paste the current to output image
    output[y1:y2,x1:x2]=outputs[i]
    #cv2.imshow(str(i),output[y1:y2,x1:x2])
    # if go to the last image of row, increase row number
    if k == n-1: j+=1
        
  
# convert to hsv space
hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)

# create window
cv2.namedWindow("TrackedBars")
cv2.resizeWindow("TrackedBars", 640, 240)

# create trackbars
cv2.createTrackbar("Hue Min", "TrackedBars", 0, 179, on_trackbar)
cv2.createTrackbar("Hue Max", "TrackedBars", 179, 179, on_trackbar)
cv2.createTrackbar("Sat Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Sat Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("Val Min", "TrackedBars", 0, 255, on_trackbar)
cv2.createTrackbar("Val Max", "TrackedBars", 255, 255, on_trackbar)
cv2.createTrackbar("Scale", "TrackedBars",70, 100, on_trackbar)

# show some stuff
on_trackbar(0)

# wait until user press any key
k = cv2.waitKey()
if k:
    cv2.imwrite("output.jpg",res)