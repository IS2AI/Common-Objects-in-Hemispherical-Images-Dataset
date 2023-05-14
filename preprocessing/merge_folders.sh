#This script was used to merge images and labels for the MS COCO and FisheyeCOCO datasets

for file in fisheye_coco/images/train2017_transformed/*.jpg; do cp "$file" coco_original/images/train2017; done

for file in fisheye_coco/labels/train2017_transformed/*.txt; do cp "$file" fisheye_coco/labels/train2017; done

cp fisheye_coco/images/val2017_transformed/*.jpg coco_original/images/val2017

cp fisheye_coco/labels/val2017_transformed/*.txt coco_original/labels/val2017