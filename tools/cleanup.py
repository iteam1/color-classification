'''
Copy images from remote to local machine
Run this script in the same directory with sessions
Author: Loc Chuong
'''
import os
import shutil
src = "."
dst = 'dst' # name of destination folder

# list all files and folders
sessions = os.listdir(src)
print("Total (sessions): ",len(sessions))

# make floders in destiation
for session in sessions:
    if len(session)==14:
        imgs = os.listdir(os.path.join(session,"pictures"))
        for img in imgs:
            if "image_detect_postion" in img and img != "image_detect_postion.jpg":
                os.remove(os.path.join(session,"pictures",img))
                print("Clean up",os.path.join(session,"pictures",img))
                
            elif "image_detect_profile" in img and (
                    (img != "image_detect_profile.jpg") or 
                    (img != "image_detect_profile_top.jpg") or 
                    (img != "image_detect_profile_bottom.jpg") or 
                    (img != "image_detect_profile_bottom.jpg")):
                os.remove(os.path.join(session,"pictures",img))
                print("Clean up",os.path.join(session,"pictures",img))
            else:
                continue
                