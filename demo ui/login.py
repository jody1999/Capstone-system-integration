from PyQt5 import QtCore, QtGui, QtWidgets
from demo import  *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
import sqlite3
import time

class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal()
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
        else:
            self.worker_signals.result.emit()
        finally:
            self.worker_signals.finished.emit()

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
    

        self.staff_id = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.staff_id.setGeometry(QtCore.QRect(160, 30, 200, 45))
        self.staff_id.setStyleSheet("background-color: rgba(0, 255, 255, 255);border: 0px solid blue")
        self.staff_id.setEnabled(False)
        
        self.btn_next = QtWidgets.QPushButton(self.gridLayoutWidget)    
        self.btn_next.setGeometry(QtCore.QRect(378, 170, 260, 260))
        self.btn_next.setStyleSheet("QPushButton{font-size: 28px;font-family: Arial;color: rgb(255, 255, 255);background-color: rgba(0, 255, 255, 0); border: 0px;}")
        self.btn_next.setText("CLICK TO START")
        
        QtCore.QMetaObject.connectSlotsByName(self.gridLayoutWidget)
        self.btn_next.clicked.connect(self.button)
        self.thread = QThreadPool()
        # self.worker = Worker(self.rfid)
        
    def button(self):
        # to be replace by the RFID code
        self.btn_next.setText("Tap Staff ID \n to Login")
        self.worker = Worker(self.rfid)
        # self.worker.worker_signals.finished.connect(self.button) #, self.btn_login_handler
        self.worker.worker_signals.result.connect(self.set_elements)
        self.thread.start(self.worker)
        ####
        # activate the rfid reading
        # once read, call function btn_login_handler()


    # def thread_execute(self):
    #     worker = Worker(self.rfid)
    #     worker.worker_signals.finished.connect(self.set_elements)
    #     self.threadpool.start(worker)

    def set_elements(self):
        self.staff_id.setText(self.staff_id_value)

        self.btn_login_handler()

    def rfid(self):
        #     card tap and read user id
        # self.main_btn.setText("Tap Staff ID \n to Login")
        self.staff_id_value = str(card_tap())
        print(self.staff_id_value)


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
            self.staff_id_value = ""
        
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
