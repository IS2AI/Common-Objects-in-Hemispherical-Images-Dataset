# Common-Objects-in-Hemispherical-Images-Dataset
Common Objects in Hemispherical Images (COHI) is a benchmark testing dataset for object detection in hemispherical/fisheye cameras. It contains 1,000 real fisheye images of 39 classes sampled from the MS COCO dataset with 14.2 object instances per image. The images were captured using a hemispherical camera ELP-USB8MP02G-L180 with the 2,448 by 3,264 pixel resolution and manually annotated with standard axis-aligned bounding boxes afterward. The samples of raw and annotated images from the COHI dataset are shown below.

<img src="https://github.com/IS2AI/Common-Objects-in-Hemispherical-Images-Dataset/blob/main/figures/COHI_samples.PNG" width="750">

The names of sampled classes and the number of bounding boxes for each class are presented in the next figure.

<img src="https://github.com/IS2AI/Common-Objects-in-Hemispherical-Images-Dataset/blob/main/figures/class_distribution.png" width="500">

## The FisheyeCOCO dataset
To train object detection models for the COHI dataset, the FisheyeCOCO dataset was generated by applying a non-linear mapping to the MS COCO dataset to obtain fisheye-looking images. The samples of raw and annotated images from the FisheyeCOCO dataset are illustrated below.

<img src="https://github.com/IS2AI/Common-Objects-in-Hemispherical-Images-Dataset/blob/main/figures/FisheyeCOCO_samples.PNG" width="750">

## Requirements
### For data preprocessing
* numpy
* PIL
* pandas

### For object detection
We used YOLOv7 to train and evaluate object detection models. All needed information can be found on their official GitHub page 
[YOLOv7](https://github.com/WongKinYiu/yolov7). 

## Pre-trained models
We trained the YOLOv7 model with 36.9 M parameters on three datasets and evaluated the performance of models with our benchmark testing dataset - COHI.

- **YOLOv7_original**: trained on the MS COCO dataset
- **YOLOv7_transformed**: trained on the FisheyeCOCO dataset
- **YOLOv7_combuned**: trained on the combination of the MS COCO and FisheyeCOCO datasets

mAP<sub>50</sub> results are summarized in the table below.

| Model | mAP<sub>50</sub> |
| :-- | :-: |
| YOLOv7_original | 58.23% |
| YOLOv7_transformed | 58.28% |
| YOLOv7_combined | 60.77% |


