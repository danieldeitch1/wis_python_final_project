from os import listdir, remove, rename
from time import ctime
from os.path import join, getsize, getmtime, dirname
from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import glob
from diagnostics import choose_ML_model, classify_data
import numpy as np
import json

# define the path for dataset directory
app_path = dirname(__file__)
dataset_path = join(app_path,'dataset')
temp_folder_path = join(app_path,'temp')
models_path = join(app_path,'models')
etc_folder_path = join(app_path,'etc')

valid_file_column_names = json.load(open(join(etc_folder_path,"valid_file_column_names"), "r"))
valid_formats = ['.csv','.xls']

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = dataset_path
#app.config['MAX_CONTENT_PATH'] = 25000000

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/view/<name>')
def html_table(name):
    if name == 'diagnosis_results.csv':
        df = pd.read_csv(join(temp_folder_path,name))
        df.columns = ['Subject state']
        df.columns.name = 'Subject ID'
    else:
        df = pd.read_csv(join(dataset_path,name))
    return render_template('view_dataset.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

# search for data in existing dataset
@app.route('/dataset_search')
def search_datasets():
   return render_template('dataset_search.html')

@app.route('/dataset_list', methods=['POST'])
def post_datasets():
    word = request.form.get('word', '')
    
    file_list = listdir(dataset_path) # create a list of files in the 'datasets' directory
    dataset_list = [] # find and include only csv files
    for file in file_list: 
        if file[-4:].lower() in valid_formats:
           dataset_list.append(file) 
    
    all_items = []
    for dataset in dataset_list:
        dataset_dict = {}
        file_path = join(dataset_path,dataset)
        dataset_dict['name'] = dataset # dataset name
        dataset_dict['size'] = getsize(file_path)/1000 # dataset size
        dataset_dict['time'] = ctime(getmtime(file_path)) # upload date
        all_items.append(dataset_dict)
    
    err = 0
    if word == '':
        return render_template('dataset_list.html',dataset_list=all_items,err=err)
    else:
        searched_items = [] # subset only datasets with the searched item
        for dataset in all_items:
                if word in dataset['name'][:-4]:
                    searched_items.append(dataset)
        
    if len(searched_items) == 0: # check if any datasets were found
            err = 1

    return render_template('dataset_list.html',dataset_list=searched_items,err=err)


# upload new data to existing dataset
@app.route('/upload')
def upload_file():
    dataset_list = listdir(dataset_path)
    all_items = []
    for dataset in dataset_list:
        dataset_dict = {}
        file_path = join(dataset_path,dataset)
        dataset_dict['name'] = dataset # dataset name
        dataset_dict['size'] = getsize(file_path)/1000 # dataset size
        dataset_dict['time'] = ctime(getmtime(file_path)) # upload date
        all_items.append(dataset_dict)
        
    return render_template('upload.html',dataset_list=all_items)
	
@app.route('/uploader', methods = ['GET', 'POST'])
def file_saver():
   if request.method == 'POST':
        
        # remove all temporary files from 'temp' folder
        temp_files = glob.glob(join(temp_folder_path,'*'))
        for file in temp_files:
            remove(file)
        
        f = request.files['file']
        page_id = request.form.get("page_id")
        
        if page_id == 'diag':
            err = -1
            relevent_columns_names = valid_file_column_names[3:]
            
        elif page_id == 'upload':
            err = 0
            relevent_columns_names = valid_file_column_names
            
        # check if user selected a file
        if f.filename == '':
            err = 1
            return render_template('uploader.html',err=err,page_id=page_id)
        
        # check if the file is in the right format (csv/xls/xlsx)
        if f.filename[-4:].lower() not in valid_formats:
            err = 2
            return render_template('uploader.html',err=err,page_id=page_id)
        
        file_temp_path = join(temp_folder_path,f.filename)
        f.save(file_temp_path) # save dataset in temp folder
        temp_dataset = pd.read_csv(file_temp_path) # load uploaded file as dataframe
        uploaded_dataset_columns = list(temp_dataset.columns) # extract columns
        
        # check if uploaded file contain all required columns 
        if not uploaded_dataset_columns == relevent_columns_names:
            check =  all(item in uploaded_dataset_columns for item in relevent_columns_names)
            if check is True: # uploaded file have all the required columns
                if len(uploaded_dataset_columns) == len(relevent_columns_names): # columns are not organized in order
                    temp_dataset = temp_dataset[relevent_columns_names]
                    temp_dataset.to_csv(file_temp_path, index=False)
                    err = 6
                
                else: # uploaded file contains extra columns which might not be in order
                    temp_dataset = temp_dataset[relevent_columns_names]
                    temp_dataset.to_csv(file_temp_path, index=False)
                    err = 7
                    
            else: # uploaded file missing required columns
                err = 8
                return render_template('uploader.html',err=err,page_id=page_id)
            
        # check for invalid negative values in data
        X = temp_dataset.copy()
        if page_id == 'upload':
            X = X.drop(['Subject','State','Diagnosis'], axis=1)
            
        data_column_names = valid_file_column_names[3:]

        invalid_columns_ind = np.array((X < 0).any(), dtype=bool)
        invalid_columns = np.array(data_column_names)[invalid_columns_ind] 
        if len(invalid_columns) > 0:
            err = 9
            return render_template('uploader.html',err=err,page_id=page_id,
                                   invalid_columns=invalid_columns)
            
        if page_id == 'upload':

            # check is file name already exists in the database
            file_list = listdir(dataset_path) # create a list of files in the 'datasets' directory
            if f.filename in file_list:
                err = 3
                return render_template('uploader.html',err=err,page_id=page_id)
            
            # check is file contant already exists in the database
            for file in file_list:
                dataset = pd.read_csv(join(dataset_path,file))
                if temp_dataset.equals(dataset):
                    err = 4
                    remove(file_temp_path) # delete the dataset from 'temp' folder
                    return render_template('uploader.html',err=err,page_id=page_id)
                
            file_path = join(dataset_path,f.filename)
            rename(file_temp_path,file_path) # save dataset in the 'datasets' folder
            #remove(file_temp_path) # delete the dataset from 'temp' folder
            
            return render_template('uploader.html', err=err,page_id=page_id), {"Refresh": "5; url=/upload"}
        
        elif page_id == 'diag':  
            file_path = join(temp_folder_path,'data_to_diagnose.csv')
            rename(file_temp_path,file_path) # save dataset in 'temp' folder (will be deleted later on)
            return render_template('choose_ref_dataset.html'), {"Refresh": "0; url=/choose_ref_dataset"}
        
# download a specific dataset
@app.route('/uploads/<name>')
def download_file(name):
    if name == 'diagnosis_results.csv':
        file_path = temp_folder_path
    elif '.csv' not in name and '.xls' not in name: # models download
        file_path = models_path
    else:
        file_path = app.config["UPLOAD_FOLDER"]
        
    return send_from_directory(file_path, name)
  


# delete a specific dataset
@app.route('/delete_dataset/<name>')
def delete_dataset_msg(name):
    return render_template('delete_dataset.html',dataset_name=name)
  
    
# delete a specific dataset
@app.route('/delete/<name>')
def delete_file(name):
    remove(join(dataset_path,name))
    err = 5
    return render_template('uploader.html',err=err,dataset_name=name), {"Refresh": "5; url=/upload"}
        
  

# upload data for diagnosis
@app.route('/diagnosis')
def get_diagnosis():
    return render_template('diagnosis.html')
    

# choose reference dataset for diagnosis 
@app.route('/choose_ref_dataset')
def choose_ref_dataset():
    file_list = listdir(dataset_path) # create a list of files in the 'datasets' directory
    dataset_list = [] # find and include only csv files
    for file in file_list: 
        if file[-4:].lower() in valid_formats:
           dataset_list.append(file) 
    
    all_items = []
    for dataset in dataset_list:
        dataset_dict = {}
        file_path = join(dataset_path,dataset)
        dataset_dict['name'] = dataset # dataset name
        dataset_dict['time'] = ctime(getmtime(file_path)) # upload date
        df = pd.read_csv(join(dataset_path,dataset))
        dataset_dict['Hsubjects'] = sum(df['State']=='H')
        dataset_dict['Csubjects'] = sum(df['State']=='C')
        all_items.append(dataset_dict)
    
    return render_template('choose_ref_dataset.html',dataset_list=all_items)
   

# choose reference dataset for diagnosis 
@app.route('/choose_classifier/<name>')
def choose_classifier(name):
    classifiers_performance = choose_ML_model(app_path,name)
    pca_img_name = name[:-4]+'_PCA.png'
    boxplot_img_name = name[:-4]+'_models_performance.png'
    return render_template('choose_classifier.html',pca_img_name=pca_img_name,
                           boxplot_img_name=boxplot_img_name,
                           ref_dataset=name,classifiers_performance=classifiers_performance)
 

# choose reference dataset for diagnosis 
@app.route('/classify_data/<name1>/<name2>')
def predict_state(name1,name2):
    data_to_diagnose_path=join(temp_folder_path,'data_to_diagnose.csv')
    chosen_model_path = join(models_path,name2)
    
    predicted_subjects_state = classify_data(data_to_diagnose_path,chosen_model_path)
    
    file_path = join(temp_folder_path,'diagnosis_results.csv')
    np.savetxt(file_path, predicted_subjects_state, fmt='%s')
    return render_template('classify_data.html',ref_dataset=name1, predicted_subjects_state=predicted_subjects_state)
