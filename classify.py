'''
Color classifier by HSV
CMD: python3 classify.py imgs/profile/img.jpg
CMD: python3 classify.py imgs/profile
'''
import os
import sys
import cv2
import numpy as np
from tqdm import tqdm

dst = "output" # name of folder contain classified images
src = "imgs"
THRESH = 0.1
class Classifier(object):
    
    def __init__(self):
        # Low and High HSV thresholds Black color
        self.BLACK_D = (40,255) 
        self.BLACK_L = np.array([0,0,0])
        self.BLACK_H = np.array([179,255,116])
        self.BLACK = (self.BLACK_L,self.BLACK_H)
        # Low and High HSV thresholds White color
        self.WHITE_D = (46,255) 
        self.WHITE_L = np.array([22,0,154])
        self.WHITE_H = np.array([116,79,255])
        self.WHITE = (self.WHITE_L,self.WHITE_H)
        # Low and High HSV thresholds Red color
        self.RED_D = (90,130) 
        self.RED_L = np.array([0,137,0])
        self.RED_H = np.array([179,255,206])
        self.RED = (self.RED_L,self.RED_H)
        # Low and High HSV thresholds Brown color 
        self.BROWN_D = (110,150)
        self.BROWN_L = np.array([2,40,0])
        self.BROWN_H = np.array([21,109,255])
        self.BROWN = (self.BROWN_L,self.BROWN_H)
        # list of color HSV low-high tuple and list of corresponding labels
        self.HSV = [self.BLACK,self.WHITE,self.RED,self.BROWN]
        self.colors = ['black','white','red','brown']
        self.distances = {'black':self.BLACK_D,
                          'white':self.WHITE_D,
                          'red':self.RED_D,
                          'brown':self.BROWN_D}
        # ROI params
        self.DIM = 400
        self.x = 1664
        self.y = 228
        # load reference image
        self.img0 = cv2.imread("zero.png")
    
    def predict(self,img):
        '''
        Predict color of input image
        Args:
            img (string,array): path of input image or numpy array (BGR)
        Return:
            pred (string): predicted color by Classifier
            threshold (float): maximum color area
        '''
        # init
        pred = None
        # check type of param img
        typ = str(type(img))
        if typ == "<class 'str'>":
            img = cv2.imread(img)
        elif typ == "<class 'numpy.ndarray'>":
            pass
        else:
            print(f'{type(img)} is not supported!')
            return pred
        # convert input to hsv color space
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        totals = []
        for color in self.HSV:
            # get HSV mask
            low = color[0]
            high = color[1]
            mask = cv2.inRange(img_hsv,low,high)
            roi = mask[self.y:self.y+self.DIM,self.x:self.x+self.DIM]
            total = np.sum(roi)/255.0
            totals.append(total)
        # find best color by max total
        idx = np.argmax(totals)
        pred = self.colors[idx]
        threshold = totals[idx]
        return pred,threshold/(self.DIM**2)
    
    def crop(self,img):
        '''
        Crop image
        '''
        return img[self.y:self.y+self.DIM,self.x:self.x+self.DIM]
    
    def cal_dE(self,img,img2):
        '''
        Calculate Delta E distance between 2 images
        Args:
            img: source image
            img2: image
        Return:
            dE: delta E
        '''
        # convert to Lab space image1
        lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
        L1,A1,B1 = cv2.split(lab)
        L1 = L1.mean()
        A1 = A1.mean()
        B1 = B1.mean()
        
        # convert to Lab space image2
        lab2 = cv2.cvtColor(img2,cv2.COLOR_BGR2LAB)
        L2,A2,B2 = cv2.split(lab2)
        L2 = L2.mean()
        A2 = A2.mean()
        B2 = B2.mean()
        
        # calculate differents
        dL = L1 - L2
        dA = A1 - A2
        dB = B1 - B2
        dE = np.sqrt(dL**2 + dA**2 + dB**2)
        return dE
        
if __name__ == "__main__":
    
    # creater instance of color classifier
    classifier = Classifier()
    
    # create output folder
    if not os.path.exists(dst):
        os.mkdir(dst)
        
    # create labels
    for color in classifier.colors:
        path = os.path.join(dst,color)
        if not os.path.exists(path):
            os.mkdir(path)
            
    # if the argument is image file 
    if ".jpg" in sys.argv[1] or ".png" in sys.argv[1]:
        # read the input image
        img = cv2.imread(sys.argv[1])
        img_org = img.copy()
        #predict
        pred,thresh = classifier.predict(img)
        img = classifier.crop(img)
        dE = classifier.cal_dE(classifier.img0,img)
        a = classifier.distances[pred][0] < dE and dE <  classifier.distances[pred][1]
        b = thresh > THRESH
        # put text
        cv2.putText(img_org,sys.argv[1],(100,100),cv2.FONT_HERSHEY_SIMPLEX,3,(4,255,0),6, cv2.LINE_AA,False)
        cv2.putText(img_org,pred,(100,200),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),6, cv2.LINE_AA,False)
        cv2.putText(img_org,str(thresh),(100,300),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),6, cv2.LINE_AA,False)
        cv2.putText(img_org,str(dE)+" "+str(a),(100,400),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),6, cv2.LINE_AA,False)
        cv2.imshow(pred,img_org)
        # wait until user press any key
        k = cv2.waitKey()
        if k:
            cv2.imwrite("out.jpg",img_org)
            
    # else the argument is path lead to image folder
    else:
        imgs = os.listdir(sys.argv[1])
        print("Total: ",len(imgs),"(images)")
        for im in tqdm(imgs):
            org = os.path.join(sys.argv[1],im)
            img = cv2.imread(org)
            img_org = img.copy()
            pred,thresh = classifier.predict(img)
            img = classifier.crop(img)
            dE = classifier.cal_dE(classifier.img0,img)
            a = classifier.distances[pred][0] < dE and dE < classifier.distances[pred][1]
            b = thresh > THRESH
            if a == True and b == True:
                path = os.path.join(dst,pred)
                path += "/" + im
            else:
                # classify an other image
                im2 = "image_detect_profile_top_"+im.split("_")[-1]
                im2 = os.path.join("imgs/top",im2)
                img = cv2.imread(im2)
                pred2,thresh = classifier.predict(img)
                if pred2 == pred:
                    path = os.path.join(dst,"white")
                    path += "/" + im
                else:
                    path = os.path.join(dst,pred)
                    path += "/" + im
                
            cv2.putText(img_org,path,(100,100),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),6, cv2.LINE_AA,False)
            cv2.putText(img_org,pred,(100,200),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),6, cv2.LINE_AA,False)
            cv2.putText(img_org,str(thresh),(100,300),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),6, cv2.LINE_AA,False)
            cv2.putText(img_org,str(dE)+" "+str(a),(100,400),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),6, cv2.LINE_AA,False)
            cv2.imwrite(path,img_org)