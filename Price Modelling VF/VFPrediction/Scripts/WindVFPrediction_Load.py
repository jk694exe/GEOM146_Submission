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

dataset = pd.read_csv("../Input/Data_Wind_Load.csv")
solar = dataset["SOLAR"].to_numpy()
wind = dataset["WIND"].to_numpy()
nuclear = dataset["NUCLEAR"].to_numpy()
others = np.empty(solar.size)
others.fill(currAvgDemand)
total = dataset["Total"].to_numpy()
highLoad = dataset["HighLoad"].to_numpy()
lowLoad = dataset["LowLoad"].to_numpy()
normLTSInput = dataset["NormLTSInput"].to_numpy()
normSTSInput = dataset["NormSTSInput"].to_numpy()
normLTSOutput = dataset["NormLTSOutput"].to_numpy()
normSTSOutput = dataset["NormSTSOutput"].to_numpy()

def PredictVF(targetWindMS, targetSolarMS, targetNuclearMS, targetOtherMS, ltsGen, stsGen, scenario):
    windScale = targetWindMS / currWindMS
    solarScale = targetSolarMS / currSolarMS
    nuclearScale = targetNuclearMS / currNuclearMS
    avgWind = currAvgDemand * targetWindMS
    ltsFactorOut = ltsGen * avgWind
    stsFactorOut = stsGen * avgWind
    ltsFactorIn = ltsFactorOut / ltsRTE
    stsFactorIn = stsFactorOut / stsRTE
    
    solarGen = solar * solarScale
    windGen = wind * windScale
    nuclearGen = nuclear * nuclearScale
    othersGen = others * targetOtherMS
    storageGen = normLTSOutput * ltsFactorOut - normLTSInput * ltsFactorIn + normSTSOutput * stsFactorOut - normSTSInput * stsFactorIn
    windGen = windGen + storageGen
    residualDemand = - solarGen - windGen - nuclearGen - othersGen
    if scenario ==0:
        residualDemand = residualDemand + total
    elif scenario ==1:
        residualDemand = residualDemand + highLoad
    elif scenario ==2:
        residualDemand = residualDemand + lowLoad
        
    residualDemand = np.where(residualDemand < 0, 0, residualDemand)
    
    avgResidual = np.sum(residualDemand,axis=0)/residualDemand.size
    normResidual = residualDemand/avgResidual
    predPrice = coef0 + normResidual * coef1 + np.power(normResidual,2) * coef2 + np.power(normResidual,3) * coef3 + np.power(normResidual,4) * coef4 + np.power(normResidual,5) * coef5
    
    windPriceMult = predPrice*windGen
    valueFactor = (np.sum(windPriceMult,axis=0)*windPriceMult.size)/(np.sum(predPrice,axis=0)*np.sum(windGen,axis=0))
    return valueFactor


with open('windVfCurr.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    header = ["Wind Market Share", "Current_Load", "High_Load", "Low_Load"]
    writer.writerow(header)
    
    endWindMS = 0.5
    stepWindMS = 0.02
    for windIndex in range(1, int(endWindMS/stepWindMS)+1):
        targetWindMS = windIndex*stepWindMS
    
        targetNuclearMS = 0.1546
        targetSolarMS = 0.044
        targetOtherMS = 0
        ltsGen = 0.0
        stsGen = 0.0
        
        row = [targetWindMS]
        
        for scenario in range(3):
            valueFactor = PredictVF(targetWindMS, targetSolarMS, targetNuclearMS, targetOtherMS, ltsGen, stsGen, scenario)
            row.append(valueFactor)
            
        writer.writerow(row)
        

        

        
        
        





