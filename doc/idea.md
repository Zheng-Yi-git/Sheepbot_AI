# Ideas for Assignment 3

## Sheepdog Bot 1

1. The easiest states to determine $T^∗(state)$ is those states where the sheep is already at the center node and the sheepdog is not at the center node.

2. For any other given state state, express a formula for $T^∗(state)$ in terms of

## Sheepdog Bot 2

## Sheepdog Bot 3

This bot utilizes the idea of machine learning. Since we have created and stored a large amount of data, we can solve this problem from a statistical perspective. We can use the data to train a model that can predict the next move of the sheepdog.

1.  1. Input space: the state of the game, which is a tuple of the positions of the sheep and the sheepdog.

    2. Output space: the next move of the sheepdog, which is the direction of the sheepdog's movement.

    3. Model space: a function that maps the input space to the output space. In particular, we can model this problem as a classification problem, and therefore we may choose tree-based classifiers, such as decision tree, random forest, and gradient boosting.

2.  To assess whether the model suffers from overfitting, we can use cross-validation. In particular, we can use k-fold cross-validation, where we split the data into k subsets, and use one subset as the testing set and the rest as the training set. We can repeat this process k times, and then average the results to get a more accurate estimate of the model's performance. Overfitting of course is an issue, but we can use regularization to prevent overfitting. For example, we can use the L2 regularization, which adds a penalty term to the loss function, to prevent the model from overfitting.

3.  Still in progress, should wait for the simulation results.
