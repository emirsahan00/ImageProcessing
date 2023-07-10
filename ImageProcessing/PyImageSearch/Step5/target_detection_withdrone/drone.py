#gerekli paketleri(kütüphaneleri) ekleriz
import cv2
import imutils
import argparse
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-v","--video",help="path to the video file") # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["video"]) #videomuzu diskten alıyoruz

while True: #frameleri okumak için sonsuz bir döngü oluşturuyoruz
    ret,frame = cap.read() #frameleri okuyoruz
    status = "No Targets" 

    if ret == 0:  #frameler okunmamışsa döngüyü kır
        break

    #print(ret) 
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #frameleri gri formata çevirdik
    blurred = cv2.GaussianBlur(gray,(7,7),0)  #gri tondaki resmimizi blurladık
    edged = cv2.Canny(blurred,50,150) #blurlanmış framelerdeki kenarları belirginleştiriyoruz

    cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #edged görüntüsündeki konturları buluyoruz
    cnts = imutils.grab_contours(cnts)

    for c in cnts: #konturların içinde geziniyoruz
        
        epsilon = cv2.arcLength(c,True) * 0.01
        approx = cv2.approxPolyDP(c,epsilon,True)

        if len(approx) >= 4 and len(approx) <= 6: #eğer kontur 4 köşeliden büyük ve eşitse and 6 köşeliden küçükse ve eşitse  
            (x,y,w,h) = cv2.boundingRect(approx)     # (x, y) koordinatları dörtgenin sınırlayıcı kutusunun sol üst köşesinin koordinatlarını temsil eder.w genişliği ve h yüksekliği ifade eder.    
            EnBoyOrani = w / float(h)  

            area = cv2.contourArea(c)                   #conturun alanını bulur    
            hullArea = cv2.contourArea(cv2.convexHull(c))  #convexHull --> dış kapuktaki conturdur burda o konturun alanını hesaplıyoruz

            solidity = area / float(hullArea)  

            keepDims = w > 25 and h > 25 #eğer ki w ve h değerler 25 ten büyükse True
            keepSolidity = solidity > 0.9 # solidty değeri 0.9'dan büyükse True
            keepEnBoyOrani = EnBoyOrani >= 0.8 and EnBoyOrani <= 1.2     #kare mi diye kontrol ediyoruz .En boy oranı bu aralıktaysa True 

            if keepDims and keepSolidity and keepEnBoyOrani:                #3 değişkende True ise 
                cv2.findContours(frame,[approx],-1,(0,0,255),4)  #bulunan konturları frame üzerine çiz

                status = "Target(s) Acquired"  #hedef saptanıldı

                M = cv2.moments(approx)                                              # bu kısım karenin ortasına artı çizdiğimiz kısım  ' + ' targett

                (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))   #konturun merkezine '+' işareti ekliyoruz
                (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
                cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)

                cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2) 

                cv2.imshow("Frame", frame) #frameler imshowlarız

                if cv2.waitKey(1) == ord('q'): #eğer ki 'q' tuşuna basıldıysa döngüyü kır 
                    break

cap.release () #frameleri serbest bırak
cv2.destroyAllWindows()  #tüm pencereleri kapat










