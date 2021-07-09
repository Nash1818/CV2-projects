import cv2
#import mediapipe as mp           ***Already imported in our module***
import HandtrackingModule as hp
import time
import numpy as np
import math
from ctypes import cast,POINTER

#Use the command prompt to install the pycaw library first
# ***pip install pycaw***

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume


wcam,hcam=640,480

cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime=0

detector=hp.handDetector()
devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))

# volume.GetMute()                  *** NOT NEEDED HERE***
# volume.GetMasterVolumeLevel()     *** NOT NEEDED HERE***

volr=volume.GetVolumeRange()        #volr is volume range
minVol=volr[0]
maxVol=volr[1]
volBar=400
vol=0
volPer=0

while True:
    succ,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)  #length between the finger and thumb
        print(length)

        #Hand range 50-270+
        #Volume Range is -65 to 0

        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBar=np.interp(length,[50,300],[400,150])
        volPer=np.interp(length,[50,300],[0,100]) 
        
        #Play around with [50,300] to best optimize volume control for your hand.
        
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol,None)

        if length<=50:
           cv2.circle(img,(cx,cy),15,(255,255,0),cv2.FILLED)
        
        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),3,cv2.FILLED)
        cv2.putText(img,f'{int(volPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,255),2)
        
    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f'FPS:{int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,0,0),2)
    cv2.imshow("Image",img)
    if cv2.waitKey(1)==ord('q'):
        break