'''*******************************************************************************************
***  Ryan Bride            
***  Code For Hackathon 1
*** Note: I utilized tracker bars to find a good values to filter out the pen cap using hsv
*** I found these values slightly widened and made the pen more clear, and solid the entire 
*** course of the video, the code I used to do this can be found in FindColors.py
***     Low     Hue = 0,        Saturation = 105,       Value = 35
***     High    Hue = 180,      Saturation = 255,       Value = 140
*******************************************************************************************'''
import sys, os, numpy, cv2

#LowHue, HighHue, LowSat, HighSat, LowValue, HighVal
red = {'lhue':0, 'hhue':180, 'lsat':105, 'hsat':255, 'lval':35, 'hval':140 }

#Create output window for what we need
cv2.namedWindow('output', cv2.WINDOW_NORMAL)
#Load Video
PenVideo = cv2.VideoCapture("Pen.Mov")
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

    #filter and pick out the pen cap
    if ret == True:
        #first blur image to reduce noise
        blurred = cv2.GaussianBlur(frame, (5,5), 0)
        #Create HSV version of the image
        frameHSV = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        #define ranges based of numbers found from my experiments
        lowerRange = numpy.array( [red['lhue'], red['lsat'], red['lval']])
        upperRange = numpy.array( [red['hhue'], red['hsat'], red['hval']])
        #Create the Filtered HSV image with white representing my target color
        mask = cv2.inRange(frameHSV, lowerRange, upperRange)
        #resized_mask = cv2.resize(mask, (1920, 1080))
        #visualize the real part of the target color
        res = cv2.bitwise_and(frame, frame, mask=mask)
        #convert the binary mask to a 3 channel image
        ascendedMask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        #Stack the mask and orignal image, and the filter
        #stacks = numpy.hstack( (ascendedMask, frame, res))
        #cv2.imshow("output", stacks)

        #Detect contours
        conts, hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #sort the contours based on their area, the pencap has the largest area
        sortedConts = sorted(conts, key=cv2.contourArea, reverse=True)
        #Define a new variable for just the largest contour instead of the whole list
        pencap_cont = sortedConts[0]
        #Draw only pen cap
        cv2.drawContours(frame, pencap_cont, -1, (0,255,0), 3)
        cv2.imshow('output', frame)

        #get center of the pencaps contour
        x,y,w,h = cv2.boundingRect(pencap_cont)
        pencap_center = (x,y)
        print(pencap_center)

        #Quit out of the window if the user hit q
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

#Unload the video and exit the window. i.e Cleanup code
PenVideo.release()
cv2.destroyAllWindows()