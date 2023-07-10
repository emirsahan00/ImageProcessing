# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
from detectors.transform import four_point_transform
import numpy as np          # sample : python transform_example.py --image hello.jpeg --coords "[(73, 239), (356, 117), (475, 265), (187, 443)]" '
import argparse
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz 
ap.add_argument("-i", "--image", help = "path to the image file") # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
ap.add_argument("-c", "--coords",
	help = "comma seperated list of source points")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # giriş görüntüsünü diskten alıyoruz
pts = np.array(eval(args["coords"]), dtype = "float32") 

warped = four_point_transform(image, pts) #image değişkenindeki görüntüyü terminalde verdiğimiz değerlere göre perspektif dönüşümü uyguluyoruz
cv2.imshow("Original", image) #orijinal resmimizi imshowlarız
cv2.imshow("Warped", warped) #ulaşmak istediğimiz resmi imshowlarız
cv2.waitKey(0)