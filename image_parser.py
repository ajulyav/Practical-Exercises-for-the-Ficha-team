# -*- coding: utf-8 -*-
"""

@author: ajuly
"""

import numpy as np 
import cv2
from PIL import Image
import os

def read_data(filename, iternum, width, height):
  # Read bin file
  # Args:
  # 
  #filename: a valid file name
  #iternum: var needed for reading possible several files
  #width, height: known image dimensions
  # Returns:
  #data: 3D array data
  
    with open(filename, 'rb') as infile:
        
        if iternum == 0:
        # change the position of the File Handle
            infile.seek(32)
        else:
            infile.seek(32+16*iternum+(height*width))
        # read
        data = np.fromfile(infile, dtype=np.uint8, count = height*width)
        
    # reshape the data into a 3D array.
    return data.reshape((height, width))


def colorCorrection(bgr):
  # Simple color correction
  # Args:
  # 
  #bgr: a valid rgb image
  # Returns:
  #balancedImg: color corrected images
    
    r, g, b = cv2.split(bgr)
    
    rAvg = cv2.mean(r)[0]
    gAvg = cv2.mean(g)[0]
    bAvg = cv2.mean(b)[0]
     
    # find the weight of each channel
    weight = (rAvg + gAvg + bAvg) / 3
    wR = weight / rAvg
    wG = weight / gAvg
    wB = weight / bAvg
     
    r = cv2.addWeighted(src1=r, alpha=wR, src2=0, beta=0, gamma=0)
    g = cv2.addWeighted(src1=g, alpha=wG, src2=0, beta=0, gamma=0)
    b = cv2.addWeighted(src1=b, alpha=wB, src2=0, beta=0, gamma=0)
     
    balancedImg = cv2.merge([b, g, r])

    return balancedImg

##################### MAIN PART #####################


# Part 1: read the raw file
iternum = 0

# lists to store raw and rgb data 
imgList = []
rgbList = []

while True:
    try:
        data = read_data('raw_images.bin', iternum, 640, 480)
        imgList.append(data)
        iternum += 1 
    except ValueError:
        print('No more data to read!')
        break
 

# Part 2: transforming into RGB and Part 3: store as lossless-compressed image

# files will be recorded inside the active folder, "GeneratedData" sub-folder
if not os.path.exists('RgbOut'):
        os.makedirs('RgbOut')
        
for i in range(len(imgList)):
    
    # demosaicing using Variable Number of Gradients
    bgr = cv2.cvtColor(imgList[i], cv2.COLOR_BAYER_BG2BGR_VNG)

    # bgr = cv2.cvtColor(imgList[i], cv2.COLOR_BAYER_BG2BGR)

    # apply color correction
    balancedImg = colorCorrection(bgr)
    imgList.append(balancedImg)

    # save rgb
    imgData = Image.fromarray(balancedImg, 'RGB')
    cv2.imwrite(os.path.join('RgbOut', str(i) + '.png'), np.float32(imgData), [cv2.IMWRITE_PNG_COMPRESSION, 0])
    
print('Finished')    