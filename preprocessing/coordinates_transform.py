#import libraries
import json
import os
import math
from PIL import Image
import time

input_path = "val2017"
output_path = "coordinates_val2017_transformed/"

f = open('instances_val2017.json')    #the same script can be used for 'instances_train2017.json'
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

a = 3264;
b = 2448;
scaling_factor = a/b;    #aspect ratio of images from COHI
count = 0
n = 4    #coordinate scaling factor coefficient
coco80 = coco91_to_coco80()

start = time.time()

for filename in file_names:
    
    #get original image 
    img = get_image(filename)
    img_id = img['id']
    img_w = img['width']*4    #because transformed images were increased by 4
    img_h = img['height']*4
    
    #resize according to the size of transformed images
    if (img_w<img_h):
        h_transf = int(img_w*scaling_factor) - (int(0.11*int(img_w*scaling_factor))-2)*2
        w_transf = img_w - (int(0.11*img_w)-2)*2
        scaling_new = int(img_w*scaling_factor)/img_h;
    else:    #img_w>img_h, img_w==img_h
        h_transf = img_h - (int(0.11*img_h)-2)*2
        w_transf = int(img_h*scaling_factor) - (int(0.11*int(img_h*scaling_factor))-2)*2
        scaling_new = int(img_h*scaling_factor)/img_w;
            
    #get annotations
    img_ann = get_image_annotation(img_id)

    if img_ann:
        #open file for current image
        file_with_annotations = open(f"{output_path}{filename[:-4]}_4.txt", "a")    #because n = 4

        for ann in img_ann:
            current_category = coco80[ann['category_id'] - 1] #yolo category IDs start from 0 
            current_bbox = ann['bbox']
            x = current_bbox[0]*4    #because transformed images were increased by 4
            y = current_bbox[1]*4
            w = current_bbox[2]*4
            h = current_bbox[3]*4
            
            #corner points of bounding box
            xtl = x
            ytl = y
            xbr = xtl + w
            ybr = ytl + h
            xtr = xbr
            ytr = ytl 
            xbl = xtl
            ybl = ybr

            #middle points
            x1 = (xtr + xtl)/2
            y1 = (ytr + ytl)/2 
            x2 = (xbl + xtl)/2
            y2 = (ybl + ytl)/2 
            x3 = (xbr + xtr)/2
            y3 = (ybr + ytr)/2 
            x4 = (xbr + xbl)/2
            y4 = (ybr + ybl)/2 
            
            coord_x_box = [xtl, xbr, xtr, xbl, x1, x2, x3, x4]
            coord_y_box = [ytl, ybr, ytr, ybl, y1, y2, y3, y4]
            
            #transformation
            coord_x_new_box = []
            coord_y_new_box = []
            for i in range(8):
                x = 2*coord_x_box[i]/img_w - 1
                y = 2*coord_y_box[i]/img_h - 1

                x1 = x*math.sqrt(1 - y**2/2);
                y1 = y*math.sqrt(1 - x**2/2);

                r = math.sqrt(x1**2 + y1**2);

                x2 = x1*math.exp(-r**2/n); 
                y2 = y1*math.exp(-r**2/n);

                xf = img_w*(x2+1)/2;
                yf = img_h*(y2+1)/2;

                coord_x_new_box.append(xf)
                coord_y_new_box.append(yf)
                
            #new coordinates of standard axis-aligned bbox
            xtl_new = min(coord_x_new_box)
            ytl_new = min(coord_y_new_box)

            xbr_new = max(coord_x_new_box)
            ybr_new = max(coord_y_new_box)
            
            if (img_w<img_h):  
                w_new = xbr_new - xtl_new
                h_new = (ybr_new - ytl_new)*scaling_new
                
            else:    #img_w>img_h, img_w==img_h   
                w_new = (xbr_new - xtl_new)*scaling_new
                h_new = ybr_new - ytl_new
            
            #find center points           
            if (img_w<img_h):
                x_centre = (xtl_new + xbr_new)/2 - (int(0.11*img_w)-2)
                y_centre = (ytl_new + ybr_new)/2*scaling_new - (int(0.11*int(img_w*scaling_factor))-2)
                
            else:    #img_w>img_h, img_w==img_h
                x_centre = (xtl_new + xbr_new)/2*scaling_new - (int(0.11*int(img_h*scaling_factor))-2)
                y_centre = (ytl_new + ybr_new)/2 - (int(0.11*img_h)-2)
        
            #normalization
            x_centre = x_centre / w_transf
            y_centre = y_centre / h_transf
            w_new = w_new / w_transf
            h_new = h_new / h_transf

            #limit upto six number of decimal places
            x_centre = format(x_centre, '.6f')
            y_centre = format(y_centre, '.6f')
            w_new = format(w_new, '.6f')
            h_new = format(h_new, '.6f')

            #write annotation to the file in the yolo format 
            file_with_annotations.write(f"{current_category} {x_centre} {y_centre} {w_new} {h_new}\n")
            
        file_with_annotations.close()
    count += 1
    print(f"{output_path}{filename[:-4]}_4.txt" + " " + str(count))
    
end = time.time()
time_needed = (end - start)/60
print(time_needed)
