## Goal

In this competition our task was to find the best way possible to form recommendations for the customers of Amazon store, because better recommendations may easily lead to sales increase and more profit for the company. 

To reach this goal we should:
1. Carefully study the data.
2. Play with the provided baseline model and try to improve it. 
3. Study the subject and investigate, what other models could be used according to our task and data.
4. Check the performance of other models.
5. Compare the results, make conclusions and choose the model for the final solution.

## Data

- ```train data```

consists of: overall product rating, user id, user name, time of review (standard and unix), review verification status, review summary, review text, number of votes on review usefullness, product id, product code, product style, product image, product rating from a particular user.

-```test data```

consists of: user id, user name, time of review (standard and unix), review verification status, number of votes on review usefullness, product id, product code, product style, product image.

-```metadata```

## Results

In this rather challenging project our team tried several different approaches, including SVD matrix factorization with Surprise, custom and ready to use deep-learning models. Unfortunately, none of them performed better than a baseline LightFM model with some improvements.
And still there is much to learn on the subject.

Prototype: https://lit-escarpment-44576.herokuapp.com/



**View on Kaggle:** 

Competition: https://www.kaggle.com/c/recommendationsv4/overview

Member: Alice C.
