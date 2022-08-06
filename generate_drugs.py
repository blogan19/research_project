import pandas as pd
import numpy as np
import random

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

def randomDrug(df): 
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
    dose = float(sample['primary_dose'][0])
    new_dose = dose/2

    if dose.is_integer():
        dose = int(dose)

    if new_dose.is_integer():
        new_dose = int(new_dose)

    #Unit 
    unit = sample['primary_dose_description'][0]
    if unit == 'tablet' or unit == 'capsule':
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

    medication = {
        "drugName" : drug_tag,
        "dose": dose_tag,
        "newdose": newDose_tag,
    }

    return medication

def randomOral():
   return randomDrug("oral_cleaned.csv")

def randomInject():
    return randomDrug("injection_cleaned.csv")

def randomInhaled(): 
    return randomDrug('inhaled_cleaned.csv')