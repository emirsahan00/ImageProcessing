#gerekli paketleri(kütüphaneleri) ekleriz
from detectors import simple_barcode_detection
from imutils.video import VideoStream
import argparse
import cv2
import time
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-v", "--video", # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
	help="path to the (optional) video file")
args = vars(ap.parse_args())

if not args.get("video",False):   #burada barkod taraması yapacağımız görüntünün video olarak mı alındığı yoksa webcam den mi geldiğinin belirlendiği kısım
    vs = VideoStream(src=0).start() #eğer ki webcamden alıcaksak görüntümüzü VideoStream ile kameramızı başlatırız
    time.sleep(1.0)     # bir saniye duraklatılmalı olarak webcam penceremiz gösterilir
else:  # eğer ki terminalden path yoluyla birlikte bir video girildiyse VideoCapture değişkeniyle vs değişkenine atılır.
    vs = cv2.VideoCapture(args["video"])


while True:      #frameleri okumak için bir döngü başlatırız
    frame = vs.read()     #frameleri okuruz
    frame = cv2.flip(frame,1)
    frame = frame[1] if args.get("video",False) else frame  #framlerin webcamden mi yoksa .avi veya .mp4 (vb.) uzantılı bir  video şeklinde mi geldiğini sorguluyoruz.

    if frame is None:   #eğer frame == None ise döngümüzü kırıyoruz
        break

    box = simple_barcode_detection.detect(frame)  #framlerimzi fonksiyonun parametresi olarak girip çıktısını box değişkenine eşitliyoruz
    if box is not None:         #fonksiyondan gelen konturlar none değilse bu konturları draWContours ile çizdiriyoruz
        cv2.drawContours(frame,[box],-1,(0,255,0),2)

    cv2.imshow("frame",frame)     #çıktımızı gösteriyoruz
    if cv2.waitKey(1) == ord('q'):        #eğer ki q tuşuna basıldıysa döngümüzü kırıyoruz
        break


if not args.get("video",False): #framelerimizi webcamden gelmediyse videoyu serbest bırakıyoruz
    vs.stop()

else:
    vs.release()  # webcamden gelen görüntüyü durduruyoruz.

cv2.destroyAllWindows()  #tüm pencereleri kapatıyoruz.
