from PyQt5 import QtCore, QtGui, QtWidgets
# from main_gui import  *
from demo import  *
from PyQt5 import QtWidgets
import sqlite3


class Ui_Form(object):

    def openwindow(self):
        self.window = QtWidgets.QMainWindow()
        print('open main window')
        self.ui = MainWindow()
        self.ui.resize(1024, 600)
        self.ui.show()
        Form.hide()

    def setupUi(self, Form):
        Form.resize(1024, 600)
        self.textBrowser = QtWidgets.QLabel("LOGO",Form)
        self.textBrowser.setGeometry(QtCore.QRect(150, 10, 361, 61))
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(100, 90, 431, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
       
        self.l_username = QtWidgets.QLabel('username',self.gridLayoutWidget)
        self.gridLayout.addWidget(self.l_username, 0, 0, 1, 1)
        self.txt_username = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.txt_username, 0, 1, 1, 1)
        
        self.btn_next = QtWidgets.QPushButton('Next',self.gridLayoutWidget)
        self.gridLayout.addWidget(self.btn_next, 2, 1, 1, 1)
        
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.btn_next.clicked.connect(self.btn_login_handler)

    def pop_window(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("{}".format(text))
        msg.setWindowTitle("{}".format(text))
        msg.exec_()
       
    def btn_login_handler(self):
        username = self.txt_username.text()
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
            self.openwindow()
        else:
            print('No user Found')
            self.pop_window('No user Found')

        
stylesheet = """
    MainWindow {
        background-image: url("bg.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)   
    
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
