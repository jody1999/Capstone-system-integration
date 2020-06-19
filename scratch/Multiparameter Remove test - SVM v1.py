import csv
import random
import math
import operator
import time
import statistics
import time
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

## -- data file path -- ##
file_data= 'data/wbc_janselect.csv'
##file_output_data= 'data/testing.csv'
file_param= 'data/jan5param_acc.csv'
##file_param_remove = 'data/novparam_remove.csv'
##file_param_rank = 'data/novparam_rank.csv'

def loadDataset(file_data):
    with open(file_data,'r') as csvfile:
        lines = csv.reader(csvfile)

        dataset = list(lines)
        data_header = dataset[0]
        
        # delet the header #
        del dataset[0]

        #set all y values to only 0 or 1
        for x in range(len(dataset)):
            if float(dataset[x][1]) < 0:
                dataset[x][1] = 0
            if float(dataset[x][1]) > 1:
                dataset[x][1] = 1
            else:
                pass
        ## setting data into dataset into its categories of float or str
        for x in range(len(dataset)):
            for y in range(len(dataset[x])):
               
                try:
                    dataset[x][y] = float(dataset[x][y])
                except:
                    dataset[x][y] = str(dataset[x][y])

    return dataset, data_header

## NEED TO NORMALISE ALL FIELDS                
def transposeData(data):
    #to transpose the data
    transpose = list(map(list,zip(*data)))
    return transpose

def normalizeData(data):
    #transpose data
    data = transposeData(data)

    minimum,maximum,rowData,norm = [],[],[],[]
    for x in range(2, len(data)):
        minimum = min(data[x])
        maximum = max(data[x])
        rowData = data[x]
        for y in range(len(data[x])):
            try:
                norm = float(data[x][y]-minimum)/(maximum - minimum)
                rowData.pop(y)
                rowData.insert(y, norm)
            except:
                return
        data.pop(x)
        data.insert(x, rowData)

    data = transposeData(data)
    
    return data

def saveData(data, file_name):
    with open(file_name, 'w', newline='') as out_f:  # Python 3
        w = csv.writer(out_f, delimiter=',')        # override for tab delimiter
        w.writerows(data)                            # writerows (plural) doesn't need for loop
    return

def print_output(MCC, TP, TN, FP, FN, P, N):
    print('========= File Data "%s' % file_data + '" ========= \n')
    print('Total =',P+N,'||  True Positive (1) =',TP,' ||  True Negatives (0) =', TN)
    print()
    print('(Sensitivity) True Positive Rate = %0.3f' %((TP/P)*100)+'%')
    print('(Specificity) True Negative Rate = %0.3f' %((TN/N)*100)+'%')
    print('(Accuracy) = %0.3f' %((TP+TN)/(P+N)*100)+'%')
    print('(Precision) Positive predictive value (PPV) = %0.3f' %(TP/(TP+FP)*100)+'%')
    print()
    print('False Negative Rate = %0.3f' %((FN/P)*100)+'%')
    print('False Positive Rate = %0.3f' %((FP/N)*100)+'%')
    print()
    print('MCC Matthews correlation coefficient = %0.3f' %(((TP*TN)-(FP*FN))/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))))
    print()
    print('Total Count = ', (P+N))
    print('========= ========== ========= ========= =========\n')
    return
    
def test(data_x, data_y, count, split):

    ### Analysis Parameters ###
##    count = 0
    total_count = 0
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    P = 0
    N = 0

    while ((P+N) <= count):
        try:
            # Training
            X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size = split)

            # SVM Classification and fitting
            ## 'rbf' is good for specificity and accuracy
            ## 'poly' seems good for sensitivity
            svclassifier = SVC(kernel='rbf', gamma = 'auto', degree=3, coef0 = 0.0)
            svclassifier.fit(X_train, y_train)

            #Predict the response for test dataset
            y_pred = svclassifier.predict(X_test)
##            matrix = confusion_matrix(y_test,y_pred)

            if len(y_pred) != 0:
                for i in range(len(y_test)):
                    if y_test[i] == 1 and y_pred[i] == 1:
                        TP += 1
                        P += 1
                    if y_test[i] == 1 and y_pred[i] == 0:
                        FN += 1
                        P += 1
                    if y_test[i] == 0 and y_pred[i] == 0:
                        TN += 1
                        N += 1
                    if y_test[i] == 0 and y_pred[i] == 1:
                        FP += 1
                        N += 1

        except:
            pass
        
    MCC = ((TP*TN)-(FP*FN))/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    return MCC, TP, TN, FP, FN, P, N

### Start ###
start=time.time()

### Variables Assign ###
split = 0.10    ## ratio/percentage to train data
k = 3

### Analysis Parameters ###
count = 0
total_count = 0
TP = 0
FP = 0
TN = 0
FN = 0
P = 0
N = 0

#Initialising variables
number = 0
param_rank = []
final_param = []
param_list =[]
count_param = 0
rank_header = []

### ---> Bootstraping Variables
max_count = 1000       #500000 is a good number
num_param = 10            #Set the number of selected parameters

### Load Data ###
data, header = loadDataset(file_data)
ini_header = header
len_param = len(header)
rank_header = header[0:2]
##data = normalizeData(data)

# load dataset into Pandas DataFrame
df = pd.DataFrame(data)
df.columns = header

# iterating the columns to get features 
features = df.columns[2:len(df.columns)]

