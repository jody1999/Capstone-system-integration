from PyQt5 import QtCore, QtGui, QtWidgets
from demo import  *
from PyQt5 import QtWidgets
import sqlite3


class Ui_Form(QMainWindow):

    def openwindow(self, staff_id_value):
        print('start new patient instance')
        self.ui = MainWindow(staff_id_value)
        self.ui.resize(1024, 600)
        self.ui.show()
#         self.close()

    def __init__(self):
        super().__init__()
        self.staff_id_value = ''
        self.gridLayoutWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.gridLayoutWidget)   
    
        # to be replace by the RFID code
        self.staff_id = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.staff_id.setGeometry(QtCore.QRect(160, 30, 200, 45))
        self.staff_id.setStyleSheet("background-color: rgba(0, 255, 255, 0);border: 0px solid blue") 
        
        self.btn_next = QtWidgets.QPushButton(self.gridLayoutWidget)    
        self.btn_next.setGeometry(QtCore.QRect(378, 170, 260, 260))
        self.btn_next.setStyleSheet("QPushButton{font-size: 28px;font-family: Arial;color: rgb(255, 255, 255);background-color: rgba(0, 255, 255, 0);}")     
        self.btn_next.setText("CLICK TO START")
        
        QtCore.QMetaObject.connectSlotsByName(self.gridLayoutWidget)
        self.btn_next.clicked.connect(self.button)
        
    def button(self):
        self.btn_next.setText("Tap Staff ID \n to Login")
        ####
        # activate the rfid reading
        # once read, call function btn_login_handler()
        self.btn_login_handler()


    def pop_window(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("{}".format(text))
        msg.setWindowTitle("{}".format(text))
        msg.exec_()
       
    def btn_login_handler(self):
        username = self.staff_id.text()
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT username FROM credentials")
        val = cursor.fetchall()
        valid = False
        if len(val) >= 1:
             for x in val:
                if username in x[0]:
                    valid = True
                    break
        if valid:
            print('Welcome')
#             self.openwindow(username)
            self.openwindow('passed from login')
        else:
            print('No user Found')
            self.pop_window('No user Found')
        
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
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)       
    ui = Ui_Form()
    ui.resize(1024, 600)
    ui.show()
    sys.exit(app.exec_())
