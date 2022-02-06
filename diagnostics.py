from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score, StratifiedKFold
import pandas as pd
from os.path import join
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pickle
from os import remove, listdir


def choose_ML_model(path,file):
    models_path = join(path,'models')
    static_folder_path = join(path,'static')
    datset_path = join(path,'dataset')

    df = pd.read_csv(join(datset_path, file))
    
    # data preprocessing
    df = df[df['Diagnosis'] != "CRC Stage I"]  # remove paitants with CRC stage I
    df = df.dropna() # remove rows with missing data
     
    # Define the predictor parameters (X) and predicted parameter (y)
    X = df.drop(['Subject','State','Diagnosis'], axis=1)
    y = df['State']
    
    # Data normalization (zscore standarization)
    scaler = preprocessing.StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    
    # Create a dictionary with all the available classifiers
    models = {'LR': LogisticRegression(solver='liblinear'),
           'LDA':LinearDiscriminantAnalysis(),
           'KNN': KNeighborsClassifier(),
           'CART': DecisionTreeClassifier(),
           'NB': GaussianNB(),
           'SVM': SVC(gamma='auto',probability=True)}
     
    # evaluate the different models using 10 cross-fold validation
    results = []
    results_dict = {}
    for model in models: # loop over models
      kfold = StratifiedKFold(n_splits=10, random_state=42, shuffle=True)
      cv_results = 100*cross_val_score(models[model], X_scaled, y, cv=kfold, scoring='accuracy')
      results.append(cv_results)
      results_dict[model] = [round(cv_results.mean(),2),round(cv_results.std(),2)]
      # print('%s: %f (%f)' % (model, cv_results.mean(), cv_results.std()))
    
    
    # delete old plots from the 'static' directory
    for file_name in listdir(static_folder_path):
        if file_name.endswith('.png'):
            remove(join(static_folder_path,file_name))
        
    # plot the accuracy distribution of each model 
    fig=plt.figure()
    plt.boxplot(results, labels=models.keys())
    plt.title('Clinical state classification:')
    plt.ylabel('Fraction of correct classifications:')
    fig.savefig(join(static_folder_path,file[:-4]+'_models_performance.png'))
    
    # plot the 2 first PCs of the data
    pca=PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    colors = y == 'C'
    fig, ax = plt.subplots()
    scatter = plt.scatter(components[:,0],components[:,1], c=colors.astype(int))
    plt.set_cmap('seismic')
    
    # produce a legend with a cross section of sizes from the scatter
    handles, labels = scatter.legend_elements()
    ax.legend(handles, labels, loc="upper right", title="Cancer state:")
    plt.xlabel('Principal component 1')
    plt.ylabel('Principal component 2')
    plt.title('Principal component analysis:')
    fig.savefig(join(static_folder_path,file[:-4]+'_PCA.png'))
    
    
    # fit and store models for later use
    for model in models:
        pickle.dump(models[model].fit(X_scaled, y), open(join(models_path,model), 'wb'))
        
    return results_dict 



def classify_data(file_path,chosen_model_path):

    df = pd.read_csv(file_path)
    
    # data preprocessing
    df = df[df['Diagnosis'] != "CRC Stage I"]  # remove paitants with CRC stage I
    df = df.dropna() # remove rows with missing data
     
    # Define the predictor parameters (X) and predicted parameter (y)
    X = df.drop(['Subject','State','Diagnosis'], axis=1)
   
    # Data normalization (zscore standarization)
    scaler = preprocessing.StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    
    chosen_model = pickle.load(open(chosen_model_path, 'rb'))
    
    predicted_subjects_state = chosen_model.predict(X_scaled)
    
    return predicted_subjects_state