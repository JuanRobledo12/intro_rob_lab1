#!/usr/bin/env python

#Intro. to Robotics Research Lab 1, Part 2.
#Team: Thanapol Tantagunninat, Juan Antonio Robledo Lara.

#This program captures video with an external webcam,
#then it changes the color channles to gray scale and
#applies a gaussian blur with a 7x7 kernel.
#The program is able to detect circles within the captured frame
#by using the Hough Circles Transform. The HoughCircles method's parameters
#where tunned with an orange dodgeball.

#Last modification Sep, 9, 2022

import cv2 as cv
import numpy as np


def calc_dist(x1,y1,x2,y2):
    dist = pow((x1 - x2), 2) + pow((y1 - y2), 2)
    return dist


#Access video capture devices
my_camera = cv.VideoCapture(2)
prev_circle = None



#Capture frame with selected device
while True:
    ret, main_frame = my_camera.read() 
    if not ret:
        break

    #Frame pre-processing
    gray_frame = cv.cvtColor(main_frame, cv.COLOR_BGR2GRAY)
    blur_frame = cv.GaussianBlur(gray_frame, (7,7), 1.5)

    #Circle detection parameters
    circle_ls = cv.HoughCircles(blur_frame, cv.HOUGH_GRADIENT, 1.5, 100, param1=200,
                              param2=50, minRadius=100,maxRadius=400)
    #Circle detection
    if circle_ls is not None:
        circle_ls = np.uint16(np.around(circle_ls))
        main_circle = None
        #Detected circle position update
        for i in circle_ls[0,:]:
            if main_circle is None:
                main_circle = i
            if prev_circle is not None:
                if calc_dist(main_circle[0], main_circle[1], prev_circle[0], prev_circle[1]) <= calc_dist(i[0], i[1],prev_circle[0], prev_circle[1]):
                    main_circle = i
            cv.circle(main_frame, (main_circle[0], main_circle[1]), 1, (0,100,100), 3)
            cv.circle(main_frame, (main_circle[0], main_circle[1]), main_circle[2], (255,0,255), 3)
            txt_mark = "x: " + str(main_circle[0]) + " y: " + str(main_circle[1]) 
            cv.putText(main_frame, txt_mark, org=(main_circle[0], main_circle[1]),fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1 ,color=(102, 255, 51), thickness=2, lineType=cv.LINE_AA)
            prev_circle = main_circle
        

    cv.imshow("circle_ls", main_frame)
    if cv.waitKey(1) & 0xFF == ord('q'): 
        break
    
cv.destroyAllWindows()
