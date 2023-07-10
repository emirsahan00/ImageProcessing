# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import numpy as np
import argparse
import imutils
import cv2       

def sort_contours(cnts, method="left-to-right"):        # sample : python sorted_contours.py --image src/legolar.png --method "top-to-bottom" 

	reverse = False
	i = 0
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
		
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1

	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),key=lambda b:b[1][i], reverse=reverse))
	return (cnts, boundingBoxes)

def draw_contour(image, c, i):
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	cv2.putText(image, "#{}".format(i + 1), (cX-20 , cY), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)

	return image

# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser() # ArgumentParser sınıfını ap değişkenine atıyoruz 
ap.add_argument("-i", "--image", required=True, help="Path to the input image")  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
ap.add_argument("-m", "--method", required=True, help="Sorting method")
args = vars(ap.parse_args())  


image = cv2.imread(args["image"]) # giriş görüntüsünü diskten alıyoruz
accumEdged = np.zeros(image.shape[:2], dtype="uint8") #image görüntüsünün ilk 2 boyutunda bir mask uyguluyoruz

for chan in cv2.split(image): #döngü başlatıyoruz
	  
	chan = cv2.medianBlur(chan, 11)  #döngüden gelen görüntümüze blur uyguluyoruz
	edged = cv2.Canny(chan, 50, 200) #blurlu görüntünün kenarlarını saptıyoruz
	accumEdged = cv2.bitwise_or(accumEdged, edged) # or işlemine sokuyoruz


cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # 'accumEdged' değişkenindeki konturları buluyoruz
cnts = imutils.grab_contours(cnts)  
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5] #alanları büyükten küçüğe sıralıyoruz ve ilk 5 değerini döndürüyoruz.
orig = image.copy() #image görüntüsünü kopyalayıp orig değişkenine atıyoruz

for (i, c) in enumerate(cnts): 
	orig = draw_contour(orig, c, i)

(cnts, boundingBoxes) = sort_contours(cnts, method=args["method"]) #konturları metoda göre sıralıyoruz

for (i, c) in enumerate(cnts):
	draw_contour(image, c, i) #konturları çiziyoruz

cv2.imshow("Unsorted", orig)
cv2.imshow("sorted",image)
cv2.imshow("Edge Map", accumEdged)
cv2.waitKey(0)
cv2.destroyAllWindows()