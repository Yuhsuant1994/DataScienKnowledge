[What is the difference between CART and boosting]

VS RandomForest

VS different boosting method



CART is Classification and Regression Trees where the dataset is 
split into number of trees depending on the criteria of splitting. 
These criteria are:- Gini, Entropy and Variance. The splitting is done till the terminal node of the tree is reached/created. The limit to which the trees must be created is explicitly given by the model. It is used for predicting classification variables or regression(or continuous variables).

Boosted Regression Trees is using regression trees while following boosting algorithm. In Boosting, trees are built iteratively using regression trees and it converts weak learners into a strong learner. The main difference is that it takes the predictive error of the previous tree and use the residual as the dependent variable and then creates the tree and again determine the residual. The final outcome is the weighted value of each tree and classifier; the weightage is dependent on the accuracy.

[Decision Tree vs Random Forest vs Gradient Boosting Machines](https://www.datasciencecentral.com/profiles/blogs/decision-tree-vs-random-forest-vs-boosted-trees-explained)
[CatBoost vs. Light GBM vs. XGBoost](https://towardsdatascience.com/catboost-vs-light-gbm-vs-xgboost-5f93620723db)
# 1. CART

Classification and Regression Tree 


## 1.1 Find best split

how do we select the right feature to split for that node? **find best split**

`criterion`: This parameter is the function used to measure the quality of a split 
and it allows users to choose between `gini` or `entropy`.
[(ref: Decision Trees: Gini vs Entropy)](https://quantdare.com/decision-trees-gini-vs-entropy/)
overall speaking, gini is faster while entropy is more complex might have
better result.

* **gini impurity**: 
 
how diverse is this dataset. (the frequency at which 
any element of the dataset will be mislabelled when it is randomly labeled.)
(we can also see it as the prob that randomly pick 2 element from the data 
set the elements are different)
the optimum split is chosen by the features with less Gini Index

[simple video explain gini impurity](https://www.youtube.com/watch?v=u4IxOk2ijSs)

* **Entropy**: 

compute the entropy value for each node and sum them all up.
in the node level we only know if this split is pure or not
range between 0 to 1 (0 it's pure, 1 is worse that it is half/half label)

[Single node entropy video explanation](https://www.youtube.com/watch?v=1IQOtJ4NI_0)
[information gain](https://www.youtube.com/watch?v=FuTRucXB9rA)

then we compute the **information gain**
`Gain(S,A)=E(S)-SUM((|Sv|/|S|)*E(Sv)) `
we can see it as the Entropy of the node minus the sum of the 
Entropy subnode (percentage weighted), therefore the higher of the entropy the better.


[continue with the video](https://www.youtube.com/watch?v=5aIFgrrTqOw&list=PLZoTAELRMXVPBTrWtJkn3wWQxZkmTXGwe&index=52)