# iterating the columns to get traget
target = df.columns[1]

#separating the features in dataframe
x = df.loc[:, features].values
x = StandardScaler().fit_transform(x)

# Separating out the target
y = df.loc[:,target].values

# Live plots
plt.axis([0, len(header)-1, 0, 1])

##while((len(list_param) != (num_param+1)) & (len(list_param) > (num_param))):
while (count_param <= (len_param-2)):
    #initialise
    test_data = []
    param = []

    print('The Initial Data Results')
    ini_MCC, ini_TP, ini_TN, ini_FP, ini_FN, ini_P, ini_N = test(x, y, max_count, split)
    print_output(ini_MCC, ini_TP, ini_TN, ini_FP, ini_FN, ini_P, ini_N)

    # Remove each parameter and append the statistics in sequence
    for i in range(len(x[1])):
        test_data = np.delete(x, i, 1) ## data, object, axis (1 = column)
##        print('The run without column %i'%i,' -->', header[i+2])

        ## test the new data set without the selected i column
        MCC, TP, TN, FP, FN, P, N = test(test_data, y, max_count, split)

        ## record the stats and metrics in param
        param.append([ header[i+2], MCC, TP/P, TN/N, (TP+TN)/(P+N),FP, FN, P, N, i] )
##        print_output(MCC, TP, TN, FP, FN, P, N)
        
    ## The sort position is vital to see which output value to use a rank
    ## 1 - MCC, 2 - TP/P, 3 - TN/N, 4 - (TP+TN)/(P+N)
    ## 1 - MCC, 2 - sensitivity, 3 - specificity, 4 - Accuracy
    ##### Select the parameter #####
    roc_param = 4

    # rank the parameters from max to min. MAX = poor corelation
    param.sort(key = operator.itemgetter(roc_param), reverse = True)

    if roc_param == 1: select = ini_MCC
    if roc_param == 2: select = ini_TP/ini_P
    if roc_param == 3: select = ini_TN/ini_N
    if roc_param == 4: select = (ini_TP+ini_TN)/(ini_P+ini_N)
    
    #add to the remove ranks
    param_rank.append([param[0][0], (ini_TP+ini_TN)/(ini_P+ini_N), ini_TN/ini_N, ini_TP/ini_P, ini_MCC])
    param_list.append(param[0])

    print()
    print('-----> The no. %i'%(count_param+1),'/ %i'%(len_param-2),'eliminated parameter is',param[0][0])
    print()
    
    plt.scatter(count_param+1, select)
    plt.pause(0.01)
    
    #remove the ranked column from data
    x = np.delete(x, param[0][9], 1) ## data, object, axis (1 = column)
    header.pop((param[0][9]+2))
    final_param = param
    if len(x[0]) == 1:
        print('The Initial Data Results')
        ini_MCC, ini_TP, ini_TN, ini_FP, ini_FN, ini_P, ini_N = test(x, y, max_count, split)
        print_output(ini_MCC, ini_TP, ini_TN, ini_FP, ini_FN, ini_P, ini_N)

        ## 1 - MCC, 2 - sensitivity, 3 - specificity, 4 - Accuracy
        if roc_param == 1: select = ini_MCC
        if roc_param == 2: select = ini_TP/ini_P
        if roc_param == 3: select = ini_TN/ini_N
        if roc_param == 4: select = (ini_TP+ini_TN)/(ini_P+ini_N)

        param_rank.append([param[1][0], (ini_TP+ini_TN)/(ini_P+ini_N), ini_TN/ini_N, ini_TP/ini_P, ini_MCC])
        plt.scatter(count_param+2, select)
        plt.pause(0.01)
        
        header.pop(2)
        print()
        print('-----> The no. %i'%(count_param+2),'/ %i'%(len_param-2),'eliminated parameter is',param[1][0])
        print()        
        break
    
      
    count_param+=1

##print(classification_report(y_test,y_pred))
## prepare Data with headers ##
##param_rank.insert(0, ['Eliminated Parameter','MCC','TP/P','TN/N', 'TP+TN)/(P+N)','FP','FN', 'P', 'N', 'Index'])
##final_param.insert(0, ['Parameter','MCC','TP/P','TN/N', 'TP+TN)/(P+N)','FP','FN', 'P', 'N', 'Index'])
param_rank.reverse()
param_rank.insert(0,[header[1],'Accuracy','Specificity','Sensitivity','MCC'])
param_rank.insert(0,[header[0],roc_param,roc_param,roc_param,roc_param])
param_rank = transposeData(param_rank)
param_rank.reverse()

## prepare final output selected data ##
final_data = df.loc[:, header].values
final_data = np.insert(final_data, 0, header, axis = 0)

final_param = df.loc[:, param_rank[4]].values
final_param = np.insert(final_param, 0, param_rank, axis = 0)

## Saving Data to Files ##
saveData(final_param, file_param)
##saveData(param_rank, file_param_remove)
##saveData(final_data, file_output_data)

### END ###
end=time.time()
print('The run took %0.6fs' % (end-start))

plt.show(block=False)
##print('Total number of random selection runs = %i' % cycles)
##print('Mean = %0.2f'%mean,' SD = %0.2F'%std, 'Median = %0.2f'%median, ' min = %0.1f'%minimum,'%', '  >90% count/1000 =', int(maxi/cycles*1000))



