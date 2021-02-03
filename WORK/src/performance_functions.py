import os
import sys
import numpy as np
import pandas as pd
from collections import defaultdict
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score, roc_curve, auc, classification_report
import shap


def model_performance(y_true, y_preds, artifact_path, artifact_ext, threshold, show_plots = False):
    matplotlib.rc_file_defaults()
    y_preds_bin = np.where(y_preds > threshold, 1, 0)
    
    
    #ROC Curve
    plt.clf()
    plt.close()
    plt.figure()
    false_positive_rate, recall, thresholds = roc_curve(y_true, y_preds)
    roc_auc = auc(false_positive_rate, recall)
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.plot(false_positive_rate, recall, 'b', label = 'AUC = %0.3f' %roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0,1], [0,1], 'r--')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.0])
    plt.ylabel('Recall')
    plt.xlabel('Fall-out (1-Specificity)')
    plt.savefig(os.path.join(artifact_path, f'roc_curve_{artifact_ext}.png'), bbox_inches = "tight")
    
    if show_plots:
        plt.show()

    print('auc score:', roc_auc)
    
    #Classification Report
    print(classification_report(y_true, y_preds_bin))
    
    #Confusion Matrix 
    plt.clf()
    plt.close()
    plt.figure()
    cm = confusion_matrix(y_true, y_preds_bin)
    labels = ['0', '1']
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, xticklabels = labels, yticklabels = labels, annot = True, fmt='d', cmap="Blues", vmin = 0.2);
    plt.title('Confusion Matrix')
    plt.ylabel('True Class')
    plt.xlabel('Predicted Class')
    plt.savefig(os.path.join(artifact_path, f'confusion_matrix_{artifact_ext}.png'), bbox_inches = "tight")
    
    if show_plots:
        plt.show()
    
    #Probability Histogram
    plt.clf()
    prob_hist = pd.Series(y_preds).hist(cumulative=True, bins=20)
    fig = prob_hist.get_figure().savefig(os.path.join(artifact_path, f'hist_plot_{artifact_ext}.png'), bbox_inches = "tight")
    
    return classification_report(y_true, y_preds_bin,output_dict = True)

##still need to test it...
#def feature_importance():
#    shap_values = shap.TreeExplainer(bst).shap_values(X_val)
#    shap.summary_plot(shap_values[1], X_val)