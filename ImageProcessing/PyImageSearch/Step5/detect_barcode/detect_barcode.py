#gerekli paketleri(kütüphaneleri) ekleriz
import cv2
import numpy as np
import argparse
import imutils
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i", "--image", required = True, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
	help = "path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])  #giriş görüntümüzü terminalden verdiğimiz yoldan alıyoruz
image = imutils.resize(image,width=500) #imutils kütüphanesi ile giriş görüntümüzün genişliği 500 olacak şekilde boyutlandırıyoruz
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #orijinal görüntümüzü gri tona çeviriyoruz

ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F  #görüntünün gradyan büyüklük temsilini oluşturmak için Scharr operatörünü kullanırız.
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)  
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

gradient = cv2.subtract(gradX, gradY) #Scharr operatörünün y gradyanını scharr operatörünün x gradyanından çıkarırız
gradient = cv2.convertScaleAbs(gradient)

blurred = cv2.blur(gradient, (9, 9))        # görüntüyü yumuşatıyoruz
ret,thresh = cv2.threshold(blurred,225,255,cv2.THRESH_BINARY) # bulanık görüntünün eşik değerini artırıyoruz ve 2 boyuta çeviriyoruz

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))      # bu fonksiyon barkodun dikey şeritleri arasındaki boşlukları kapatmamızı sağlar.
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)      # kernelimizi eşiklenmiş görüntümüze uygulayarak morfolojik işlemimizi gerçekleştiriyoruz


closed = cv2.erode(closed, None, iterations = 4)   #görüntüdeki beyaz pikselleri ve küçük lekeleri ortadan kaldırmak için erode ve dilate fonksiyonu uygularız
closed = cv2.dilate(closed, None, iterations = 4)  # bu işlemi dikey çizgiler arasındaki çizgiler kapansın diye yaparız.

cnts = cv2.findContours(closed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #birçok işlemden geçmiş closed değişkenimizdeki konturları buluruz
cnts = imutils.grab_contours(cnts)
c = sorted(cnts,key=cv2.contourArea,reverse=True)[0]   #cnts değişkenindeki konturları sıralarız ve en büyüğünü c değişkenine atarız

rect = cv2.minAreaRect(c) #en büyük kontur için minimum sınırlayıcı kutuyu belirliyoruz ve bir dikdörtgen döndürülür.
box = cv2.boxPoints(rect) if imutils.is_cv2 else cv2.boxPoints(rect)   #döndürülmüş dikdörtgenin köşe noktalarını döndürür.
box = np.int0(box)         # ondalıklı koordinatları tam sayıysa döndürür.
 
cv2.drawContours(image,[box],-1,(0,255,0),3) #belirlenen konturlar image üzerine çizilir.

cv2.imshow("image",image)  #çıktımızı görüntüleriz  
#cv2.imshow("th",thresh)  
#cv2.imshow("th2",closed)
#cv2.imshow("blured",blurred)
#cv2.imshow("gradient",gradient)
cv2.waitKey(0)

