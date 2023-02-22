'''
Analyze the effects of channels to color's density in the specific color space  
CMD: python3 tools/analyze.py crop/red
'''
import os
import sys
import cv2

src = sys.argv[1]

imgs = os.listdir(src)

if __name__ == "__main__":
    
    print(len(imgs))




