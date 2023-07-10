# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
from detectors.transform import four_point_transform
from skimage.filters import threshold_local  
import numpy as np
import argparse
import cv2  
import imutils
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i", "--image", required = True,   # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])  # giriş görüntüsünü diskten alıyoruz
ratio = image.shape[0] / 500.0   # giriş görüntüsünü yüksekliğini 500'e böleriz
orig = image.copy()  #görüntüyü kopyalayıp orig değişkenine atarız
image = imutils.resize(image,height=500 )  #orijinal görüntüyü yüksekliği 500 olmak üzere boyutlandırırız

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #boyutlandırılmış resmi gri tona çeviririz
gray = cv2.GaussianBlur(gray,(5,5),0) #gri resmi blurlarız
edged = cv2.Canny(gray,75,200) #gri tondaki resmin köşelerini saptarız
print("ADIM 1:  EDGE DETECTION")

cnts = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) #edged değişkenindeki konturları buluruz
cnts = imutils.grab_contours(cnts)

cnts = sorted(cnts,key = cv2.contourArea ,reverse=True)[:5] #alan olarak büyükten küçüğe(reverse=true) konturları sıralarız ve en büyük ilk 5 değer döndürürüz

for c in cnts: # kare olan konturu bulmak için for döngüsü başlatırız
    epsilon = cv2.arcLength(c,True)*0.02
    approx = cv2.approxPolyDP(c,epsilon,True)
    
    if len(approx) == 4:  #kare konturu bulduktan sonra approx değişkenini screenCnt değerine eşitleriz
        screenCnt = approx
        break
    
print("ADIM 2 : FIND CONTOURS OF PAPER")
cv2.drawContours(image,[screenCnt],-1,(0,255,0),2) #kare olarak bulunan konturları çizeriz


warped = four_point_transform(orig,screenCnt.reshape(4,2)*ratio) #çarpıklığı önleyip karşıdan bakılan bir perspektif görüntüsü elde ederiz

warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY) #bu görüntüyü gri formata çeviririz

T = threshold_local(warped,11,offset=10,method="gaussian") #local bir thresh uygularız
warped = (warped>T).astype("uint8") * 255 #eşik değerindeki piksel değerleriyle karşılaştırırız (true olursa 255 ile çarpılıp beyaz renk elde edilir)

print("ADIM 3: Apply perspective transform")
cv2.imshow("Original", imutils.resize(orig, height = 650)) #kırpılmış resmimizi ve ulaşmak istediğimiz görüntüyü imshowlarız
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
#cv2.imshow("Edged", imutils.resize(edged, height = 650))
cv2.waitKey(0)
cv2.destroyAllWindows()
