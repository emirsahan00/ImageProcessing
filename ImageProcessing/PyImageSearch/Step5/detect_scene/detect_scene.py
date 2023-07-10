# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import argparse
import imutils
import cv2
import os

# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()        # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-v", "--video", required=True, type=str,     # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
	help="path to input video file")
ap.add_argument("-o", "--output", required=True, type=str,
	help="path to output directory to store frames")
ap.add_argument("-p", "--min-percent", type=float, default=1.0, 
	help="lower boundary of percentage of motion")
ap.add_argument("-m", "--max-percent", type=float, default=10.0,
	help="upper boundary of percentage of motion")
ap.add_argument("-w", "--warmup", type=int, default=200,
	help="# of frames to use to build a reasonable background model")
args = vars(ap.parse_args())

fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()     #arka plan çıkarıcı modelimizi fgbg değişkenine atıyoruz

captured = False   #değişkenlerimize false ve 0 değerlerini veriyoruz
total = 0
frames = 0

vs = cv2.VideoCapture(args["video"])  # kullanılacak videoumuzu diskten yüklüyoruz
W, H = (None, None)   #width ve height değerlerimizi none olarak belirliyoruz

while True:      #frameler için döngü başlatıyoruz 
    ret,frame = vs.read()     #framelerimizi okuyoruz

    if frame is None:        #veya ret == False:
        break       # frame = None ise döngüyü kır 

    orig = frame.copy()   #framelerimizi kopyalayıp orig değişkeninine atıyoruz 
    frame = imutils.resize(frame,width=400)   #imutils kütüphanesi kullanarak framelerin genişliği 300 olacak şekilde boyutlandırıyoruz
    mask = fgbg.apply(frame) #bu kod satırı bir başlangıç arka plan görüntüsü üzerinde eğitilir ve ardından mevcut görüntü ile arka plan arasındaki farkı hesaplamak için kullanılır 

    mask = cv2.erode(mask, None, iterations=2)  #gürültüyü ortadan kaldırmak için gerekli morfolojik işlemlerimizi yaparız (erode,dilate)
    mask = cv2.dilate(mask, None, iterations=2) 


    if W is None or H is None:  #width ya da height değişkenlerimizi none olup olmadığına bakarız
        H, W = mask.shape[:2]     #eğer none ise mask frameinin height ve width değerlerine eşitleriz

    p = (cv2.countNonZero(mask) / float(W * H)) * 100 # ön plan ile arka plan arasındaki maske yüzdesini hesaplıyoruz(hareketin durup durmadığını belirlemek için)

    if p < args["min_percent"] and not captured and frames > args["warmup"]:   #ön plan piksel yüzdesini p min_percent sabitiyle karşılaştırırız.(2) görüntü yakalamamışsak (3) ısınma sürecinin tamamlanıp tamamlanmadığını sorgularız
        #cv2.imshow("captured",captured)
        captured = True  #görüntü yakaladık

        fileName = " {}.png".format(total)   # dosya ismini total değişkeniyle belirledik
        path = os.path.sep.join([args["output"],fileName]) 
        total +=1 #total değişkenini  bir artırdık

        print("kaydediliyor {}".format(path))
        cv2.imwrite(path,orig) # orig (frame.copy) görüntüsünü path ile verilen yoldaki dosyaya kaydettik
    elif captured and p>= args["max_percent"]:   
        captured = False

    cv2.imshow("Frame", frame) #orijinal framelerizi gösteririrz
    cv2.imshow("Mask", mask) #framelerin birçok morfolojik işlemden geçmiş mask halini imshowlarız
    if cv2.waitKey(1) == ord('q'):  #eğerki q ya basılırsa döngüyü kır
        break

    frames +=1 #frames değişkenindeki değeri bir arttırırız

vs.release()  #görüntüyü(framleri) serbest bırakırız