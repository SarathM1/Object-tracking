import numpy as np
import cv2
import imutils


cap = cv2.VideoCapture('/home/wa/Desktop/openCV/openCV2.mp4')
firstFrame = None

while(1):
	ret, frame = cap.read()

	try:
		if ret:
			frame = imutils.resize(frame,width = 500)
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray,(21,21),0)
			if firstFrame is None:
				firstFrame = gray
				continue
			# compute the absolute difference between the current frame and
			# first frame
			frameDelta = cv2.absdiff(firstFrame, gray)
			thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
 
			# dilate the thresholded image to fill in holes, then find contours
			# on thresholded image
			thresh = cv2.dilate(thresh, None, iterations=2)
			(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			for c in cnts:
				if cv2.contourArea(c) < 1000:
					continue
				# compute the bounding box for the contour, draw it on the frame,
				# and update the text
				(x, y, w, h) = cv2.boundingRect(c)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

			# show the frame and record if the user presses a key
			cv2.imshow("Security Feed", frame)
			cv2.imshow("Thresh", thresh)
			cv2.imshow("Frame Delta", frameDelta)
			key = cv2.waitKey(1) & 0xFF
		 
			# if the `q` key is pressed, break from the lop
			if key == ord("q"):
				break
		else:
			break
		
	except Exception, e:
		print "\n\nError!!!\n\n"
		raise e
	
	k = cv2.waitKey(30)
	if k == 27:
		break


cap.release()
cv2.destroyAllWindows()
