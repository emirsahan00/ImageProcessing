# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
from skimage import transform
from skimage import filters
import argparse
import cv2

# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()          # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i", "--image", required=True,  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
	help="path to input image file")
ap.add_argument("-d", "--direction", type=str,
	default="vertical", help="seam removal direction")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])  # giriş görüntüsünü terminalden belirttiğimiz yolu baz alarak diskten alıyoruz
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #giriş görüntümüzü gri tona çeviriyoruz

mag = filters.sobel(gray.astype("float")) #sobel filtresini uygularız ve görüntünün kenarlarını yakalarız.piksellerin yoğunluk değerlerindeki değişiklikleri hesaplamak için yaparız
cv2.imshow("ORIGINAL",image) #giriş görüntüsünü gösteriyoruz.

for numSeams in range(20,140,20):  # 20'den başlayarak 140'a (dahil değil) kadar 20'şer artan bir döngü başlatıyoruz.

    carved =transform.seam_carve(image,mag,args["direction"],numSeams)  #gerekli argümanları alarak şekli resmi istediğimiz bir yönde boyutlandırırz(numSeams belirler kırpılan boyutu)

    print("[INFO] removing {} seams; new size: ""w = {} ,h = {}".format(numSeams,carved.shape[1],carved.shape[0])) # yeni width ve height yazdırırız
    
    cv2.imshow("carved",carved) #kırpılmış resmi gösteririz
    cv2.waitKey(0) 

    
