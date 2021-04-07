[deal with imbalance data](https://towardsdatascience.com/methods-for-dealing-with-imbalanced-data-5b761be45a18)
# How to deal with imbalance data

1. Change the performance metric : 
    * [note for recall / precision / F1Score](../DSConcept/recall_precision.md)
    * MCC: correlation coefficient between the observed and predicted binary classifications.
    * AUC: relation between true-positive rate and false positive rate.
2. use different method: decision tree for example is good for imbalance data
3. Resample: 
    * undersampleing: more majority removing data points
    * oversampleing: add more sample by copying, important to do it after 
spliting, good when we don't have many data points
    * SMOTE: similar to over sampleing uses a nearest neighbors algorithm to generate new 
    and synthetic data we can use for training our model. (not real data)
4. Parameters giving the weight of the classification data.
5. Use K-fold Cross-Validation


