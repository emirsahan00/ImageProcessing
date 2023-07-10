# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
from imutils.video import VideoStream
import imutils
import time
import cv2

saliency = None      #saliency değerini none olarak başlatıyoruz
vs = VideoStream(src=0).start()   #webcamimizi başlatıyoruz
time.sleep(2.0)  #sistemin 2.0 saniye geç açılmasını istiyoruz

while True:       #frameleri okumak için sonsuz bir döngü başlatıyoruz
    frame = vs.read()    #frameleri okuyoruz
    frame = cv2.flip(frame,1)   #framleri y eksenine göre döndürüp ayna görüntüsü elde ediyoruz
    frame = imutils.resize(frame,width=500)  #frameleri boyutlandırıyoruz(bilgisayarın daha hızlı çalışması için (işlenecek veri ne kadar azsa işlem hattımız o kadar hızlı çalışabilir))
    
    if saliency is None:  #eğer ki  saliency değerimiz None ise 
        saliency = cv2.saliency.MotionSaliencyBinWangApr2014_create()   #hareketli belirgin nesne bulma fonksiyonunu saliency değişkenine eşitliyoruz
        saliency.setImagesize(frame.shape[1],frame.shape[0])       #çıktı boyutunu ayarlıyoruz
        saliency.init() 
        
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  #framelerimizi gri tona çeviriyoruz
    success,saliencyMap = saliency.computeSaliency(gray)    #gri tonla gelen framelerin belirgin kısımlarındaki koordinatları saliencyMap değişkenine atıyoruz
    
    saliencyMap = (saliencyMap * 255).astype("uint8")  #değerleri [0,255] aralığına sokuyoruz (beyaz veya siyah)
    

    cv2.imshow("saliencyMap",saliencyMap)  #bir çok işlemden geçmiş çıktımızı gösteriyoruz
    cv2.imshow("frame",frame) #orijinal framelerimizi gösteriyoruz

    if cv2.waitKey(1) == ord('q'):  #eğer ki q'ya basılırsa döngüyü kır
        break

cv2.destroyAllWindows()  #tüm pencereleri kapat
vs.stop()  #webcami durdur