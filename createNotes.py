from distutils.util import change_root
import pandas as pd
import random
from generate_drugs import randomAny,randomOral, randomInhaled, randomInject, medicationList
from generate_details import HCP,Pharmacist, Patient, randDay, randomDate,randTimePeriod,please, Relative, pharmacokineticChange, randomGuidance, randomDrugClass,ivostReasons,contraindicationType, sideEffects, pharmokineticIssue, planAuthor
from actions import discontinueActions,represcribeActions,reduction_actions,startActions, discontinueActionPastTense, startPastTense,increase_actions
reductions = pd.read_csv("oral_cleaned.csv")


def tagsentences(choice):
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
    return(arr)


 
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
        19: drug['drugName'] + ["interacts with the following medications:"] + medicationList(random.randint(2,8)) + actionChoice + ["of"]+ drug['drugName']
    }
    #pick a random sentence from dict

    sentence_pick = 19
    #sentence_pick = random.randrange(0,len(reductions),1)


    choice = reductions[sentence_pick] 
    return (tagsentences(choice))
    


def increaseDose():
    pass


def IncorrectMedications(drug1, drug2):
    actionChoice = represcribeActions[random.randrange(0,len(represcribeActions),1)]
    discontinue = discontinueActions[random.randrange(0,len(discontinueActions),1)]
    start = startActions[random.randrange(0,len(startActions),1)]
    sentences = {
        0: drug1['drugName'] + ['has been prescribed instead of'] + drug2['drugName'] + please() + ['review this prescription and'] + [('discontinue','B-Action')] + drug1['drugName'] + random.choice([[' and prescribe correct medication'],[f'and prescribe {drug2["drugName"]}']]),
        1: ['Has'] + drug1['drugName'] + ['been prescribed intentionally. Should the prescription read'] + drug2['drugName'] + ['please'] + actionChoice + ['prescription'],
        2: random.choice([['The prescription for'],[f'A prescription dated {randomDate()}']]) + drug1['drugName'] +['for'] + Patient('') + random.choice([['is for a medication that the patient has never received'],['is not something they have taken before'],['is a medication that would not fit with their past medical history'],['was stopped by the gp last year'],['is a drug the patient no longer takes'],['does not fit with the presenting complaint'],[f'is similar in named to {drug2["drugName"]}'],['does not have an obvious indication'],[f'is a medication their {Relative()} normally takes. Has this been prescribed using an incorrect medication history'],[f'has a similar spelling to {drug2["drugName"]} has this been mistakenly selected on the electronic prescribing system']]) + please()  + actionChoice + ['prescription and'] + discontinue + ['the incorrect medication'],
        3: ['has this presciption been written in error. Should'] + drug2['drugName'] + ['have been prescribed instead of'] + drug1['drugName'] + ['review need to'] + start + ['for'] + drug1['drugName'] + ['and'] + discontinue + drug2['drugName'],
        4: random.choice([['The prescription for'],['']])+ drug1["drugName"] + ['may have been written in error'] + random.choice([['can this be reviewed urgently'],['review this prescription'],['check that this is correct']]) + start + drug2['drugName'] + ['in its place if appropriate'],
        5: Patient('') + ['has been prescribed'] + drug1['drugName'] + ['on'] + [randomDate()] + random.choice([['this is a drug the patient has never had before.'],['the patient doesnt appear to have had this before'],['they have never taken this drug'],['has this been started as a new prescription']]) + random.choice([['is this correct'],['is this the correct medication'],['has the correct medication been selected']]) + discontinue + drug1['drugName'] + ['as appropriate'],
        6: Patient('') + ['has been prescribed'] + drug1['drugName'] + ['on'] + [randomDate()] + random.choice([['this is a drug the patient has never had before.'],['the patient doesnt appear to have had this before'],['they have never taken this drug'],['this isnt a drug they normally taken'],['this is not a medication they normally receive']]) + random.choice([['is this correct'],['is this the correct medication'],['has the correct medication been selected'],['has this been started as a new prescription']]) +drug1['dose'] + ['would be quite a high dose to start someone on initially'] +  discontinue  + drug1['drugName'] + ['as appropriate']  + ['or please clarify why this has been prescribed']
    }

    sentence_pick = random.randrange(0,len(sentences),1)

    choice = sentences[sentence_pick] 
    return (tagsentences(choice))

