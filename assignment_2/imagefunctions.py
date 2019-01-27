##############################################
# Anil Osman TUR
# 12290551 COM466 Digital Image Processing Assignment 2
# -------------------------------------------
# 1 - flipImage(image, flag)
#     -> returns fliped image vertical or horizontal
#     -> flag will indicates the direction horizontal or vertical
# -------------------------------------------
# 2 - inverseImage(image) 
#     -> returns inversed image
#     -> inverse process:
#        - if the range of image is [0 - L] and,
#        - if X is a gray level of a specific location,
#        - new X = L-X
# -------------------------------------------
# 3 - averageIntensity (image)
#     -> it returns avgerage intensity of the image 
#         if the image is chrome it will return array with 3 average
#     -> operation applied: total intensity / total # of pixels
#
# -------------------------------------------
# 4 - thresholdImage (image, thresholdValue)
#     -> it takes image and tresholding value as parameters
#     -> just the values above that will be in the result image
# 
# -------------------------------------------
# 5 - thresholdWithAvg (image)
#     -> it just takes image as argument
#     -> with the help of averageIntensity it will find the average and 
#        call the thresholdImage with that averageValue as the threshold value
#
# -------------------------------------------
# 6 - generateHistogram (image)
#     -> it will generate histogram of the image
#     -> if the image is colored it will return 3 histogram array otherwise 1
#
# -------------------------------------------
# 7 - equalizeHistogram (image)
#     -> it takes image as argument
#     -> it will use generateHistogram to find histogram of the image
#     -> returns histogram equlizedImage
#
# -------------------------------------------
# 
# *-> This documents just contains the implementations of these functions.
# *-> Usages will be in another document 
#############################################

import cv2
import numpy as np

## 1. flipImage (image, flag)  image flip function
def flipImage(image, flag):
    # lets choose 1 for vertical 0 for horizontal and 2 for both
    if ( flag == 1 ):
        # vertical flip
        new_image = image[:,::-1]
    elif ( flag == 0 ):
        # horizontal flip
        new_image = image[::-1,:]
    elif (flag == 2 ):
        # origin flip
        new_image = image[::-1, ::-1]
        
    return new_image


#  2. inverseImage (image) image reverse function
def inverseImage(image):
    
    w = image.shape[0]
    h = image.shape[1]
    
    for i in range(w):
        for j in range(h):
            if not (len(image.shape) == 3):
                image[i,j] = np.uint8(255 - image[i,j])
            else:
                image[i,j][0] = np.uint8(255 - image[i,j][0])
                image[i,j][1] = np.uint8(255 - image[i,j][1])
                image[i,j][2] = np.uint8(255 - image[i,j][2])

    return image


# 3. averageIntensity (image)
def avgIntensity(image):
    
    w = image.shape[0]
    h = image.shape[1]
    
    
    if len(image.shape) == 3: # it is colored
        b,g,r = cv2.split(image)
        ciAvg = np.array([np.sum(b),np.sum(g),np.sum(r)]) / (w*h) # color intesity average
        print ("average intensities: ", ciAvg)
        return ciAvg
    else:
        iAvg = int( np.sum(image) / (w*h) )
        print ("average intensity: ", iAvg)
        return iAvg
    
    return -1 # if haven't returned yet there is a problem


# 4. thresholdImage (image, thresholdValue)
def thresholdImg(image, threshold):
    
    if len(image.shape) == 3: # it is colored
        colors = cv2.split(image)
        
        if not isinstance(threshold, int):
            
            if len(threshold) == 3:
                for i in range(3):
                    colors[i] = np.uint8(255) * (colors[i] > threshold[i])
            else:
                print ("3 parameter needed to apply treshold with different values")
        
        else:
            for i in range(3):
                colors[i] = np.uint8(255) * (colors[i] > threshold)
        return cv2.merge(colors)
    
    else:
        
        return 255 * ( image > threshold )
    
    return -1  # if haven't returned yet there is a problem

# 5. thresholdWithAvg (image)
def tresholdWithAvg(image):
	avgI = avgIntensity(image)
    return thresholdImg(image, avgI)
	
# 6. generateHistogram (image)
def generateHistogram(image):
    
    cols = image.shape[0]
    rows = image.shape[1]
    
    if (len(image.shape) == 2 ):
        histData = np.zeros(256) # as a range 0 - 255 used
        flatImage = image.flatten()
        
        for i in range(len(flatImage)):
            histData[flatImage[i]] += 1
        
        return histData
        
    elif (len(image.shape) == 3):
        b,g,r = cv2.split(image)
        histData = [generateHistogram(b),generateHistogram(g),generateHistogram(r)]
 
        return histData

    return -1 # if haven't returned yet there is a problem


# 7. equalizeHistogram (image)
def equalizeHistogram(image):
    
    cols = image.shape[0]
    rows = image.shape[1]
    hist = generateHistogram(image)
    
    if (len(image.shape) == 2 ):
        sample = image.size
        histFunc = hist / float(sample)
        
        for i in range(1,hist.size):
            histFunc[i] = histFunc[i-1] + histFunc[i]
        #print (histFunc)
        new_image = np.zeros(image.shape, dtype=np.uint8)   
        
        for i in range(cols):
            for j in range(rows):
                new_image[i,j] = np.uint8( round( histFunc[image[i,j]] * image[i,j] ) )
        
        return new_image
    
    elif (len(image.shape) == 3):
        b,g,r = cv2.split(image)
        b = equalizeHistogram(b)
        g = equalizeHistogram(g)
        r = equalizeHistogram(r)
        new_image = cv2.merge((b,g,r))
        
        return new_image
        
    return -1 # if haven't returned yet there is a problem
