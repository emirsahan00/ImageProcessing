#gerekli paketleri(kütüphaneleri) ekleriz
from sqlite3 import Timestamp
from imutils.video import VideoStream
from detector.basicmotiondetector import BasicMotionDetector
from detector.panorama import Stitcher
#from __future__ import print_function

import numpy as np
import imutils
import time
import cv2
import datetime

leftStream = VideoStream(src=0).start()   #webcamdan görüntü almaya başlarız ,usb camera yani pcdeki kamera  (webcam)
rightStream = VideoStream(usePiCamera=True).start()             # Raspberry Pi kameradan da görüntü almaya başlarız  
time.sleep(1.0) #sistemi 1 saniyelik bir gecikme ile başlatırız

stitcher = Stitcher()                      # görüntü bu fonksiyon ile birleştirilir
motion = BasicMotionDetector(minArea= 500)  
total = 0

while True:  #sonsuz bir döngü başlatırız(frameleri okumak için)
    leftFrame = leftStream.read()  #webcamden ve  Raspberry Pi kameradan gelen görüntülerdeki frameleri okuruz
    rightFrame = rightStream.read()

    leftFrame = imutils.resize(leftFrame,width=400)            #framelerimizi boyutlandırdık
    rightFrame = imutils.resize(rightFrame,width=400)          #genişlik : 400 

    result = stitcher.stitch([leftFrame,rightFrame])  # 2 farklı görüntü burada tek bir değişkende olmak üzere birleştirilir
    # frameler her zaman soldan sağa yazılmalı 

    if result is None:  #sonuç none ise 
        print("homografi hesaplanamadı")
        break #döngüyü kır

    gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)  #birşleştirilmiş resimi bgr formatından gray formata çeviririz
    gray = cv2.GaussianBlur(gray,(21,21),0)  #blur uygularız
    locs = motion.upadate(gray)            # İşlenen panorama daha sonra hareket detektörüne geçirilir.
    
    if total > 32 and len(locs) > 0:
        (minX,minY) = (np.inf,np.inf)
        (maxX,maxY) = (-np.inf,-np.inf)

        for l in locs:
            (x,y,w,h) = cv2.boundingRect(l)
            (minX,minY) = (min(minX,x),max(maxX ,x + w))
            (minY, maxY) = (min(minY, y), max(maxY, y + h))

        cv2.rectangle(result,(minX,minY),(maxX,maxY),(0,0,255),3)

    total +=1
    timestamp = datetime.datetime.now()    #anlık zamanı döndürür         
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")       # o andaki zamanı string olarak ts değişkenine eşitledik.
    cv2.putText(result, ts, (10, result.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.imshow("Result", result)  #birleştirilmiş görünüyü imshowlarız
    cv2.imshow("Left Frame", leftFrame)  #webcamden gelen ve
    cv2.imshow("Right Frame", rightFrame) #Raspberry Pi kameradan gelen frameleri imshowlarız
    
    if cv2.waitKey(1) == ord('q'): #'q' tuşuna basılırsa döngüyü kır 
        break


cv2.destroyAllWindows() #tüm pencereleri kapt 
leftStream.stop() #webcamden görüntü almayı durdur
rightStream.stop() #Raspberry Pi kameradan görüntü almayı durdur







