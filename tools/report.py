'''
Report to json file the summary of output
CMD: python3 tools/report.py output
'''
import os
import sys
import json

scr = sys.argv[1]

my_dict = {} # summary

if __name__ == "__main__":
    
    print("Summary:",scr)
    labels = os.listdir(scr)
    print("Total labels:",len(labels),"\n",labels)
    
    for label in labels:
        path = os.path.join(scr,label)
        imgs = os.listdir(path)
        d = {"no":len(imgs),"img":imgs}
        my_dict[label] = d
        
    with open('output.json','w') as f:
        json.dump(my_dict,f)