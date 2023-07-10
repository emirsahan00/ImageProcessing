from imutils.perspective import four_point_transform   #gerekli kütüphaneleri tanımlarız
from imutils import contours 
import imutils
import cv2

DIGITS_LOOKUP = {           #sayıları(0-9) dictionary yapısını kullanarak tanımlarız
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

image = cv2.imread("recognize_digits\src\input.png") #resmi okuruz
image = imutils.resize(image,height=500)  #resmi boyutlandırırız
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #resmi gri tona çeviririz
blurred = cv2.GaussianBlur(gray,(5,5),0)   #resmi blurlarız
edged = cv2.Canny(blurred,50,200,255)

cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #resmin konturlarını bulduk
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts,key=cv2.contourArea,reverse=True)  #bulduğumuz konturları büyükten küçüğe sıraladık
displayCnt = None 

for c in cnts:
    epsilon = cv2.arcLength(c,True) * 0.02        # köşe sayısını bulmak için gerekli işlemler
    approx = cv2.approxPolyDP(c,epsilon,True)

    if len(approx) == 4:            #for ile içinde gezindiğimiz en büyük konturun köşe sayısı dört mü diye sorguladık 
        displayCnt = approx        # eğer 4 ise displayCnt değişkenine eşitledik
        break

warped = four_point_transform(gray,displayCnt.reshape(4,2))     #resmin yan açılardan çekilmesine karşın perspektif dönüşümü uyguladık
output =  four_point_transform(image,displayCnt.reshape(4,2)) 

ret,thresh = cv2.threshold(warped,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) # Basamakların kendilerini elde etmek için eşik değeri belirledik

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,5))   #eşikli görüntüyü temizledik
thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)

cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #temizlediğimiz görüntünün konturlarını bulduk
cnts = imutils.grab_contours(cnts)
digitCnts= []



for c in cnts:
    (x,y,w,h) = cv2.boundingRect(c)         # o andaki conturun koordinatlarını bulduk
    #cv2.drawContours(warped,[c],-1,(0,0,255),2,8)
    if w >= 15 and (h >= 30 and h <= 40):   #konturun width ve height değerlerini istenen aralıkta mı diye kontrol ettik
        digitCnts.append(c)               # sağlanan konturları digitCnt dizine append ile ekledik
#cv2.imshow("wared",warped)
#cv2.waitKey(0)
digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0] # digitCnt içindeki conturları soldan sağa sıraladık
digits = []

for c in digitCnts:                     #rakam konturlarının her birinde döngü başlattık
    (x,y,w,h) = cv2.boundingRect(c)       
    roi = thresh[y:y+h,x:x+w]       #thresh görüntüsünden ilgileneceğimiz alanı roi değişkenine attık

    # bu rakamların her biri için sınırlayıcı kutu oluşturuyoruz.
    (roiH,roiW) = roi.shape            #roi görüntülerinin genişlik ve yüksekliğini hesaplıyoruz
    (dW,dH) = (int(roiW * 0.25),int(roiH * 0.15))    #ROI boyutlarına dayalı olarak her segmentin yaklaşık genişliğini ve yüksekliğini hesaplıyoruz.
    dHC = int(roiH * 0.05)  
 
    segments = [                                        # yedi parçaya karşılık gelen x ve y koordinatlarının bir listesini tanımlarız. 
		((0, 0), (w, dH)),	# en üst
		((0, 0), (dW, h // 2)),	# üst-sol
		((w - dW, 0), (w, h // 2)),	# üst-sağ
		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # orta
		((0, h // 2), (dW, h)),	# alt-sol
		((w - dW, h // 2), (w, h)),	# alt-sağ
		((0, h - dH), (w, h))	# en alt
	]
    on = [0] * len(segments)     # 7 tane 0'lardan oluşan bir dizi oluşturup on değişkenine atıyoruz.                          

    for (i,((xA,yA),(xB,yB))) in enumerate(segments):   # 7 tane olan her parçanın üzerinde döngü yapıyoruz
        segROI = roi[yA:yB,xA:xB]           #her parçanın roisini(ilgili alan) çıkarıyoruz
        total = cv2.countNonZero(segROI)    # sıfır olmayan piksel sayısını total değişkenine atıyoruz.
        area = (xB-xA) * (yB-yA)         
        #print(total)
        if total / float(area) > 0.5:  #Sıfır olmayan piksellerin toplam alana oranı %50 den büyükse segmentin açık olduğunu düşünebiliriz
            on[i] = 1

    try:                           # Eğer ki keyError verecekse olursa except bloğuna yollayıp döngüyü devam ettiriyoruz
        digit = DIGITS_LOOKUP[tuple(on)]
        digits.append(digit)
        cv2.rectangle(output,(x,y),(x + w,y + h),(0,255,0),1)
        cv2.putText(output,str(digit),(x-10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,255,0),2)
    except KeyError:         # KeyError hatasına karşın olarak while döngüsünü devam ettiririz.
        continue


#print(u"{}{}.{} \u00b0C".format(*digits))
#print(digits)
cv2.imshow("image",image)
cv2.imshow("output",output)

cv2.waitKey(0)
cv2.destroyAllWindows()