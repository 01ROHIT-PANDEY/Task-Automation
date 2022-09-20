
import numpy as np
import cv2
import pytesseract
from PIL import Image

import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#This Function taking a path if image 

def Eval(path):
    
    image_file=path
    img=cv2.imread(image_file)

    #Binarization
    def binarization(img):
        return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    grayImage=binarization(img)

    threshold,imageBW=cv2.threshold(grayImage,127,255,cv2.THRESH_BINARY)




    #Noise removal
    def removalNoise(img):
        kernal=np.ones((1,1),np.uint8)
        image=cv2.dilate(img,kernal,iterations=1)
        kernal=np.ones((1,1),np.uint8)
        image=cv2.erode(img,kernal,iterations=1)
        #this morphology is removing the noise
        image=cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernal)
        image=cv2.medianBlur(img,3)

        return image


    noiseRemove=removalNoise(imageBW)
    cv2.imwrite(r"D:\Final Year Project\Phase-2\Automation\Image_To_Text\noise.jpg",noiseRemove)
    


    NewImage=Image.open(r"D:\Final Year Project\Phase-2\Automation\Image_To_Text\noise.jpg")
    text = pytesseract.image_to_string(NewImage)
    text=text.strip('\n');
    os.remove(r"D:\Final Year Project\Phase-2\Automation\Image_To_Text\noise.jpg")
    return (text)



#
#tex=Eval("D:\Final Year Project\Phase-2\Automation\download.jpg")
#print(tex)


