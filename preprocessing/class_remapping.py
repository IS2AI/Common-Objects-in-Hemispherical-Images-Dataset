#This script was used to remap class IDs assigned by Roboflow to the COHI dataset to coco80 convention
#For example, Roboflow assigned '0' class ID to 'apple' while it has '47' class ID in coco80

#import libraries
import pandas as pd
import time
import os

new_dataset = [*range(0, 39, 1)]
coco_dataset = [47, 24, 46, 13, 73, 39, 45, 2, 51, 67, 56, 74, 57, 41, 60, 42, 26, 66, 43, 63, 68, 64, 49, 69, 58, 72, 65, 76, 71, 44, 11, 28, 77, 27, 79, 62, 25, 75, 40]

def class_remapping(filename, directory):
    file = pd.read_csv(directory + "/" + filename, sep = " ", names = ['class_id', 'x', 'y', 'w', 'h'], index_col = False)
    
    for i in range (len(file)):
        for j in range (len(new_dataset)):
            if file.loc[i, 'class_id'] == new_dataset[j]:
                file.loc[i, 'class_id'] = coco_dataset[j]
                break
            
    cols = ['x', 'y', 'w', 'h']
    #round to six decimal places
    file[cols] = file[cols].round(6) 
    file.to_csv("output/" + filename, header = None, index = False, sep = " ")    #save to 'output' directory


directory = 'roboflow/labels'    #directory with original labels
start = time.time()
count = 1

for filename in os.listdir(directory):
    f = os.path.join(directory, filename) 
    print(f + " " + str(count))
    count = count+1
    class_remapping(filename, directory)
end = time.time()

time = (end - start)/60
print(time)
