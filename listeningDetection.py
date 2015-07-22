import cv2
import numpy as np
import urllib2

cap = cv2.VideoCapture(0)
listening = False
host = "enter host name here"

# The Amazon Echo Blue range
lower_blue = np.array([110,200,200], dtype=np.uint8)
upper_blue = np.array([130,255,255], dtype=np.uint8)


while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Get all of the points that passed the filter
    pixelPoints = np.transpose(np.nonzero(mask))

    # print "There are %d white points" % len(pixelPoints)
    if (len(pixelPoints) > 10) and not listening:
        # Send volume=20 to media center
        print "Setting volume to 20"
        listening = True
        urllib2.urlopen(host+"?volume=20")
    elif (len(pixelPoints)==0) and listening:
        print "Setting volume back to 100"
        listening = False
        urllib2.urlopen(host+"?volume=200")

    # cv2.imshow('frame',frame)
    # cv2.imshow('mask',mask)
    # cv2.imshow('res',res)

    # If the user presses esc, exit.
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
