# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import imutils
import cv2

# giriş görüntüsünü diskten yol vererek alıyoruz
image = cv2.imread("D:/pyImageSearch/Nasil_Baslarim/Step3/starting_example/src/image.jpeg")
(h, w, d) = image.shape   #orijinal resmin boyutlarını h,w ve d değişkenlerine eşitliyoruz.

print("width={}, height={}, depth={}".format(w, h, d))  #width, height ve depth değerlerini yazdırıyoruz.
roi = image[60:160, 100:120]    #orijnal resmimizden ilgileneceğimiz alanı seçip roi değişkenine atıyoruz

(B, G, R) = image[100, 50]     #resmin x=100 ,y=50 olan pikselindeki b,g ve r değerini b ,g ve r değişkenine eşitliyoruz 
print("R={}, G={}, B={}".format(R, G, B))      

resized = imutils.resize(image, width=100)  #orijinal resmimizi imutils kütüphanesi kullanarak width=300 olacak şekilde boyutlandırıyoruz

center = (w // 2, h // 2)       #görüntünün merkezine erişiriz

M = cv2.getRotationMatrix2D(center, -45, 1.0) #görüntünün merkez noktasını center değişkeninden alarak -45(saat yönünün tersine) derecelik açıyla döndürürüz  1->Görüntünün boyutu değişmeden döndermek demek.
rotated = cv2.warpAffine(image, M, (w, h))    #orijinal görüntüyü M dönüş matrisine göre döndürerek rotated isimli değikene atarız.

out = image.copy()   #orijinal görüntüyü kopyalayıp out değişkenine atarız 
output = image.copy()  
cv2.putText(output, "OpenCV + Jurassic Park!!!", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

cv2.imshow("out", out)     
cv2.imshow("rotated", rotated)    # döndürülmüş resmimizi gösteririz.
cv2.imshow("roi", roi)        #kırpılmış resmimizi imshowlarız 
cv2.imshow("Image", image) 
cv2.waitKey(0)          #bir tuşa basana kadar pencere açık kalır 






