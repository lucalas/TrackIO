import numpy as np
import cv2 as cv
import imutils
from imutils.video import VideoStream
import time
import pyautogui
#from pymouse import PyMouse



vs = cv.VideoCapture(2)

time.sleep(2.0)

debounce = 5
debounceCount=0

#m = PyMouse()
while True:
    frame = vs.read()
    frame = frame[1]

    #frame = imutils.resize(frame, width=600)

    # Making image smoother
    median = cv.medianBlur(frame,5)

    # Filtering image by color
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_yellow = np.array([15, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    mask = cv.inRange(hsv, lower_yellow, upper_yellow)

    kernel = np.ones((10,10),np.uint8)
    morphed = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    ret,thresh = cv.threshold(morphed,127,255,cv.THRESH_BINARY)
    contours,hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        cnt = contours[0]

        #usefull in case to look at what we are filtering
        #res = cv.bitwise_and(frame, frame, mask = morphed)

        (x,y),radius = cv.minEnclosingCircle(cnt)
        #m.move(x,y)
        if (debounceCount % debounce == 0):
            pyautogui.moveTo(x,y, 0.1)
            debounceCount = 0

        center = (int(x),int(y))
        radius = int(radius)
        img = cv.circle(morphed,center,radius,(255, 255, 0),2)
        #cv.imshow('frame', img)
        #print(x,y)
        #time.sleep(0.001)
        debounceCount = debounceCount + 1
    #else:
        #cv.imshow('frame', morphed)
    
    if cv.waitKey(10) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break