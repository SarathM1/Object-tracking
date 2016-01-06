import numpy as np
import cv2
import imutils

def diffImg(t0,t1,t2):
	d1 = cv2.absdiff(t2,t1)
	d2 = cv2.absdiff(t1,t0)
	return cv2.bitwise_and(d1,d2)

cam = cv2.VideoCapture("openCV2.mp4")
ret,frame = cam.read()
print ret

t_minus = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)

while True:
	ret,frame = cam.read()

	if not ret:
		print "Error opening file"
		break

	mov = diffImg(t_minus,t,t_plus)
	thresh = cv2.threshold(mov,30,255,cv2.THRESH_BINARY)[1]
	thresh1 = cv2.dilate(thresh,None,iterations=4)
	(cnts,_) = cv2.findContours(thresh1.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts:
		if cv2.contourArea(c)<2000:
			continue
		(x,y,w,h)  = cv2.boundingRect(c)
		#cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.imshow('movement',frame)
	cv2.imshow('threshold',thresh)
	cv2.imshow('threshold1',thresh1)
	cv2.imshow('difference',mov)

	t_minus = t
	t = t_plus
	t_plus = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)
	key = cv2.waitKey(10)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
print "GoodBye"
cam.release()
cv2.destroyAllWindows()