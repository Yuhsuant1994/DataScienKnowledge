<img src="https://miro.medium.com/max/945/1*pOtBHai4jFd-ujaNXPilRg.png" height="300">
<img src="https://miro.medium.com/max/540/1*DIhRgfwTcxnXJuKr2_cRvA.png" height="150">

which one to focus on depending on what's the cost of false positive and
false negative.

* **Precision**: out of all the predicted positive how many of them is predicted true positive, 
we improve precision meaning reduce false positive. (we don't want when we predict it's positive it's not) we don't want to predict positive when it's actually not. like in the pharmacie, medication sector.
* **Recall**: out of all the real positive how many of them is predicted true positive.
when we improve recall we try to reduce false negative (we don't want when we predict it's negative it's actually not) like in the fraud project.
* **F1 Score**: the weighted average of precision and recall. (take both matric into consideration)


Precision is a good measure to determine when the cost of false positives is high. E.g. — email spam detection. Recall- When there is a high cost associated with false negatives. E.g. — fraud detection or sick patient detection.


[ref: Precision vs Recall](https://medium.com/@shrutisaxena0617/precision-vs-recall-386cf9f89488)
