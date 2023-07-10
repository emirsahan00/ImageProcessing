# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
from imutils import paths
import argparse
import cv2

def variance_of_laplacian(image): #cv2.laplacion fonksiyonu kenar bulur ve kenarların ne kadar belirgin olduğunu ölçer. (mesela bir dağın yanında mavi bir gökyüzü veya bir ağacın yapraklarıyla gövdesi arasındaki ayrım kenardır)

    return cv2.Laplacian(image,cv2.CV_64F).var()  # var fonksiyonu ile döndürülen matrisin varyansını hesaplarız
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()  # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i", "--images", required=True, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.  
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

for imagePath in paths.list_images(args["images"]): #bu döngüde args değişkeniyle gelen görüntü dosyalarını listeliyoruz
    image = cv2.imread(imagePath)     # giriş görüntüsünü listenen imagePath değişkeninden image değişkenine atıyoruz.
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)    # resmi gri tonlara çeviriyoruz
    fm = variance_of_laplacian(gray)       # bulunan varyans fm değişkenine atanır
    text = "Bulankk degil" 
    
    if fm < args["threshold"]:     #default olarak  verilmiş 100 değerinin(eşik değeri) altındaysa resim bulanıktır
        text = "Bulanik"

    cv2.putText(image,"{}: {:.2f}".format(text,fm),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),3)  #bulunan sonuçlar görüntü üzerine yazılır 
    cv2.imshow("Image",image)
    if cv2.waitKey(0) == ord('q'):      #q tuşuna basılırsa döngü kırılır
        break

