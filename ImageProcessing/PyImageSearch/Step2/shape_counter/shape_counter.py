#  gerekli paketleri(kütüphaneleri) içe aktarıyoruz 
import argparse
import imutils
import cv2                     

# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()        # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i", "--input", required=True,  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
	help="path to input image")
ap.add_argument("-o", "--output", required=True,
	help="path to output image")
args = vars(ap.parse_args())                  	

# giriş görüntüsünü diskten yüklüyoruz
image = cv2.imread(args["input"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   #orijinal resmimizi gri tona çeviriyoruz
blurred = cv2.GaussianBlur(gray,(5,5),0)           # gri tona çevrilmiş resmi blurluyoruz(gürültü azaltma)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]     #blurlu resmin eşik değerini artırıyoruz 

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #thresh değişkenindeki resmin conturlarını buluyoruz
cnts = imutils.grab_contours(cnts)     

for c in cnts:    #bulduğumuz konturlar üzerinde geziniyoruz
	cv2.drawContours(image,c, -1, (0, 0, 255), 2)      # ve eşzamanlı olarak o konturları orijinal resmimizin üzerine çiziyoruz
	 

 
text = "I found {} total shapes".format(len(cnts))   #görüntüdeki toplam şekil sayısını text değişkenine atıyoruz
cv2.putText(image, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
	(255, 255, 255), 2)

cv2.imwrite(args["output"], image)    #çıktı görüntüsünü terminaden yolunu verdiğimiz yere kaydediyoruz