# Recommender-System-Algorithms
Various collaborative filtring algorithms evaluated using RMSE. The algorithms impleamented include:
1. User-User CF with Pearson correlation to calculate similarity.
2. User-User CF with Cosine similarity to calculate similarity.
3. User-User CF biased, taking into account the baseline when predicting ratings.
4. Item-Item Slope One algorithm.

All files have a main method which allows you to choose the dataset along with the test data metrix. Furthermore, in the computeNearestNeighbor functions, the end variable cnt2 allows the tester to change the nearest K-Neighbors. Altering the test data used, and the K-nearest neighbors for the UserUser  provides different values.  
