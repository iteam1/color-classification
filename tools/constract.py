'''
White balance tool
CMD: python3 tools/constract.py imgs/profile/image_detect_profile_682.jpg
'''
import os
import sys
import cv2
import numpy as np

if len(sys.argv) == 2:
    path = sys.argv[1]
    
scale = 20

def boost_constract(img):
    # converting to LAB color space
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    result = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return result

def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1) # a = a - ((avg_a-128) * L/255 * 1.1
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1) # b = b - ((avg_b-128) * L/255 * 1.1
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

if __name__ == "__main__":
    path = "ooo/FC917109-B5C9-4C0A-85D7-89F2EF88462C_1_201_a copy.jpg"
    # read the image
    img = cv2.imread(path)
    
    # boost constract
    result = boost_constract(img)
    
    cv2.imwrite("result.jpg",result)
    
    # stack the image
    result = np.hstack((img,result))
    
    # resize
    result = cv2.resize(result,(0,0),fx=scale/100,fy=scale/100)
    
    # show result
    cv2.imshow("result",result)
    k = cv2.waitKey()
    # cv2.imwrite("result.jpg",result)
    cv2.destroyAllWindows()