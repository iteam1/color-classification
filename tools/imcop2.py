'''
Copy images from remote to local machine
Run this script in the same directory with sessions
Author: Loc Chuong
CMD: python3 imcop2.py
'''
import os
import shutil

src = "." # directory of source folder
dst = 'dst' # directory of destination folder

# create destination model
if not os.path.exists(dst):
   os.mkdir(dst)

# create sub floder
subs = ['top','profile','postion']
for sub in subs:
    path = os.path.join(dst,sub)
    if not os.path.exists(path):
        os.mkdir(path)

# list all files and folders
sessions = os.listdir(src)
print("Total (sessions): ",len(sessions))

# make floders in destiation
for session in sessions:
    if len(session)==14 and session.isalnum():
        try:
            print("Copying:",session)
            
            # image_detect_position
            name  = f"postion/image_detect_postion_{session}.jpg"
            source = os.path.join(session,"pictures/image_detect_postion.jpg")
            target = os.path.join(dst,name)
            shutil.copy(source, target)
            
            # image_detect_profile
            name  = f"profile/image_detect_profile_{session}.jpg"
            source = os.path.join(session,"pictures/image_detect_profile.jpg")
            target = os.path.join(dst,name)
            shutil.copy(source, target)
            
            # image_detect_profile_top
            name  = f"top/image_detect_profile_top_{session}.jpg"
            source = os.path.join(session,"pictures/image_detect_profile_top.jpg")
            target = os.path.join(dst,name)
            shutil.copy(source, target)
            
        except Exception as e:
            print(e)
            continue
