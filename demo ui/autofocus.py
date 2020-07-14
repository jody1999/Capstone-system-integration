import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = 'T' # To circumvent ffortl error
import numpy as np # must be above PySpin in modules importing, else there will be mk1 error
import PySpin
import cv2
import matplotlib.pyplot as plt
from  scipy import ndimage
import serial
import queue
import time

def autofocus():
    
    #key variables
    Capture_FPS = 25    #Capture FPS used for show and test
    exposure = 20000      #time in us
    gain = 0            #gain value 0-40
    font = cv2.FONT_HERSHEY_SIMPLEX
    Contvalue_C = []  # for storing of contrast values to set threshold
    Contvalue2_C = []

    # values for ROI
    x1 = 600
    x2 = x1 + 200
    y1 = 200
    y2 = y1 + 200



    ### initialize the camera ###
    # get system000
    system = PySpin.System.GetInstance()

    # get camera list
    cam_list = system.GetCameras()
    print(cam_list)

    # use primary camera
    cam = cam_list.GetByIndex(0)

    # initialize camera
    cam.Init()

    ### Camera setting ###
    # Set acquisition mode to continuous
    cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)

    # turn off auto exposure
    cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)

    # Ensure desired exposure time does not exceed the maximum
    exposure_time_to_set = exposure   #in us
    exposure_time_to_set = min(cam.ExposureTime.GetMax(), exposure_time_to_set)
    cam.ExposureTime.SetValue(exposure_time_to_set)

    # set width to maximum
    cam.OffsetX.SetValue(0)
    ##cam.Width.SetValue(cam.Width.GetMax())

    # set height to value
    ##cam.Height.SetValue(cam.Height.GetMax())
    cam.OffsetY.SetValue(0)
    ##cam.Height.SetValue(cam.Height.GetMax())

    # set gain
    cam.GainAuto.SetValue(PySpin.GainAuto_Off)
    cam.Gain.SetValue(gain)

    # frame rate
    cam.AcquisitionFrameRateEnable.SetValue(True)
    cam.AcquisitionFrameRate.SetValue(Capture_FPS)
    framerate = cam.AcquisitionFrameRate.GetValue()

    # serial comms with arduino
    arduino = serial.Serial('COM3', 115200, timeout=0.04)
    time.sleep(1)
    arduino.flushInput()
    arduino.flushOutput()
    time.sleep(1)

    cam.BeginAcquisition()
    run = 1

    # send first arduino signal
    arduino.write('S'.encode())

    start = time.time()
    while(run):
        # Acquire images
        image = cam.GetNextImage()
        image_main = image.GetNDArray()
        image_denoised = cv2.medianBlur(image_main, 3)
        image_roi = image_denoised[y1:y2, x1:x2]

        # Canny edge detection
        can = cv2.Canny(image_roi, 100, 200)
        can = np.uint8(np.absolute(can))
        can_sum = np.sum(can)

        Contvalue_C.append(can_sum)

        cv2.putText(image_denoised, str(can_sum), (100, 50), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.imshow('livestream', image_denoised)
        cv2.waitKey(1)

        if time.time() - start > 7:
            cv2.destroyAllWindows()
            cam.EndAcquisition()
            run = 0
            break

        else:
            continue

    threshold = 0.9 * max(Contvalue_C)
    cam.BeginAcquisition()
    run = 1

    # second signal to Arduino to move to focused position
    arduino.write('R'.encode())

    while(run):
        # Get image
        image = cam.GetNextImage()
        image_main = image.GetNDArray()
        image_denoised = cv2.medianBlur(image_main, 3)
        image_roi = image_denoised[y1:y2, x1:x2]


        # Canny edge detection
        can2 = cv2.Canny(image_roi, 100, 200)
        can2 = np.uint8(np.absolute(can2))
        can2_sum = np.sum(can2)

        Contvalue2_C.append(can2_sum)

        cv2.putText(image_denoised, str(can2_sum), (100, 50), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image_denoised, str(threshold), (100, 100), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.imshow('livestream', image_denoised)
        cv2.waitKey(1)

        # if measured value is greater than threshold, send signal to arduino to stop motor motion
        if can2_sum > threshold:
            arduino.write('E'.encode())
            return False
    #         cv2.putText(image_denoised, "Auto-focus completed!", (200, 50), font, 2, (0, 255, 0), 1, cv2.LINE_AA)
    return True


