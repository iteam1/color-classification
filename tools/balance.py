'''
White balance tool
CMD: python3 tools/balance.py imgs/profile/image_detect_profile_682.jpg
'''
import os
import sys
import cv2
import numpy as np

path = sys.argv[1]
scale = 20

def white_balance_loops(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    for x in range(result.shape[0]):
        for y in range(result.shape[1]):
            l, a, b = result[x, y, :]
            # fix for CV correction
            l *= 100 / 255.0
            result[x, y, 1] = a - ((avg_a - 128) * (l / 100.0) * 1.1)
            result[x, y, 2] = b - ((avg_b - 128) * (l / 100.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
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
    # read the image
    img = cv2.imread(path)
    
    # white balance
    result = white_balance(img)
    
    # stack the image
    result = cv2.hconcat([img,result])
    
    # resize
    result = cv2.resize(result,(0,0),fx=scale/100,fy=scale/100)
    
    # show result
    cv2.imshow("result",result)
    k = cv2.waitKey()
    cv2.imwrite("result.jpg",result)
    cv2.destroyAllWindows()