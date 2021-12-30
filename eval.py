'''
Evaluation script for the CeyMo Road Marking Dataset

gt_dir should contain the ground truth json files and pred_dir should contain prediction json files respectively.
The file system should follow the following order.
home_directory/
|___ gt_dir/
|      |___001.json
|      |___002.json
|      |___ ....
|___ pred_dir/
       |___001.json
       |___002.json
       |___ ....
'''

from shapely.geometry import Polygon
from tabulate import tabulate
from os import listdir

import json
import argparse

class_dict = {'SA':0, 'LA':0, 'RA':0, 'SLA':0, 'SRA':0, 'DM':0, 'PC':0, 'JB':0, 'SL':0, 'BL':0, 'CL':0}
scene_dict = {'normal':0, 'crowded':0, 'dazzle light':0, 'night':0, 'rain':0, 'shadow':0}

def get_IoU(pol_1, pol_2):

    # Define each polygon
    polygon1_shape = Polygon(pol_1)
    polygon2_shape = Polygon(pol_2)

    if ~(polygon1_shape.is_valid):polygon1_shape = polygon1_shape.buffer(0)
    if ~(polygon2_shape.is_valid):polygon2_shape = polygon2_shape.buffer(0)

    # Calculate intersection and union, and return IoU
    polygon_intersection    = polygon1_shape.intersection(polygon2_shape).area
    polygon_union           = polygon1_shape.area + polygon2_shape.area - polygon_intersection

    return polygon_intersection / polygon_union

def match_gt_with_pred(gt_polygons, pred_polygons, iou_threshold):

    candidate_dict_gt  = {}  
    assigned_predictions = []

    # Iterate over ground truth
    for idx_gt, gt_itm in enumerate(gt_polygons):
        pts_gt       = gt_itm['points']
        label_gt     = gt_itm['label']
        gt_candidate = {'label_pred':None, 'iou':0}
        assigned_prediction = None

        # Iterate over predictions
        for idx_pred, pred_itm in enumerate(pred_polygons):
            pts_pred   = pred_itm['points']
            label_pred = pred_itm['label']
            iou        = get_IoU(pts_pred, pts_gt)
            
            # Match gt with predicitons
            if (iou > iou_threshold) and (gt_candidate['iou'] < iou) and (label_gt == label_pred) and str(idx_pred) not in assigned_predictions:
                gt_candidate['label_pred'] = label_pred + '*' + str(idx_pred)
                gt_candidate['iou']        = iou
                assigned_prediction        = str(idx_pred)
    
        if assigned_prediction is not None:
            assigned_predictions.append(assigned_prediction)

        candidate_dict_gt[label_gt + '*' + str(idx_gt)] = gt_candidate
    
    return candidate_dict_gt

