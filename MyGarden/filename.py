#simple listing 
#from subprocess import call
#call(["ls", "-l", "/home/pi/webcam/"])

import glob
import os
dataset_path = '/home/pi/webcam/'
files = glob.glob(dataset_path+'*')   
files.sort(key=os.path.getmtime) #order files
print(files[len(files)-1]) #get last (most recent) file
