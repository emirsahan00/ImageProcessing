# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2
import argparse 
import numpy as np
import imutils
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i","--image",required=True,  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
    help="path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])   # giriş görüntüsünü diskten alıyoruz

lower = np.array([0,0,0])  #alt aralığımızı belirliyoruz
upper = np.array([15,15,15]) #üst aralığımızı belirliyoruz
shapeMask = cv2.inRange(image,lower,upper)   # '[0,0,0] [15,15,15]' arasındaki pikselleri beyaz aralıkta olmayan pikselleri siyah yapar

cnts = cv2.findContours(shapeMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #maskelenmiş görüntüdeki konturları buluyoruz
cnts = imutils.grab_contours(cnts)

print("---I found {} black shapes---".format(len(cnts)))  #kaç şekil bulunduysa yazdırıyoruz

for c in cnts:  #bulunun konturlar içinde geziniyoruz
    cv2.drawContours(image,[c],-1,(0,255,0),2)  #konturları çiziyoruz
    cv2.imshow("image",image)  #image ve shapeMask değişkenimizi imshowluyoruz
    cv2.imshow("mask",shapeMask)
    cv2.waitKey(0)


