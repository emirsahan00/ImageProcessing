# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2
import numpy as np
import argparse

# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i","--image",  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
    help="path to the image")
args=vars(ap.parse_args())

image = cv2.imread(args["image"]) # giriş görüntüsünü terminalden belirttiğimiz yolu baz alarak diskten alıyoruz
 
boundaries = [   
	([17, 15, 100], [50, 56, 200]),    #4 farklı renk aralığını giriyoruz
	([86, 31, 4], [220, 88, 50]),
	([103, 86, 65], [145, 133, 128]),
    ([25, 146, 190], [62, 174, 250])
]

for (lower,upper) in boundaries:  #açtığımız döngü ile renk aralıklarında geziniyoruz
    lower = np.array(lower,dtype="uint8")  
    upper = np.array(upper,dtype="uint8")

    mask = cv2.inRange(image,lower,upper) #döngüden gelen alt ve üst değerler ile mask oluşturuyoruz
 
    output = cv2.bitwise_and(image,image,mask=mask)  #görüntüyü filtreliyoruz
    cv2.imshow("output",output)  #filtrelenmiş görüntümüzü imshowlıyoruz
    cv2.waitKey(0)
