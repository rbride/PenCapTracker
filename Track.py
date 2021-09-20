'''*******************************************************************************************
***  Ryan Bride            
***
***  Note: I utilized tracker bars to find a good values to filter out the pen cap using hsv
***  I found these values slightly widened and made the pen more clear, and solid the entire 
***  course of the video, the code I used to do this can be found in FindColors.py
***      Low     Hue = 0,        Saturation = 105,       Value = 35
***      High    Hue = 180,      Saturation = 255,       Value = 140
***  Furthmore the Folder this code is contained in contains a file called tracking.py
***  this file shows the initial pen tracking code I Created to track the contour of the
***  Pen cap itself. 
***  This code was written on September 20th, 2021
*******************************************************************************************'''
import sys, os
import numpy
import cv2
from matplotlib import pyplot

#LowHue, HighHue, LowSat, HighSat, LowValue, HighVal
red = {'lhue':0, 'hhue':180, 'lsat':105, 'hsat':255, 'lval':35, 'hval':140 }
#Create output window for what we need
cv2.namedWindow('output', cv2.WINDOW_NORMAL)
#cv2.namedWindow('MaskOutput', cv2.WINDOW_NORMAL)
#cv2.namedWindow('X and Y vs Time', cv2.WINDOW_NORMAL)
#Load Video
PenVideo = cv2.VideoCapture("Pen.Mov")
#var to count frames to reset video if it ends
frameCounter = 0

fig = pyplot.figure()
#List of centerpoint to store and plot later
center_point_x_list = []
center_point_y_list = []

while(PenVideo.isOpened()):
    ret, frame = PenVideo.read()
    #loop video
    #frameCounter += 1
    #if the last frame is reached reset the video and the frame counter
    #if frameCounter == PenVideo.get(cv2.CAP_PROP_FRAME_COUNT):
    #    frameCounter = 0
    #    PenVideo.set(cv2.CAP_PROP_POS_FRAMES, 0)
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
        #Stack the mask and orignal image, and the filter old 
        stacks = numpy.hstack( (ascendedMask, frame, res))
        #cv2.imshow("MaskOutput", stacks)

        #Detect contours
        conts, hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #sort the contours based on their area, the pencap has the largest area
        sortedConts = sorted(conts, key=cv2.contourArea, reverse=True)
        #Define a new variable for just the largest contour instead of the whole list
        pencap_cont = sortedConts[0]
    
        #Get the center of the contour at any given moment
        moment = cv2.moments(pencap_cont)
        cx = int(moment["m10"] / moment["m00"])
        cy = int(moment["m01"] / moment["m00"])

        #append the centerpoint to a list
        center_point_x_list.append(cx)
        center_point_y_list.append(cy)

        #draw marker at center of pencap
        cv2.drawMarker(frame, (cx,cy), color=(0,255,0), 
            markerType=cv2.MARKER_CROSS, thickness=5 )
        
        #draw pixel cordinates of marker
        pixelstring = "X: " + str(cx) + "  Y: " + str(cy)
        print(pixelstring)
        #Label for the Pixel location
        cv2.putText(frame, "Pen Cap Center", (50,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
        cv2.putText(frame, pixelstring, (50,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)

        #Draw only the pencap contour
        cv2.drawContours(frame, pencap_cont, -1, (0,255,0), 4)
        #Render the final image
        #cv2.imshow('output', frame)

        #update data
        line1 = pyplot.plot(numpy.array(center_point_x_list))
        line1 = pyplot.plot(numpy.array(center_point_y_list))

        #redraw the canvas to update the matlab plot
        fig.canvas.draw()
        #convert matlab canvas to opencv image
        plotimage = numpy.fromstring(fig.canvas.tostring_rgb(), dtype=numpy.uint8, sep='')
        plotimage  = plotimage.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plotimage = cv2.cvtColor(plotimage, cv2.COLOR_RGB2BGR)
        #cv2.imshow('X and Y vs Time', plotimage)
        
        #make the plot image the same dimensions as the video so that they can be combined into one window
        ndim = (frame.shape[1], frame.shape[0])
        resized_plot = cv2.resize(plotimage, ndim, interpolation = cv2.INTER_AREA)
        
        #Combine the matlab plot and the pencap video into one window
        vertical = numpy.concatenate((frame, resized_plot), axis=1)
        cv2.imshow("output", vertical)

        #Quit out of the window if the user hit q
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

#Unload the video and exit the window. i.e Cleanup code
#PenVideo.release()
#cv2.destroyAllWindows()