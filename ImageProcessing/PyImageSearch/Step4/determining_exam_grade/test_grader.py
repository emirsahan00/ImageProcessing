# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np                   
import argparse
import imutils
import cv2
# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()    # ArgumentParser sınıfını ap değişkenine atıyoruz
ap.add_argument("-i", "--image", required=True, # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz. 
	help="path to the input image")
args = vars(ap.parse_args())

ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}  #cevap anahtarlarını sözlük biçiminde tanımlarız
 
image = cv2.imread(args["image"]) # giriş görüntüsünü diskten alıyoruz
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #giriş görüntüsünü bgr tondan gray tonuna çeviriyoruz
blurred = cv2.GaussianBlur(gray, (5, 5), 0) #gri tondaki resmi blurluyoruz
edged = cv2.Canny(blurred,75,200)  #blurlu resimdeki köşeleri belirginleştiriyoruz

cnts = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #konturları buluyoruz
cnts = imutils.grab_contours(cnts)

docCnt = None  

if len(cnts) > 0:   #kontur olduğu sürece
    cnts = sorted(cnts,key=cv2.contourArea,reverse=True) #konturları büyükten küçüğe sıralıyoruz

    for c in cnts:  #bulduğumuz konturların içinde geziniriz 
        epsilon = cv2.arcLength(c,True)*0.02
        approx = cv2.approxPolyDP(c,epsilon,True)

        if len(approx) == 4:  #eğer kontur 4 köşeli ise
            docCnt = approx #approx değerini 'docCnt' değişkenine eşitleriz
            break

paper = four_point_transform(image, docCnt.reshape(4, 2))  # çarpıklığı önlüyoruz ve resmi karşıdan bakılmış bir perspektif veriyoruz
warped = four_point_transform(gray, docCnt.reshape(4, 2)) 

ret,thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) #warped değişkenini thresholdarız

cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #threshold uygulanmış resimdeki konturları buluruz
cnts = imutils.grab_contours(cnts)
questionsCnts = []                 # bunun içinde balonlukların kontur koordinatları var toplamda 25 tane 

for c in cnts: 
    (x,y,w,h) = cv2.boundingRect(c) #konturun x ,y ,yükselik ve genişlik değerini dönderir
    oran = w / float(h)    

    if w >= 20 and h>=20 and oran >= 0.9 and oran <= 1.1:  # yuvarlağın değerleri  
        questionsCnts.append(c)  #if koşulunu sağlayan kontuları questionsCnts listesine ekleriz
 
questionsCnts = contours.sort_contours(questionsCnts,method="top-to-bottom")[0]  #eklenen konturları yukardan aşağı sıralarız
correct = 0 

for (q,i) in enumerate(np.arange(0, len(questionsCnts),5)):       # --> #np.arange(0,10,3)   Output: array([0, 3, 6, 9])
    
    #len(questionsCnts) = 25
    cnts = contours.sort_contours(questionsCnts[i:i+5]) [0]  
    bubbled = None

    for (j,c) in enumerate(cnts): #konturların içinde geziniriz
        mask = np.zeros(thresh.shape,dtype="uint8")  #thresh boyutlarında bir mask oluştururuz
        cv2.drawContours(mask,[c],-1,255,-1) #bulunan konturları çizeriz
        
        mask = cv2.bitwise_and(thresh,thresh,mask=mask) 
        total = cv2.countNonZero(mask) 
        

        if bubbled is None or total > bubbled[0]:  
            bubbled = (total,j)

        color = (0,0,255)
        k = ANSWER_KEY[q]

        if  k == bubbled[1]: 
            color = (0,255,0)
            correct+=1
    
    cv2.drawContours(paper,[cnts[k]],-1,color,3)    

score = (correct / 5.0) * 100 #doğru cevap sayısını 5'e bölüp 100'le çarpıyoruz
print("INFO : score {:.2f}%".format(score)) #score değerini yazdırırız

cv2.putText(paper,"{:.2f}%".format(score),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),2) #paper üstüne score değerini yazdırırız
cv2.imshow("original",image) #image,paper ve thresh görüntülerimizi imshowluyoruz
cv2.imshow("exam",paper)
cv2.imshow("thresh",thresh)
cv2.waitKey(0)

        

