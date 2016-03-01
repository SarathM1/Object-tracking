import numpy as np
import cv2
from threading import Thread, Event
from Queue import Queue
import time
from datetime import datetime as dt


class motionDetect(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.cap = cv2.VideoCapture(0)
		# Daemon threads won't prevent process from exiting
		self.fgbg = cv2.BackgroundSubtractorMOG()


	def run(self):
		print "Starting motionDetect"
		while stopEvent.isSet():
			ret, frame = self.cap.read()
			#frame = cv2.medianBlur(frame,11)
			fgmask = self.fgbg.apply(frame)
			dilate = cv2.dilate(fgmask,None,iterations=4)

			(cnts,_) = cv2.findContours(dilate.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			for c in cnts:
				if cv2.contourArea(c)>500:
					(x,y,w,h)  = cv2.boundingRect(c)
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
					queue.put(frame)
					#cv2.drawContours(frame, [c], 0, (0,255,0), 1)
			
			#cv2.imshow('BG Subtctn',fgmask)
			#cv2.imshow('Dilation',dilate)
			cv2.imshow('Input',frame)
			cv2.waitKey(20)
			#if cv2.waitKey(20) & 0xFF == ord('q'):
			#	break
		self.cap.release()
		cv2.destroyAllWindows()
		print "Ending motionDetect"

class frameShow(Thread):
	
	def __init__(self):
		Thread.__init__(self)
	
	def run(self):
		print "Starting frameShow"
		
		while stopEvent.isSet():
			if not queue.empty():
				size = queue.qsize()
				if size > 4:
					print "Warning: Que size = ", size, " !!"
				img = queue.get()

				timeStamp = dt.strftime(dt.now(),'%d:%m:%y:%H:%M:%S')
				cv2.imwrite('Img'+str(timeStamp)+'.jpg',img)
		print "Ending frameShow"

if __name__ == '__main__':
	queue = Queue(maxsize=100)
	stopEvent = Event()
	stopEvent.set()

	threadPool = []
	
	thread1 = motionDetect()
	thread2 = frameShow()
	threadPool.append(thread1)
	threadPool.append(thread2)

	thread1.start()
	thread2.start()

	try:
		while True:
			pass
	except KeyboardInterrupt, e:
		stopEvent.clear()
		print "Cleaning Queue"
		while not queue.empty():
			queue.get()
		print "Done"
		#time.sleep(3)
		for each_thread in threadPool:
			each_thread.join()
		print e
