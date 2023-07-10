# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2                     
import imutils              
import numpy as np

coin = cv2.imread("D:/Coin-Counting-Mission/source/coin1.jpg")    #giriş görüntümüzü diskten alıyoruzz
coin = imutils.resize(coin,width=500)                     #giriş görüntümüzü bilgisayarı çok yormamak için boyutlandırıyoruz.(genişlik = 500)
gray = cv2.cvtColor(coin,cv2.COLOR_BGR2GRAY)            #görüntümüzü gri tona çeviriyoruz.
kernel = np.ones((5,5),np.uint8)    # 5 satır 5 sütunluk ve elemanları 1 olan dizi oluşturuyoruz.

thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,5,2)  #2 boyutlu görüntümüze paraları tespit etmemizin kolay olması için threshold uyguluyoruz
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) #eşik değeriyle oynanmış görüntümüzdeki gürültüleri azaltıyoruz
dilate = cv2.dilate(closing,kernel,iterations = 2)  #yeterli yineleme sayısı(iterations) vererek closingden gelen piksel değerlerinideki beyaz değerlerinin ağırlığını artırıyoruz

mask = dilate.copy() #orijinal resimdeki madeni paraların arka planını siyah yapmak için  dilate değişkenini kopyalayıp mask değişkenine atıyoruz                                      
mask = cv2.bitwise_and(coin, coin, mask=mask) #and kapısıyla birlikte arka planımızı(background) siyah yapıyoruz

ret,thresh2 =  cv2.threshold(mask,0,255,cv2.THRESH_BINARY)  #madeni paraların bulunduğu ve arka planın siyah olduğu mask değişkenini threshold uyguluyoruz

kernel2 = np.ones((3,3),np.uint8) # 3 satır 3 sütunluk ve elemanları 1 olan dizi oluşturuyoruz.
opening = cv2.morphologyEx(thresh2,cv2.MORPH_OPEN,kernel2,iterations=3) #threshold uygulanmış resmin gürültülerini azaltıyoruz ve daha net bir görüntü elde ediyoruz.
dilation = cv2.dilate(opening,kernel2,iterations=3) #yeterli yineleme sayısı(iterations) vererek openingten gelen piksel değerlerinideki beyaz değerlerinin ağırlığını artırıyoruz
 
opening = cv2.cvtColor(opening,cv2.COLOR_BGR2GRAY) #yukarda uygulanan işlemler sonucu görüntümüz 3 boyutlu olmuştur ve  bu nedenden dolayı aşağıdaki fonksiyonlar çalışmayacaktır.
dilation = cv2.cvtColor(dilation,cv2.COLOR_BGR2GRAY) #bu nedenden dolayı opening ve dilaion değişkenlerini 2 boyuta indirgiyoruz.

dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2,5) #görüntüdeki nesnelerin kenarlarını belirlemek veya nesneler arasındaki uzaklıkları hesaplamak için bu işlemi yaptık
ret, sure_fg = cv2.threshold(dist_transform, 0.30*dist_transform.max(), 255, 0)  #dist_transformden gelen değerin %30ununu altındaki değerleri 0 üstündeki değerleri ise 255 değerine eşitliyoruz 
sure_fg = cv2.erode(sure_fg,kernel,iterations=1) ##yeterli yineleme sayısı(iterations) vererek sure_fg gelen piksel değerlerinideki siyah değerlerinin ağırlığını artırıyoruz
sure_fg = np.uint8(sure_fg) #sure_fg değişkenini uint8 veri tipine dönüştürdük.8 bitlik (0-255 aralığında) tamsayı değerlerini temsil etmek için kullanırız

unknown = cv2.subtract(dilation, sure_fg) #dilation görüntüsünden sure_fg görüntüsünü çıkardık.(iki görüntü arasındaki piksel değerlerini çıkartmayı sağlar)
_, markers = cv2.connectedComponents(sure_fg) #sure_fg görüntüsündeki bağlı değişkenleri bulmamızı sağlar (yani her bir parayı)
markers = markers + 1  #markers görüntüsündeki tüm piksellere 1 eklenir 
markers[unknown == 255] = 0  #unknown görüntüsündeki piksel değerleri 255 olan değerleri markers görüntüsünde 0'a eşitler
 
cv2.watershed(coin, markers)  #nesneleri ve arka planı ayrıştırmak için kullanılırız  
coin[markers == -1] = [0, 0, 255]   #markers görüntüsündeki işaretsiz yani işlenmeyen pikselleri kırmızı değerine eşitleriz
num_coins = len(np.unique(markers)) - 1  

print("Madeni para adeti :",num_coins) #para adetini yazdırırırz

cv2.imshow("coin",coin)  #işlenmiş görüntülerimizi imshowlarız
cv2.imshow("sure_fg",sure_fg)
cv2.imshow("thresh",thresh2)
cv2.imshow("mask",mask)

cv2.waitKey(0) 
cv2.destroyAllWindows()

