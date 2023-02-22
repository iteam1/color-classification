'''
Report to json file the summary of output
CMD: python3 tools/summary.py ideal.json output.json
'''
import sys
import json

ideal = sys.argv[1]
pred = sys.argv[2]

if __name__ == "__main__":
    
    print("Summary Report")
    print("-"*5)
    
    with open(ideal,"r") as f:
        ideal = json.load(f)
        
    with open(pred,"r") as f:
        pred = json.load(f)

    ideal_keys = list(ideal.keys())
    print("Ideal: ",ideal_keys)
    
    pred_keys = list(pred.keys())
    print("Output: ",pred_keys)
    
    print("Labels:")
    
    for key in [i for i in pred_keys if i != 'limbo']:
        pred_imgs = pred[key]["img"]
        ideal_imgs = ideal[key]["img"]
        count = 0
        for im in pred_imgs:
            if im in ideal_imgs:
                count += 1        
        print("\t",key,":",count,"/",len(ideal_imgs))