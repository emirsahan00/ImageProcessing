#gerekli paketleri(kütüphaneleri) ekleriz
from imutils.video import VideoStream
from keyclipwriter import KeyClipWriter
import argparse
import datetime
import imutils                        
import time
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-o", "--output", required=True, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
	help="path to output directory") 
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="mp4v",    # 'mp4v' uzantı
	help="codec of output video")
ap.add_argument("-b", "--buffer-size", type=int, default=32,
	help="buffer size of video clip writer")
args = vars(ap.parse_args())


vs = VideoStream(0).start()  #webcam den görüntüyü almaya başlıyoruz
time.sleep(2.0) #sistemi 2 saniye bekletiyoruz

blueLower = (101,50,38)  #alt ve üst mavi değerlerini giriyoruz
blueUpper = (110,255,255)

kcw = KeyClipWriter(bufSize=args["buffer_size"])
consecFrames = 0

while True: #sonsuz bir döngü başlatıyoruz
	
	frame = vs.read() #frameleri okuyoruz
	frame = imutils.resize(frame,width=600) #imutils ile framelerin genişliği 600 olacak şekilde ayarlıyoruz
	updateConsecFrames = True 
	
	blurred = cv2.GaussianBlur(frame, (11, 11), 0) #frameleri blurlıyoruz
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) #blurlanmış görüntüyü bgr formatından hsv formatına dönüştürüyoruz
	
	mask = cv2.inRange(hsv, blueLower, blueUpper)  #mask uyguluyoruz
	mask = cv2.erode(mask, None, iterations=2) #bir takım morfolojik işlemlerden geçiriyoruz
	mask = cv2.dilate(mask, None, iterations=2)
	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #mask'imizin üstündeki konturları buluyoruz
	cnts = imutils.grab_contours(cnts)
	print("lenn :  ",len(cnts))
    
	if len(cnts) > 0: #kontur bulmuşmu diye kontrol ediyoruz
		
		c = max(cnts, key=cv2.contourArea)  #bulduğumuz konturlardan alanı en büyük olanı c değişkenine atıyoruz
		((x, y), radius) = cv2.minEnclosingCircle(c) #bulduğumuz kontur üzerindeki minimum çemberin merkez noktalarının koordinatlarını ve yarıçapı değerini döndürür.
		updateConsecFrames = radius <= 10 #eğer ki radius değeri 10 küçük ve eşitse 'updateConsecFrames' değişkenine eşitleriz
		
		if radius > 10: #eğer yarıçap 10'dan büyükse
			
			consecFrames = 0
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2) # o koordinatlara bir çember çizeriz
			if not kcw.recording: #eğer kayıt yapılmıyorsa 
				timestamp = datetime.datetime.now()  #anlık zamanı verir
				p = "output/{}.mp4".format(args["output"], #kaydedeceğimiz yolu belirliyoruz
					timestamp.strftime("%Y%m%d-%H%M%S"))
				kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]),args["fps"]) #videoyu kaydetmeye başlıyoruz p dosyanın yolu, karekter kodu ve kare hızını parametre olarak alırız(defaukt)

			if updateConsecFrames: 
				consecFrames += 1  #ardışık karelerin sayısını bir artırırız
			kcw.update(frame) 
	
			if kcw.recording and consecFrames == args["buffer_size"]:
				kcw.finish() 
			 
			cv2.imshow("Frame", frame)  #framalerimizi gösteririz
			if cv2.waitKey(1) == ord('q'): #eğer ki 'q' tuşuna basılırsa döngüyü kır
				break

if kcw.recording: #eğer hala kayıt yapılıyorsa kaydı durdururuz
	kcw.finish()
cv2.destroyAllWindows() #tüm pencereleri kapatıp 
vs.stop() #web camden alınan görüntüyü durdururuz


    

    

    



