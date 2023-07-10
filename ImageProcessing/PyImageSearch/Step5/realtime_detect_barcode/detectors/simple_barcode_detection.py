#gerekli paketleri(kütüphaneleri) ekleriz
import numpy as np 
import cv2
import imutils

def detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #orijinal görüntümüzü gri tona çeviriyoruz

    ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F   #görüntünün gradyan büyüklük temsilini oluşturmak için Scharr operatörünü kullanırız.
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

    gradient = cv2.subtract(gradX, gradY)    # Scharr operatörünün y gradyanını scharr operatörünün x gradyanından çıkarırız
    gradient = cv2.convertScaleAbs(gradient)

    blurred = cv2.blur(gradient, (9, 9))    # görüntüyü yumuşatıyoruz
    ret,thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY) # bulanık görüntünün eşik değerini artırıyoruz ve 2 boyuta çeviriyoruz

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7)) # bu fonksiyon barkodun dikey şeritleri arasındaki boşlukları kapatmamızı sağlar.
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) # kernelimizi eşiklenmiş görüntümüze uygulayarak morfolojik işlemimizi gerçekleştiriyoruz

    closed = cv2.erode(closed, None, iterations=4) #görüntüdeki beyaz pikselleri ve küçük lekeleri ortadan kaldırmak için erode ve dilate fonksiyonu uygularız
    closed = cv2.dilate(closed, None, iterations=4) # bu işlemi dikey çizgiler arasındaki çizgiler kapansın diye yaparız.

    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #birçok işlemden geçmiş closed değişkenimizdeki konturları buluruz
    cnts = imutils.grab_contours(cnts)

    if len(cnts) == 0:    #eğerki contur yoksa fonsiyona frame değerini none döndürür ve döngü devam eder
        return None
    
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0] #cnts değişkenindeki konturları sıralarız ve en büyüğünü c değişkenine atarız
    rect = cv2.minAreaRect(c) #en büyük kontur için minimum sınırlayıcı kutuyu belirliyoruz ve bir dikdörtgen döndürülür.
    box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect) #döndürülmüş dikdörtgenin köşe noktalarını döndürür.
    box = np.int0(box)    # ondalıklı koordinatları tam sayıysa döndürür.
 
    return box #box değikenini return eder
