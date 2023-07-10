# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import cv2
import imutils

image = cv2.imread("d:/pyimagesearch/nasil_baslarim/step4/exterme_points_hand/src/hand.png") # giriş görüntüsünü belirttiğimiz yoldan alıyoruz
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #giriş görüntüsünü gri tona çeviriyoruz
gray = cv2.GaussianBlur(gray,(5,5),0) #gri tondaki resmi blurlıyoruz

ret,thresh = cv2.threshold(gray,45,255,cv2.THRESH_BINARY) #blurlu resmi threshold uyguluyoruz
thresh = cv2.erode(thresh,None,iterations=2) #threshli resmimize morfolojik işlemlerden geçiriyoruz
thresh = cv2.dilate(thresh,None,iterations=2)

cnts = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #birçok işlemden geçmiş resmimizdeki kontuları buluyoruz
print(len(cnts))
cnts = imutils.grab_contours(cnts)

c = max(cnts,key = cv2.contourArea)   #kontur listesindeki alanı en büyük olan konturu c değişkenine atıyoruz

extLeft = tuple(c[c[:, :, 0].argmin()][0])  #en sağ,en sol,en aşağı ve en yukarıdaki konturları döndürüyoruz
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])

cv2.drawContours(image, [c], -1, (0, 255, 255), 2) #bulunan tüm konturları çiziyoruz

cv2.circle(image, extLeft, 8, (0, 0, 255), -1)  #en sağ,en sol,en aşağı ve en yukarıdaki kontur koordinatlarına çember çiziyoruz
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)

cv2.imshow("image",image) #ve son olarak resmimizi imshowluyoruz
cv2.waitKey(0)
cv2.destroyAllWindows() #tüm pencereleri kapatıyoruz