# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
from imutils import build_montages             
from imutils import paths
import argparse
import random
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i","--images",  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
    help="path to input directory of images")
ap.add_argument("-s","--sample",type=int,default=21,
    help="# of images to sample")
args=vars(ap.parse_args())  

imagePaths = list(paths.list_images(args["images"])) #giriş görüntülerimizi dosya halinde alıp listeliyoruz
random.shuffle(imagePaths) #karıştırıyoruz
imagePaths = imagePaths[:args["sample"]] 
 
images = [] #images isminde bir liste oluşturuyoruz
for imagePath in imagePaths: #imagelerin içinde geziniyoruz
	
	image = cv2.imread(imagePath)  #resmi okuyoruz
	images.append(image) #images listesine ekliyoruz

montages = build_montages(images, (128, 196), (3, 7)) #(128, 196) boyutu - (3, 7) açılan alan boyutu
for montage in montages: #mntajlanmış resimlerimizi imshowlarız
	cv2.imshow("Montage", montage)
	cv2.waitKey(0)