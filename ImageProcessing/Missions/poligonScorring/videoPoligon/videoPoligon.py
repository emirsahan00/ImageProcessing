import cv2 #gerekli kütüphaneleri tanımlarız
import math
import numpy as np
import time

def findcenter(cnt): #parametre olarak vereceğimiz konturların center(merkez) koordinatlarını dönderirir
    
    M = cv2.moments(cnt)  #konturun momentini buluruz
    # if M['m00'] == 0:  # konturun alanı sıfırsa moment hesaplamasını yapmadan direkt (0, 0) koordinatını döndürürüz.
    #     return (0, 0)
    cx = int(round(M['m10']/M['m00']))
    cy = int(round(M['m01']/M['m00']))
    center = (cx, cy)
    return center

image1 = cv2.imread('D:/ImageProcessing/Missions/poligonScorring/videoPoligon/src/1.png') #atış yapılmamış resmimizi içe aktarırırz
cap = cv2.VideoCapture('D:/ImageProcessing/Missions/poligonScorring/videoPoligon/src/video.mp4') #atış yapılacak olan videomuzu içe aktarırız
while True: #frameleri okumak için sonsuz döngü
    
    ret,frame = cap.read() #frameleri okuruz
    if ret == False: #eğer ki video bittiyse yani frameler okunamadıysa döngüyü kır
        break
    time.sleep(2.0)
    foto_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #atış yapılmış olan framemizi bgr formatından hsv formatına çeviririz
    h,s,v = cv2.split(foto_hsv) 
    v_mask = cv2.inRange(v, 0, 160) #resmimize mask uygularız
    contours, _ = cv2.findContours(v_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #mask uygulanmış resmin konturlarını buluruz

    biggest_cntr = None #en büyük konturu bulmak için biggest_cntr isimli bir değişken oluştururuz
    biggest_area = 0 #en büyük konturun alanını bulmak için biggest_area isimli bir değişken oluştururuz
    shoted = frame.copy() #atış yapılmış framemizi kopyalarız
    for contour in contours: #bulduğumuz konturların içinde geziniriz
        area = cv2.contourArea(contour) #konturun alanını area değişkenine eşitleriz
        if area > biggest_area: #eğer area en büyük alandan büyükse 
            biggest_area = area #area değişkenindeki alanı en büyük alana eşitleriz
            biggest_cntr = contour #contur değişkenindeki konturu en büyük kontura eşitleriz
    cv2.drawContours(shoted, [biggest_cntr], -1, (0, 255, 0), 3) #bulduğumuz en büyük konturu yani hedef tahtasını çevreleyen çemberi çizdirdik
    big_radius = math.sqrt(biggest_area / math.pi) #en büyük konturun yarıçapını bulduk

    center = findcenter(biggest_cntr) #en büyük konturun merkez koordinatlarını dönderdik

    shoted = cv2.circle(shoted, center, 4, (0,0,255), -1) #merkez noktasına kırmızı bir içi dolu çember çizdik

    diff_image = cv2.absdiff(image1, frame) #atışları tespit edebilmek için atış yapılmamış hedef tahtasıyla arasındaki farkları buluyoruz
    diff_image = cv2.medianBlur(diff_image, 7) #konturları daha düzgün bulabilmesi için medianBlur işlemi uyguluyoruz
    diff_image =cv2.cvtColor(diff_image,cv2.COLOR_BGR2GRAY) #atışların bulunduğu resmin konturlarını bulabilmek için gri formatına çeviriyoruz
    ret,thresh =  cv2.threshold(diff_image,128,255,cv2.THRESH_BINARY) #threshold uyguluyoruz
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #atışların konturlarını bulduk

    holes = [] #atışların merkezlerini saklamak için liste oluşturduk
    
    for contour in contours: #atışların konturları arasında gezdik
        c = findcenter(contour) #her bir atışın merkez koordinatlarını dönderdik
        holes.append(c) #holes listesine merkezleri ekliyoruz
        shoted = cv2.circle(shoted, c, 2, (0,0,240), -1) #merkez noktasına içi dolu kırmızı bir çember çizeriz


    slices = big_radius / 5  # hedef tahtamız 5 adet iç içe çemberden oluşmaktadır bu yüzden 5'e böldük

    scores = [] #skorumuzu ekrana yazdırmak için scores adlı liste oluştururuz
    for hole in holes: #atışların merkezleri içinde geziniriz
        #atışların merkezleriyle hedef tahtasının merkezlerini bir takım matematiksel işlemden geçirip merkeze olan uzaklığını buluruz
        dx = hole[0] - center[0] 
        dy = hole[1] - center[1]
        dist = math.sqrt(dx*dx + dy*dy) #atışların merkeze olan uzaklığınu bulduk
        
        #print('Hedef tahtasının yarıçapı :',big_radius)
        
        if dist < 0: #eğer ki mesafe sıfırdan küçükse tam ortaya atış yapılmış demektir listeye 5 olarak ekler ekrana 100 puan olarak yazdırırız
            scores.append(5)
        elif dist > 281: #eğer ki atış,hedef tahtasının dışına çıktıysa 0 puan olarak ekleriz
            scores.append(0)
        else: #eğer ki mesafe 0 dan büyükse mesafeyi her bir çember aralığını bölüp 5 ten çıkarırız
            scores.append(5 - int(dist / slices))
    
    font = cv2.FONT_HERSHEY_SIMPLEX #yazı tipimizi belirleriz
    for a in range(len(holes)): #atış adeti kadar dönecek bir döngü oluştururuz
        holescenter = (holes[a][0], holes[a][1]) #puanı yazdırmak için atışların merkezlerini holescenter listesinden alırız
        shoted = cv2.putText(shoted, str(scores[a]*20), holescenter, font, 0.95, (0,0,220), 2, cv2.LINE_AA) #aldığımız scorları 20 ile çarpıp ekrana yazdırırız

    cv2.imshow('shoted',shoted) #hedef görüntümüzü imshowluyoruz
    if cv2.waitKey(5)==ord('q'): #eğer ki 'q' tuşuna basıldıysa döngüyü kır 
        break 
cv2.destroyAllWindows() #tüm pencereleri kapat
