<img src="scripts/kabloom.jpg" alt="Logo" width="400" height="200">

<br />

<p style="text-align:center">The kaBLOOM app uses satellite imagery to find poppy blooms.</p>
    
<p style="text-align:center">For this proof-of-concept demo I used data from the 2017-2020 poppy seasons (March-April) at three California locations.</p>
    
<p style="text-align:center">This repository contains the code I used to create the app.</p>

<br />

<p style="text-align:center">
<a href="https://youtu.be/guCyMfn1zSo">View YouTube demo</a>
·
<a href="http://35.164.63.227:8501/">Demo the app</a>
    </p>
    
    
    
## Table of Contents

* [Repository contents](#repository-contents)
    * [Data](#data)
    * [Notebooks](#notebooks)
      * [Analysis pipeline](#analysis-pipeline)
      * [EDA](#eda)
    * [Scripts](#scripts)
* [Roadmap](#roadmap)
* [Contact](#contact)



<br />

<!-- REPOSITORY CONTENTS -->
## Repository contents


<br />

<!-- DATA -->
### Data

The 'data' folder has the processed data needed for use in the app. I did not upload the raw satellite data because it is quite large, but I included the code I used to get and process the data from the Sentinel hub.


<br />

<!-- NOTEBOOKS -->
### Notebooks

The 'notebooks' folder contains two subfolders: 'eda' and 'analysis_pipeline'. It also contains a Jupyter notebook called 'kabloom_code_demo' that has an abridged version of the analysis pipeline.

The analysis_pipeline folder contains 7 Jupyter notebook files, and the eda folder contains 4 Jupyter notebook files. All of these files are briefly described below.

<br />

<!-- ANALYSIS_PIPELINE -->
#### Analysis pipeline

The following is a general description of what each Jupyter notebook file does and the order in which to run them.

1. get_data.ipynb <br /> This file contains the code to download satellite data from the Sentinel Hub. For this project I looked at three areas: Antelope Valley, Grass Mountain, and Lake Elsinore, and I got all available data for these areas for March and April of 2017-2020. At this point the eda files can be run to visualize the satellite images.


2. label_initial.ipynb <br /> Here I hand label a small subset of seed pixels as either poppy or not poppy. I chose the poppy pixels from one image per region taken during a bloom, and I chose the non-poppy pixels randomly from one image per region taken before the bloom started.

At this point I did model exploration (see file in eda folder).


3. fit_evaluate_update.ipynb <br /> Here is where the active learning takes place. I import the labelled pixels (either from iteration0 labelled in step 2 above, or from a previous iteration of this file), then fit and evaluate a classifier. Then I either exit the active learning loop and save the classifier (if the evaluation reveals that the model is good enough), or I add a small number of corrected hand labelled pixels to the pool of labelled pixels and move on to another iteration (if the evaluation reveals that the model is still making mistakes).


4. predict_blooms.ipynb <br /> After creating a satisfactory model above, I move on to classify all the pixels in all of the images that I have and save the predictions.


5. get_areas.ipynb <br /> Here I process the classification matrices from step 4 and segment them into poppy bloom areas (also called patches). I also get the centroids of each area.


6. process_areas.ipynb <br /> Here I get information from the poppy bloom areas from step 5 (like number of patches and size of each patch) and prepare the info for the app. 


7. get_lat_long.ipynb <br /> Here I get the latitude and longitude for the centroid of every patch identified in step 5.


8. feature importances.ipynb <br /> This file has information about feature importances in the final model.


At this point I have everything I need to run the app.


<br />

<!-- EDA -->
#### EDA

1. eda_antelope.ipynb, eda_elsinore.ipynb, eda_grassmtn.ipynb <br /> Exploratory data analysis - these files visualize the recreated true color satellite images for all of the dates with satellite data available in March and April of 2019. These files can be run after step 1 above.


2. model_exploration.ipynb <br /> In this notebook I explore and compare the results from 5 different binary classifiers (logistic regression, random forest, naive bayes, stochastic gradient descent, and gradient boosting). In the end I chose to go with the random forest because it performed the best out of the box and generalized the best to unseen data. I ran this analysis between steps 2 and 3 of the analysis pipeline.



<br />

<!-- SCRIPTS -->
### Scripts

The 'scripts' folder has the Python code that I used to create the app in Streamlit.



<br />

<!-- ROADMAP -->
## Roadmap

The following are some open issues and future plans. Most of these are big and can be their own projects. Contact me if you'd like to work on these - or feel free to go ahead and tackle them on your own (or develop them into a separate project). I'm new to open source, so I'd love to hear from you if you have that experience and would like to work together on this project (and get teamwork experience!).


1. Add forecasting ability (use weather data etc.)
2. See if I can get free Sentinel API access. Otherwise, consider other satellites
3. Engineer data storage pipeline
4. Get automatic download ability for continuous updates from satellite as the info becomes available
5. Automate the online analysis as info becomes available
6. Scale to more locations - figure out if I should  just do broad sweeps of large areas to look for blooms, or if I should take a more targeted (but manual) approach of choosing locations based on past blooms
7. Include other types of flowers. I came across some massive purple blooms in a central california image. (Don't know what those flowers were, maybe do a bit of research). Also saw some yellow blooms.



<br />

<!-- CONTACT -->
## Contact

LinkedIn: [linkedin.com/in/esther-richler/](https://www.linkedin.com/in/esther-richler/)

Twitter: [@EstherRichler](https://twitter.com/estherrichler)

email: [estherrichler@gmail.com](estherrichler@gmail.com)