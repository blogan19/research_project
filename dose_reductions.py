from distutils.util import change_root
import pandas as pd
import random
from generate_details import HCP, Patient
import names 
reductions = pd.read_csv("oral_cleaned.csv")


#Generates a random oral dose with tags e.g. ("Amlodipine","B-Drug")
def randomOral(): 
    df = reductions = pd.read_csv("oral_cleaned.csv")
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
    new_dose = dose/2

    if dose.is_integer():
        dose = int(dose)

    if new_dose.is_integer():
        new_dose = int(new_dose)


    #Unit 
    unit = sample['primary_dose_description'][0]
    if unit == 'tablet':
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

    hcp = HCP()
    patient = Patient()

    
    medication = {
        "drugName" : drug_tag,
        "dose": dose_tag,
        "newdose": newDose_tag,
        "hcp": hcp,
        "ptname": patient
    }

    return medication

def reduceDoses():
    #Get Drug
    drug = randomOral()

    #actions: reduce, chagen, decrease 

    #Patient normally takes xmg of drug x please ammend dose
    #Patient is prescribed drug at a dose of 100mg review need to reduce dose
    #Patient is prescribed drug at a dose of 100mg review need to reduce to 50mg
    #'Drug is prescribed at a dose of '

    #xmg is too high. drug a should be prescribed as y
    #patient was advised to decrease the dose of x by hcp
    #Patient states drug was reduced to 5mg by 
    #'Patient is prescribed drug x a a dose of x please change dose'
    #Patient Name is normally taking drug at a dose of 10mg please review 

    reduction_actions = {
        0: [('re-prescribe','B-Action'),('at','I-Action'),('a','I-Action'),('lower','I-Action'),('dose','L-Action')],
        1: [('ammend','B-Action'),('dose','L-Action')],
        2: [('decrease','B-Action'),('dose','L-Action')],
        3: [('reduce','B-Action'),('dose','L-Action')],
        4: [('re-prescribe','B-Action')],
        5: [('please','o'),('represcribe','B-Action')],
        6: [('change','B-Action'),('dose','L-Action')]
    }
    actionChoice = reduction_actions[random.randrange(0,len(reduction_actions),1)]

    reductions = {
        1: [("Patient","o"), ("normally","o"), ("takes","o")] + drug['dose'] + [("of","o")] +  drug['drugName'] + [("please","o")] + actionChoice,
        2: [("Patient","o"), ("is","o"), ("prescribed","o")] +  drug['drugName'] + [("at","o"),("a","o"),("dose","o"),("of","o")] + drug['dose'] + [(". Review","o"),("need","o"),("to","o")] + actionChoice,
        3: [("Patient","o"), ("is","o"), ("prescribed","o")] +  drug['drugName'] + [("at","o"),("a","o"),("dose","o"),("of","o")] + drug['dose'] + [(". Review","o"),("need","o"),("to","o")] + actionChoice + [("to","o")] + drug['newdose'],
        4: drug['drugName'] + [("is","o"),("prescribed","o"),("at","o"),("a","o"),("dose","o"),("of","o")] + drug['dose'] + [("is","o"),("this","o"),("meant","o"),("to","o"),("be","o")] + drug['newdose'] + actionChoice,
        5: drug["dose"],
        6: [("Patient","o"), ("is","o"), ("prescribed","o")] +  drug['drugName'] + [("at","o"),("a","o"),("dose","o"),("of","o")] + drug['dose'] + [(". Review","o"),("need","o"),("to","o")] + actionChoice + [("as","o"),("this","o"),("has","o"),("likely","o"),("been","o"),("prescribed","o"),("in","o"),("error","o")]
    }

    #pick a random sentence from dict
    sentence_pick = random.choice([2])
    choice = reductions[sentence_pick]

    sent = []
    tokens = []

    for i in choice:
        if i[1] == 'o':
            sent.append(i[0])
            tokens.append(i[1])
        else: 
            sent.append(i[0])
            tokens.append(i[1])
    print(drug)
    print(sent)
    print(tokens)

    #print(reductions[sent_pick])

reduceDoses()
