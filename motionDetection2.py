import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#fgbg = cv2.BackgroundSubtractorMOG2(500,100,False)
fgbg = cv2.BackgroundSubtractorMOG()

while(1):
	ret, frame = cap.read()

	fgmask = fgbg.apply(frame)
	dilate = cv2.dilate(fgmask,None,iterations=4)
	(cnts,_) = cv2.findContours(dilate.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts:
		if cv2.contourArea(c)>1000:
			(x,y,w,h)  = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			#cv2.drawContours(frame, [c], 0, (0,255,0), 1)
	
	cv2.imshow('BG Subtctn',fgmask)
	cv2.imshow('Dilation',dilate)
	cv2.imshow('Input',frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
