# uplift modeling

[Uplift modelling](https://en.wikipedia.org/wiki/Uplift_modelling),
 also known as incremental modelling, true lift modelling, 
or net modelling is a predictive modelling technique that directly models 
the incremental impact of a treatment (such as a direct marketing action) on an 
individual's behaviour.

It is commonly seen for marketing / sales related modeling. When the input 
variable and target variable. for example because they buy more we predict 
they will buy more and tell sales to follow up, while sales following up
/ or already did might be the reason they buy more. Then we cannot really 
say thanks to our prediction, customer buy more.

## who are we targeting?

![seg](img/uplift_seg.png)
![matrix](img/uplift_targ.png)

*conceptional 2x2 Matrix (Kane, et al., 2014)*

We are targeting **maximize targeting "persuadable"** group 

for "lost cause" / "sure thing" seems no effect on treatment so why not target as well? 
(just minimize the "do not disturb"). we need to see the use case, some b2b use case
do not disturb can be ignore already.

Depending on the treatment we can have different explanation
* **Emailing**: barely cost. However if we also targeting "lost cause" / "sure thing" it is 
hare to accurately track the model performance in the future (real revenue margin it provide).
Moreover, it only said they the purchase behavior would not change, it didn't mean they
would not be bombarded by the email and unsubscrib it or put it to spam. (here we can argue that
in this case it is already sleeping dog)
* **Lead treating**: telling sales to treat the leads might lead to they are not confidence in
our model. Or waste many humain resources.

## calculation 

uplift of conversion rate = conversion rate if treated / conversion rate if not treated

we want to maximize uplift (check Qini curve so call AUUC)

**CALCULATION ISSUE**

There exist calculation issue. Due to per customer we only have either treated or non-treated
real value. That is we never able to calculate the true value of uplift. but we can find
way to treat the bias and make a more reasonable estimation / assumption.

## implementation

python CausalML / Pylift



# reference

* Gutierrez, Pierre. and G´erardy, Jean-Yves. Causal inference and uplift modelling: A review of the literature. In International Conference on Predictive Applications and APIs, pages 1-13, 2017
* [uplifted blog](https://humboldt-wi.github.io/blog/research/theses/uplift_modeling_blogpost/)