def duplicatedTherapy(drug1, drug2):
    # Flucloxacillin has been prescribed both as IV and Oral route 
    # Drug x has been prescribed twice please review 
    # drug x is the same medication class as y 
    # drug y is also a calcium channel blocker
    # Drug x and Drug y have the same mechanism of action 
    # Drug x and y work in the same way 
    discontinue = discontinueActions[random.randrange(0,len(discontinueActions),1)]
    discontinuePastTense = discontinueActionPastTense[random.randrange(0,len(discontinueActionPastTense),1)]

    injection = randomInject('')
    sentences = {
        0: injection['drugName'] + ['has been prescribed intravenously at'] + injection['dose'] +['and also oraly at a dose of'] + injection['newdose'] + random.choice([['Should this therapy have been duplicated like this'],['is this correct'],['this is most likley unintentional'],['this appears to have been done in error']]) + please() + discontinue + ['one of the prescriptions'] + random.choice([['can IV be stopped'],['is IV indicated?'],['oral option is sufficient']]) + ivostReasons(),
        1: drug1['drugName'] + ['has been prescribed twice'] + please() + discontinue + ['one of the prescriptions'],
        2: Patient('') + ['has two active prescriptions for'] + drug1['drugName'] + random.choice([['There is an increased risk of overdose'],['patient is at risk of overdise']]) + ['can one ot the prescriptions be'] + discontinuePastTense,
        3: drug1['drugName'] + ['and'] + drug2['drugName'] + ['are in the same medication class'] + random.choice([['no advantage is gained by prescribing both'],['increasing risk of overdose']]) + ['can one of the drugs be'] + discontinuePastTense + please(),
        4: ['Both'] + drug1['drugName'] + ['and'] + drug2['drugName'] + ['are'] + randomDrugClass() + ['is this intentional normally the two wouldnt be prescribed together one of the medications may need to be']  + discontinueActionPastTense + ['please review as a matter of urgency thanks'],
        5: random.choice([['both'],['two of the medications prescribed for this patient'],['the two medications'],['the two drugs']]) + drug1['drugName'] + ['and'] + drug2['drugName'] + random.choice([['have the same mechanism of action'],['have a very similar mechanism of action'],['work in exactly the same way'],['have an identical mechanism of action']]) + ['review the need to'] + discontinue + drug1['drugName']
    }
    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])


def contraindications(drug1,drug2):
    # Medication is contraindicated	
    # Cyclizine is contraindicated in heart failure review need for alternative antiemetic
    # several of these medications are contraindicated in (drug list )
    # Drug x is not recomended in 
    # x condition means that drug y is not advised 
    # X guidance advises that drug y should not be used in patients with 
    # Mr Smith has unstable angina. Drug y has been newly started. This goes against hospital policy as it is a knwon caution/CI
    discontinue = discontinueActions[random.randrange(0,len(discontinueActions),1)]
    discontinuePastTense = discontinueActionPastTense[random.randrange(0,len(discontinueActionPastTense),1)]
    start = startActions[random.randrange(0,len(startActions),1)]
    startPast  = startPastTense[random.randrange(0,len(startPastTense),1)]
    sentences = {
        0: ["use of"] + drug1['drugName'] + ['is contraindicated in this patient please review this prescription and'] + discontinue + drug1['drugName'],
        1: drug1['drugName'] + random.choice([['increases the risk of'],['may increase the risk of'],['can cause']]) + sideEffects() + please() + ['review need to'] + discontinue + drug1['drugName'] + ['and start'] + drug2['drugName']+ ['instead'],
        2: drug1['drugName'] + random.choice([['increases the risk of'],['may increase the risk of'],['can cause'],['can increase the risk of'],['significantly increases risk of']]) + sideEffects() + ['particularly in patients with'] + pharmokineticIssue() + ["review this prescription and"] + discontinue + ['is appropriate'],
        3: ['The medications'] + medicationList(3) + ['are all'] + random.choice([['cautioned'],['contraindicated'],['inappropriate']]) + ['in patients with'] + contraindicationType() + ['and may need to be'] + discontinuePastTense,
        4: drug1['drugName'] + ['is not recomended in'] + contraindicationType() + ['can an alternative be'] + startPast,
        5: randomGuidance() + random.choice([['states'],['dictates'],['recommends'],['advises'],['stipulates']])+ ['that'] + drug1['drugName'] + random.choice([['is not the first line choice'],['should be avoided'],['should not be used']]) + ['in patients with'] + contraindicationType() + please() + ['review need to'] + discontinue + drug1['drugName'] + ['and'] + start + drug2['drugName'],
        6: randomGuidance() + random.choice([['states'],['dictates'],['recommends'],['advises'],['stipulates']])+ ['that'] + drug1['drugName'] + random.choice([['is not the first line choice'],['should be avoided'],['should not be used']]) + ['in patients with'] + contraindicationType() + please() + discontinue + drug1['drugName'],
        7: sideEffects() + ['prevents the use of'] + drug1['drugName'] + discontinue + drug1['drugName'],
        8: Patient('') + ['has'] + contraindicationType() + ['and'] + drug1['drugName'] + ['has been newly started'] + ['this goes against advice from'] + randomGuidance() + ['as it is a known contraindication and is significant'] + [('review','B-Action'),('prescription','L-Action')]
    
    }
    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])

