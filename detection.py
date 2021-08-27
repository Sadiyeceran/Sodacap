import cv2
import numpy as np 
from numpy.lib.function_base import median 
import scipy as sp
import scipy.ndimage as nd

class detection:
        
    # resize the images
    def img_resize(img):

        scale_percent = 25
        width = int((img.shape[1] * scale_percent) / 100)
        height = int((img.shape[0] * scale_percent) / 100)
        img = cv2.resize(img, (width,height))

        return img


    # turn 8 bit image and blured
    def gray_blur(img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)

        return blur 



    # detect edges
    def autoCanny(img, sigma=0.3):
        
        median = np.median(img)
        lower = int(max(0, (1.0 - sigma) * median))
        upper = int(min(255, (1.0 + sigma) * median))
        canny = cv2.Canny(img, lower, upper)

        return canny



    # dilation opertion and background 
    def morphological_operations(img):
    
        kernel = np.ones((3,3), np.uint8)
        dilation = cv2.dilate(img, kernel, iterations=1)
        ret, labels = cv2.connectedComponents(dilation)
        
        N =600
        for i in range(1, labels.max() + 1):
            pts =  np.where(labels == i)
            if len(pts[0]) < N:
                labels[pts] = 0

        label_hue = np.uint8(179*labels/np.max(labels))
        blank_ch = 255*np.ones_like(label_hue)
        
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue==0] = 0    
        labeled_img = cv2.cvtColor(labeled_img,cv2.COLOR_BGR2GRAY)

        return labeled_img


    # fill the object inside 
    # https://stackoverflow.com/questions/36294025/python-equivalent-to-matlab-funciton-imfill-for-grayscale
    def flood_fill(img, h_max=255):
 
        el = nd.generate_binary_structure(2,2).astype(np.int)
        inside_mask = nd.binary_erosion(~np.isnan(img), structure=el)
        output_array = np.copy(img)
        output_array[inside_mask]=h_max
        output_old_array = np.copy(img)
        output_old_array.fill(0)   
        el = nd.generate_binary_structure(2,1).astype(np.int)

        while not np.array_equal(output_old_array, output_array):
            output_old_array = np.copy(output_array)
            output_array = np.maximum(img, nd.grey_erosion(output_array, size=(3,3), footprint=el))
        
        return output_array



    #Hough Circle Transform 
    def hough_circle(img, src):
        rows = src.shape[0]
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, rows /5,
                               param1=100, param2=15,
                               minRadius=35, maxRadius=55)
    
        if circles is not None:
            circles = np.uint16(np.around(circles))

            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(src, center, 1, (0, 0, 100), 3)
                # circle outline
                radius = i[2]
                cv2.circle(src, center, radius, (255, 0, 255 ), 3)
                cv2.putText(src, "Detected Soda Cap", center, cv2.FONT_HERSHEY_DUPLEX, 0.5,(255,0,0),2)
            
        cv2.imshow("detected image", src)

        return src