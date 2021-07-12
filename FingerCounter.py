import cv2
#import mediapipe as mp           ***Already imported in our module***
import HandtrackingModule as hp
import time
import numpy as np
import math
import os

wcam,hcam=800,800
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime=0

#For importing Images
folder="images"
myli=os.listdir(folder)
print(myli)
overlaylist=[]
for imPath in myli:
    image=cv2.imread(f'{folder}/{imPath}')
    overlaylist.append(image)

#print(len(overlaylist))

detector=hp.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]

while True:
    succ,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    print(lmlist)

    if len(lmlist)!=0:
        fingers=[]
        #Thumb
        if lmlist[tipIds[0]][1]>lmlist[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        #For 4 fingers
        for id in range(1,5):

            if lmlist[tipIds[id]][2]<lmlist[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            #print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)

        h,w,c=overlaylist[totalFingers].shape
        img[0:h,0:w]=overlaylist[totalFingers]    #using dimensions of the image
        
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,0,0),2)

    cv2.imshow("Image",img)

    if cv2.waitKey(1)==ord('q'):
        break