# EPINuc app - WIS Advanced Python course final project
Students names: Daniel Deitch and Nir Erez

# Overview:
Epigenetics of Plasma Isolated Nucleosomes (“EPINuc”). The test comprehensively profiles the epigenetics landscape of plasma DNA together with protein cancer biomarkers. Our system, which combines total internal reflection microscopy (TIRF) and DNA sequencing, enables us to measure for each blood sample a verity of different parameters (e.g., the distribution of different cell free nucleosomes histone modifications, global DNA methylation levels and quantity of cancer associated protein biomarkers) and generate a multi-layered characterization of the sample in single-molecule resolution.

In our project, we aimed to develop a Python based applcation that receives EPINuc data from different samples (e.g. healthy or cancer patients) and then, by using a diverse set of machine-learning algorithms, classify the samples to their corresponding prognosis groups.

This repository contains all the required files in order to run and use our application.

# Installation: how to install EPINuc app on Windows OS
1. Install `python3` (any version will work) and `gitbash`/`conda` prompt on your personal computer
2. Fork/download the this repository to your personal computer
3. Change directory to our repostory. This directory should contain the `requirements.txt`, `app.py` and `diagnostics.py` files.
4. Install the required moduls/packages by typing in the the command promp: `pip install -r requirements.txt`
5. Run the application by typing in the the command promp `export FLASK_APP=app` and then `flask run`
6. The epected output should be:
```
* Serving Flask app "app"
* Environment: production
  WARNING: This is a development server.
  Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
7. Open you favorite internet browser and type in the address `http://127.0.0.1:5000/` in the search bar.
   (note that the address might change depending on your OS).
8. Thats it! The homepage of our EPINuc application should appear on your screen.


# Documentation:
The EPINuc application have three main features that are currently available to use:
## Feature 1 - Diagnose data:
This feature allows the user to upload his own patients derived EPINuc data and recieve the diagnosis (Healthy or Cancer) for each of the samples in the dataset.
<br>The workflow has four steps:
<br>**A. <ins>Upload data for diagnosis</ins>:**
<br>In the first step the user can pick and upload a table of EPINuc data from his own personal computer.
<br>Upload a file to analyze is done pressing the "choose file" button followed by clicking the "submit" button. 

<ins>Requirements and quality assurance</ins>:
* The data should be a table/matrix in a `.csv` or `.xls` format
* The data should contain measurments from all the required EPINuc features specified in the `valid_file_column_names.json` provided in the `etc` directory of this repository.
* The  `Subject`, `State` and `Diagnosis` features are optional and will not be used in the analysis.
* In cases some of the features are missing, an error will araise stating the features that are missing. In this case we recommend using a different dataset for diagnosis.
* There are no restrictions on the order of the features in the data. In case that the order of the features is not as mentioned in the `valid_file_column_names.json` file, the application will detect the instance, raise a warning and reorgnize the data so it will be suitable for analysis.
* The aplication should detect datasets with invalid negative values and raise an appropriate error messege.
* The application should detect cases in which a file was not submitted by the user and raise an appropriate error messege.

<br>**B. <ins>Choose a reference dataset for model fitting</ins>:**
<br>The EPINuc application provides a variety of machine learning algorithems to choose from in order to diagnose your patiants.
<br>In order to train and fit these classifiers the user can an available dataset from the existing database to be used a reference data for the traning/model fitting phase.
<br>The application will display the available datasets in a form of a table and specify the amount of samples from each of the two categories of patients.
<br>The user can inpect the dataset by pressing the `Veiw` option before choosing it.
<br>If the user is not satisfied by the default datasets provided, it is possible to upload new datasets to the database by using the `Update database` feature of the application (see below).

<br>**C. <ins>Choose a machine learning algorithm for patients' state prediction</ins>:**
<br>After choosing the reference data and fitting the different models, the EPINuc application will display statistics and visuallizations that will help the user to appreciate the performance of the different models and the quality of the training dataset.

<ins>The available classifiers are</ins>:
1. Logistic Regression (LR)
2. Decision Tree Classifier (CART)
3. k-Nearest Neighbors (KNN)
4. Linear Discriminant Analysis (LDA)
5. Naive Bayes classifier (NB)
6. Support Vector Machine (SVM)

<br>Each classifier has different assumptions and uses different aspects of the data to perform its predictions.
<br>Therefore, it will be wise to intersect the results produced by the different classifiers in order to decrease the probability for a miscalssification.
<br>Note that we used the defualt parameters for all the classifiers. 

Currently the availeable summaries are:
* Principal component analysis (PCA) - a linear dimentionality reduction algorithm performed on all the 24 features of the EPINuc data.
<br> The analysis results in a scatter plot based on the first two principal components of the data. The heathly patients data points are colored in blue and the cancer patients in red.
* Boxplots illustrating the distribution of percentage of correct classifications for each classifier as obtained using 10-fold cross-validation.
* Summary table displying statistics about the performance of each classifier.

