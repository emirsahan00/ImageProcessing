# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import numpy as np
import argparse
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-m", "--model", required=True,  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
	help="path to BING objectness saliency model")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-n", "--max-detections", type=int, default=10,  #Varsayılan olarak 10 a ayarlı olarak incelenecek maksimum tespit sayısı.
	help="maximum # of detections to examine")
args = vars(ap.parse_args())

image = cv2.imread(args["image"]) # giriş görüntüsünü terminalden belirttiğimiz yolu baz alarak diskten alıyoruz

saliency = cv2.saliency.ObjectnessBING_create()  #resmin en belirgin(en göze çarpan bölgelerini) noktalarını tespit ediyoruz 

saliency.setTrainingPath(args["model"])  #eğitim yolunu oluştururz

success,saliencyMap = saliency.computeSaliency(image)  #resmin en belirgin kısımlarının koordinatlarını döndürüyoruz

numDetecitons = saliencyMap.shape[0]  # saliencyMap değişkeninin [0] indexindeki boyutunu döndürürüz

for i in range(0,min(numDetecitons,args["max_detections"])):  #komut satırımızda bulunan maksimum algılama sayısına kadar algılamalar üzerinde döngü yapmaya başlarız
    
    startX,startY,endX,endY = saliencyMap[i].flatten() #algılanan kısımların sınırlayıcı kutu koordinatlarını buluyoruz.

    output = image.copy() #giriş görüntüsünü kopyalayıp output değişkenine atıyoruz
    color = np.random.randint(0,255,size=(3,)) #color değişkenine random renk atıyoruz 0,255 arası 3 elemanlı bir dizi
    color = [int(c) for c in color] 

    cv2.rectangle(output,(startX,startY),(endX,endY),color,2) #algılanan kısımları sınırlayıcı kutu olarak output'un üstüne çizdiriyoruz

    cv2.imshow("output",output) #ve çıktıyı gösteriyoruz
    cv2.waitKey(0) 
