# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2
import argparse
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i","--image",required=True, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
    help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # giriş görüntüsünü terminalden belirttiğimiz yolu baz alarak diskten alıyoruz

#saliency = cv2.saliency.StaticSaliencySpectralResidual_create() #resmin en belirgin(en göze çarpan bölgelerini) noktalarını tespit ediyoruz 
#success, saliencyMap =saliency.computeSaliency(image)  #belirgin yerlerin koordinatlarını atarız saliencyMap değişkenine

saliency = cv2.saliency.StaticSaliencyFineGrained_create()  #bu yukardaki fonksiyondan daha hassas ama aynı işlev(resmin en belirgin(en göze çarpan bölgelerini) noktalarını tespit ediyoruz)
success, saliencyMap = saliency.computeSaliency(image) #belirgin yerlerin koordinatlarını atarız saliencyMap değişkenine
print(saliencyMap.shape[0])
saliencyMap = (saliencyMap * 255).astype("uint8") #değerleri [0,255] arası ölçeklendiriyoruz
ret,threshMap = cv2.threshold(saliencyMap.astype("uint8"),0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU) #resmin conturlarını bulabilmek için threshold uyguluyoruz.(thresh_otsu resmin ortalam ağırlığına göre thresh atan bir değişken)

cv2.imshow("Image",image)  #giriş görüntümüzü görüntüleriz
cv2.imshow("Output",saliencyMap) #threshold uygulanmadan önceki görüntümüzü görüntüleriz
cv2.imshow("threshMap",threshMap) #en son olarak ulaşmak istediğimiz görüntüyü imshowlarız 
cv2.waitKey(0)
cv2.destroyAllWindows() #tüm pencereleri kapat