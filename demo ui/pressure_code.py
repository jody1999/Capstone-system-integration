import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = 'T' # To circumvent ffortl error
import numpy as np # must be above PySpin in modules importing, else there will be mk1 error
import serial
import queue
import time

def pressure_run():
    # serial comms with arduino
    arduino = serial.Serial('COM3', 115200, timeout=0.04)

    # send first arduino signal
    arduino.write('S'.encode())



    # let the pressure check only work for once instead of loop??
    # or keep the loop inside ino code, we manually cut the loop in the python using...

    # ending arduino signal
    arduino.write('E'.encode())