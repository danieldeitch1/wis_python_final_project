# EPINuc app - WIS Advanced Python course final project
by Daniel Deitch and Nir Erez

# Installation: how to install EPINuc app in Windows OS
1. Install `python3` (any version will work) and `gitbash`/`Conda` prompt on your personal computer
2. Fork/download the EPINuc_app repository to your personal computer
3. Change directory to our repostory. This directory should contain the `requirements.txt`, `app.py` and `diagnostics.py` files.
4. Install the required moduls/packages by typing in the the command promp: `pip install -r requirements.txt`
5. Run the application by typing in the the command promp: `python app.py`
6. The epected output should be:
```
* Serving Flask app "app" (lazy loading)
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
For a step-by-step user guide, please read the *manual.doc* file.

The EPINuc application have three main features that are currently available to use:
### 1. <ins>Diagnose data</ins>:
This feature allows the user to upload his own patients derived EPINuc data and recieve the diagnosis (Healthy or Cancer) for each of the samples in the dataset.
<br>The workflow has four steps:
<br>**A. <ins>Upload data for diagnosis</ins>:**
<br>In the first step the user can pick and upload a table of EPINuc data from his own personal computer.

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
1. 

Currently the availeable summaries are:
* Principal component analysis (PCA) - a linear dimentionality reduction algorithm performed on all the 24 features of the EPINuc data.
<br> The analysis results in a scatter plot based on the first two principal components of the data. The heathly patients data points are colored in blue and the cancer patients in red.
* Percentage of correct classifications for each of the 


### 2. <ins>Search database</ins>:
<br> This feature allows the user to search through different EPINuc datasets which were uploaded to the application. The user can search a spesific dataset according to charachter/substring of its file name, and subsequently, also to view and download it to its computer. The user can view all the datasets that are currently uploaded to the app by searching dataset by an entering an empty string.

### 3. <ins>Update database</ins>:
<br> This feature allows the user to upload/update/delete EPINuc database file:

* In order to upload new database the file should be in a correct format as mentioned in the "Requirements and quality assurance" section.
* The user can upload new databaseby pressing the "choose file" button followed by clicking the "submit" button.
* The user can update database file, by deleting the old version file from the application using the "delete" button, followed by uploading the update EPINuc database, as mentioned above. Alternativly, the user can add to date or version number to the file name and upload it directly to the app without deleting the previous version of the database file.
