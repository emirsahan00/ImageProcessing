from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init__(self):
        
        colors =OrderedDict ({
            "reds" : (0,0,255),
            "green" : (0,255,0),
            "blue" : (255,0,0)})
        
        self.lab =np.zeros((len(colors),1,3),dtype="uint8")
        #print((self.lab).shape)  --> output : (3, 1, 3)

        self.colorName = []

        for (i,(name,rgb)) in enumerate(colors.items()):
            self.lab[i] = rgb
            print(rgb)
            
            self.colorName.append(name)
        
        self.lab = cv2.cvtColor(self.lab,cv2.COLOR_BGR2LAB)


    def label(self,image,c):


        mask = np.zeros(image.shape[:2],dtype="uint8")
        cv2.drawContours(mask,[c],-1,255,-1)
        mask = cv2.erode(mask,None,iterations=2)
        mean = cv2.mean(image,mask=mask)[:3]

        minDist =  (np.inf,None)             #burayı

        for(i,row) in enumerate(self.lab):

            d = dist.euclidean(row[0],mean)     #burayı

            if d < minDist[0]:         
                minDist = (d,i)

        return self.colorName[minDist[1]]
    

