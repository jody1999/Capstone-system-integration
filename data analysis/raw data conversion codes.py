# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 18:30:01 2020

@author: Marcus
"""

import pandas as pd
import numpy as np

WBC_Raw = pd.read_csv('Raw.csv')
RBC_Raw = pd.read_csv('RBC_Raw.csv')
count_para = pd.read_csv('Count.csv')


def WBC_Total(data_WBC):
    InvL35_cols = data_WBC.iloc[:,2:37]
    InvL350_cols = data_WBC.iloc[:,37:72]
    L35_cols = data_WBC.iloc[:,72:107]
    L350_cols = data_WBC.iloc[:,107:142]
    
    InvL35_Total = np.asarray(InvL35_cols.sum(axis=1), dtype=np.float)
    InvL350_Total = np.asarray(InvL350_cols.sum(axis=1), dtype=np.float)
    L35_Total = np.asarray(L35_cols.sum(axis=1), dtype=np.float)
    L350_Total = np.asarray(L350_cols.sum(axis=1), dtype=np.float)
    
    data_T = {'InvL35.Total':InvL35_Total, 'InvL350.Total':InvL350_Total,'L35.Total':L35_Total,'L350.Total':L350_Total}
    Totals = pd.DataFrame(data_T)
    return Totals


def WBC_Counts(total_WBC,data_CountPara):
    InvL35_WBC_s = np.asarray((total_WBC['InvL35.Total'] * 1000000)/ (data_CountPara['InvL35_Exposure(us)'] * data_CountPara['InvL35_Total Frames']))
    InvL350_WBC_s= np.asarray((total_WBC['InvL350.Total'] * 1000000)/ (data_CountPara['InvL350_Exposure(us)'] * data_CountPara['InvL350_Total Frames']))
    L35_WBC_s= np.asarray((total_WBC['L35.Total'] * 1000000)/ (data_CountPara['L35_Exposure(us)'] * data_CountPara['L35_Total Frames']))
    L350_WBC_s = np.asarray((total_WBC['L350.Total'] * 1000000)/ (data_CountPara['L350_Exposure(us)'] * data_CountPara['L350_Total Frames']))

    data_Counts = {'InvL35.WBC.s':InvL35_WBC_s, 'InvL350.WBC.s':InvL350_WBC_s,'L35.WBC.s':L35_WBC_s,'L350.WBC.s':L350_WBC_s}
    Counts = pd.DataFrame(data_Counts)
    return Counts

    
def WBC_Means(data_WBC,total_WBC):
    CountM = pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['count1m','count2m','count3m','count4m'])
    Adder = pd.DataFrame(float(1), index=np.arange(len(data_WBC)), columns=['add1'])
    
    Means = pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['InvL35.Mean','InvL350.Mean','L35.Mean','L350.Mean'])

    for a in range(2,37):
        Means['InvL35.Mean'] += CountM['count1m']*data_WBC.iloc[:,a]
        CountM['count1m'] += Adder['add1']

    for b in range(37,72):
        Means['InvL350.Mean'] += CountM['count2m']*data_WBC.iloc[:,b]
        CountM['count2m'] += Adder['add1']

    for c in range(72,107):
        Means['L35.Mean'] += CountM['count3m']*data_WBC.iloc[:,c]
        CountM['count3m'] += Adder['add1']

    for d in range(107,142):
        Means['L350.Mean'] += CountM['count4m']*data_WBC.iloc[:,d]
        CountM['count4m'] += Adder['add1']    

    Means['InvL35.Mean'] = Means['InvL35.Mean']/total_WBC['InvL35.Total']
    Means['InvL350.Mean'] = Means['InvL350.Mean']/total_WBC['InvL350.Total']
    Means['L35.Mean'] = Means['L35.Mean']/total_WBC['L35.Total']
    Means['L350.Mean'] = Means['L350.Mean']/total_WBC['L350.Total']  
    return Means


def WBC_SD(data_WBC, means_WBC, total_WBC):
    Counts = pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['count1s','count2s','count3s','count4s'])
    Adder = pd.DataFrame(float(1), index=np.arange(len(data_WBC)), columns=['add1'])
    
    SD = pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['InvL35.SD','InvL350.SD','L35.SD','L350.SD'])
    
    for a in range(2,37):
        SD['InvL35.SD'] += data_WBC.iloc[:,a]*((Counts['count1s'] - means_WBC['InvL35.Mean'])**2)
        Counts['count1s'] += Adder['add1']

    for b in range(37,72):
        SD['InvL350.SD'] += data_WBC.iloc[:,b]*((Counts['count2s'] - means_WBC['InvL350.Mean'])**2)
        Counts['count2s'] += Adder['add1']

    for c in range(72,107):
        SD['L35.SD'] += data_WBC.iloc[:,c]*((Counts['count3s'] - means_WBC['L35.Mean'])**2)
        Counts['count3s'] += Adder['add1']

    for d in range(107,142):
        SD['L350.SD'] += data_WBC.iloc[:,d]*((Counts['count4s'] - means_WBC['L350.Mean'])**2)
        Counts['count4s'] += Adder['add1']
    
    SD['InvL35.SD'] = (SD['InvL35.SD'] / total_WBC['InvL35.Total'])**0.5
    SD['InvL350.SD'] = (SD['InvL350.SD'] / total_WBC['InvL350.Total'])**0.5
    SD['L35.SD'] = (SD['L35.SD'] / total_WBC['L35.Total'])**0.5
    SD['L350.SD'] = (SD['L350.SD'] / total_WBC['L350.Total'])**0.5
    
    return SD


def WBC_Skew(data_WBC,means_WBC,sd_WBC,total_WBC):
    CountSkew = pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['count1sk','count2sk','count3sk','count4sk'])
    Adder = pd.DataFrame(float(1), index=np.arange(len(data_WBC)), columns=['add1'])
    
    Skew = pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['InvL35.Skewness','InvL350.Skewness','L35.Skewness','L350.Skewness'])
    
    for a in range(2,37):
        Skew['InvL35.Skewness'] += data_WBC.iloc[:,a]*((CountSkew['count1sk'] - means_WBC['InvL35.Mean'])**3)
        CountSkew['count1sk'] += Adder['add1']

    for b in range(37,72):
        Skew['InvL350.Skewness'] += data_WBC.iloc[:,b]*((CountSkew['count2sk'] - means_WBC['InvL350.Mean'])**3)
        CountSkew['count2sk'] += Adder['add1']

    for c in range(72,107):
        Skew['L35.Skewness'] += data_WBC.iloc[:,c]*((CountSkew['count3sk'] - means_WBC['L35.Mean'])**3)
        CountSkew['count3sk'] += Adder['add1']

    for d in range(107,142):
        Skew['L350.Skewness'] += data_WBC.iloc[:,d]*((CountSkew['count4sk'] - means_WBC['L350.Mean'])**3)
        CountSkew['count4sk'] += Adder['add1']

    Skew['InvL35.Skewness'] = Skew['InvL35.Skewness']*((total_WBC['InvL35.Total']-1)**0.5)/((total_WBC['InvL35.Total']-2)*(total_WBC['InvL35.Total']**0.5))/(sd_WBC['InvL35.SD']**3)
    Skew['InvL350.Skewness'] = Skew['InvL350.Skewness']*((total_WBC['InvL350.Total']-1)**0.5)/((total_WBC['InvL350.Total']-2)*(total_WBC['InvL350.Total']**0.5))/(sd_WBC['InvL350.SD']**3)
    Skew['L35.Skewness'] = Skew['L35.Skewness']*((total_WBC['L35.Total']-1)**0.5)/((total_WBC['L35.Total']-2)*(total_WBC['L35.Total']**0.5))/(sd_WBC['L35.SD']**3)
    Skew['L350.Skewness'] = Skew['L350.Skewness']*((total_WBC['L350.Total']-1)**0.5)/((total_WBC['L350.Total']-2)*(total_WBC['L350.Total']**0.5))/(sd_WBC['L350.SD']**3)

    return Skew

def WBC_Kurt(data_WBC,means_WBC,sd_WBC,total_WBC):
    CountK = pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['count1k','count2k','count3k','count4k'])
    Adder = pd.DataFrame(float(1), index=np.arange(len(data_WBC)), columns=['add1'])
    
    Kurt = pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['InvL35.Kurt','InvL350.Kurt','L35.Kurt','L350.Kurt'])
    
    for a in range(2,37):
        Kurt['InvL35.Kurt'] += data_WBC.iloc[:,a]*((CountK['count1k'] - means_WBC['InvL35.Mean'])**4)
        CountK['count1k'] += Adder['add1']

    for b in range(37,72):
        Kurt['InvL350.Kurt'] += data_WBC.iloc[:,b]*((CountK['count2k'] - means_WBC['InvL350.Mean'])**4)
        CountK['count2k'] += Adder['add1']

    for c in range(72,107):
        Kurt['L35.Kurt'] += data_WBC.iloc[:,c]*((CountK['count3k'] - means_WBC['L35.Mean'])**4)
        CountK['count3k'] += Adder['add1']

    for d in range(107,142):
        Kurt['L350.Kurt'] += data_WBC.iloc[:,d]*((CountK['count4k'] - means_WBC['L350.Mean'])**4)
        CountK['count4k'] += Adder['add1']
        
    Kurt['InvL35.Kurt'] = Kurt['InvL35.Kurt']/(total_WBC['InvL35.Total']*(sd_WBC['InvL35.SD']**4))
    Kurt['InvL350.Kurt'] = Kurt['InvL350.Kurt']/(total_WBC['InvL350.Total']*(sd_WBC['InvL350.SD']**4))
    Kurt['L35.Kurt'] = Kurt['L35.Kurt']/(total_WBC['L35.Total']*(sd_WBC['L35.SD']**4))
    Kurt['L350.Kurt'] = Kurt['L350.Kurt']/(total_WBC['L350.Total']*(sd_WBC['L350.SD']**4))
    
    return Kurt


def RBC_Total(data_RBC):
    InvL35_Rcols = data_RBC.iloc[:,2:18]
    InvL350_Rcols = data_RBC.iloc[:,18:34]
    L35_Rcols = data_RBC.iloc[:,34:50]
    L350_Rcols = data_RBC.iloc[:,50:66]
    
    InvL35_RTotal = np.asarray(InvL35_Rcols.sum(axis=1), dtype=np.float)
    InvL350_RTotal = np.asarray(InvL350_Rcols.sum(axis=1), dtype=np.float)
    L35_RTotal = np.asarray(L35_Rcols.sum(axis=1), dtype=np.float)
    L350_RTotal = np.asarray(L350_Rcols.sum(axis=1), dtype=np.float)
    
    data_RT = {'R_InvL35.Total':InvL35_RTotal, 'R_InvL350.Total':InvL350_RTotal,'R_L35.Total':L35_RTotal,'R_L350.Total':L350_RTotal}
    RTotals = pd.DataFrame(data_RT)
    return RTotals


def RBC_Means(data_RBC, total_RBC):
    CountR = pd.DataFrame(float(0), index=np.arange(len(data_RBC)), columns=['count1r','count2r','count3r','count4r'])
    Adder = pd.DataFrame(float(1), index=np.arange(len(data_RBC)), columns=['add1'])
    
    r_means = pd.DataFrame(float(0), index=np.arange(len(data_RBC)), columns=['R_InvL35.Mean','R_InvL350.Mean','R_L35.Mean','R_L350.Mean'])

    for a in range(2,18):
        r_means['R_InvL35.Mean'] += CountR['count1r']*data_RBC.iloc[:,a]
        CountR['count1r'] += Adder['add1']

    for b in range(18,34):
        r_means['R_InvL350.Mean'] += CountR['count2r']*data_RBC.iloc[:,b]
        CountR['count2r'] += Adder['add1']

    for c in range(34,50):
        r_means['R_L35.Mean'] += CountR['count3r']*data_RBC.iloc[:,c]
        CountR['count3r'] += Adder['add1']

    for d in range(50,66):
        r_means['R_L350.Mean'] += CountR['count4r']*data_RBC.iloc[:,d]
        CountR['count4r'] += Adder['add1']    

    r_means['R_InvL35.Mean'] = r_means['R_InvL35.Mean']/total_RBC['R_InvL35.Total']
    r_means['R_InvL350.Mean'] = r_means['R_InvL350.Mean']/total_RBC['R_InvL350.Total']
    r_means['R_L35.Mean'] = r_means['R_L35.Mean']/total_RBC['R_L35.Total']
    r_means['R_L350.Mean'] = r_means['R_L350.Mean']/total_RBC['R_L350.Total']
    
    return r_means


def Basic_Features(data_WBC,data_CountPara,data_RBC):
    W_Total = WBC_Total(data_WBC)
    W_Mean = WBC_Means(data_WBC,W_Total)
    SD = WBC_SD(data_WBC, W_Mean, W_Total)
    Skew = WBC_Skew(data_WBC,W_Mean,SD,W_Total)
    Kurt = WBC_Kurt(data_WBC,W_Mean,SD,W_Total)
    Patient = data_WBC['Patient']
    Count = WBC_Counts(W_Total,data_CountPara)
    Sample = data_WBC['Sample']

    R_Total = RBC_Total(data_RBC)
    R_Mean = RBC_Means(data_RBC, R_Total)
    
    Size =  pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['Size_InvL35','Size_InvL350','Size_L35','Size_L350'])
    Size['Size_InvL35'] = 5.8 + (W_Mean['InvL35.Mean']-R_Mean['R_InvL35.Mean'])*0.2
    Size['Size_InvL350'] = 5.8 + (W_Mean['InvL350.Mean']-R_Mean['R_InvL350.Mean'])*0.2
    Size['Size_L35'] = 5.8 + (W_Mean['L35.Mean']-R_Mean['R_L35.Mean'])*0.2
    Size['Size_L350'] = 5.8 + (W_Mean['L350.Mean']-R_Mean['R_L350.Mean'])*0.2

    MeanSize =  pd.DataFrame(float(0), index=np.arange(len(data_WBC)), columns=['MeanSize_35','MeanSize_350','MeanSize_InvL','MeanSize_L'])
    MeanSize['MeanSize_35'] = 0.5*Size['Size_InvL35'] + 0.5*Size['Size_L35']
    MeanSize['MeanSize_350'] = 0.5*Size['Size_InvL350'] + 0.5*Size['Size_L350']
    MeanSize['MeanSize_InvL'] = 0.5*Size['Size_InvL35'] + 0.5*Size['Size_InvL350']
    MeanSize['MeanSize_L'] = 0.5*Size['Size_L35'] + 0.5*Size['Size_L350']
    
    Df = pd.concat([Sample,Patient,W_Mean,Size,MeanSize,SD,Skew,Kurt,Count],axis=1)
    return Df

Basic_Dataset = Basic_Features(WBC_Raw,count_para,RBC_Raw)
















