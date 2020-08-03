# kaBLOOM


The following is a general description of what each notebook file does and the order in which to run them.


1. get_data.ipynb

This file contains the code to download satellite data from the Sentinel Hub. For this project I looked at three areas: Antelope Valley, Grass Mountain, and Lake Elsinore, and I got all available data for these areas for March and April of 2017-2020.

1a. eda_antelope.ipynb, eda_elsinore.ipynb, eda_grassmtn.ipynb

Exploratory data analysis - these files visualize the recreated true color satellite images for all of the dates with satellite data available in March and April of 2019.


2. label_initial.ipynb

Here I hand label a small subset of seed pixels as either poppy or not poppy. I chose the poppy pixels from one image per region taken during a bloom, and I chose the non-poppy pixels randomly from one image per region taken before the bloom started.

2a. model_exploration.ipynb

In this notebook I explore and compare the results from 5 different binary classifiers (logistic regression, random forest, naive bayes, stochastic gradient descent, and gradient boosting). In the end I chose to go with the random forest because it performed the best out of the box and generalized the best to unseen data.


3. fit_evaluate_update.ipynb

Here is where the active learning takes place. I import the labelled pixels (either from iteration0 labelled in step 2 above, or from a previous iteration of this file), then fit and evaluate a classifier. Then I either exit the active learning loop and save the classifier (if the evaluation reveals that the model is good enough), or I add a small number of corrected hand labelled pixels to the pool of labelled pixels and move on to another iteration (if the evaluation reveals that the model is still making mistakes).


4. predict_blooms.ipynb

After creating a satisfactory model above, I move on to classify all the pixels in all of the images that I have and save the predictions.


5. get_areas.ipynb

Here I process the classification matrices from step 4 and segment them into poppy bloom areas (also called patches). I also get the centroids of each area.


6. process_areas.ipynb

Here I get information from the poppy bloom areas from step 5 (like number of patches and size of each patch) and prepare the info for the app. 


7. get_lat_long.ipynb

Here I get the latitude and longitude for the centroid of every patch identified in step 5.


At this point I have what I need to run the app.
