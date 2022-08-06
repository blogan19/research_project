from distutils.util import change_root
import pandas as pd
import random
from generate_drugs import randomOral, randomInhaled, randomInject, medicationList
from generate_details import HCP,Pharmacist, Patient, randDay, randTimePeriod,please, Relative, pharmacokineticChange, randomGuidance
import names 
reductions = pd.read_csv("oral_cleaned.csv")


#Generates a random oral dose with tags e.g. ("Amlodipine","B-Drug")
reduction_actions = {
        0: [('re-prescribe','B-Action'),('at','I-Action'),('a','I-Action'),('lower','I-Action'),('dose','L-Action')],
        1: [('ammend','B-Action'),('dose','L-Action')],
        2: [('decrease','B-Action'),('dose','L-Action')],
        3: [('reduce','B-Action'),('dose','L-Action')],
        4: [('re-prescribe','B-Action')],
        5: [('represcribe','B-Action')],
        6: [('change','B-Action'),('dose','L-Action')],
        7: [('review','B-Action'),('need','I-Action'),('to','I-Action'),('ammend','I-Action'),('the','I-Action'),('dose','L-Action')],
        8: [('lower','B-Action'),('the','I-Action'),('dose','L-Action')],
        9: [('decrease','B-Action'),('the','I-Action'),('dose','L-Action')]
    }

def reduceDoses(drug1, drug2):
    drug = drug1
    secondDrug = drug2

    actionChoice = reduction_actions[random.randrange(0,len(reduction_actions),1)]

    reductions = {
        0: drug['drugName'] + ["needs to be"] + [("reduced","o")] +["to"] + drug['dose'] + actionChoice,
        1: ["Patient normally takes"] + drug['dose'] + ["of"] +  drug['drugName'] + ["please"] + actionChoice,
        2: ["Patient is prescribed"] +  drug['drugName'] + ["at a dose of"] + drug['dose'] + ["please review need to"] + actionChoice,
        3: ["Patient is prescribed"] +  drug['drugName'] + ["at a dose of"] + drug['dose'] + ["Review need to"] + actionChoice + ["to"] + drug['newdose'],
        4: drug['drugName'] + ["is prescribed at a dose of"] + drug['dose'] + ["is this meant to be"] + drug['newdose'] + actionChoice,
        5: drug["dose"] + ["is a dose which is higher than the patients usual dose"] + drug['newdose'] + ["review need to reduce dose thanks"],
        6: ["Patient is prescribed"] +  drug['drugName'] + ["at a dose of"] + drug['dose'] + ["Review need to"] + actionChoice + ["as this has likely been prescribed in error"],
        7: ["patient was advised to reduce the dose of"] + drug["drugName"] + ["to"] + drug["newdose"] + ["by"] + HCP() + ["in the clinic last"] + randDay("any"),
        8: Patient('gendered')+ ["has been taking"] + drug["drugName"] + ["at a dose of"] + drug["newdose"] + ["for the past"] + randTimePeriod('any') +  please() + actionChoice,
        9: ["Patient states dose was reduced but cannot remember who told them to do so"] + drug["drugName"] + ["therefore needs reviewing and potentially reducing to"] + drug['newdose'],
        10:["The"] + Relative() + ["of"] +  Patient("gendered") + ["states that they were recently seen in clinic and the dose of"] + drug['drugName'] + ["was reduced from"] + drug["dose"] + ["to"] + drug["newdose"],
        11: drug["drugName"] + ["was reduced from"] + drug["dose"] + ["to"] + drug["newdose"] + ["due to an interaction with"] +secondDrug["drugName"] + actionChoice,
        12: drug["drugName"] + ["increases the plasma concentration of"] + secondDrug["drugName"] + ["when co-administered. A dose of"] +drug["dose"] +["is therefore too high"] + actionChoice,
        13: drug["drugName"] + ["increases the plasma concentration of"] + secondDrug["drugName"] + ["when co-administered. It is currentely prescribed as"] +drug["dose"] +["can this be"] + [("reduced",'B-Action')] + ["to"] + drug["newdose"],
        14: ["The levels of"] + drug["drugName"] + ["are increased by"] + secondDrug["drugName"] + actionChoice,
        15: pharmacokineticChange()  + ["review dose of"] + drug["drugName"] + ["this may need"] +[("reducing","o")]+ ["from"]+drug["dose"]+ ["to"] + drug["newdose"],
        16: pharmacokineticChange()  + ["please review"] + drug["drugName"] + ["this may need"] + ["(reducing","o"] + ["to"] + drug["newdose"],
        17: ["patient has a renal function of"] + [(f"{random.randrange(10,90,1)}ml/min","o")] + ["and is prescribed"] + drug["drugName"] + ["as per"] + randomGuidance() + random.choice([["this should be"],["this needs to be"],["can this be"],["should this be"]]) + [("reduced","o")] + ["to"] + drug["newdose"],
        18: drug['drugName'] + ["needs to be"] + [("reduced","o")] +["to"] + drug['dose']+ [f'{random.choice([["due to serious drug drug interaction"],["as it interacts with feed"],["is incompatible with feeding regime"]])}']+ actionChoice,
        19: drug['drugName'] + ["interacts with the following medications:"] + medicationList(random.randint(2,8)) + actionChoice + drug['drugName']
        #Patient was advised to recude their drug dose from x to y by hcp
    }
    #pick a random sentence from dict

    sentence_pick = 19
    #sentence_pick = random.randrange(0,len(reductions),1)


    choice = reductions[sentence_pick] 
    #randomly add a pharmacist details to the end of the note
    pharmacistPicker = random.randint(0,100)
    if pharmacistPicker >= 66:
        pharmacist = Pharmacist()
        choice = choice + pharmacist
    arr = []
    for i in choice:
        if type(i) == str:
            sent = i.split(" ")
            for x in sent:
                arr.append((x,'o'))
        if type(i) == tuple:
            arr.append(i)
    print(arr)


def create():
    oral1 = randomOral()
    oral2 = randomOral()
    reduceDoses(oral1, oral2)

    inhaled1 = randomInhaled()
    inhaled2 = randomInhaled()
    reduceDoses(inhaled1, inhaled2)

    injection1 = randomInject()
    injection2 = randomInject()
    reduceDoses(injection1,injection2)
create()

