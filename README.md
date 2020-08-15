# Capstone-system-integration
mainly focus on systme integration in GUI code

software 
- GUI operation
- data storage 
- computer video video analysis 
- feature creation (2 levels) 
- machine learning classification 

hardware subsystem operation 
- camera homing
- camera autofocusing
- pressure system control
  (motor and sensor for clamp and switch control)


# Data Analysis 

## data analysis in testing
This readme content is only for preloaded model prediction for data analysis during the testing process. 

### Involved files
The GUI is calling external backend functions from 2 files:
```python
from generate_features import generate_features
from classification import classification
```
### Process
1. def generate_features: read from local raw count csv file, generate a feature csv file with all features, stored locally.
2. def classification: read from local feature csv file, load classification model from local saved pickle, choose only the selected features, predict by the model, and return the binary result.

## data analysis in training
The readme content only for training during the experimenting stage. It is the extracted version of model training R code content

### Involved files
generate_features.py, data_training.py

### Process
1. def generate_features: read from local raw count csv file, generate a feature csv file with all features, stored locally.
2. def extract_gamma: read from local gamma data csv file, select out the gamma value corresponding to the parameter used in the chip test, return value will be used in the model as parameter.
3. def extract_data: read from local features csv file, process features by selecting the resizing. Return numpy variable will be user in the model as dataset. 
4. def train: carrying out a gridsearch for best c value with iteration through every gamma value. dump and save the model to local pickle, which will be used for prediction in the sample testing process. 


## Execute
The python file are written in modularized functions such as it will be directly called by the GUI code. To test on the code individually, simply initiate a new code to import and call the functions, or add to the end of the code in the corresponding files:
```python 
if __name__ == "__main__":
   the_function_you_want_to_run()
```
and then call in the terminal 
```bash
python generate_features.py
python data_training.py
python classification.py
```


## data storage
The readme content is for database operation in the application stage. It is closely connected to the GUI code and only executed by calling from GUI code. 

###database structure
The database result.db has two tables, one "results" for testing results recording, another "user" for staff id storage so only the rfid value read that is in the user table can be verified and carried out the testing.

### Process
```python
from data_storage import store_data
```
1. The store function will first create a Result instance, which is a specific data structure that store the required information as an object. 
2. The csv file will be converted to a blob by function convertToBinaryData, the video will be save in the local disk and a video_id in the database that annotates the location. 
3. The SQL execution will be called to create and store a new entry of testing data
~~~~sql
 INSERT INTO results (patient_id ,NRIC_number , 
                operator_id , time , classification, 
                WBC_count, RBC_count, 
                raw_video_id, confirmation)
                VALUES (?,?,?,?,?,?,?,?,?)
~~~~

4. To read the stored data, import and call read_data function 
```python
from data_storage import read_data
```
