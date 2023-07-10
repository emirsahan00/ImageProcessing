# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2
import numpy as np
import argparse                      
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz                          
ap = argparse.ArgumentParser()   # ArgumentParser sınıfını ap değişkenine atıyoruz                         
ap.add_argument("-s","--source",required=True,  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
    help="path to the image ")
ap.add_argument("-t","--target",required=True,
    help="path to the image ")
args = vars(ap.parse_args())

source = cv2.imread(args["source"]) #kaynak görüntümüzü diskten alıyoruz
target = cv2.imread(args["target"])  #hedef görüntümüzü diskten alıyoruz


#source ->>kaynak       target -->hedef
def color_transfer(source,target):
    source = cv2.cvtColor(source,cv2.COLOR_BGR2LAB).astype("float32")  #kaynak görüntümüzün veri tipini float yapıp bgr formatından lab formatına dönüştürüyoruz
    target = cv2.cvtColor(target,cv2.COLOR_BGR2LAB).astype("float32")#hedef görüntümüzün veri tipini float yapıp bgr formatından lab formatına dönüştürüyoruz

    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source) # L*, a* ve b* kanallarının her biri için piksel yoğunluklarının ortalamasını ve standart sapmasını hesaplıyoruz
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)
  
    (l, a, b) = cv2.split(target)
   
    l -= lMeanTar          
    a -= aMeanTar
    b -= bMeanTar
  
    l = (lStdTar / lStdSrc) * l
    a = (aStdTar / aStdSrc) * a
    b = (bStdTar / bStdSrc) * b
   
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc
  
    l = np.clip(l, 0, 255) #skalaya sokuluyor(oran)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)
	
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)
	
    return transfer

def image_stats(image):
	(l, a, b) = cv2.split(image)
	(lMean, lStd) = (l.mean(), l.std())
	(aMean, aStd) = (a.mean(), a.std())
	(bMean, bStd) = (b.mean(), b.std())

	return (lMean, lStd, aMean, aStd, bMean, bStd)

cv2.imshow("Source",source) 
cv2.imshow("Target",target)
cv2.imshow("Transfer",color_transfer(source,target))


cv2.waitKey(0)
cv2.destroyAllWindows()