def eval_detections(gt_dir, pred_dir, iou_threshold = 0.3):

    gt_json_count   = len([f for f in listdir(gt_dir) if f.endswith('.json')])
    pred_json_count = len([f for f in listdir(pred_dir) if f.endswith('.json')])
    
    assert gt_json_count == pred_json_count, "Ground truth json file count does not match with prediction json file count"

    print("Evaluating road marking detection performance on " + str(gt_json_count) + " files")
    print()

    classwise_results    = [['Class', 'Precision', 'Recall', 'F1_Score']]
    scenariowise_results = [['Category', 'Precision', 'Recall', 'F1_Score']]

    filenames = [f for f in listdir(gt_dir) if f.endswith('.json')]

    sigma_tp = 0
    sigma_fp = 0
    sigma_fn = 0

    tp_class_dict   = class_dict.copy()
    gt_class_dict   = class_dict.copy()
    pred_class_dict = class_dict.copy()

    tp_scenario_dict   = scene_dict.copy()
    gt_scenario_dict   = scene_dict.copy()
    pred_scenario_dict = scene_dict.copy()

    # Iterate over each file
    for file in filenames:

        # Load ground truth json file
        gt      = open(gt_dir + '/' + file) 
        gt_json = json.load(gt) 
        gt.close()

        # Load pred json file
        pred      = open(pred_dir + '/' + file) 
        pred_json = json.load(pred) 
        pred.close()

        gt_polygons   = gt_json['shapes']
        pred_polygons = pred_json['shapes']

        scenario = gt_json['category']

        for polygon in gt_polygons:
            gt_class_dict[polygon['label']]  += 1
            gt_scenario_dict[scenario] += 1

        for polygon in pred_polygons:
            pred_class_dict[polygon['label']]  += 1
            pred_scenario_dict[scenario] += 1

        tp_gt = 0

        candidate_dict_gt = match_gt_with_pred(gt_polygons, pred_polygons, iou_threshold)

        for idx, lab in enumerate(candidate_dict_gt):
            label    = lab.split('*')[0]
            pred_lab = candidate_dict_gt[lab]['label_pred']

            if pred_lab != None:
                tp_gt                      += 1
                tp_class_dict[label]       += 1
                tp_scenario_dict[scenario] += 1

        tp = tp_gt
        fp = len(pred_polygons) - tp
        fn = len(gt_polygons) - tp

        sigma_tp += tp
        sigma_fp += fp
        sigma_fn += fn

    # Calculate precision, recall and F1 for the whole dataset
    if (sigma_tp + sigma_fp) != 0:
        precision = sigma_tp / (sigma_tp + sigma_fp)
    else:
        precision = 0

    if (sigma_tp + sigma_fn) != 0:
        recall = sigma_tp / (sigma_tp + sigma_fn)
    else:
        recall = 0

    if (precision + recall) != 0:
        F1_score = (2 * precision * recall) / (precision + recall)
    else:
        F1_score = 0

    class_F1_scores_list = []

    # Calculate class-wise performance metrics
    for label in tp_class_dict:
        l_tp = tp_class_dict[label]
        l_fp = pred_class_dict[label] - l_tp
        l_fn = gt_class_dict[label] - l_tp

        if (l_tp + l_fp) != 0:
            l_precision = l_tp / (l_tp + l_fp)
        else:
            l_precision = 0

        if (l_tp + l_fn) != 0:
            l_recall = l_tp / (l_tp + l_fn)
        else:
            l_recall = 0

        if (l_precision + l_recall) != 0:
            l_F1_score = (2 * l_precision * l_recall) / (l_precision + l_recall)
        else:
            l_F1_score = 0

        classwise_results.append([label, round(l_precision, 4), round(l_recall, 4), round(l_F1_score, 4)])

        class_F1_scores_list.append(l_F1_score) 

    # Calculate scenario-wise performance metrics
    for scene in tp_scenario_dict:
        s_tp = tp_scenario_dict[scene]
        s_fp = pred_scenario_dict[scene] - s_tp
        s_fn = gt_scenario_dict[scene] - s_tp

        if (s_tp + s_fp) != 0:
            s_precision = s_tp / (s_tp + s_fp)
        else:
            s_precision = 0

        if (s_tp + s_fn) != 0:
            s_recall = s_tp / (s_tp + s_fn)
        else:
            s_recall = 0

        if (s_precision + s_recall) != 0:
            s_F1_score = (2 * s_precision * s_recall) / (s_precision + s_recall)
        else:
            s_F1_score = 0

        scenariowise_results.append([scene, round(s_precision, 4), round(s_recall, 4), round(s_F1_score, 4)])

    macro_F1_score = sum(class_F1_scores_list) / len(class_F1_scores_list)

    print('Class-wise road marking detection results')
    print(tabulate(classwise_results, headers='firstrow', tablefmt='grid'))
    print()

    print('Scenario-wise road marking detection results')
    print(tabulate(scenariowise_results, headers='firstrow', tablefmt='grid'))
    print()

    print("Overall Precision : " + str(round(precision, 4)))
    print("Overall Recall    : " + str(round(recall, 4)))
    print("Overall F1-Score  : " + str(round(F1_score, 4)))
    print("Macro F1-Score    : " + str(round(macro_F1_score, 4)))

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gt_dir', type = str, help = 'Filepath containing ground truth json files')
    parser.add_argument('--pred_dir', type = str, help = 'Filepath containing prediction json files')
    parser.add_argument('--iou_threshold', type = float, default = 0.3, help = 'IoU threshold to count a prediction as a true positive')
    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = parse_opt()
    eval_detections(opt.gt_dir, opt.pred_dir, opt.iou_threshold)