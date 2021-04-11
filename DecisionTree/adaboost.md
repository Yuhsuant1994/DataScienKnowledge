[statquot](https://www.youtube.com/watch?v=LsK-xG1cLYA)
[krish](https://www.youtube.com/watch?v=NLRO1-jp5F8)

random forest
Gradient Boost


Ensemble Learning, Bootstrap Aggregating (Bagging) and Boosting
https://www.youtube.com/watch?v=m-S9Hojj1as


- ensemble model avoid over fitting 

Overfitting is a topic
Ensemble model is another topic to see implementation

# Ensemble model

ensemble model is a combination of different ML models. (random forest is an ensemble 
model for decision tree)

[video concept](https://www.youtube.com/watch?v=m-S9Hojj1as), [Decision Tree Ensembles- Bagging and Boosting](https://towardsdatascience.com/decision-tree-ensembles-bagging-and-boosting-266a8ba60fd9)

* **Bagging (Bootstrap Aggregation)** is used when our goal is to reduce the variance of a 
decision tree. Here idea is to create several subsets of data from training sample chosen r
andomly **with replacement**. Now, each collection of subset data is used to train their 
decision trees. As a result, we end up with an ensemble of different models. 
**Average of all the predictions** from different trees are used which is more robust than 
a single decision tree.

(**Random Forest** is an extension over bagging. It takes one extra step where in addition 
to taking the random subset of data, it also takes the **random selection of features** rather 
than using all features to grow trees. When you have many random trees. It’s called Random Forest)

* **Boosting** is another ensemble technique to create a collection of predictors. we fit consecutive trees (random sample) and at every 
step, the goal is to solve for net error from the prior tree. we randomly choose the first bag as 
bagging but second bag we would keep all the wronly predicted data point from the first bag and 
then the rest randomly take from the training data set etc... this teach the model where the point 
usually go wrong. tend to over fit and increase the variance.