import numpy as np
import cv2 as cv
import pyvjoy

showWebCam=False
debug=True
MAX_VJOY = 32767
frameWidth=540
frameHeight=400
lower_yellow = (15, 100, 100)
upper_yellow = (40, 255, 255)

kernel = np.ones((10,10),np.uint8)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

def thresholdEnable(value, old, thresholdValue):
    return abs(value - old) > thresholdValue


threshold = 2

xHistory = 0
yHistory = 0

lower_yellow = (15, 100, 100)
upper_yellow = (40, 255, 255)

kernel = np.ones((10,10),np.uint8)

vs = cv.VideoCapture(5)
j = pyvjoy.VJoyDevice(1)

while True:
    frame = vs.read()
    frame = frame[1]

    # Making image smoother
    median = cv.medianBlur(frame,5)

    # Filtering image by color
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_yellow, upper_yellow)

    morphed = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    #ret,thresh = cv.threshold(morphed,127,255,cv.THRESH_BINARY)
    contours,hierarchy = cv.findContours(morphed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        #usefull in case to look at what we are filtering
        #res = cv.bitwise_and(frame, frame, mask = morphed)

        (x,y),radius = cv.minEnclosingCircle(contours[0])
        # TODO verify if threshold can help us to became more precisely
        #if (thresholdEnable(x, xHistory, threshold) and thresholdEnable(y, yHistory, threshold)):
            #xHistory = x
            #yHistory = y
            #yHistory = y

        assex = x
        assey = y

        if (x > frameWidth):
            x = MAX_VJOY
        elif (x < 100):
            x = 0
        else:
            x = translate(x - 90, 0, frameWidth, 0, MAX_VJOY)
        
        if (y > frameHeight):
            y = MAX_VJOY
        elif (y < 80):
            y = 0
        else:
            y = translate(y, 0, frameHeight, 0, MAX_VJOY)
        j.data.wAxisX = MAX_VJOY - x
        j.data.wAxisY = MAX_VJOY - y
        j.update()

        if (debug):
            print(assex, assey, j.data.wAxisX, j.data.wAxisY)

    if (showWebCam):
        cv.imshow('frame', frame)
    key = cv.waitKey(20)

    if key == 27: # exit on ESC
        break
        break
