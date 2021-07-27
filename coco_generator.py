# -*- coding: utf-8 -*-
"""

@author: ajuly
"""

import json
import random
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
import os


def TransformForeground(foreground):
  # Apply foreground transformations
  # Args:
  # 
  #foreground: a valid foreground image  
  # Returns:
  #frgImage: the final image after transformations


  # Rotate the foreground
  angle = random.randint(0, 359)  
  frgImage = foreground.rotate(angle, resample=Image.BICUBIC, expand=True)

  # Scale the foreground
  #scale = random.random() * 0.5 + 0.5
  #newSize = (int(frgImage.size[0] * scale), int(frgImage.size[1] * scale))
  #transfImage = frgImage.resize(newSize, resample=Image.BICUBIC)

  # Possible to add other transformations 
  # . . . 

  return frgImage


def CreateAnnotation(data, annotationId, x, y, xEnd, yEnd):
  # Simple function to write one annotation
  # Args:
  # data: data structure
  # annotationId: unique id
  # x, y, xEnd, yEnd: COCO-format bbox 
  # Returns:
  # data: updated data structure
  
  
  data['annotations'].append({
    "id": annotationId, 
    "bbox": [x,y,xEnd,yEnd],
})
  
  return data   



def GenerateImages(foreground, background, numGenerations = 1000):
  # Composes a foreground image and a background image
  # Args:
  #
  #foreground: a valid foreground image
  #background: a valid background image
  #
  #numGenerations: number of images to generate (1000 by default)
  # Returns:
  #data: data to save in .JSON

  # convert it to the RGBA space
  background = background.convert('RGBA')

  # data structure to write annotations
  data = {}
  data['annotations'] = []
  
  # init unique id
  annotationId = 1

  for num in range(numGenerations):
    
    # deep copy of bkg for each of 1000 synthetic images  
    final = copy.deepcopy(background)

    # random from 0 to 4 objects
    numObj = random.randint(0, 4)
    
    if numObj == 0:

      # as it was asked to generate 0 foreground obj, store this type of annotations
      data = CreateAnnotation(data, annotationId, 0,0,0,0)
      final = background
      annotationId += 1 
     
    for obj in range(numObj):
      
      # call a function to transform the foreground obj
      frgImage = TransformForeground(foreground)

      # choose a random x,y position for the foreground
      maxX = final.size[0] - frgImage.size[0]
      maxY = final.size[1] - frgImage.size[1]

      # generate a new postion for the object
      objPosition = (random.randint(0, maxX), random.randint(0, maxY))

      # create annotation, save the obj position
      data = CreateAnnotation(data, annotationId, objPosition[0], objPosition[1], frgImage.size[0],frgImage.size[1])
      annotationId += 1 
     
      # place the foreground object on the background
      newFgObj = Image.new('RGBA', final.size, color = (0, 0, 0, 0))
      newFgObj.paste(frgImage, objPosition)

      # Extract the alpha channel from the foreground and paste it into a new image the size of the composite
      alpha_mask = frgImage.getchannel(3)
      new_alpha_mask = Image.new('L', final.size, color = 0)
      new_alpha_mask.paste(alpha_mask, objPosition)
      final = Image.composite(newFgObj, final, new_alpha_mask)
      
      
    # save     
    name = './GeneratedData/img_' + str(annotationId-1) + '.png'
    final.save(name, 'PNG')
    
    # extra simple plot part if needed  
    # fig, ax = plt.subplots()

    # ax.imshow(final)
    # plt.show() 
      
  return data


##################### MAIN PART #####################

try: 
    background = Image.open('background.png')
    foreground = Image.open('object.png')
except FileNotFoundError:
    print("Make sure that both files are in the folder with the code.")

# files will be recorded inside the active folder, "GeneratedData" sub-folder
if not os.path.exists('GeneratedData'):
        os.makedirs('GeneratedData')

# call the function to generate 1000 images
data = GenerateImages(foreground,background)

# save to JSON 
with open('./GeneratedData/annotations.json', 'w') as outfile:
     json.dump(data, outfile)
    
    