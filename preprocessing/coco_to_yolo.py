#import libraries
import json
import os
import math
from PIL import Image
import time

input_path = "val2017"
output_path = "coordinates_val2017/"

f = open('instances_train2017.json')
data = json.load(f)
f.close()

def get_image_annotation(image_id):    #returns image annotations  
    image_ann = []
    isFound = False
    for ann in data['annotations']:
        if ann['image_id'] == image_id:
            image_ann.append(ann)
            isFound = True
    if isFound:
        return image_ann
    else:   
        return None

def get_image(filename):    #returns image
    for img in data['images']:
        if img['file_name'] == filename:
            return img

def coco91_to_coco80():  # converts 91-convention classes to 80-convention classes
    classes80 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, None, 24, 25, None,
         None, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, None, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
         51, 52, 53, 54, 55, 56, 57, 58, 59, None, 60, None, None, 61, None, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
         None, 73, 74, 75, 76, 77, 78, 79, None]
    return classes80

file_names = []
def load_images_from_folder(folder):
    count = 0
    for filename in os.listdir(folder):
        file_names.append(filename)
        count += 1
        print(filename + " " + str(count))

load_images_from_folder(input_path)

count = 0
coco80 = coco91_to_coco80_class()

start = time.time()
for filename in file_names:
  
    #get original image 
    img = get_image(filename)
    img_id = img['id']
    img_w = img['width']
    img_h = img['height']
    
    #get annotations
    img_ann = get_image_annotation(img_id)

    if img_ann:
        #opening file for current image
        file_with_annotations = open(f"{output_path}{filename[:-4]}.txt", "a")

        for ann in img_ann:
            
            current_category = coco80[ann['category_id'] - 1] #yolo category IDs start from 0 
            current_bbox = ann['bbox']
            x = current_bbox[0]
            y = current_bbox[1]
            w = current_bbox[2]
            h = current_bbox[3]

            #top left and bottom right points
            xtl = x
            ytl = y
            xbr = xtl + w
            ybr = ytl + h


            #find center points
            x_centre = (xtl + xbr)/2
            y_centre = (ytl + ybr)/2 
            
            #normalization
            x_centre = x_centre / img_w
            y_centre = y_centre / img_h
            w_new = w / img_w
            h_new = h / img_h

            #limit upto six number of decimal places
            x_centre = format(x_centre, '.6f')
            y_centre = format(y_centre, '.6f')
            w_new = format(w_new, '.6f')
            h_new = format(h_new, '.6f')

            #write annotation to the file in the yolo format
            file_with_annotations.write(f"{current_category} {x_centre} {y_centre} {w_new} {h_new}\n")
            
        file_with_annotations.close()   
    count += 1
    print(f"{output_path}{filename[:-4]}.txt" + " " + str(count))
    
end = time.time()
time_needed = (end - start)/60
print(time_needed)
