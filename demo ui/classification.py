import pandas 
import numpy as np
from sklearn.svm import SVC
from joblib import dump, load
import os

cwd = os.getcwd()
filename = os.path.join(cwd, "data/single_sample_Feature" + "." + "csv")
model_path = os.path.join(cwd, "model" + "." + "joblib")

def classification():
    df: pandas.DataFrame = pandas.read_csv(filename)
    columns = ["Size_L35", "kl_L35", "L35.Mean", "MeanSize_35", "combo3" , "Size_InvL35", "MeanSize_L", "InvL35.Mean", "combo5", "L35.Skewness", "L35.Kurt", "combo8", "combo10", "MeanSize_InvL", "combo9", "combo4", "L350.WBC.s", "combo6", "kl_invL35", "L35.WBC.s"]
    selected_features = df[columns].to_numpy()
    X_test = selected_features

#    load the model from pickles
    sv_classifier = SVC()
    sv_classifier = load(model_path)
#    print(X_test)
    prediction = sv_classifier.predict(X_test)
    print(prediction.tolist()[0])
    return prediction.tolist()[0]
#classification()
