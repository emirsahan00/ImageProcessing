
from collections import deque
from threading import Thread
from queue import Queue
import time
import cv2
class KeyClipWriter:
	def __init__(self, bufSize=64, timeout=1.0):
		
		self.bufSize = bufSize
		self.timeout = timeout
		
		self.frames = deque(maxlen=bufSize)
		self.Q = None
		self.writer = None
		self.thread = None
		self.recording = False
	def update(self, frame):
		
		self.frames.appendleft(frame)
		
		if self.recording:
			self.Q.put(frame)
			
	def start(self, outputPath, fourcc, fps):
		self.recording = True
		self.writer = cv2.VideoWriter(outputPath, fourcc, fps,
			(640,640), True)
		self.Q = Queue()
		
		for i in range(len(self.frames), 0, -1):
			self.Q.put(self.frames[i - 1])
		
		self.thread = Thread(target=self.write, args=())
		self.thread.daemon = True
		self.thread.start()
	def write(self):
		
		while True:
			
			if not self.recording:
				return
			if not self.Q.empty():
				
				
				frame = self.Q.get()
				self.writer.write(frame)
			
			else:
				time.sleep(self.timeout)
	def flush(self):
		
		while not self.Q.empty():
			frame = self.Q.get()
			self.writer.write(frame)
	def finish(self):
		
		self.recording = False
		self.thread.join()
		self.flush()
		self.writer.release()
		

    


	
	
	

	
	