import cv2 as cv
import numpy as np

#Access video capture devices
videoCapture = cv.VideoCapture(2)



#Capture frame
while True:
    #ret, saves a boolean value of whether the frame was captured or not
    #frame, is where the frame info of the camera will be storaged
    ret, frame = videoCapture.read() 
    if not ret:
        break
    blur_img = cv.medianBlur(frame, 5)
    gray_img = cv.cvtColor(blur_img, cv.COLOR_BGR2GRAY)
    #Shows image or video in a window ("window name", variable where the frame is stored)
    cv.imshow("frame", gray_img)

    #If we click 'q' the loop breaks
    if cv.waitKey(1) & 0xFF == ord('q'): break

#Releases the video capture and kills all open windows
videoCapture.realease()
cv.destroyAllWindows()