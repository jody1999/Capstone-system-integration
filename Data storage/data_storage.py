import sqlite3
import os

class Result:
    '''a structure to store all the information required in the results database'''
    def __init__(self, patient_id, NRIC_number, operator_id , time, classification, WBC_count, RBC_count, raw_video_id):
        self.patient_id = patient_id
        self.NRIC_number = NRIC_number 
        self.operator_id  = operator_id 
        self.time = time
        self.classification = classification 
        self.WBC_count = convertToBinaryData(WBC_count)
        self.RBC_count = convertToBinaryData(RBC_count) 
        self.raw_video_id = raw_video_id        
                
        self.confirmation = 0
    def confirm():
        self.confirmation = 1
        ### need to change the record in database!!
        
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insert_result(result):
    try:
        conn = sqlite3.connect('results.db') #create and connect 
        c = conn.cursor()# cursor to access command 
        query = '''
                INSERT INTO results (patient_id ,NRIC_number , 
                operator_id , time , classification, WBC_count, RBC_count, raw_video_id, confirmation)
                VALUES (?,?,?,?,?,?,?,?,?)
                '''
        data_tuple = (result.patient_id, result.NRIC_number, result.operator_id , 
        result.time, result.classification, result.WBC_count, result.RBC_count, 
        result.raw_video_id, result.confirmation)
        
        c.execute(query, data_tuple)
        conn.commit()
        print("inserted successfully into the table")
        c.close()
        print('close successfully')
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("===== the sqlite connection is closed ===== ")
            
def writeTofile(data, filename):
# Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readData(id = None):
    try:
        conn = sqlite3.connect('results.db')
        c = conn.cursor()
        if id: 
            query = """SELECT * from results where id = ?"""
            c.execute(query, (id,))
        else:
            query = """SELECT * from results """
            c.execute(query)
        
        record = c.fetchall()
        for row in record:
            print(row[:6])
            wbc, rbc, video = row[6], row[7], row[8]
            
            entry_folder = r"D:\Capstone\CODE\resume\\" + str(row[0])+ "\\"            
            if not os.path.exists(entry_folder):
                os.makedirs(entry_folder)
            writeTofile(wbc, entry_folder+ "\\wbc.csv")
            writeTofile(rbc, entry_folder+ "\\rbc.csv")
#             writeTofile(video, entry_folder+ "\\video.avi")
            print("Storing blob image and resume on disk \n")

        c.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("===== sqlite connection is closed ===== ")
            
def store_data(data):
    result = Result(data) 
#     result = Result('patient_tyesss', 'G1234565M', 'operator_1', '2020-05-01', 13543, 'features.csv','MK data.csv', 'sample1.avi')
    insert_result(result)
    print('data stored successfully!')
