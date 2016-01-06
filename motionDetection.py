import numpy as np
import cv2
import imutils

def diffImg(t0,t1,t2):
	d1 = cv2.absdiff(t2,t1)
	d2 = cv2.absdiff(t1,t0)
	op = cv2.bitwise_and(d1,d2)
	
	#cv2.imshow('d1',d1)
	#cv2.imshow('d2',d2)
	#cv2.imshow('op',op)
	
	return op


cam = cv2.VideoCapture("openCV2.mp4")
ret,frame = cam.read()
print ret

frame1 = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)
frame2 = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)
frame3 = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)

while True:
	ret,frame = cam.read()

	if not ret:
		print "Error opening file"
		break

	mov = diffImg(frame1,frame2,frame3)
	thresh = cv2.threshold(mov,30,255,cv2.THRESH_BINARY)[1]
	thresh1 = cv2.dilate(thresh,None,iterations=4)
	(cnts,_) = cv2.findContours(thresh1.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts:
		if cv2.contourArea(c)<2000:
			continue
		(x,y,w,h)  = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.imshow('threshold',thresh)
	cv2.imshow('threshold1',thresh1)
	cv2.imshow('difference',mov)
	cv2.imshow('movement',frame)
	
	frame1 = frame2
	frame2 = frame3
	frame3 = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)
	
	if cv2.waitKey(0) & 0xFF == ord('q'):	# To move frame by frame
	#if cv2.waitKey(25) & 0xFF == ord('q'):
		print "Pressed Q, quitting!!"
		break
print "GoodBye"
cam.release()
cv2.destroyAllWindows()