The user will be able to download the train model of each classifier by clicking the `Download` button or choose a specific classifier for predicting the patients' health state.

<br>**D. <ins>Predict patients' health state</ins>:**
<br> after choosing the desired classification model, the application will use it in order to predict the health state of each sample in the uploaded test dataset.
<br> The user can later either view or download the results by clicking the `View file` or `Download file` buttons respectively.

## Feature 2 - Search database:
This feature allows the user to search through the different  EPINuc datasets available in our database.
<br>The user can search a specific dataset according to charachter/substring of the dataset name, and subsequently, also to view and download it to its computer.
<br>The datasets found by the search engine will be displayed in the form of a table containg  discriptive information (e.g., time of upload, file size and dataset name) about the datasets.
<br>Entering an empty string in the search box will result in displating all the datasets that are currently available in the application database.
<br>In case the database does not contain a dataset including the searched item in its name, the application will raise an error massage notifing the user to search again using different substring.
<br>Finally, after searching and finding the datasets of interset, the user will be able to either view or download the results by clicking the `View` or `Download` buttons respectively.


## Feature 3 - Update database:
This feature allows the user to update the existing EPINuc database by either uploading new EPINuc datesets from the user personal computer or by permanently deleting existing datasets from the database.
<br>The user can upload a file by pressing the `Choose file` button followed by pressing the `Submit` button.
<br>The user can also update a file, by deleting the old version file from the databse pressing the `Delete` button and then uploading the newer version of the file following the procedure mentioned above.
<br>Alternativly, the user can add and extention/indentifier to the file name and then upload it directly to the database.

It is important to note that in order to upload new database, the user should first validate that the file of interst satisfy the following requirements and restrictions:
1. The data must be a table/matrix in a `.csv` or `.xls` format.
2. The dataset must contain measurments from all the required EPINuc features specified in the `valid_file_column_names.json` provided in the `etc` directory of this repository.
3. The name of the chosen dataset  does not already exist in the database.
4. The chosen dataset is not a duplicate of an other dataset already exist in the database.
5. There are not negative values in the chosen dataset.

Nevertheless, our application is programmed to detect and notify the using in the following scenarios:
* Cases in which the user has chosen to upload a file with an invalid format will be detected by the application which later will notify the user by displaying an error messege.
* Cases in which the user has chosen to upload a file with missing data features will be detected by the application which later will notify the user by displaying an error messege.
* In case the chosen dataset contains additional features beyond thos specified in the `valid_file_column_names.json` the application will detect the instance, raise a warning and remove the extra features from the dataset before uploading it to the database.
* There are no restrictions on the order of the features in the data. In case that the order of the features is not as mentioned in the `valid_file_column_names.json` file, the application will detect the instance, raise a warning and reorgnize the data so it will be suitable for analysis.
* Cases in which the chosen dataset name already existing in the database will raise an appropriate error messege.
* The aplication should detect datasets which are a duplicate of other already existing datasets in the database.
* The aplication should detect datasets with invalid negative values and raise an appropriate error messege.
* The application should detect cases in which a file was not submitted by the user and raise an appropriate error messege.
* The user can upload new databaseby pressing the `choose file` button followed by clicking the `submit` button.


# Testing and quality assurance:
To facilitate the testing of our application by user , we included in to our repository a folder (i.e., `tests`) containg a veraity of additional 'test' files.

When uploading files in the `diagnose data` or `update database` features use the following files:
* `wrong_format.xlsx` - this file has an invalid `xlsx` format. Uploading this file will raise the following error: *"Error! Invalid file format!"*
* `non_valid_negative_values.csv`- this file contain negative values in some of the data features. Uploading this file will raise the following error: *"Error! Negative values found in data!"*
* `missing_columns.csv` - this file contain a missing data feature. Uploading this file will send the following error: *"Error! Missing columns!"*
* `extra_columns.csv` - this file contain a redundant data feature call `extra`. Uploading this file will raise the following message: *"Warning: File contains more columns than required and had to be reorganized to be uploaded successfully!"*
* `diff_name_same_data.csv` - this file has a unique name but contain data already existing in the database (its a duplicate of the 'example_dataset.csv' file). Uploading this file will raise the following error: *"Error! Dataset already exist!"*
* `example_dataset.csv` - this file has unique data but has a name that already exist in the database. Uploading this file will send the following error: *"Error! Upload failed!"*
* `wrong_columns_order.csv` - this is a valid file, however, the order of some of the different data features was shuffled. Uploading this file will send the following message: *"Warning: File columns had to be reorganized for file to be uploaded successfully!"*

In addition, in order to test the performance of diagnosis analysis, we included two additional datasets to our repository - `example_test_data.csv` and `example_test_data_shuffled.csv`.
<br>These datasets contain data on subjects that are not included in the available datasets (e.g., `example_dataset.csv`) and therefor are suitable for testing the generalization of the different classifiers used by our application.

