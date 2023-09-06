# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 22:15:15 2023

@author: Jasleen
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

coef0 = -1.5334
coef1 = 11.3356
coef2 = -21.2098 
coef3 = 19.4511 
coef4 = -8.5243
coef5 = 1.4513 


currWindMS = 0.2671
currSolarMS = 0.044
currNuclearMS = 0.1546

currAvgDemand = 33034.61343

ltsRTE = 0.5
stsRTE = 0.75

dataset = pd.read_csv("Data_Solar.csv")
solar = dataset["SOLAR"].to_numpy()
wind = dataset["WIND"].to_numpy()
nuclear = dataset["NUCLEAR"].to_numpy()
others = np.empty(solar.size)
others.fill(currAvgDemand)
total = dataset["Total"].to_numpy()
normLTSInput = dataset["NormLTSInput"].to_numpy()
normSTSInput = dataset["NormSTSInput"].to_numpy()
normLTSOutput = dataset["NormLTSOutput"].to_numpy()
normSTSOutput = dataset["NormSTSOutput"].to_numpy()

def PredictVF(targetWindMS, targetSolarMS, targetNuclearMS, targetOtherMS, ltsGen, stsGen):
    windScale = targetWindMS / currWindMS
    solarScale = targetSolarMS / currSolarMS
    nuclearScale = targetNuclearMS/currNuclearMS
    avgSolar = currAvgDemand * targetSolarMS
    ltsFactorOut = ltsGen * avgSolar
    stsFactorOut = stsGen * avgSolar
    ltsFactorIn = ltsFactorOut / ltsRTE
    stsFactorIn = stsFactorOut / stsRTE
    
    solarGen = solar * solarScale
    windGen = wind * windScale
    nuclearGen = nuclear * nuclearScale
    othersGen = others * targetOtherMS
    storageGen = normLTSOutput * ltsFactorOut - normLTSInput * ltsFactorIn + normSTSOutput * stsFactorOut - normSTSInput * stsFactorIn
    solarGen = solarGen + storageGen
    residualDemand = total - solarGen - windGen - nuclearGen - othersGen 
    residualDemand = np.where(residualDemand < 0, 0, residualDemand)
    
    avgResidual = np.sum(residualDemand,axis=0)/residualDemand.size
    normResidual = residualDemand/avgResidual
    predPrice = coef0 + normResidual * coef1 + np.power(normResidual,2) * coef2 + np.power(normResidual,3) * coef3 + np.power(normResidual,4) * coef4 + np.power(normResidual,5) * coef5
    
    solarPriceMult = predPrice*solarGen
    valueFactor = (np.sum(solarPriceMult,axis=0)*solarPriceMult.size)/(np.sum(predPrice,axis=0)*np.sum(solarGen,axis=0))
    return valueFactor

with open('solarVfCurr.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    header = ["Solar Market Share", "Value Factor"]
    writer.writerow(header)
    
    endSolarMS = 0.25
    stepSolarMS = 0.01
    for solarIndex in range(1, int(endSolarMS/stepSolarMS)+1):
        targetSolarMS = solarIndex*stepSolarMS
    
        targetNuclearMS = 0.1546
        targetWindMS = 0.2671
        targetOtherMS = 0
        ltsGen = 0.0
        stsGen = 0.0
        
        row = [targetSolarMS]
        
        valueFactor = PredictVF(targetWindMS, targetSolarMS, targetNuclearMS, targetOtherMS, ltsGen, stsGen)
        row.append(valueFactor)
            
        writer.writerow(row)
        
with open('solarVfwrtWindMS.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    header = ["Solar Market Share"]
    msList = []
    for index in range(0,5):
        msList.append(index*0.1)
        header.append("Wind MS " + str(index*10) + "%")
    

    writer.writerow(header)
    
    endSolarMS = 0.25
    stepSolarMS = 0.01
    for solarIndex in range(1, int(endSolarMS/stepSolarMS)+1):
        targetSolarMS = solarIndex*stepSolarMS
    
        targetNuclearMS = 0.2
        targetOtherMS = 0
        ltsGen = 0.0
        stsGen = 0.0
        
        row = [targetSolarMS]
        
        for ms in msList:
            targetWindMS = ms
            
            valueFactor = PredictVF(targetWindMS, targetSolarMS, targetNuclearMS, targetOtherMS, ltsGen, stsGen)
            row.append(valueFactor)
            
        writer.writerow(row)
        
with open('solarVfwrtNuclearMS.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    header = ["Solar Market Share"]
    msList = []
    for index in range(0,5):
        msList.append(index*0.1)
        header.append("Nuclear MS " + str(index*10) + "%")
    

    writer.writerow(header)
    
    endSolarMS = 0.25
    stepSolarMS = 0.01
    for solarIndex in range(1, int(endSolarMS/stepSolarMS)+1):
        targetSolarMS = solarIndex*stepSolarMS
    
        targetWindMS = 0.2
        targetOtherMS = 0
        ltsGen = 0.0
        stsGen = 0.0
        
        row = [targetSolarMS]
        
        for ms in msList:
            targetNuclearMS = ms
            
            valueFactor = PredictVF(targetWindMS, targetSolarMS, targetNuclearMS, targetOtherMS, ltsGen, stsGen)
            row.append(valueFactor)
            
        writer.writerow(row)
        

with open('solarVfwrtLTS.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    header = ["Solar Market Share"]
    msList = []
    for index in range(0,5):
        msList.append(index*0.1)
        header.append("LTS " + str(index*10) + "%")
    

    writer.writerow(header)
    
    endSolarMS = 0.25
    stepSolarMS = 0.01
    for solarIndex in range(1, int(endSolarMS/stepSolarMS)+1):
        targetSolarMS = solarIndex*stepSolarMS
    
        targetWindMS = 0.2
        targetNuclearMS = 0.2
        targetOtherMS = 0
        stsGen = 0.0
        
        row = [targetSolarMS]
        
        for ms in msList:
            ltsGen = ms
            
            valueFactor = PredictVF(targetWindMS, targetSolarMS, targetNuclearMS, targetOtherMS, ltsGen, stsGen)
            row.append(valueFactor)
            
        writer.writerow(row)
        
        
with open('solarVfwrtSTS.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    header = ["Solar Market Share"]
    msList = []
    for index in range(0,5):
        msList.append(index*0.1)
        header.append("STS " + str(index*10) + "%")
    

    writer.writerow(header)
    
    endSolarMS = 0.25
    stepSolarMS = 0.01
    for solarIndex in range(1, int(endSolarMS/stepSolarMS)+1):
        targetSolarMS = solarIndex*stepSolarMS
    
        targetWindMS = 0.2
        targetNuclearMS = 0.2
        targetOtherMS = 0
        ltsGen = 0.0
        
        row = [targetSolarMS]
        
        for ms in msList:
            stsGen = ms
            
            valueFactor = PredictVF(targetWindMS, targetSolarMS, targetNuclearMS, targetOtherMS, ltsGen, stsGen)
            row.append(valueFactor)
            
        writer.writerow(row)
        
    
    
        
        
        
        





