import cv2
import numpy as np
from imutils.video import FPS
from skimage.feature import blob_dog, blob_log, blob_doh
import math
import time
import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
from pandas import DataFrame


### ----- Parameters to Change ----- ###
H = 140             #No. of pixels to select for height of Region Of Interest
blur_value = 7      #value = 3,5 or 7 (ODD).median Blur value determines the accuracy of detection
Delay = 1           #time value in miliseconds. (Fastest) Minimum = 1ms
Show = 1            #To display the image. 1 = On, 0 = Off
Skip_frames = 20     #number of frames to skip before Im showing
Channels = 28       #number of Channels
### ----- Parameters to Change ----- ###

def bgSubtract(mask,frame):
    fgmask = mask.apply(frame)
    return fgmask

#open file and set all file locations into an array "filename"
def open_video():
    
    root = tk.Tk()
    root.withdraw()
    filename = askopenfilenames(filetypes= [("Import Video File", ("*.avi", "*.mp4"))])
    
    return(filename)


#main initialising 
file = open_video() #Getting all open files location
total_sum = []
roi_sel = []

# cut the frame to only Region of Interest(28 pillars)
for roi in range(len(file)):
    cap = cv2.VideoCapture(file[roi])
    print('***** PROCESSING ROI for RUN %i ***** File:' % (roi+1))
    print(file[roi])

    # Read image start image
    ret, image = cap.read()
    
    # Select ROI
    ## r = Return (x, y ,width , height) from top left corner.
    ## top left corner = (0,0)
    print('Please select the region of interest (ROI)')
    sel = cv2.selectROI(image)
    roi_sel.append(list(sel))
    cv2.destroyAllWindows()
    print('')
print('total number of files :%i' % len(file))
print('total number of ROI :%i' % len(roi_sel))
print('')
    
for cur in range(len(file)):
    cap=cv2.VideoCapture(file[cur])
    print('***** PROCESSING RUN %i ***** File:' % (cur+1),file[cur])
    
    # Read image start image
    ret, frame = cap.read()

    # Select ROI
    ## r = Return (x, y ,width , height) from top left corner.
    ## top left corner = (0,0)
    r = roi_sel[cur]

    #input number of channels
    ch = Channels
    print('[ROI] (x , y, width, height) is', r)

    # Crop image
    y1 = int(r[1])
    y2 = int(r[1]+r[3])
    x1 = int(r[0])
    x2 = int(r[0]+r[2])

    ##print(x1,x2,y1,y2)
    imCrop = frame[y1:(y1+H), x1:x2]

    #the array for sub-channels
    sub_ch = []

    # draw lines on crop frame
    for x in range(ch+1):
        sub_ch_x = round(x*(r[2]/(ch)))
        sub_ch.append(sub_ch_x)
        cv2.line(imCrop, (sub_ch[x],0), (sub_ch[x], H), (200,200,100),1) 

    cv2.namedWindow('Cropped Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Cropped Image',imCrop)
    cv2.waitKey(Delay)
    
    ##initialise all the values
    count=0
    spot_all = []
    #mask = cv2.createBackgroundSubtractorMOG2()
    mask = cv2.createBackgroundSubtractorMOG2(history = 3,
                                                varThreshold = 100,
                                                detectShadows = False)
    sum_ch1 = [0]*ch

    #metrics
    fps = FPS().start()
    start = time.time()
    error = 0
    
    #run count
    while(cap.isOpened()):
            
        count += 1
        ret, pic = cap.read()
        
        # if the frame/pic was not grabbed, then we have reached the end of stream
        if not ret: break
        cycle_start = time.clock()

        pic = pic[y1:(y1+H), x1:x2]
        #crop = bgSubtract(mask,pic)
        # Background Substracting
        crop = mask.apply(pic)
        crop = cv2.medianBlur(crop,blur_value)
        crop = cv2.threshold(crop, 125, 255, cv2.THRESH_BINARY)[1]

        # find contours
        contours, hierarcy = cv2.findContours(crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # list of all the coordinates (tuples) of each cell
        coord_list = [] 

        # to find the coordinates of the cells
        # to decide which channel it is in and update the channel cell count
        for i in range(len(contours)):
            avg = np.mean(contours[i], axis = 0)
            coord = (int(avg[0][0]), int(avg[0][1])) ##Coord is (y,x)
            if Show == 1:
                cv2.circle(pic, coord, 10, (255, 0, 255), 1)
            ch_pos = int(math.floor((coord[0])/sub_ch[1]))
            try:
                # add one count to a channel at ch_pos
                sum_ch1[ch_pos] += 1
            except:
                error += 1

        #show the counting
        if Show == 1 and count%Skip_frames == 0:
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.imshow('frame', pic)
            #set the time delay to 1 ms so that the thread is freed up to do the processing we want to do.
            cv2.waitKey(Delay)

        fps.update()
        cycle_end = time.clock()

    end=time.time()
    fps.stop()
    
    #set an array of sub channel dimension
    print('[RESULTS] for RUN',(cur+1),'is ', sum_ch1)
    print('[ERROR] Count is: ',error)    

    # stop the timer and display FPS information
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    print('[INFO] Each cycle time taken = %0.5fs'%(cycle_end-cycle_start))
    print('----------------------------------------------------------------------')

    cap.release()    
    cv2.destroyAllWindows()

    # sum_chl is for count in one frame
    total_sum.append(sum_ch1)

###write dataframes and export to an Excel file
check = 0 
title = []
for j in range(len(total_sum)):
    if check < len(total_sum[j]):
        check = len(total_sum[j])
    title.append('Run %i '%(j+1)+str(file[j]))

index=np.arange(0,check,1)

for k in range(len(total_sum)):
    if len(total_sum[k]) < check:
        for l in range(len(total_sum[k]),check):
            total_sum[k].append(0)

TTotal_sum = list(map(list, zip(*total_sum)))
#print(TTotal_sum)
df = DataFrame(data=TTotal_sum, columns = title)
savefile = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),("All files", "*.*") )) 
df.to_excel(savefile+".xlsx", index=False, sheet_name="Results")


