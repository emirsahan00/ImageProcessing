# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2
import imutils                                  
import argparse
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i", "--image", required=True,     # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.       
	help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])  # giriş görüntüsünü terminalden belirttiğimiz yolu baz alarak diskten alıyoruz

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #orijinal resmimizi gri tona çeviriyoruz
#edged = cv2.Canny(gray,30,150)
thresh = cv2.threshold(gray,225,255,cv2.THRESH_BINARY_INV)[1]  #gri tona çevirdiğimiz resmin eşik değerini artırıyoruz ve 2 boyuta çeviriyoruz
#mask = thresh.copy()
#mask = cv2.erode(mask, None, iterations=5)


cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #thresh değişkenindeki görüntünün conturlarını buluyoruz
cnts = imutils.grab_contours(cnts)
output = image.copy()           #orijinal resmimizi kopyalayıp output değişkenine atıyoruz

#mask = thresh.copy()                                       'arka planı siyah yapmak istersem'
#output = cv2.bitwise_and(image, image, mask=mask)

for c in cnts:                        #konturlar üzerinde geziniyoruz
    cv2.drawContours(output,[c],-1,(240,0,159),3)           #tespit edilmiş her conturu çiziyoruz
    
text = 'I found {} total shapes '.format(len(cnts))        #toplam kontur sayısını len(cnts) ile alıyoruz
cv2.putText(output,text,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,155,255),2)        #orijinalinden kopyaladığımız resmin üstüne yazıyoruz

#cv2.imshow("MASK", mask)
cv2.imshow("Contours", output)            #ve çıktımızı görüntülüyoruz
cv2.waitKey(0)