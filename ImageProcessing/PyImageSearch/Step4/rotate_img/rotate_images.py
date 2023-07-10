# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2 
import argparse                                        
import imutils
import numpy as np
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i","--image",required=True,   # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
    help="path to the image file")
args=  vars(ap.parse_args())

image = cv2.imread(args["image"])   # giriş görüntüsünü diskten alıyoruz

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)    #orijinal resmimizi gri tona çeviriyoruz
gray = cv2.GaussianBlur(gray,(5,5),0) # #orijinal resmimizi blurlıyoruz
edged = cv2.Canny(gray,20,100) #gri tona dönüşmüş resmin kenarlarını belirginleştiriyoruz

cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #resmin konturlarını buluyoruz
cnts = imutils.grab_contours(cnts)

if len(cnts) > 0:  #eğer ki kontur varsa 
    c =max(cnts,key=cv2.contourArea)  #bulunan konturlardan alanı en büyük olanı c değişkenine ata
    mask = np.zeros(gray.shape,dtype="uint8")  #gray değişkenindeki görüntünün boyutlarında bir mask oluşturuyoruz
    cv2.drawContours(mask,[c],-1,255,2) #maskın üstüne bulduğumuz konturu çiziyoruz
    (x,y,w,h) = cv2.boundingRect(c)  #bu konturun x ve y koordinatlarını ayrıyetende yükseklik ve genişlik değerlerini buluyoruz
    ImageROI = image[y:y+h,x:x+w] #resmi ilgilendiğimiz alanını kırpıp ImageROI değişkenine atıyoruz
    maskROI = mask[y:y + h, x:x + w]
    ImageROI = cv2.bitwise_and(ImageROI,ImageROI,mask=maskROI)  

    for angle in np.arange(25, 360, 15):   #(ilk derece,son derece,15'er derece döndürüyoruz)
        rotated = imutils.rotate(ImageROI, angle)  #döndürümesini sağlayan fonksiyon
        cv2.imshow("Rotated (Problematic)", rotated) #dönderilmiş halini gösteriyoruz
        cv2.waitKey(0)
