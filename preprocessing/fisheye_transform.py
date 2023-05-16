#import libraries
import os
from PIL import Image
import math
import numpy as np
import time

def fisheye_transform(filename, file_path, output_dir, n, scaling_factor):
    
    image_orig = Image.open(file_path)      
    h = image_orig.size[1]
    w = image_orig.size[0]   
    
    #resize to have the same aspect ration as images from COHI and reduce image quality degradation after non-linear mapping
    if (w<h):
        image_resized = image_orig.resize((4*w, 4*int(w*scaling_factor)), Image.BICUBIC);     
    else: #w>h w==h
        image_resized = image_orig.resize((4*int(h*scaling_factor), 4*h), Image.BICUBIC);

           
    num_rows = image_resized.size[1]
    num_cols = image_resized.size[0]  
    I = np.asarray(image_resized)

    
    #non-linear fisheye transformations            
    if image_resized.mode == "RGB":    #RGB
        I_new = np.zeros([num_rows, num_cols, 3])

        for i in range(num_rows):
            for j in range(num_cols):
                #normalize between -1 and +1
                x = 2*i/num_rows - 1   
                y = 2*j/num_cols - 1

                x1 = x*math.sqrt(1 - y**2/2)
                y1 = y*math.sqrt(1 - x**2/2)

                r = math.sqrt(x1**2 + y1**2)

                x2 = x1*math.exp(-r**2/n)
                y2 = y1*math.exp(-r**2/n)

                xf = int(num_rows*(x2+1)/2)
                yf = int(num_cols*(y2+1)/2)

                I_new[xf, yf,:] = I[i, j,:]
    
    else:    #grayscale ('L')
        I_new = np.zeros([num_rows, num_cols])

        for i in range(num_rows):
            for j in range(num_cols):
                #normalize between -1 and +1
                x = 2*i/num_rows - 1
                y = 2*j/num_cols - 1

                x1 = x*math.sqrt(1 - y**2/2)
                y1 = y*math.sqrt(1 - x**2/2)

                r = math.sqrt(x1**2 + y1**2)

                x2 = x1*math.exp(-r**2/n)
                y2 = y1*math.exp(-r**2/n)

                xf = int(num_rows*(x2+1)/2)
                yf = int(num_cols*(y2+1)/2)

                I_new[xf, yf] = I[i, j]
                
    I_new = np.uint8(I_new)
    image_transformed = Image.fromarray(I_new)
    
    #crop black borders
    #use 0.11 if n = 4, 0.141 if n = 3, 0.091 if n = 5
    image_cropped = image_transformed.crop([int(0.11*num_cols)-2, int(0.11*num_rows)-2, num_cols-int(0.11*num_cols)+2, num_rows-int(0.11*num_rows)+2])
    image_cropped.save(output_dir + filename[:-4] + '_4.jpg')    #because n = 4
                          

a = 3264;
b = 2448;
scaling_factor = a/b;    #aspect ratio of images in COHI

directory = 'val2017'    #the same script can be used for 'train2017'
start = time.time()
count = 1

for filename in os.listdir(directory):

    file_path = os.path.join(directory, filename)
    print(file_path + " " + str(count))
    count = count+1
    fisheye_transform(filename, file_path, 'val2017_transformed/', 4, scaling_factor)

end = time.time()
timer = (end - start)/60
print(timer)
