'''************************************************************
***  Ryan Bride            
***  Code For Hackathon 1
***  Open CV used for this assignment
***  
************************************************************'''
import sys, os
import numpy 
import cv2

"""
Note I utilized tracker bars to find a good values to filter out the pen cap using hsv
I found these values slightly widened and made the pen more clear, and solid the entire 
course of the video
Low     Hue = 0, Saturation = 105, Value = 35
High    Hue = 180, Saturation = 255, Value = 140
"""
#Pass functions 
def nothing(x):
    pass

#redUpper = (140, 0, 0)
#redLower = (110, 55, 55)
#For test sliders
red = (110, 140, 0, 55, 0, 55)

cv2.namedWindow('output', cv2.WINDOW_NORMAL)
cv2.namedWindow("TrackerBars", cv2.WINDOW_NORMAL)
PenVideo = cv2.VideoCapture("Pen.Mov")

#trackerbars to test the color of the image
cv2.createTrackbar("L - H", "TrackerBars", 0, 225, nothing)
cv2.createTrackbar("L - S", "TrackerBars", 0, 255, nothing)
cv2.createTrackbar("L - V", "TrackerBars", 0, 255, nothing)
cv2.createTrackbar("U - H", "TrackerBars", 179, 225, nothing)
cv2.createTrackbar("U - S", "TrackerBars", 255, 255, nothing)
cv2.createTrackbar("U - V", "TrackerBars", 255, 255, nothing)

#var to count frames to reset video if it ends
frameCounter = 0
while(PenVideo.isOpened()):
    ret, frame = PenVideo.read()
    #loop video
    frameCounter += 1
    #if the last frame is reached reset the video and the frame counter
    if frameCounter == PenVideo.get(cv2.CAP_PROP_FRAME_COUNT):
        frameCounter = 0
        PenVideo.set(cv2.CAP_PROP_POS_FRAMES, 0)

    if ret == True:
        #display video frame by frame
        #cv2.imshow("frame", frame)
        #image = cv2.resize(frame, (1920,1080))
        #cv2.imshow("output", image)
        # Get the new values of the trackbar in real time as the user changes them
        l_h = cv2.getTrackbarPos("L - H", "TrackerBars")
        l_s = cv2.getTrackbarPos("L - S", "TrackerBars")
        l_v = cv2.getTrackbarPos("L - V", "TrackerBars")
        u_h = cv2.getTrackbarPos("U - H", "TrackerBars")
        u_s = cv2.getTrackbarPos("U - S", "TrackerBars")
        u_v = cv2.getTrackbarPos("U - V", "TrackerBars")

        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lowerRange = numpy.array( [l_h, l_s, l_v])
        upperRange = numpy.array( [u_h, u_s, u_v])
        #Create the Filtered HSV image with white representing my target color
        mask = cv2.inRange(frameHSV, lowerRange, upperRange)
        #resized_mask = cv2.resize(mask, (1920, 1080))
        #visualize the real part of the target color
        res = cv2.bitwise_and(frame, frame, mask=mask)
        #convert the binary mask to a 3 channel image
        ascendedMask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        #Stack the mask and orignal image, and the filter
        stacks = numpy.hstack( (ascendedMask, frame))
        cv2.imshow("output", stacks)
        cv2.resizeWindow("TrackerBars", 720, 720)
        #show it at 40% size
        #cv2.imshow('TrackerBars',cv2.resize(stacks,None,fx=0.4,fy=0.4))
        
        #cv2.imshow("output", resized_mask)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

PenVideo.release()
cv2.destroyAllWindows()

