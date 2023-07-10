from __future__ import print_function        #prejemiz için gerekli kütüphaneler
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()                     # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-o", "--output", required=True, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
	help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="XVID",
	help="codec of output video")
args = vars(ap.parse_args())


vs = VideoStream(0).start()   #görüntüyü webcamden almak için VideoStream fonksiyonunu kullanıyoruz
time.sleep(2.0)             #2.0 saniye geç çıktı vermesini istiyoruz
fourcc = cv2.VideoWriter_fourcc(*args["codec"])   #videoyu kaydetmek için gerekli değişkenleri fourcc değişkenine atıyoruz

cap = None  
(h,w) = (None,None)  #height ve width in none olarak tanımlarız
zeros = None

while True:                
    frame = vs.read()                            #frameleri okuyoruz
    frame = cv2.flip(frame,1)                  #frameleri y eksenine göre döndürüyoruz ki gerçek bir görüntü alalım
    frame = imutils.resize(frame,width=300)       #frameleri width=300 olacak şekilde boyutlandırıyoruz

    if cap is None:     # cap değeri None ise:
        (h,w) = frame.shape[:2]                #framelerin height ve width değerlerine ihtiyacımız olduğu için 0 ve 1. döndürülen değeri alıyoruz(3. değer boyut verir)
        cap = cv2.VideoWriter(args["output"],fourcc,args["fps"],(w*2,h*2),True)      #kaydedilmesi gereken frameleri cap değişkenine eşitliyoruz
        
        
    zeros = np.zeros((h,w),dtype="uint8")        # shape ile aldığımız height ve width değerler ile zeros isimli bir tuval oluşturuyoruz.
    (B, G, R) = cv2.split(frame)              # split fonksiyonu renkli bir görüntüyü veya frame'i mavi yeşil ve kırmızı kanallarına ayırarak bu kanalları ayrı değişkenlere atar
    R = cv2.merge([zeros, zeros, R])            # B ve G kanallarını sıfırlayarak (siyah renk) R değişkenindeki değerle birleştirir.
    G = cv2.merge([zeros, G, zeros])            # B ve R kanallarını sıfırlayarak (siyah renk) G değişkenindeki değerle birleştirir.
    B = cv2.merge([B, zeros, zeros])

    output = np.zeros((h * 2, w * 2, 3), dtype="uint8")   # orijinal resimdeki h ve w değerlerinin iki katı olacak boyutlarda 3 boyutlu(rgb) bir tuval oluşturduk.
    output[0:h, 0:w] = frame              #frameleri tek pencere göstermek için parçalara bölüyoruz
    output[0:h, w:w * 2] = R
    output[h:h * 2, w:w * 2] = G
    output[h:h * 2, 0:w] = B

    cap.write(output)        # outputtan gelen frameleri write metodu ile VideoWriter'daki yolunu belirleyeceğimiz dosyamıza kaydederiz.
        

    cv2.imshow("r", R)             #frame çıktılarını gösteriyoruz
    cv2.imshow("Frame", frame)
    cv2.imshow("Output", output)
    if cv2.waitKey(1) == ord("q"):    # klavyeden 'q' tuşuna basılınca while break yani frame okumasını durduruyoruz ve pencereleri kapatıp frameleri serbest bırakıyoruz.     
        break

cv2.destroyAllWindows() #tüm pencereler kapatırız
vs.stop() #görüntü almayı durdururuz
cap.release() #frameleri serbest bırakırız

