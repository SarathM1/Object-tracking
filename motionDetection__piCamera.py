from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time
import numpy as np
import cv2		#importing opencv
from datetime import datetime as dt

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (300, 300)
camera.framerate = 64
rawCapture = PiRGBArray(camera, size=(300, 300))
time.sleep(0.1)

frameCnt = 0
def diffImg(t0,t1,t2):
	d1 = cv2.absdiff(t2,t1)
	d2 = cv2.absdiff(t1,t0)
	op = cv2.bitwise_and(d1,d2)
	
	return op


flag = 1
for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	frame = frame.array
	frame3 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	#frame = imutils.resize(frame, width = 500)
	if flag:
		frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		frame2 = frame1
		frame3 = frame1
		flag = 0
	mov = diffImg(frame1,frame2,frame3)
	thresh = cv2.threshold(mov,30,255,cv2.THRESH_BINARY)[1]
	thresh1 = cv2.dilate(thresh,None,iterations=4)
	(cnts,_) = cv2.findContours(thresh1.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts:
		if cv2.contourArea(c)<1000:
			continue
		#print "Detected!!",frameCnt
		frameCnt+=1
		
		if(frameCnt%10 == 0):
					timeStamp = dt.strftime(dt.now(),'%d:%m:%y:%H:%M:%S')
					print str(timeStamp)
					print cv2.imwrite('./Detected/'+str(timeStamp)+'.jpg',frame)
		(x,y,w,h)  = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.imshow('threshold',thresh)
	cv2.imshow('threshold1',thresh1)
	cv2.imshow('difference',mov)
	cv2.imshow('movement',frame)
	
	frame1 = frame2
	frame2 = frame3
	#frame3 = cv2.cvtColor(cam.read()[1],cv2.COLOR_BGR2GRAY)
	
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if cv2.waitKey(20) & 0xFF == ord('q'):	# To move frame by frame
	#if cv2.waitKey(25) & 0xFF == ord('q'):
		print "Pressed Q, quitting!!"
		break
print "GoodBye"
cv2.destroyAllWindows()
