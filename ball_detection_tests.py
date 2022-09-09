import cv2 as cv
import numpy as np


def calc_dist(x1,y1,x2,y2):
    dist = pow((x1 - y1), 2) + pow((y1-y2), 2)
    return dist


#Access video capture devices
videoCapture = cv.imread("./tennis_ball.jpg")
prevCircle = None



#Capture frame
while True:
    #ret, saves a boolean value of whether the frame was captured or not
    #frame, is where the frame info of the camera will be storaged
    frame = videoCapture
    

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

    #1st parameter is the source image.
    #2nd parameter is the Hough Circle method which is oftern the Hough Gradient.
    #3rd parameter is the dp, larger values will make two circles that are very close to merge.
    #4th parameter is the mean  distance, which is the minimum distance between two possible circles
    #that are found. If only one circle will be detected it is recommend it to set it high.
    #5th parameter is the sensitivity of circle detection. High values will detect less circles,
    #low values will detect more circles.
    #6th parameter is the accuracy of circle detection, sets the number of edge point needed to
    #identify circles. High values identify less circles, low values identify more circles.
    #7th parameter is the min radius, which is the minimum size of a circle to be detected.
    #8th parameter is the max radius, which is the maximum size of a circle to be detected.
    #The HoughCircles method returns a list of the circles that it found with the provided parameters.
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.2, 100, param1=100,
                              param2=30, minRadius=75,maxRadius=400)
    
    if circles is not None:
        #Convert circle list into a numpy array.
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0,:]:
            if chosen is None:
                chosen = i
            if prevCircle is not None:
                if calc_dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= calc_dist(i[0], i[1],prevCircle[0], prevCircle[1]):
                    chosen = i
            cv.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)
            cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255), 3)
            prevCircle = chosen
        
    #Shows image or video in a window ("window name", variable where the frame is stored)
    cv.imshow("circles", frame)

    #If we click 'q' the loop breaks
    if cv.waitKey(1) & 0xFF == ord('q'): 
        break

#Releases the video capture and kills all open windows
videoCapture.realease()
cv.destroyAllWindows()