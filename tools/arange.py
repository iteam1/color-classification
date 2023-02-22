import os
import shutil

# source folder
src = 'dst'

# destination folder
dst = 'imgs'
if not os.path.exists(dst):
    os.mkdir(dst)
# create sub floder
subs = ['top','profile','postion']
for sub in subs:
    path = os.path.join(dst,sub)
    if not os.path.exists(path):
        os.mkdir(path)

# list all folder in source
dates = os.listdir(src)
# loop over date
for date in dates:
    #list all sessions
    sessions = os.listdir(os.path.join(src,date))
    
    # purge out of format files or folders
    for session in sessions:
        path=os.path.join(src,date,session)
        if os.path.isdir(path):
            if len(session) != 14:
                print("Deleting Floder:",path)
                os.rmdir(path)
        elif os.path.isfile(path):
            print("Deleting File:",path)
            os.remove(path)
        else:
            print("Unknown:",path)

# loop over date again
count = 0 # value count
for date in dates:
    #list all sessions
    sessions = os.listdir(os.path.join(src,date))
    print("Executing:",os.path.join(src,date),"Session:",len(sessions))
    for i,session in enumerate(sessions):
        path = os.path.join(src,date,session)
        imgs = os.listdir(path)
        for j,img in enumerate(imgs):
            if img == "image_detect_profile.jpg":
                # copy image
                shutil.copy2(os.path.join(path,img),os.path.join(dst,"profile"))
                # rename
                name = "image_detect_profile_"+str(count)+".jpg"
                os.rename(os.path.join(dst,"profile","image_detect_profile.jpg"),os.path.join(dst,"profile",name))
            elif img == "image_detect_postion.jpg":
                # copy image
                shutil.copy2(os.path.join(path,img),os.path.join(dst,"postion"))
                # rename
                name = "image_detect_postion_"+str(count)+".jpg"
                os.rename(os.path.join(dst,"postion","image_detect_postion.jpg"),os.path.join(dst,"postion",name))
            elif img == "image_detect_profile_top.jpg":
                # copy image
                shutil.copy2(os.path.join(path,img),os.path.join(dst,"top"))
                # rename
                name = "image_detect_profile_top_"+str(count)+".jpg"
                os.rename(os.path.join(dst,"top","image_detect_profile_top.jpg"),os.path.join(dst,"top",name))
            else:
                pass
            # increase value count
        count +=1