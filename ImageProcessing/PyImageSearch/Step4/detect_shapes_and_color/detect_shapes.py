# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
from detectors.shapedetector import ShapeDetector 
from detectors.colorlabeler import ColorLabeler
import argparse
import imutils  
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i", "--image",required=True, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
    help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # giriş görüntüsünü terminalden belirttiğimiz yolu baz alarak diskten alıyoruz
resized = imutils.resize(image,width=400)  #giriş görüntümüzü boyutlandırıyoruz
ratio = image.shape[0] /float(resized.shape[0])  #orijinal görüntümüzün yüksekliğini resized görüntüsündeki yüksekliğe bölüyoruz
print(image.shape[0]) 
print(float(resized.shape[0]))
# print(ratio)

blurred = cv2.GaussianBlur(resized,(5,5),0) #boyutlandırılmış resme blur uyguluyourz
gray = cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)  #blurlu görüntüdeki bgr renk kanalını gray formatına çeviriyoruz
lab = cv2.cvtColor(blurred,cv2.COLOR_BGR2LAB) 

ret,thresh = cv2.threshold(gray,60,255,cv2.THRESH_BINARY) #gri tona çevrilmiş resmin thresholdlıyoruz

cnts = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #threshli resimdeki konturları buluyoruz
cnts = imutils.grab_contours(cnts) 

sd = ShapeDetector()  # ShapeDetector sınıfını sd değişkenine eşitleriz
cl = ColorLabeler()  #ColorLabeler sınıfını cl değişkenine eşitleriz



for c in cnts:  #bulduğumuz konturların içinde gezinmek için for döngüsü başlatırız

    M =cv2.moments(c)   #konturun merkezini(ağırlık merkezi) buluruz
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    
    shape = sd.detect(c)   
    color = cl.label(lab,c)

    c = c.astype("float")  #float veritipine çeviririz  
    c *= ratio  #sağlıklı bir çizim yapabilmek için boyutlandırılmış oranla çarparız
    c = c.astype("int") #integer veri tipine dönüştürürüz

    text = "{} {} ".format(color,shape) 
    
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)  #kontuları image üstüne çizdiririz
    cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)  #ağırlık merkezlerine renk ve geometrik verileri yazarız

    cv2.imshow("Image", image)  #resmi imshowlarız
    cv2.waitKey(0)
    