def incorrectDoseIncrease(drug1,drug2):
    #the dose for x has been increased from a to b review need to reduce 
    # x has been increased on admission
    # The dose of y has been increase however there is no documentation int the notes
    # drug x has been increased above the maximum dose 
    # the plan was to increase the dose of y however the dose for x has been increasedT
    # The dose has been increased above the recomended dose for a patient with a renal function of
    # has been increase however the hr ha snot dropped
    # has ben increase but pt now experienceing side effects
    start = startActions[random.randrange(0,len(startActions),1)]
    reduce = reduction_actions[random.randrange(0,len(reduction_actions),1)]
    increase = increase_actions[random.randrange(0,len(increase_actions),1)]
    
    sentences = {
        0: ["the dose of"] + drug1["drugName"] + ["has been increased from"] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['was this an intentional increased'],['has this been done intentionally'],['however there is no documentation in the notes'],['this is not documented in the medical plan']]) + random.choice([['can this be reviewed'],['please review prescription'],['please review']]) + ['and'] + reduce + random.choice([['if this change was unintentional'],['if appropriate'],['if change was made in error']]),
        1: ["the dose of"] + drug1["drugName"] + ["has been increased from"] + drug1['dose'] + ['to'] + drug1['newdose'] + ['however the plan in the medical notes was to increase the dose from next'] + randDay('any'),
        2: drug1['drugName'] + random.choice([['was prescribed at a dose of'],['has been issued at'],['has been prescribed as']]) + drug1['newdose'] + ['since admission The patient normally only takes'] + drug1['dose'] + ['and this was the dose they were admitted on was this change intentional review need to'] + reduce,
        3: ['patient normally takes'] + drug1['drugName'] + drug1['dose'] + ['prescribed as'] + drug1['newdose'] + ['review need to'] + reduce,
        4: ['the increased dose of'] + drug1['newdose'] + ['for']  + drug1['dose'] + ['is now above the max dose as per'] + randomGuidance() + ['review need to'] + reduce,
        5: drug1['drugName'] + ['has been increased to'] + drug1['newdose'] + ['however the maximum recommended dose for'] + drug1['drugName'] + ['is'] + drug1['dose'] + ['please'] + reduce + ['or'] + start + ['an alternative'] + randomDrugClass() + ['such as'] + drug2['drugName'] + drug2['dose'],
        6: ['The plan as per the'] + planAuthor() + ['was to increase the dose'] + drug1['dose'] + ['from'] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['this hasnt been done as of yet'],['this has not been actioned']])+ please() + [("increase","B-Action"),('dose','L-Action')],
        7: ['The plan as per the'] + planAuthor() + ['was to increase the dose of'] + drug1['drugName'] + ['from'] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['this hasnt been done as of yet'],['this has not been actioned however the dose of']])+ drug2['drugName'] + ['has been increased from'] + drug2['dose'] + ['to'] + drug2['newdose'] +['has the wrong drug been increased'] + please() + ['review need to'] + reduce + ['of'] +drug2['drugName'] + ['and'] + increase + drug1['drugName'] + ['from'] + drug1['dose'] + ['to'] + drug2['newdose']
    }
    choice = random.randrange(0,len(sentences),1)
    choice = 7
    return tagsentences(sentences[choice])

def create():
    oral1 = randomOral('reduce')
    oral2 = randomOral('reduce')
    #print(IncorrectMedications(oral1, oral2))

    inhaled1 = randomInhaled('reduce')
    inhaled2 = randomInhaled('reduce')
    #print(IncorrectMedications(inhaled1, inhaled2))

    injection1 = randomInject('reduce')
    injection2 = randomInject('reduce')
    #print(IncorrectMedications(injection1,injection2))

    drug1 = randomAny('increase')
    drug2 = randomAny('increase')
    print(incorrectDoseIncrease(drug1,drug2))

create()

