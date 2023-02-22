'''
Check different files between predict and ideal
CMD: tools/diff.py ideal.json output
'''
import os
import sys
import json

src = sys.argv[1] # ideal json file
dst = sys.argv[2] # prediction folder
content = "" # content 

if __name__ == "__main__":
    
    # read ideal file
    with open(src,'r') as f:
        ideal = json.load(f)
    
    # list all labels in prediction folder
    labels = os.listdir(dst)
    
    # check if label in ideal key
    for label in labels:
        # if label in ideal key
        if label in ideal.keys():
            path = os.path.join(dst,label)
            # list all images in label
            imgs = os.listdir(path)
            lines = ""
            count = 0
            for img in imgs:
                if img not in ideal[label]["img"]:
                    line = "\n\t"+img
                    lines += line
                    count +=1
            # write down to text file
            msg = f"\n{label}:{count}"
            content += msg
            content += lines
            print(msg)
            print(lines)
                
    # export text file
    with open('diff.txt','w') as f:
        f.writelines(content)
            