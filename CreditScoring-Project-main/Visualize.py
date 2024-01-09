#!/usr/bin/env python
# coding: utf-8

# Import libraries
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import metrics
import streamlit as st

def confusion_matrix(cf, group_labels, categories):
    
    '''
    This function will make a pretty plot of an sklearn Confusion Matrix cm using a Seaborn heatmap visualization.
    
    '''
    group_counts = ['{0:0.0f}'.format(value) for value in
                    cf.flatten()]
    box_labels = [f"{v1}\n\n{v2}" for v1, v2 in zip(group_labels,group_counts)]
    box_labels = np.asarray(box_labels).reshape(2,2)

    fig = plt.figure(figsize=(15,6))
    ax = sns.heatmap(cf, annot=box_labels, cmap='Blues', fmt='')

    ax.set_title('Confusion Matrix with labels\n');
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values ');

    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(categories)
    ax.yaxis.set_ticklabels(categories)

    ## Display the visualization of the Confusion Matrix.
    st.pyplot(fig)
    

def roc_curve(model, x, y):
    
    ''' This function will generate roc curve to explain the performance of classifier '''
    
    fig = plt.figure(figsize=(15,5))
    y_pred_proba = model.predict_proba(x)[::,1]
    fpr, tpr, _ = metrics.roc_curve(y,  y_pred_proba)
    auc = metrics.roc_auc_score(y, y_pred_proba)
    plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
    plt.title('ROC curve plots TPR vs. FPR')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc=4)
    st.pyplot(fig)