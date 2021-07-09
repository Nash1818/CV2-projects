import cv2
import mediapipe as mp
import time

from mediapipe.python.solutions import hands

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        
        
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self,img,draw=True):

        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:                         
            for handLms in self.results.multi_hand_landmarks:       #HandLms is for single hand information
                #for id,lm in enumerate(handLms.landmark):     #getting the index no and id no for relating to exact index number of our fingers
                #print(id,lm)
                   # h,w,c=img.shape
                  #  cx,cy=int(lm.x*w),int(lm.y*h)
                  #  print("Given id=",id,cx,cy)

                   # if id ==0:  #For detecting certain points on the hand if required ids are pre assigned by mediapipe to different parts of hand
                   #     cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)   #The "mpHands.HAND_CONNECTIONS" function is used for drawing connectionns between the red dots
        return img
    
    #Now we create a module for extracting hand information i.e a list of co-ordinates,which hand etc.

    def findPosition(self,img,handNo=0,draw=True):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]

            for id,lm in enumerate(myHand.landmark):     #getting the index no and id no for relating to exact index number of our fingers
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                 #print("Given id=",id,cx,cy)
                lmlist.append([id,cx,cy])

               # if id ==0:  #For detecting certain points on the hand if required ids are pre assigned by mediapipe to different parts of hand
                if draw:
                   cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
        return lmlist

def main():
    ptime=0
    cTime=0
    cap=cv2.VideoCapture(0)
    detector=handDetector()

    while True:
         succ,img=cap.read()
         img=detector.findHands(img)
         lmlist=detector.findPosition(img)
         if len(lmlist)!=0:
             print(lmlist[4])
         cTime=time.time()
         fps=1/(cTime-ptime)          #For FPS
         ptime=cTime

         cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)  #Displaying Fps  
         cv2.imshow("Image",img)
         if cv2.waitKey(1)==ord('q'):
            break
    

if __name__=="__main__":
    main()
        