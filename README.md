# CeyMo Road Marking Dataset

![image_grid](https://github.com/oshadajay/CeyMo/blob/main/figures/image_grid.png)

## Overview

CeyMo is a novel benchmark dataset for road marking detection which covers a wide variety of challenging urban, sub-urban and rural road scenarios. 
The dataset consists of 2887 total images of 1920 &times; 1080 resolution with 4706 road marking instances belonging to 11 classes. 
The test set is divided into six categories: normal, crowded, dazzle light, night, rain and shadow.

For more details, please refer to our paper [CeyMo: See More on Roads - A Novel Benchmark Dataset for Road Marking Detection](https://openaccess.thecvf.com/content/WACV2022/papers/Jayasinghe_CeyMo_See_More_on_Roads_-_A_Novel_Benchmark_Dataset_WACV_2022_paper.pdf).

## Download

The train set, the test set and a sample of the CeyMo road marking dataset can be downloaded from the following Google Drive links.
* [Train Set](https://drive.google.com/file/d/1-TDEfGXtEQ4s037M_ynmV6aiOfNp2NZv/) - 2099 images (1.17 GB)
* [Test Set](https://drive.google.com/file/d/1YhWld3kxR5Ahz4Q-hy61UKI0KN_so9fa/) - 788 images (442 MB)
* [Sample](https://drive.google.com/file/d/1XSHT6v3PNA8Z38F542OGWTTosfQtEcFr/) - 10 images (5 MB)

A set of raw video clips recorded from the two cameras can be downloaded from [here](https://drive.google.com/drive/folders/1cjlMDGeM4twNo33959_urmiL3gKx36jC?) as unlabeled data.

## Annotations

The road marking annotations are provided in three formats: polygons, bounding boxes and pixel-level segmentation masks.
The polygon annotations in JSON format are considered as the ground truth and bounding box annotations in XML format and segmentation masks in PNG format are provided as additional annotations. 
The camera and the vehicle used for capturing each image, and the category (only for test images) are also annotated. 

![annotation_formats](https://github.com/oshadajay/CeyMo/blob/main/figures/annotation_formats.png)

[Labelme](https://github.com/wkentaro/labelme) can be used to visualize the polygon annotations (Images and JSON files should be copied to the same folder) and [LabelImg](https://github.com/tzutalin/labelImg) can be used to visualize the bounding box annotations (Images and XML files should be copied to the same folder).
The segmentation masks have the following color mapping for the 11 classes in the dataset. Colors are given as RGB color codes.

| Road Marking Class             |  Color Code  |
|--------------------------------|---------------|
| Bus Lane (BL)	                 | (0,255,255)   |
| Cycle Lane (CL)                | (0,128,255)   |
| Diamond (DM)                   | (178,102,255) |
| Junction Box (JB)              | (255,255,51) |
| Left Arrow (LA)                | (255,102,178) |
| Pedestrian Crossing (PC)	     | (255,255,0)   |
| Right Arrow (RA)               | (255,0,127)   |
| Straight Arrow (SA)	         | (255,0,255)   |
| Slow (SL)	                     | (0,255,0)     |
| Straight-Left Arrow (SLA)	     | (255,128,0)   |
| Straight-Right Arrow (SRA)	 | (255,0,0)     |

## Statistics

The column graph (a) shows the frequency of each class in the dataset while the pie chart (b) shows the proportion of each scenario in the test set.

![dataset_statistics](https://github.com/oshadajay/CeyMo/blob/main/figures/dataset_statistics.png)

## Evaluation

The evaluation script requires the following dependencies to be installed with Python 3.

```bash
pip install argparse shapely tabulate
```

The class-wise, scenario-wise and overall results can be obtained by running the provided python script as follows. *<gt_dir>* should
contain the ground truth json files and *<pred_dir>* should contain the prediciton json files following the same format as per the ground truth.

```bash
python eval.py --gt_dir=<gt_dir> --pred_dir=<pred_dir>
```

## Results

The performance of the four baseline models trained and evaluated on our dataset are as follows.

|Model &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;  | SSD-MobileNet-v1 | SSD-Inception-v2 | Mask-RCNN-Inception-v2 | Mask-RCNN-ResNet50 |
|----------|:------------------:|:-----------------:|:----------------------:|:------------------:|
|Normal|86.57|87.10|93.20|**94.14**|
|Crowded |79.45|82.51|82.04|**85.78**|
|Dazzle light|84.97|85.90|86.06|**89.29**|
|Night|83.08|84.85|**92.59**|91.51|
|Rain|73.68|81.87|87.50|**89.08**|
|Shadow|85.25|86.53|85.60|**87.30**|
|Overall F1-Score|82.90|85.16|89.04|**90.62**|
|Macro F1-Score|80.93|82.88|85.75|**88.33**|
|Speed (FPS)|**83**|61|42|13|

## Citation

If you use our dataset in your work, please cite the following paper.
```
@InProceedings{Jayasinghe_2022_WACV,
    author    = {Jayasinghe, Oshada and Hemachandra, Sahan and Anhettigama, Damith and Kariyawasam, Shenali and Rodrigo, Ranga and Jayasekara, Peshala},
    title     = {CeyMo: See More on Roads - A Novel Benchmark Dataset for Road Marking Detection},
    booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
    month     = {January},
    year      = {2022},
    pages     = {3104-3113}
}
```


