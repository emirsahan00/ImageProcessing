#gerekli paketleri(kütüphaneleri) ekleriz
from detector.panorama import Stitcher
import cv2
import argparse
import imutils											

# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-f", "--first", required=True, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
	help="path to the first image")
ap.add_argument("-s", "--second", required=True,
	help="path to the second image")
args = vars(ap.parse_args())



imageA = cv2.imread(args["first"]) #ilk görüntümüzü diskten alırız
imageB = cv2.imread(args["second"]) #ikinci görüntümüzü diskten alırız

imageA = imutils.resize(imageA,width=400) #ilk görüntümüzü genişliği 400 olmak üzere boyutlandırırız
imageB = imutils.resize(imageB,width=400) #ikinci görüntümüzü genişliği 400 olmak üzere boyutlandırırız

stitcher = Stitcher()  #bu sınıf ile görüntüleri birleştiriyoruz
(result,vis) = stitcher.stitch([imageA,imageB],showMatches = True) #ilk ve ikinci görüntüleri birleştiriyoruz

cv2.imshow("A",imageA)  #ilk ,ikinci ve birleştirilmiş görüntümüzü imshowlıyoruz
cv2.imshow("B",imageB)
cv2.imshow("Vis",vis)
cv2.imshow("Result",result)

cv2.waitKey(0) 
cv2.destroyAllWindows()





