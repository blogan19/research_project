import pandas as pd
import numpy as np
import random

from generate_details import randomFrequency


def frequency_convert(freq):
    frequency_conversions = {
        'QDS': ("four times daily",4),
        '6H': ("6 hourly",4),
        "OM": ("each morning",1),
        "ON": ("each night",1),
        "BD": ("twice daily",2),
        "3H": ("three hourly",8),
        "4H": ("four hourly",6),
        "TDS": ("three times daily",3),
        "OD": ("once daily",1),
        "8H": ("eight hourly",3),
        "12H": ("twelve hourly",2),
        "Five times a day": ("five times daily",5),
        "Six times a day": ("six times daily",6),
        "2H": ("2 hourly",12)
    }
    
    dose = frequency_conversions.get(freq)
    if dose != None:
        # if not in list just return once daily because cba
        return ("once daily",0)
    else:
        return(freq)

def medicationList(drugNo):
    #generates a random medication list 
    df = pd.read_csv('oral_cleaned.csv')
    drugList = np.array(df['drug'].unique())
    
    drugArray = []
    for d in range(drugNo):
        drug = random.choice(drugList).split(" ")

        for i,x in enumerate(drug):
            if i == 0:
                drugArray.append((x,"B-Drug"))
            elif i == len(drug)-1:
                drugArray.append((x,"L-Drug"))
            else: 
                drugArray.append((x,"I-Drug"))
    
    return drugArray

def randomDrug(df,type): 
    reductions = pd.read_csv(df)
    sample = reductions.sample(1).reset_index()
    
    drug = sample['drug'][0].split(" ") 
    
    #Drug
    drug_tag = []
    for i,x in enumerate(drug):
        if i == 0:
            drug_tag.append((x,"B-Drug"))
        elif i == len(drug)-1:
            drug_tag.append((x,"L-Drug"))
        else: 
            drug_tag.append((x,"I-Drug"))

    #Dose
    dose = sample['primary_dose'][0]
    if isinstance(dose, str):
        dose = dose.replace(',','')
    dose = float(dose)
    if type == 'reduce':
        new_dose = dose/2
    if type == 'increase': 
        new_dose = dose*2
    else:
        new_dose = random.choice([dose*2,dose/2])
    

    if dose.is_integer():
        dose = int(dose)

    if new_dose.is_integer():
        new_dose = int(new_dose)

    #Unit 
    unit = sample['primary_dose_description'][0]
    if unit == 'tablet' or unit == 'capsule' or unit == 'patch' or unit == 'application':
        dose = f"{dose} {unit}s"
        new_dose = f"{new_dose} {unit}s"
    else: 
        dose = f"{dose}{unit}"
        new_dose = f"{new_dose}{unit}"

    dose = dose.split(" ")
    dose_tag = []
    for i,x in enumerate(dose):
        if i == 0:
            dose_tag.append((x,"B-Dose"))
        elif i == len(drug)-1:
            dose_tag.append((x,"L-Dose"))
        else: 
            dose_tag.append((x,"I-Dose"))

    new_dose = new_dose.split(" ")
    newDose_tag = []
    for i,x in enumerate(new_dose):
        if i == 0:
            newDose_tag.append((x,"B-Dose"))
        elif i == len(drug)-1:
            newDose_tag.append((x,"L-Dose"))
        else: 
            newDose_tag.append((x,"I-Dose"))

    route = sample['route'][0].split(" ")
    route_tag = []
    for i,x in enumerate(route):
        if i == 0:
            route_tag.append((x,"B-Route"))
        elif i == len(drug)-1:
            route_tag.append((x,"L-Route"))
        else: 
            route_tag.append((x,"I-Route"))

    
    frequency = sample['frequency_description'][0]
    frequency = str(frequency)
    frequency_tag = []
    freq = frequency_convert(frequency)[0].split(" ")
    for i,x in enumerate(freq):
        if i == 0:
            frequency_tag.append((x,"B-Freq"))
        elif i == len(drug)-1:
            frequency_tag.append((x,"L-Freq"))
        else: 
            frequency_tag.append((x,"I-Freq"))

    

    medication = {
        "drugName" : drug_tag,
        "dose": dose_tag,
        "newdose": newDose_tag,
        "route": route_tag,
        "frequency": frequency_tag
    }

    return medication




def randomOral(changeType):
   return randomDrug("oral_cleaned.csv",changeType)

def randomInject(changeType):
    return randomDrug("injection_cleaned.csv",changeType)

def randomInhaled(changeType): 
    return randomDrug('inhaled_cleaned.csv',changeType)

def randomAny(changeType):
    return randomDrug('drug_list_dose_clean.csv',changeType)