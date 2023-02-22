'''
crop image tool
CMD: python3 tools/imcrop.py output
'''

import os
import sys
import cv2
from tqdm import tqdm

DIM = 400
PADDING = 20
X = 1664
Y = 228 + PADDING
src = sys.argv[1]
dst = "crop"

# create destination model
if not os.path.exists(dst):
    print("creating destination folder")
    os.mkdir(dst)

# list all of labels
labels = os.listdir(src)
print("Total: ",len(labels)," ",labels)

# create labels in destination folder
for label in tqdm(labels):
    path = os.path.join(dst,label)
    if not os.path.exists(path):
        os.mkdir(path)
    
    # list images and crop
    path = os.path.join(src,label)
    imgs = os.listdir(path)
    for img in imgs:
        path = os.path.join(src,label,img)
        im = cv2.imread(path)
        roi = im[Y:Y+DIM,X:X+DIM]
        path = os.path.join(dst,label,img)
        cv2.imwrite(path,roi) # save cropped image to the destination folder