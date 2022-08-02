import pandas as pd
import random
reductions = pd.read_csv("oral_cleaned.csv")

#reduction types


'Patient normally takes xmg of drug x please ammend dose'
'Drug is prescribed at a dose of '


def randomOral(): 
    df = reductions = pd.read_csv("oral_cleaned.csv")
    sample = reductions.sample(1).reset_index()

    drug = sample['drug'][0].split(" ") 
    
    drug_tag = []
    for i,x in enumerate(drug):
        if i == 0:
            drug_tag.append((x,"B-Drug"))
        elif i == len(drug)-1:
            drug_tag.append((x,"L-Drug"))
        else: 
            drug_tag.append((x,"I-Drug"))


    medication = {
        "drugName" : drug_tag
    }

    return medication

def createScript():
    print(randomOral())
    dose = None
    doseTag = None
    
    drug = randomOral()
 

    sent_pick = random.choice([1])
    reductions = {
        1: [("Patient","o"), ("normally","o"), ("takes","o"), (dose,doseTag), ("of","o")] +  drug['drugName'] + [("please","o"), ("ammend","o"),("dose","o")]
    }

    choice = reductions[sent_pick]

    sent = []
    tokens = []


    for i in choice:
        if i[1] == 'o':
            sent.append(i[0])
            tokens.append(i[1])
        else: 
            sent.append(i[0])
            tokens.append(i[1])
    print(sent)
    print(tokens)

    #print(reductions[sent_pick])

createScript()
