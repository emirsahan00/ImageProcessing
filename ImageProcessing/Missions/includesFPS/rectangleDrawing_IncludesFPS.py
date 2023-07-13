import cv2 #gerekli kütüphanelerimizi aktarıyoruz
import time

def dikdortgen_ciz(event,x,y,flag,param):  #dikdörtgen çizme fonksiyonumuzu oluştururuz
    global pt1,pt2,topLeft_clicked,botRight_clicked #global değişkenlerimizi tanımlarız

    if event == cv2.EVENT_LBUTTONDOWN: #eğer mouse sol click tıklanmışsa

        if topLeft_clicked == True & botRight_clicked == True:  #sağ ve sol click tıklanmışsa dikdörtgen çizdirilmiştir demektir ve default değerlere eşitleriz.
            pt1 = (0,0)
            pt2 = (0,0)
            topLeft_clicked = False
            botRight_clicked = False
        
        if topLeft_clicked == False: #sol click tıklanmışsa değerimizi true ve o koordinatları pt1 değişkenine eşitleriz
            pt1 = (x,y)
            topLeft_clicked = True
        elif botRight_clicked == False: #sağ click tıklanmışsa değerimizi true ve o koordinatları pt2 değişkenine eşitleriz
            pt2 = (x,y)
            botRight_clicked =True

#global değişkenlerim
pt1 = (0,0)
pt2 = (0,0)
topLeft_clicked = False
botRight_clicked = False

cap = cv2.VideoCapture(0) #Görüntüyü webcam den alıyoruz
cv2.namedWindow('test')
cv2.setMouseCallback('test',dikdortgen_ciz)

prev_frame_time = 0 #fps hesaplamak için framelerin zamanına ihtiyacımız olacak bu nedenle bu iki değişkeni tanımlarız
new_frame_time = 0

# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  #görümtümüzün genişliğini buluruz
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #görümtümüzün yüksekliğini buluruz
# x = width // 2 
# y = height // 2
# w =width // 4
# h =height //4 
while True:          #sonsuz bir döngü oluştururuz
    ret,frame = cap.read()  #framelerimizi okuruz
    frame = cv2.flip(frame,1)  #frameleri y eksenine göre yansıtırız

    #FPS
    new_frame_time = time.time()   #iki frame arasındaki zaman farkını(saniye cinsinden) ölçmek için başlangıç zamanını 'new_frame_time' değişkenine atarız
    fps = 1/(new_frame_time-prev_frame_time) #sonraki frameden önceki frame'in zamanını çıkarırız ve 1 böleriz(gecikme buluruz bir bakıma)
    prev_frame_time = new_frame_time   #sonraki frame zamanını önceki frame zamanına eşitleriz ki bir sonraki framede fpsimizi bulabilelim
    fps = "FPS:{}".format(str(fps))  #frameler üzerine yazdırabilmek için fps değişkenindeki float değerimizi string değere dönüştürüp fps değişkenine atarız
    cv2.putText(frame,fps, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)  #ve fps değerimizi eş zamanlı olarak frame üstüne yazdırırırz.


    if topLeft_clicked == True:  #eğer sol click tıklanmışsa o koordinatlara  içi dolu yuvarlak  çizdiririz
        cv2.circle(frame,pt1,5,(0,0,0),-1) 
    if topLeft_clicked and botRight_clicked: #eğer sol ve sağ tık tıklanmışsa pt1 ve pt2 köşe noktaları belirlenmiş bir dikdörtgen çizdiririz
        cv2.circle(frame,pt2,5,(0,0,0),-1)
        cv2.rectangle(frame,pt1,pt2,(0,0,0),2)

    cv2.imshow('test',frame)  #framelerimizi imshowlarız
    if cv2.waitKey(1)==ord('q'):  #q tuşuna basınca döngümüzü sonlandırırız
        break

cap.release()  #görüntüyü serbest bırakırız
cv2.destroyAllWindows()  #tüm pencereleri kapatırız