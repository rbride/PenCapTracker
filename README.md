# PenCapTracker
Simple Pen Tracking OpenCV application
This application uses no real fancy Opencv features, instead just using and HSV to isolate a pens cap from the background of a video
after isolating the pencap based on its color, it selects the cap based on contour size, then plots a marker at the center of the centroid. It also displays the pixel
location of this marker at all times in the top left hand corner of the video
Furthermore, the application also graphs the x and y value of the pixel location of the marker vs time using pyplot 
this plot is attached to the video in the same windows.
A picture of the final output can be shown.

In addition to the final code for the project. code files are included to show how the values used to filter the color were founds, as well as the code used to initially track
the contour of the pen cap.

- Ryan Bride
