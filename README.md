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
### 1. Diagnose data:
This feature allows the user to upload his own patiants derived EPINuc data and recieve the diagnosis (Healthy or Cancer) for each of the samples in the dataset.
The workflow has four steps:
A. Upload data for diagnosis - In the first step the user can pick and upload a table of EPINuc data from his own personal computer. 
The data should be a table/matrix in a `.csv` or `.xls` format and should contain measurments from all the required EPINuc features specified in the `valid_file_column_names.json` provided in the `etc` directory of this repository.

Important to note:
* The  `Subject`, `State` and `Diagnosis` are optional and would not be used in the analysis.
* In cases 
* There are no restrictions on the order of the features in the data. The application will detect and order 

### 2. Search database:

### 3. Update database:
