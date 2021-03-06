from PyQt5.QtWidgets import *
import time
from datetime import datetime
from pynput.keyboard import Key, Controller
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from autofocus import autofocus
from gpio_test import card_tap
from generate_features import generate_features
from data_storage import store_data
import traceback
from classification import classification
from PyQt5.QtCore import *
from getpass import getpass
from login import *

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.worker_signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.worker_signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.worker_signals.finished.emit()

            
class MainWindow(QMainWindow):        
#     def login_page(self):
#         self.ui = Ui_Form()
#         self.ui.resize(1024, 600)        
#         self.ui.show()
        
    def new_main_page(self):
        self.ui = MainWindow(self.staff_id_value)
        self.ui.resize(1024, 600)        
        self.ui.show()
        
    def btn_exit_handler(self):                        
        self.close()       
        
    def new_patient_instance(self):
        self.close() 
        self.new_main_page()
        
        
    def __init__(self, staff_id_value):
        super().__init__()
        self.count = -1
        self.WBC_count = None
        self.RBC_count = None
        self.video_id = None
        self.time = datetime.now()
         
        self.green = QPixmap('green tick.png').scaled(32, 32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.grey = QPixmap('grey tick.png').scaled(32, 32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.white = QPixmap('white tick.png').scaled(32, 32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)   
        
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(780, 100, 200, 390))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.formLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QtWidgets.QLabel('System Prep',self.formLayoutWidget) 
        self.label.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel('Chip Priming', self.formLayoutWidget)
        self.label_2.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel('Test', self.formLayoutWidget)
        self.label_3.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.verticalLayout.addWidget(self.label_3)        
        self.label_4 = QtWidgets.QLabel('Data Conversion',self.formLayoutWidget)
        self.label_4.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel('Data Analysis',self.formLayoutWidget)
        self.label_5.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.verticalLayout.addWidget(self.label_5)
        
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel('Data Analysis',self.formLayoutWidget)
        self.label_5.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.verticalLayout.addWidget(self.label_5)
        
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(730, 100, 70, 390))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.formLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        
        ## loading ticks
        self.label_6 = QtWidgets.QLabel('label_6',self.formLayoutWidget_2)
        self.label_6.setPixmap(self.white)    
        self.verticalLayout_2.addWidget(self.label_6)        
        self.label_7 = QtWidgets.QLabel("label_7",self.formLayoutWidget_2)
        self.label_7.setPixmap(self.white)   
        self.verticalLayout_2.addWidget(self.label_7)        
        self.label_8 = QtWidgets.QLabel("label_8",self.formLayoutWidget_2)
        self.label_8.setPixmap(self.white)   
        self.verticalLayout_2.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel("label_9",self.formLayoutWidget_2)
        self.label_9.setPixmap(self.white)   
        self.verticalLayout_2.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel("label_10",self.formLayoutWidget_2)
        self.label_10.setPixmap(self.white)   
        self.verticalLayout_2.addWidget(self.label_10)
        
        '''not showing the check list at step1'''
        self.formLayoutWidget.close()
        self.formLayoutWidget_2.close()
        
        ## IDs 
        self.staff_id = QtWidgets.QLineEdit(self.centralwidget)
        self.staff_id.setGeometry(QtCore.QRect(160, 30, 200, 45))
        self.staff_id.setStyleSheet("border: 0px solid blue")    
        self.staff_id.setText(staff_id_value)
        
        self.patient_id = QtWidgets.QLineEdit(self.centralwidget)
        self.patient_id.setGeometry(QtCore.QRect(760, 30, 200, 45))
        self.patient_id.setStyleSheet("border: 0px solid blue")        
        self.loading_label = QtWidgets.QLabel(self.centralwidget)        
        self.loading_label.setGeometry(QtCore.QRect(326, 80, 430, 430))                   
        
        # Buttons
        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setGeometry(QtCore.QRect(30, 500, 190, 60))
        self.cancel_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0);border:0px") 
        self.cancel_btn.clicked.connect(self.btn_exit_handler)    
        
        self.new_patient_btn = QtWidgets.QPushButton(self.centralwidget)
        self.new_patient_btn.setGeometry(QtCore.QRect(30, 390, 190, 60))
        self.new_patient_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0); border:0px")
        self.new_patient_btn.clicked.connect(self.new_patient_instance)    
        
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(740, 500, 220, 65))
        self.start_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0);border:0px;")  
        self.start_btn.clicked.connect(self.step3)
        
        self.scan_label = QtWidgets.QLabel(self.centralwidget)
        self.scan_label.setGeometry(QtCore.QRect(440, 330, 200,100))                  
        self.barcode_image = QPixmap('barcode.png').scaled(150, 90, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.scan_label.setPixmap(self.barcode_image)      
        
        
        self.main_btn = QtWidgets.QPushButton(self.centralwidget)
        self.main_btn.setGeometry(QtCore.QRect(378, 170, 260, 260))
        self.main_btn.setText("Scan Patient \n Barcode")
        self.patient = ""
        self.process = QProcess(self)

        self.patient_id.setEnabled(False)
        self.main_btn.setText("Machine Initialization\n Insert Test Chip")
        self.loading = QPixmap('red bar.png')
        self.loading_label.setPixmap(self.loading)
        self.scan_label.clear()
    
        self.step1()


#     for mannual working flow 
    def button_function(self):
        if self.count == 3:
            self.step3()
        elif self.count == 4:
            self.step4()
        elif self.count == 5:
            self.step5()
        elif self.count == 6:
            self.step6()
        elif self.count == 7:
            self.step7()
        elif self.count == 8:
            self.step8()
        self.count +=1
            

    def step1(self):  # pressure clamp,switch init; optics home
              
#        initiating the clamp code (pressure system connection)         
#        initiating of the pressure system 
#        sequential: camera homing 
 
        self.start_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0);background-image: url('Start button.png');")
        self.loading = QPixmap('green bar.png')
        self.loading_label.setPixmap(self.loading)  
        self.main_btn.setText("Press Start \n to Begin the Test")
        self.count = 3


    def step3(self): # check chip inserted, autofocusing
        self.count = 4
        self.start_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0);border :0px")   
        self.formLayoutWidget.show()
        self.formLayoutWidget_2.show()
        self.main_btn.setText("Autofocusing \n in Progress")
        self.loading_label.setGeometry(QtCore.QRect(300, 80, 430, 430))
        movie = QtGui.QMovie("loading.gif")
        self.loading_label.setMovie(movie)
        movie.start() 
        self.label.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_6.setPixmap(self.grey)    
                
# assumed chip inserted
# autofocusing of optics system
        try:
            autofocusing()
        except:
            print("autofocusing failed")  
        self.step4() # automatic shift to next step
        
        self.label.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.label_2.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_6.setPixmap(self.green)
        self.label_7.setPixmap(self.grey)
        self.main_btn.setText("Priming \n in Progress")
        
    def step4(self):  # priming: pressure(clamp and swtich control) 
  #     primung process: call both Arduino to pressure valves control and sensor      
    
        self.label_2.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.label_3.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_7.setPixmap(self.green)
        self.label_8.setPixmap(self.grey)
        self.main_btn.setText("Test \n in Progress")

    def step5(self):  # testing: switch/clamp open, pressurize, camera save video 
 # another call of pressure system: both arduino loops     
 # camera reading adn saving video, no arduino call required
 # generate a hashed raw video id 
        self.video_id = "jhdkujhh_video_idnbfjkdbvks" 

        self.label_3.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.label_4.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_8.setPixmap(self.green)
        self.label_9.setPixmap(self.grey)
        self.main_btn.setText("Data Conversion \n in Progress")

    def step6(self):  # data conversion
#  call CV for raw_count csv
        self.WBC_count = 'wbc_count'
        self.RBC_count = 'rbc_count'
        self.label_4.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.label_5.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_9.setPixmap(self.green)
        self.label_10.setPixmap(self.grey)
        self.main_btn.setText("Data Analysis \n in Progress")
      
    
    def step7(self):  # data analysis: get features, classify, store the data       
        # classify
         # get feature from raw csv
        generate_features()

        self.result = (classification() == 1)
        print(self.result)
 
        self.label_4.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_10.setPixmap(self.green)

       # self.step8()
        
        
    def step8(self): #show result, pressure adn optics go home
        self.formLayoutWidget.close()
        self.formLayoutWidget_2.close()
        
        self.loading_label.setGeometry(QtCore.QRect(326, 80, 430, 430))
        self.loading = QPixmap('green bar.png')
        self.loading_label.setPixmap(self.loading) 
        if self.result:  # classification == 1 
            self.main_btn.setText("Result: Positive")
        else:
            self.main_btn.setText("Result: Negative")
        :
        # store the data
        data_entries = (self.patient_id_str, self.patient_nric, self.staff_id_str, self.time, self.result, self.WBC_count, self.RBC_count, self.video_id)
        store_data(data_entries)


'''
step1: prepare {red bar}
step2: prepare finish {green bar; start button}
step3: prepare progress {loading; check list; 0 green, 1 grey, 4 white circles}
step4: priming progress {loading; check list; 1 green, 1 grey, 3 white circles}
step5: test progress {loading; check list; 2 green, 1 grey, 2 white circles}
step6: data conversion progress {loading; check list; 3 green, 1 grey, 1 white circles}
step7: data analytics progress {loading; check list; 4 green, 1 grey, 0 white circles}
step8: showing result {green bar}
'''


stylesheet = """
    MainWindow {
        background-image: url("bg.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
    Ui_Form {
        background-image: url("login_bg.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)     
    window = MainWindow('1234')
    window.showFullScreen()
    window.resize(1024, 600)
    window.show()
    sys.exit(app.exec_())
