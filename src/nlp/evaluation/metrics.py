import json
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from src.nlp.utils.io import read_json_datas

names = ['text', 'label', 'POS', 'LEN', 'WFOF', 'TI', 'TR']

def parse_tags(texts, preds, infer=False):
    keywords = []
    for text, pred in zip(texts, preds):
        if infer==False:
            text = text.split(' ')
        K_B_index = [i for i, tag in enumerate(pred) if (tag == 'B-KP' or tag == 'U-KP')]
        for index in K_B_index:
            if index == len(pred) - 1:
                keywords.append(text[index])
            else:
                temp = [text[index]]
                for i in range(index + 1, len(pred)):
                    if pred[i] == 'I-KP':
                        if i + 1 == len(pred):
                            temp.append(text[i])
                        elif pred[i+1] != 'O' and pred[i-1] != 'O':
                            temp.append(text[i])
                    elif pred[i] == 'B-KP' or pred[i] == 'O' or pred[i] == 'U-KP':
                        break
                keywords.append(" ".join(temp))
    return list(set(keywords))    

# Calculate the P, R and F1 values of the extraction datas
def evaluate(y_preds, y_targets):
    STP, STE, STA, NUM =  0.0, 0.0, 0.0, 0.0
    for index, y_pred in enumerate(y_preds):
        y_true = y_targets[index]
        NUM += len(y_true)
        TP = len(set(y_pred) & set(y_true))
        STP += TP
        STE += len(y_pred)
        STA += len(y_true)
    p = (STP / STE) if STE != 0 else 0
    r = (STP / STA) if STA != 0 else 0
    f1 = ((2 *  r * p) / (r + p)) if (r + p) != 0 else 0
    p = round(p * 100, 2)
    r = round(r * 100, 2)
    f1 = round(f1 * 100, 2)
    return p, r, f1, NUM

def calc_scores(TP,FN,FP,TN):
    accuracy = (TP+TN)/(TP+FN+FP+TN)
    misclassification = (FP+FN)/(TP+TN+FP+FN)
    precision = TP/(TP+FP) if (TP+FP) > 0 else 0
    sensitivity = TP/(TP+FN) if (TP+FN) > 0 else 0
    specificity = TN/(TN+FP) if (TN+FP) > 0 else 0
    f1score=(2 * precision * sensitivity) / (precision + sensitivity) if (precision + sensitivity) > 0 else 0
    print("""    Accuracy:\t{:5f}
    Misclassification:\t{:5f}
    Precision:\t{:5f}
    Sensitivity/Recall:\t{:5f}
    Specificity:\t{:5f}
    F1 Score:\t{:5f}""".format(accuracy,misclassification,precision, sensitivity,specificity,f1score))
    return (accuracy,misclassification,precision, sensitivity,specificity,f1score)

def get_metrics(text_arr, kws_arr, gs_arr, mappers=False):
    if mappers==False:
        test_mappers = []
        gs_mappers = []

        for idx,text in enumerate(text_arr):
            text_len = len(text)
            test_kws = [x.split() for x in kws_arr[idx]]
            gs_kws = [x.split() for x in gs_arr[idx]]
            test_mapper = [0]*text_len
            gs_mapper = [0]*text_len

            for kw in test_kws:
                kw_len = len(kw)
                i=0
                while i<text_len-kw_len:
                    if text[i:i+kw_len]==kw and test_mapper[i:i+kw_len]==[0]*kw_len:
                        test_mapper[i:i+kw_len]=[1]*kw_len
                    i+=1

            for kw in gs_kws:
                kw_len=len(kw)
                i=0
                while i<text_len-kw_len:
                    if text[i:i+kw_len]==kw and gs_mapper[i:i+kw_len]==[0]*kw_len:
                        gs_mapper[i:i+kw_len]=[1]*kw_len
                    i+=1 
            test_mappers.append(test_mapper)
            gs_mappers.append(gs_mapper)
    else:
        test_mappers=kws_arr
        gs_mappers=gs_arr
        
    TP, TN, FN, FP = 0, 0, 0, 0
    N = len(text_arr)
    i=0
    matrix = np.zeros(9).reshape(3,3)
    labels=['U-KP','B-KP','I-KP','L-KP','O']
    while i<N:
        matrix += confusion_matrix(gs_mappers[i],test_mappers[i], labels=labels)
        i+=1
    
    print("Confusion Matrix:\n", matrix)
    
    precision_arr = []
    f1score_arr = []
    specificity_arr = []
    sensitivity_arr = []
    accuracy_arr = []
    Total = np.sum(matrix[:,:])
    for i in range(3):
        TP = matrix[i,i]
        FN = np.sum(matrix[i,:]) - TP
        FP = np.sum(matrix[:,i]) - TP
        TN = Total - (FN + FP + TP)
        print("{}\nLabel: {}\nTP:{} FN:{} FP:{} TN:{}\n{}".format('-'*50,labels[i],TP,FN,FP,TN,'-'*50))
        result = calc_scores(TP, FN, FP, TN)   
        accuracy_arr.append(result[0])
        precision_arr.append(result[2])
        sensitivity_arr.append(result[3])
        specificity_arr.append(result[4])
        f1score_arr.append(result[5])
    
    print("=-"*50)
    print("Avg. Accuracy: {:.5f}\nAvg. Precision: {:5f}\nAvg. F1-Score: {:5f}\nAvg. Sensitivity: {:5f}\nAvg. Specificity: {:5f}".format(np.mean(accuracy_arr),np.mean(precision_arr),np.mean(f1score_arr),np.mean(sensitivity_arr),np.mean(specificity_arr)))
    print("=-"*50)

def performance_metrics(pred_tags, info_path):
    texts = pd.read_csv(info_path.replace("_info.json", ".txt"),
                        sep=' <sep> ', engine='python', names=names).text
    info = read_json_datas(info_path)
    target_keywords, pred_keywords = [], []
    for i in range(len(info)):
        key, item = tuple(tuple(info[i].items())[0])
        target_keyword = item[0]
        pred = pred_tags[item[1]: item[2]]
        text = texts[item[1]: item[2]].tolist()
        pred_keyword = parse_tags(text, pred)
        target_keywords.append(target_keyword)
        pred_keywords.append(pred_keyword)
    metrics = evaluate(pred_keywords, target_keywords)
    return metrics
