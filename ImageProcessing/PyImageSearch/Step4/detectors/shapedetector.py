import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self,c):
        shape = "unidentified"
        
        epsilon = 0.04*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)  #len içine alırsak köşe sayısı buluyor

        if len(approx) == 3:
            shape = "triangel"
        elif len(approx) == 4:
            #en boy oranı hesaplanıyor
            (x,y,w,h) = cv2.boundingRect(approx)  #koordinatları verir
        
            #print(x,y,w,h)
            #print(oran)
            oran = w /float(h)
            shape = "square" if oran >= 0.95 and oran <= 1.05 else "rectangle"

        elif len(approx)==5:
            shape = "pentagon"
        else:
            shape = "circle"
        return shape
    
