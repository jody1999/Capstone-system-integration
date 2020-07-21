import copy
import pandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
from joblib import dump, load
import os

def extract_data(filename: str):
    df: pandas.DataFrame = pandas.read_csv(filename)
    columns = ["Size_L35", "kl_L35", "L35.Mean", "MeanSize_35", "combo3" , "Size_InvL35", "MeanSize_L", "InvL35.Mean", "combo5", "L35.Skewness", "L35.Kurt", "combo8", "combo10", "MeanSize_InvL", "combo9", "combo4", "L350.WBC.s", "combo6", "kl_invL35", "L35.WBC.s"]

    selected_features = df[columns].to_numpy()
    labels = df["Patient"].to_numpy()
    labels = np.where(labels >= 0, labels, 0)
    labels = np.where(labels <= 1, labels, 1)
    
    reshaped_cell_data = selected_features.transpose()
    processed_data = np.zeros_like(selected_features)
    row_size = reshaped_cell_data.shape[1]

    for i in range(reshaped_cell_data.shape[0]):
        col_max = np.max(reshaped_cell_data[i,:],axis=0)
        col_min = np.min(reshaped_cell_data[i,:],axis=0)
        diff = col_max - col_min
        ret_val = (reshaped_cell_data[i,:] - np.full((row_size,),col_min)) / diff
        # print(diff)
        processed_data[:,i] = ret_val

    return processed_data, labels

def extract_gamma(filename: str):
    gamma_values: np.ndarray = np.genfromtxt(filename, delimiter=',')[1:,1:]
    gamma_values = gamma_values.flatten()
    return gamma_values

def metric_generation(predicted: list, gold: np.ndarray):
    predicted = np.asarray(predicted)
    accuracy = np.sum((predicted == gold))/len(gold)
    true_negative = np.sum((gold == 0))
    false_negative = np.sum((predicted < gold))
    true_positive = np.sum((gold == 1))
    return true_positive/(true_positive + false_negative), true_negative/(true_negative + false_negative), accuracy

def train(x_data: np.ndarray, y_data: np.ndarray, gamma_values, path):
    model_list = []
    metrics = []
    best_metrics = []
    C_values = [0.25,0.5,1,2,4]
    for i in range(1,101):
        gamma = gamma_values[i-1]
        X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=i)
        parameters = {'kernel' : ['rbf'], 'C': C_values, 'gamma':[gamma]}
        sv_classifier = SVC()
        gridsearch_svm = GridSearchCV(sv_classifier, parameters)
        gridsearch_svm.fit(X_train, y_train)
        best_c = gridsearch_svm.best_estimator_.C

        sv_classifier_test = SVC(C=best_c, gamma=gamma)
        sv_classifier_test.fit(X_train, y_train)
        prediction = sv_classifier_test.predict(X_test)

        val_sens, val_spe, accuracy = metric_generation(prediction, y_test)
        roc_score = roc_auc_score(y_test, prediction)
        metrics.append([accuracy, val_spe, val_sens, roc_score])

        dump(sv_classifier_test, model_path) 


    return metrics

cwd = os.getcwd()    
gamma_path = os.path.join(cwd, "\data\250 Gamma data" + "." + "csv")
processed_path = os.path.join(cwd, "\data\Processed Data" + "." + "csv")
model_path = os.path.join(cwd, "\data\model" + "." + "joblib")
    
gamma_values = extract_gamma(gamma_path)
processed_data, labels = extract_data(processed_path)
metrics = train(processed_data, labels, gamma_values, model_path)
# print(np.mean(metrics, axis=0))

