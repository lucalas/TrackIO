import numpy as np
import cv2 as cv
from pynput.mouse import Controller

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

vs = cv.VideoCapture(2)
mouse = Controller()

while True:
    frame = vs.read()
    frame = frame[1]

    # Making image smoother
    median = cv.medianBlur(frame,5)

    # Filtering image by color
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_yellow, upper_yellow)

    morphed = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    ret,thresh = cv.threshold(morphed,127,255,cv.THRESH_BINARY)
    contours,hierarchy = cv.findContours(morphed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        #usefull in case to look at what we are filtering
        res = cv.bitwise_and(frame, frame, mask = morphed)

        (x,y),radius = cv.minEnclosingCircle(contours[0])

        x = translate(x, 0, 600, 0, 2120)
        y = translate(y, 0, 600, 0, 1280)
        mouse.position = (x,y)
        cv.imshow('frame', res)