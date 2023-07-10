# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2
import imutils
import argparse
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i","--image",required=True,  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
    help="path to the input image")
args=vars(ap.parse_args())

image = cv2.imread(args["image"])  # giriş görüntüsünü diskten alıyoruz

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #orijinal resmimizi gri tona çeviriyoruz
blurred = cv2.GaussianBlur(gray,(5,5),0)          #gri tondaki resmimizi blurluyoruz ve gürültüleri azaltıyoruz
ret,thresh = cv2.threshold(blurred,65,255,cv2.THRESH_BINARY)    #gri tona çevirdiğimiz resmin eşik değerini artırıyoruz ve 2 boyuta çeviriyoruz

cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #thresh değişkenindeki görüntünün conturlarını buluyoruz
cnts = imutils.grab_contours(cnts)

for c in cnts:  # bulduğumuz konturlar üzerinde döngü yapıyoruz

    M = cv2.moments(c)          # konturların alanının merkezini buluyoruz
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
  
    cv2.drawContours(image,[c],-1,(0,255,0),2)  #orijinal resmimizin üstüne bulunan konturları çiziyoruz
    cv2.circle(image,(cX,cY),7,(0,0,255),-1)     #bulunan konturların cX,cY merkezli ve 7 birim yarıçaplı bir çember çiziyoruz
    cv2.putText(image,"center",(cX-20,cY-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)   #merkez kısmının üst kısmına merkez yazdırıyoruz (orijinal resim üstüne)
    
    cv2.imshow('image',image) #çıktımızı görüntülüyoruz
    cv2.waitKey(0)
    cv2.destroyAllWindows() #tüm pencereleri kapatırız 


