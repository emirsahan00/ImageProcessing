#gerekli paketleri(kütüphaneleri) ekleriz
from imutils.video import VideoStream
import datetime
import argparse                 
import imutils
import time                                                                 
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-p", "--picamera", type=int, default=-1, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
vs = VideoStream(0).start() #görüntü almaya başlıyoruz
# vs = VideoStream(usePiCamera=args["picamera"]>0).start()
time.sleep(1.0)        # programın çalışmasını içine girilen saniye kadar duraklatır 

while True: #sonsuz bir döngü başlatırız
    frame = vs.read() #frameleri okuruz
    frame= cv2.flip(frame,1) #görüntüyü y eksenine göre döndeririz
    frame = imutils.resize(frame,width=500) #frameleri genişliği 500 olmak üzere boyutlandırıyoruz

    timestamp = datetime.datetime.now() #anlık zamanı döndürür
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p") #string bir değere dönüşür

    cv2.putText(frame,ts,(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.60,(0,0,0),1) #framelerin üstüne anlık zamanı yazdırırız

    cv2.imshow("frame",frame)  #frameleri imshowlarız
    if cv2.waitKey(1) == ord('q'): # eğer ki 'q' tuşuna basılırsa döngüyü kır 
        break
cv2.destroyAllWindows()  #tüm pencereleri kapat
vs.stop() #görüntü almayı durdur