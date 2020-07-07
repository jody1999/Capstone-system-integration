from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore.Qt import KeepAspectRatio, FastTransformation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.staff_id.setText("Technician Kerwin")
        
        self.patient_id = QtWidgets.QLineEdit(self.centralwidget)
        self.patient_id.setGeometry(QtCore.QRect(760, 30, 200, 45))
        self.patient_id.setStyleSheet("border: 0px solid blue")
        self.patient_id.setText("G89843883M")
        
        self.loading_label = QtWidgets.QLabel(self.centralwidget)        
        self.loading_label.setGeometry(QtCore.QRect(326, 80, 430, 430))
        self.loading = QPixmap('red bar.png')
        self.loading_label.setPixmap(self.loading)   
                
        # Buttons
        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setGeometry(QtCore.QRect(30, 500, 190, 60))
        self.cancel_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0);") 
        self.cancel_btn.clicked.connect(self.step2)
        
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(740, 500, 220, 65))
        self.start_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0);")   
        self.start_btn.clicked.connect(self.step3)
               
        self.main_btn = QtWidgets.QPushButton(self.centralwidget)
        self.main_btn.setGeometry(QtCore.QRect(378, 170, 260, 260))
        self.main_btn.setText("Prepare and \n Insert Test Chip")
        self.main_btn.setStyleSheet("QPushButton{font-size: 28px;font-family: Arial;color: rgb(255, 255, 255);background-color: rgba(0, 255, 255, 0);}")
        
        self.main_btn.clicked.connect(self.step8)
        
        
        

    def step2(self):
        self.start_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0);background-image: url('Start button.png');")
        self.loading = QPixmap('green bar.png')
        self.loading_label.setPixmap(self.loading)  
        self.main_btn.setText("Press Start \n to Begin the Test")


    def step3(self):
        self.start_btn.setStyleSheet("background-color: rgba(0, 255, 255, 0);")   
        self.formLayoutWidget.show()
        self.formLayoutWidget_2.show()
        self.main_btn.setText("Preparation \n in Progress")
        self.loading_label.setGeometry(QtCore.QRect(300, 80, 430, 430))
        movie = QtGui.QMovie("loading.gif")
        self.loading_label.setMovie(movie)
        movie.start()
        
        self.label.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_6.setPixmap(self.grey)    
        
    def step4(self):
        self.label_1.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.label_2.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_6.setPixmap(self.green)   
        self.label_7.setPixmap(self.grey)  
        self.main_btn.setText("Priming \n in Progress")
    
    def step5(self):
        self.label_2.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.label_3.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_7.setPixmap(self.green)   
        self.label_8.setPixmap(self.grey)    
        self.main_btn.setText("Test \n in Progress")
        
    def step6(self):
        self.label_3.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.label_4.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_8.setPixmap(self.green)   
        self.label_9.setPixmap(self.grey)    
        self.main_btn.setText("Data Conversion \n in Progress")
        
    def step7(self):
        self.label_4.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: grey;")
        self.label_5.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";color: black;")
        self.label_9.setPixmap(self.green)   
        self.label_10.setPixmap(self.grey)    
        self.main_btn.setText("Data Analysis \n in Progress")
        
        
    def step8(self):
        self.formLayoutWidget.close()
        self.formLayoutWidget_2.close()
        
        self.loading_label.setGeometry(QtCore.QRect(326, 80, 430, 430))
        self.loading = QPixmap('green bar.png')
        self.loading_label.setPixmap(self.loading)  
        self.main_btn.setText("Result: ")
        

       
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
"""

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)     
    window = MainWindow()
    window.resize(1024, 600)
    window.show()
    sys.exit(app.exec_())