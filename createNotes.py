import pandas as pd
import random
from generate_drugs import randomAny,randomOral, randomInhaled, randomInject, medicationList
from generate_details import HCP, HCP_location,randomWard,Pharmacist, Patient, randDay, randomDate,randTimePeriod,please, Relative, pharmacokineticChange, randomGuidance, randomDrugClass,ivostReasons,contraindicationType, sideEffects, pharmokineticIssue, planAuthor,allergyReaction, medRecSource,administrationTimes,randomFrequency, randomRoute,randomIndication,randomBiochem,multipleFrequency 
from actions import discontinue,represcribe,represcribePastTense,start, discontinued, started,changeFrequency, increase_dose, reduce_dose,amendRoute,biochemMonitoring,reviewDate, reduced, increased
from grammar import keyboardError
reductions = pd.read_csv("oral_cleaned.csv")


def tagsentences(choice):
     #randomly add a pharmacist details to the end of the note
    pharmacistPicker = random.randint(0,100)
    if pharmacistPicker >= 60:
        pharmacist = Pharmacist()
        choice = choice + pharmacist
    arr = []

    for i in choice:
        if type(i) == str:
            sent = i.split(" ")
            for x in sent:
                arr.append((x.lower(),'o'))
        if type(i) == tuple:
            arr.append((str(i[0]).lower(),i[1]))

    grammar = random.randint(0,100)
    if grammar > 97:
        keyboardError(arr)
    
    return(arr)


 
def reduceDoses(drug1, drug2):
    drug = drug1
    secondDrug = drug2
    biochem = randomBiochem()

    reductions = {
        0: drug['drugName'] + ["needs to be"] + [("reduced","B-Action")] +["to"] + drug['dose'] + reduce_dose(),
        1: ["Patient normally takes"] + drug['dose'] + ["of"] +  drug['drugName'] + ["please"] + reduce_dose(),
        2: ["Patient is prescribed"] +  drug['drugName'] + ["at a dose of"] + drug['dose'] + ["please review need to"] + reduce_dose(),
        3: ["Patient is prescribed"] +  drug['drugName'] + ["at a dose of"] + drug['dose'] + ["Review need to"] + reduce_dose() + ["to"] + drug['newdose'],
        4: drug['drugName'] + ["is prescribed at a dose of"] + drug['dose'] + ["is this meant to be"] + drug['newdose'] + reduce_dose(),
        5: drug["dose"] + ["is a dose which is higher than the patients usual dose"] + drug['newdose'] + ["review need to"] + reduce_dose(),
        6: ["Patient is prescribed"] +  drug['drugName'] + ["at a dose of"] + drug['dose'] + ["Review need to"] + reduce_dose() + ["as this has likely been prescribed in error"],
        7: ["patient was advised to"] + [("reduce","B-Action"),("the","I-Action"),("dose","L-Action")] + ["of"] + drug["drugName"] + ["to"] + drug["newdose"] + ["by"] + HCP() + ["in the clinic last"] + randDay("any"),
        8: Patient('gendered')+ ["has been taking"] + drug["drugName"] + ["at a dose of"] + drug["newdose"] + ["for the past"] + randTimePeriod('any') +  please() + reduce_dose(),
        9: ["Patient states dose was"] + [("reduced"),("B-Action")]+ ["but cannot remember who told them to do so"] + drug1["drugName"] + ["therefore needs reviewing and potentially"] + [("reducing","B-Action")] + ["to"] + drug1['newdose'],
        10:["The"] + Relative() + ["of"] +  Patient("gendered") + ["states that they were recently seen in clinic and the dose of"] + drug1['drugName'] + ["was"] + [("reduced","B-Action")]  + ["from"] + drug1["dose"] + ["to"] + drug1["newdose"],
        11: drug["drugName"] + ["was reduced from"] + drug["dose"] + ["to"] + drug["newdose"] + ["due to an interaction with"] +secondDrug["drugName"] + reduce_dose(),
        12: drug["drugName"] + ["increases the plasma concentration of"] + secondDrug["drugName"] + ["when co-administered. A dose of"] +drug["dose"] +["is therefore too high"] + reduce_dose(),
        13: drug["drugName"] + ["increases the plasma concentration of"] + secondDrug["drugName"] + ["when co-administered. It is currentely prescribed as"] +drug["dose"] +["can this be"] + [("reduced",'B-Action')] + ["to"] + drug["newdose"],
        14: ["The levels of"] + drug["drugName"] + ["are increased by"] + secondDrug["drugName"] + reduce_dose(),
        15: pharmacokineticChange()  + ["review dose of"] + drug["drugName"] + ["this may need"] +[("reducing","B-Action")]+ ["from"]+drug["dose"]+ ["to"] + drug["newdose"],
        16: pharmacokineticChange()  + ["please review"] + drug["drugName"] + ["this may need"] + [("reducing","B-Action")] + ["to"] + drug["newdose"],
        17: ["patient has a renal function of"] + [(f"{random.randrange(10,90,1)}ml/min","o")] + ["and is prescribed"] + drug["drugName"] + ["as per"] + randomGuidance() + random.choice([["this should be"],["this needs to be"],["can this be"],["should this be"]]) + [("reduced","o")] + ["to"] + drug["newdose"],
        18: drug['drugName'] + ["needs to be"] + [("reduced","B-Action")] +["to"] + drug['dose']+ [f'{random.choice([["due to serious drug drug interaction"],["as it interacts with feed"],["is incompatible with feeding regime"]])}']+ reduce_dose(),
        19: drug['drugName'] + ["interacts with the following medications:"] + medicationList(random.randint(2,8)) + reduce_dose() + ["of"]+ drug['drugName'],
        20: ['Patient has a low'] + [biochem['test']]  + drug1['drugName'] + random.choice([['is know to cause this'],[f'is known to reduce {biochem["test"]}'],['can often be the cause']]) + reduce_dose() + ['to'] + drug1['newdose'],
        21: drug1['drugName'] + ['needs to be'] + reduced() + ['it has been prescribed for'] + randTimePeriod('any') + ['the dose should therefore be reduced to'] + drug1['dose'] + random.choice([['not documented in notes as intentional change'],['not sure if intentional change']])
    }
    #pick a random sentence from dict
    sentence_pick = random.randrange(0,len(reductions),1)
    choice = reductions[sentence_pick] 
    return (tagsentences(choice))
    


def increaseDose(drug1,drug2):
    biochem = randomBiochem()
    sentences = {
        0: pharmacokineticChange() + ['please review need to'] + increase_dose() + ['of'] + drug1['drugName'] + ['to'] + drug1['dose'],
        1: ['Patients renal function has improved significantly since'] + randDay('any') + ['please review need to'] + random.choice([[discontinue()],[start()],[f'{changeFrequency()} of']]) + drug1['drugName'],
        2: drug1['drugName'] + ['needs to be'] + increased() + ['it has been prescribed for'] + randTimePeriod('any') + ['the dose should therefore be reduced to'] + drug1['dose'],
        3: drug1['drugName'] + ["needs to be"] + [("increased","B-Action")] +["to"] + drug1['dose'] + increase_dose(),
        4: random.choice([["Patient is prescribed"],["Patient normally takes"]]) +  drug1['drugName'] + ["at a dose of"] + drug1['dose'] + random.choice([["please review need to"],['review need to'],['please']]) + increase_dose(),
        5: drug1['drugName'] + ["is prescribed at a dose of"] + drug1['dose'] + ["is this meant to be"] + drug1['newdose'] + reduce_dose(),
        6: drug1["dose"] + ["is a dose which is lower than the patients usual dose"] + drug1['newdose'] + ["review need to"] + increase_dose(),
        7: ["Patient is prescribed"] +  drug1['drugName'] + ["at a dose of"] + drug1['dose'] + ["Review need to"] + reduce_dose() + ["as this has likely been prescribed in error"],
        8: ["patient was advised to"] + [("increase","B-Action"),("the","I-Action"),("dose","L-Action")] + ["of"] + drug1["drugName"] + ["to"] + drug1["newdose"] + ["by"] + HCP() + ["in the clinic last"] + randDay("any"),
        9: Patient('gendered')+ ["has been taking"] + drug1["drugName"] + ["at a dose of"] + drug1["newdose"] + ["for the past"] + randTimePeriod('any') +  please() + increase_dose(),
        10: ["Patient states dose was"] + [("increased"),("B-Action")] +["but cannot remember who told them to do so"] + drug1["drugName"] + ["therefore needs reviewing and potentially"] + [("increasing","B-Action")] + ["to"] + drug1['newdose'],
        11:["The"] + Relative() + ["of"] +  Patient("gendered") + ["states that they were recently seen in clinic and the dose of"] + drug1['drugName'] + ["was"] + [("increased","B-Action")]  + ["from"] + drug1["dose"] + ["to"] + drug1["newdose"],
        12: drug1["drugName"] + ["was reduced from"] + drug1["dose"] + ["to"] + drug1["newdose"] + ["due to an interaction with"] +drug2["drugName"] + increase_dose(),
        13: drug1["drugName"] + ["reduces the plasma concentration of"] + drug2["drugName"] + ["when co-administered. A dose of"] +drug1["dose"] +["is therefore too low"] + increase_dose(),
        14: drug1["drugName"] + ["reduces the plasma concentration of"] + drug2["drugName"] + ["when co-administered. It is currentely prescribed as"] +drug1["dose"] +["can this be"] + [("increased",'B-Action')] + ["to"] + drug1["newdose"],
        15: ["The levels of"] + drug1["drugName"] + ["are reduced by"] + drug2["drugName"] + increase_dose(),
        16: pharmacokineticChange()  + ["review dose of"] + drug1["drugName"] + ["this may need"] +[("reducing","B-Action")]+ ["from"]+drug1["dose"]+ ["to"] + drug1["newdose"],
        17: pharmacokineticChange()  + ["please review"] + drug1["drugName"] + ["this may need"] + [("reducing","B-Action")] + ["to"] + drug1["newdose"],
        18: ["patient has a renal function of"] + [(f"{random.randrange(10,90,1)}ml/min","o")] + ["and is prescribed"] + drug1["drugName"] + ["as per"] + randomGuidance() + random.choice([["this should be"],["this needs to be"],["can this be"],["should this be"]]) + [("reduced","o")] + ["to"] + drug1["newdose"],
        19: drug1['drugName'] + ["needs to be"] + [("increased","B-Action")] +["to"] + drug1['dose']+ [f'{random.choice([["due to serious drug drug interaction"],["as it interacts with feed"],["is incompatible with feeding regime"]])}']+ increase_dose(),
        20: drug1['drugName'] + ["interacts with the following medications:"] + medicationList(random.randint(2,8)) + reduce_dose() + ["of"]+ drug1['drugName'],
        21: ['Patient has a low'] + [biochem['test']]  + drug1['drugName'] + random.choice([['is know to cause this'],[f'is known to increase {biochem["test"]}'],['can often be the cause']]) + increase_dose() + ['to'] + drug1['newdose'],
        22: drug1['drugName'] + ['needs to be'] + increased() + ['it has been prescribed for'] + randTimePeriod('any') + ['the dose should therefore be reduced to'] + drug1['dose'],
        23: random.choice([['decreased dose of'],['reduced dose of'],['the lower dose of']]) + drug1['drugName'] + random.choice([['is likely wrong'],['is probably wrong'],['is possibly wrong']]) + increase_dose()
    }
    choice = random.randrange(0, len(sentences),1)
    return tagsentences(sentences[choice])


def IncorrectMedications(drug1, drug2):
    actionChoice = represcribe()
    sentences = {
        0: drug1['drugName'] + ['has been prescribed instead of'] + drug2['drugName'] + please() + ['review this prescription and'] + [('discontinue','B-Action')] + drug1['drugName'] + random.choice([[' and prescribe correct medication'],[f'and prescribe {drug2["drugName"]}']]),
        1: ['Has'] + drug1['drugName'] + ['been prescribed intentionally. Should the prescription read'] + drug2['drugName'] + ['please'] + actionChoice + ['prescription'],
        2: random.choice([['The prescription for'],[f'A prescription dated {randomDate()}']]) + drug1['drugName'] +['for'] + Patient('') + random.choice([['is for a medication that the patient has never received'],['is not something they have taken before'],['is a medication that would not fit with their past medical history'],['was stopped by the gp last year'],['is a drug the patient no longer takes'],['does not fit with the presenting complaint'],[f'is similar in named to {drug2["drugName"]}'],['does not have an obvious indication'],[f'is a medication their {Relative()} normally takes. Has this been prescribed using an incorrect medication history'],[f'has a similar spelling to {drug2["drugName"]} has this been mistakenly selected on the electronic prescribing system']]) + please()  + actionChoice + ['prescription and'] + discontinue() + ['the incorrect medication'],
        3: ['has this presciption been written in error. Should'] + drug2['drugName'] + ['have been prescribed instead of'] + drug1['drugName'] + ['review need to'] + start() + ['for'] + drug1['drugName'] + ['and'] + discontinue() + drug2['drugName'],
        4: random.choice([['The prescription for'],['']])+ drug1["drugName"] + ['may have been written in error'] + random.choice([['can this be reviewed urgently'],['review this prescription'],['check that this is correct']]) + start() + drug2['drugName'] + ['in its place if appropriate'],
        5: Patient('') + ['has been prescribed'] + drug1['drugName'] + ['on'] + [randomDate()] + random.choice([['this is a drug the patient has never had before.'],['the patient doesnt appear to have had this before'],['they have never taken this drug'],['has this been started as a new prescription']]) + random.choice([['is this correct'],['is this the correct medication'],['has the correct medication been selected']]) + discontinue() + drug1['drugName'] + ['as appropriate'],
        6: Patient('') + ['has been prescribed'] + drug1['drugName'] + ['on'] + [randomDate()] + random.choice([['this is a drug the patient has never had before.'],['the patient doesnt appear to have had this before'],['they have never taken this drug'],['this isnt a drug they normally taken'],['this is not a medication they normally receive']]) + random.choice([['is this correct'],['is this the correct medication'],['has the correct medication been selected'],['has this been started as a new prescription']]) +drug1['dose'] + ['would be quite a high dose to start someone on initially'] +  discontinue()  + drug1['drugName'] + ['as appropriate']  + ['or please clarify why this has been prescribed'],
        7: ['The prescription for'] + drug1['drugName'] + random.choice([['appears to have been written in error'],['is not a medication the patient normally takes'],['is a drug this patient has never had before'],['does not sppear to be indicated for this patient'],[' has no clear indication in this patient']]) + ['review the need to'] + discontinue() + drug1['drugName'],
        8: please() + discontinue() + ['the prescription for'] + drug1['drugName'] + ['it'] + random.choice([['appears to have been written in error'],['is not a medication the patient normally takes'],['is a drug this patient has never had before'],['does not sppear to be indicated for this patient'],[' has no clear indication in this patient']]),
        9: drug1['drugName'] + ['prescribed as'] + drug2['drugName'] + represcribe(),
        10: random.choice([['please review the following medicines that the patient was taking prior to admission and '],['PLease review the following meds not prescribed'],['rv following meds not px']]) + start() + random.choice([['if clinically appropriate'],['if suitable'],['if appropriate']]) + medicationList(3),

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
    injection = randomInject('')
    sentences = {
        0: injection['drugName'] + ['has been prescribed intravenously at'] + injection['dose'] +['and also oraly at a dose of'] + injection['newdose'] + random.choice([['Should this therapy have been duplicated like this'],['is this correct'],['this is most likley unintentional'],['this appears to have been done in error']]) + please() + discontinue() + ['one of the prescriptions'] + random.choice([['can IV be stopped'],['is IV indicated?'],['oral option is sufficient']]) + ivostReasons(),
        1: drug1['drugName'] + ['has been prescribed twice'] + please() + discontinue() + ['one of the prescriptions'],
        2: Patient('') + ['has two active prescriptions for'] + drug1['drugName'] + random.choice([['There is an increased risk of overdose'],['patient is at risk of overdise']]) + ['can one ot the prescriptions be'] + discontinued(),
        3: drug1['drugName'] + ['and'] + drug2['drugName'] + ['are in the same medication class'] + random.choice([['no advantage is gained by prescribing both'],['increasing risk of overdose']]) + ['can one of the drugs be'] + discontinued() + please(),
        4: ['Both'] + drug1['drugName'] + ['and'] + drug2['drugName'] + ['are'] + randomDrugClass() + ['is this intentional normally the two wouldnt be prescribed together one of the medications may need to be']  + discontinued() + ['please review as a matter of urgency thanks'],
        5: random.choice([['both'],['two of the medications prescribed for this patient'],['the two medications'],['the two drugs']]) + drug1['drugName'] + ['and'] + drug2['drugName'] + random.choice([['have the same mechanism of action'],['have a very similar mechanism of action'],['work in exactly the same way'],['have an identical mechanism of action']]) + ['review the need to'] + discontinue() + drug1['drugName'],
        6: ['the patient chart has two instances of'] + drug1['drugName'] + ['this need to be looked at and'] + discontinued(),
        7: drug1['drugName'] + ['has been duplicated'] +discontinue() + drug1['drugName'],
        8: drug1['drugName'] + ['is prescribed via two separate routes review need to'] + discontinue() + ['one of the routes'],
        9: ['a'] + randomDrugClass() + ['and a'] + randomDrugClass() + ['provide the same therapeutic effect'] + ['please review this and'] + discontinue() + ['as appropriate']
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
    discontinuePastTense = discontinued()
    startPast  = started()
    sentences = {
        0: ["use of"] + drug1['drugName'] + ['is contraindicated in this patient please review this prescription and'] + discontinue() + drug1['drugName'],
        1: drug1['drugName'] + random.choice([['increases the risk of'],['may increase the risk of'],['can cause']]) + sideEffects() + please() + ['review need to'] + discontinue() + drug1['drugName'] + ['and start'] + drug2['drugName']+ ['instead'],
        2: drug1['drugName'] + random.choice([['increases the risk of'],['may increase the risk of'],['can cause'],['can increase the risk of'],['significantly increases risk of']]) + sideEffects() + ['particularly in patients with'] + pharmokineticIssue() + ["review this prescription and"] + discontinue() + ['is appropriate'],
        3: ['The medications'] + medicationList(3) + ['are all'] + random.choice([['cautioned'],['contraindicated'],['inappropriate']]) + ['in patients with'] + contraindicationType() + ['and may need to be'] + discontinuePastTense,
        4: drug1['drugName'] + ['is not recomended in'] + contraindicationType() + ['can an alternative be'] + startPast,
        5: randomGuidance() + random.choice([['states'],['dictates'],['recommends'],['advises'],['stipulates']])+ ['that'] + drug1['drugName'] + random.choice([['is not the first line choice'],['should be avoided'],['should not be used']]) + ['in patients with'] + contraindicationType() + please() + ['review need to'] + discontinue() + drug1['drugName'] + ['and'] + start() + drug2['drugName'],
        6: randomGuidance() + random.choice([['states'],['dictates'],['recommends'],['advises'],['stipulates']])+ ['that'] + drug1['drugName'] + random.choice([['is not the first line choice'],['should be avoided'],['should not be used']]) + ['in patients with'] + contraindicationType() + please() + discontinue() + drug1['drugName'],
        7: sideEffects() + ['prevents the use of'] + drug1['drugName'] + discontinue() + drug1['drugName'],
        8: Patient('') + ['has'] + contraindicationType() + ['and'] + drug1['drugName'] + ['has been newly started'] + ['this goes against advice from'] + randomGuidance() + ['as it is a known contraindication and is significant'] + [('review','B-Action'),('prescription','L-Action')],
        9: ['Patient suffers from'] + contraindicationType() + ['meaning that prescribing'] + drug1['drugName'] + random.choice([['would be inappropriate'],['should be avoided'],[f'is against {randomGuidance()} advice']]) + ['please review and'] + discontinue(),
        10: [('do','B-Action'),('not','I-Action'),('give','L-Action')] + drug1['drugName'] + ['it is contraindicated in'] + contraindicationType() 
    
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
    sentences = {
        0: ["the dose of"] + drug1["drugName"] + ["has been increased from"] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['was this an intentional increased'],['has this been done intentionally'],['however there is no documentation in the notes'],['this is not documented in the medical plan']]) + random.choice([['can this be reviewed'],['please review prescription'],['please review']]) + ['and'] + reduce_dose() + random.choice([['if this change was unintentional'],['if appropriate'],['if change was made in error']]),
        1: ["the dose of"] + drug1["drugName"] + ["has been increased from"] + drug1['dose'] + ['to'] + drug1['newdose'] + ['however the plan in the medical notes was to increase the dose from next'] + randDay('any'),
        2: drug1['drugName'] + random.choice([['was prescribed at a dose of'],['has been issued at'],['has been prescribed as']]) + drug1['newdose'] + ['since admission The patient normally only takes'] + drug1['dose'] + ['and this was the dose they were admitted on was this change intentional review need to'] + reduce_dose(),
        3: ['patient normally takes'] + drug1['drugName'] + drug1['dose'] + ['prescribed as'] + drug1['newdose'] + ['review need to'] + reduce_dose(),
        4: ['the increased dose of'] + drug1['newdose'] + ['for']  + drug1['drugName'] + ['is now above the max dose as per'] + randomGuidance() + ['review need to'] + reduce_dose(),
        5: drug1['drugName'] + ['has been increased to'] + drug1['newdose'] + ['however the maximum recommended dose for'] + drug1['drugName'] + ['is'] + drug1['dose'] + ['please'] + reduce_dose() + ['or'] + start() + ['an alternative'] + randomDrugClass() + ['such as'] + drug2['drugName'] + drug2['dose'],
        6: ['The plan as per the'] + planAuthor() + ['was to increase the dose'] + drug1['dose'] + ['from'] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['this hasnt been done as of yet'],['this has not been actioned']])+ please() + [("increase","B-Action"),('dose','L-Action')],
        7: ['The plan as per the'] + planAuthor() + ['was to increase the dose of'] + drug1['drugName'] + ['from'] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['this hasnt been done as of yet'],['this has not been actioned however the dose of']])+ drug2['drugName'] + ['has been increased from'] + drug2['dose'] + ['to'] + drug2['newdose'] +['has the wrong drug been increased'] + please() + ['review need to'] + reduce_dose() + ['of'] +drug2['drugName'] + ['and'] + increase_dose() + drug1['drugName'] + ['from'] + drug1['dose'] + ['to'] + drug2['newdose'],
        8: drug1['drugName'] + ['has a maximum dose of'] + drug1['dose'] + ['the does has been increased above this'] + please() + reduce_dose(),
        9: reduce_dose() + ['of'] + drug1['drugName'] + ['and'] + drug2['drugName'] + ['their doses have both been prescribed higher than the maximum dose']
    }
    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])

def incorrectDoseDecrease(drug1,drug2):
    sentences = {
        0: ["the dose of"] + drug1["drugName"] + ["has been decreased from"] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['was this an intentional decreased'],['has this been done intentionally'],['however there is no documentation in the notes'],['this is not documented in the medical plan']]) + random.choice([['can this be reviewed'],['please review prescription'],['please review']]) + ['and'] + increase_dose() + random.choice([['if this change was unintentional'],['if appropriate'],['if change was made in error']]),
        1: ["the dose of"] + drug1["drugName"] + ["has been decreased from"] + drug1['dose'] + ['to'] + drug1['newdose'] + ['however the plan in the medical notes was to decrease the dose from next'] + randDay('any'),
        2: drug1['drugName'] + random.choice([['was prescribed at a dose of'],['has been issued at'],['has been prescribed as']]) + drug1['newdose'] + ['since admission The patient normally only takes'] + drug1['dose'] + ['and this was the dose they were admitted on was this change intentional review need to'] + increase_dose(),
        3: ['patient normally takes'] + drug1['drugName'] + drug1['dose'] + ['prescribed as'] + drug1['newdose'] + ['review need to'] + increase_dose(),
        4: ['the decreased dose of'] + drug1['newdose'] + ['for']  + drug1['drugName'] + ['is now below the minimum dose as per'] + randomGuidance() + ['review need to'] + increase_dose(),
        5: drug1['drugName'] + ['has been decreased to'] + drug1['newdose'] + ['however the minimum recommended dose for'] + drug1['drugName'] + ['is'] + drug1['dose'] + ['please'] + increase_dose() + ['or'] + start() + ['an alternative'] + randomDrugClass() + ['such as'] + drug2['drugName'] + drug2['dose'],
        6: ['The plan as per the'] + planAuthor() + ['was to decrease the dose'] + drug1['dose'] + ['from'] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['this hasnt been done as of yet'],['this has not been actioned']])+ please() + [("decrease","B-Action"),('dose','L-Action')],
        7: ['The plan as per the'] + planAuthor() + ['was to decrease the dose of'] + drug1['drugName'] + ['from'] + drug1['dose'] + ['to'] + drug1['newdose'] + random.choice([['this hasnt been done as of yet'],['this has not been actioned however the dose of']])+ drug2['drugName'] + ['has been decreased from'] + drug2['dose'] + ['to'] + drug2['newdose'] +['has the wrong drug been decreased'] + please() + ['review need to'] + increase_dose() + ['of'] +drug2['drugName'] + ['and'] + reduce_dose() + drug1['drugName'] + ['from'] + drug1['dose'] + ['to'] + drug2['newdose'],
        8: drug1['drugName'] + ['has a minimum dose of'] + drug1['dose'] + ['the does has been decreased below this'] + please() + increase_dose(),
        9: increase_dose() + ['of'] + drug1['drugName'] + ['and'] + drug2['drugName'] + ['their doses have both been prescribed higher than the maximum dose'],
        10: drug1['drugName'] + random.choice([['has had its dose reduced to'],['has been reduced to'],['was changed to']]) + drug1['newdose'] + ['from'] + drug1['dose'] +['in response to'] + random.choice([['an increase in creatinine'],['a drop in eGFR'],['a low blood pressure'],['a high BP'],['a raised lactate'],['an AKI'],['reduced renal function']]) + ['this has now resolved review need to'] + increase_dose(),
        11: increase_dose() + ['of'] + drug1['drugName'] + ['it has been reduced in error'],
        12: increase_dose() + ['of'] + drug1['drugName'] + ['from'] + drug1['dose'] + ['to'] + drug1['newdose'] + ['it has likely been changed in error']
    }
    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])

def knownAllergy(drug1, drug2):
    # Medication Prescribed with known allergy	
    #GP records states patient previously had a bad rection too
    # Patient has previously had an allergic reaction to trimethoprim please review 
    # Allergy status has not bee updated and patient has previously had an allergic reaction to this medication 
    # Risk of cross reaction with allergy 
    # Patient has not tolerated this in the past
    # Patient recently had a reaction to this but it could have been that

    sentences = {
        0: Patient('gendered') + ['has a known allergy to'] + drug1['drugName'] + ['however it has been prescribed this admission'] + please() + ['review need to'] + discontinue(),
        1: ['Patient has a known allergy to'] +  drug1['drugName'] + ['having had a reaction of'] + allergyReaction() + please() + ['review need to'] + discontinue(),
        2: ['Patient has previously had an allergic reaction to'] +  drug1['drugName'] + ['review need to'] + start() + drug2['drugName'] + ['as an alternative'],
        3: ['The allergy history for this patient has not been updated since'] + [randomDate()] + ['the'] + medRecSource() + ['states that the patient recently had an allergic reaction to'] + drug1['drugName'] + random.choice([['please weigh up risk vs benefit and review neeed to'],['weigh up risks'],['review need to']]) + discontinue() + drug1['drugName'] + drug2['drugName'] + ['may provide a suitable alternative'],
        4: discontinue() + drug1['drugName'] + ['and'] + drug2['drugName'] + ['according to'] + random.choice([Relative(),medRecSource()]) +  ['patient has had a bad reaction to these in the past if alternative is required if an altenartive is required one of the following can be presrcribed'] + medicationList(3),
        5: [f'There is a {random.randint(1,10)}% risk of allergy cross-reaction with'] + drug2['drugName'] + ['when patient has a known allergy to'] + drug1['drugName'] + please() + start() + ['an alternative'],
        6: Patient('gendered') + random.choice([['has previously not tolerated'],['had previous bad reactions to'],['states they had a funny turn with'],['cannot tolerate'],['states they do not want to take'],['would rather avoid taking'],[f'has suffered from {allergyReaction()} whilst taking']]) + drug1['drugName'] + ['please'] +  discontinue() + ['and'] +start() + ['alternative'],
        7: ['A medication'] + Patient('gendered') + ['was recently started on caused them to suffer from'] + allergyReaction() + ['this could have been either'] + drug2['drugName'] + ['or'] + drug1['drugName'] + ['review need to'] + discontinue() + ['these medications'] + ['or'] + start() + ['an alternative'],
        8: random.choice([['Patient cannot remember their allergy status but thinks that they be allergic to'],['patient does not remember their allergies'],['patient cannot recall reaction to'],['patient thinks may have had a childhood reaction to']]) + drug1['drugName'] + ['review need to'] + discontinue(),
        9: ['Patient cant remember what type of reaction they have with'] + drug1['drugName'] + ['review need to']  + discontinue(),
        10: drug1['drugName'] + ['may cause'] + allergyReaction() + ['review need to'] + start() + ['alternative'] + ['such as'] + drug2['drugName']
    }
    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])

def adminTime(drug1,drug2):
    sentences = {
        0: drug1['drugName'] + ['has been prescribed'] + administrationTimes() + ['review need to'] + changeFrequency(),
        1: drug1['drugName'] + random.choice([['should be administered on an empty stomach as administering with food reduces the drugs absorbtion review need to'],['should be administered on an empty stomach'],['should be given separately to meal times'],['should not be given with food']])  + changeFrequency(),
        2: ['administration of'] + drug1['drugName'] + [f'should be at least {random.randint(1,5)} hours after and {random.randint(1,5)} before administration of'] + drug2['drugName'] + please() + changeFrequency() + ['of either'] + drug1['drugName'] + ['or'] + drug2['drugName'],
        3: drug2['drugName'] + random.choice([['should not be co-administered'],['cannot be given at the same time as'],['should not be administered with'],['administration should not be at the same time as']]) + drug1['drugName'] + changeFrequency(),
        4: Patient('gendered') + ['is prescribed'] + drug1['drugName'] + ['it is currently prescribed'] + administrationTimes() + ['it may be more appropriate to prescribe this']  + administrationTimes() + please() + changeFrequency()  + ['of'] + drug1['drugName'],
        5: ['Review need to'] + changeFrequency() + ['of'] + medicationList(3) + random.choice([['the enteral feed is likely to reduce their absorption'],['the efficacy of these medications will be reduced by the enteral feed'],['co-administration with the enteral feed will reduce absorbtion']]),
        6: ['Timing of the next dose of'] + drug1['drugName'] + [f'needs to be changed to allow for a {random.randint(1,3)} hour medication free period. review the need to'] + changeFrequency(),
        7: Patient('gendered') + ['is taking'] + drug1['drugName'] + randomGuidance() + random.choice([['states that the best time of administration is'],['advises that administration should be']]) + random.choice([['in the morning'],['at night'],['before food'],['after food'],['4 hours before food'],['at lunch time'],['in the evening'],['prior to bed'],['30 minutes before food']]) + changeFrequency(),
        8: ['Please'] + changeFrequency() + ['of'] + drug1['drugName'] + ['administration'] + administrationTimes() + random.choice([['is not advised'],['should be avoided'],['is advised against']]),
        9: random.choice([['the next dose of'],['the last dose of'],['a dose of']]) + drug1['drugName'] + ['is scheduled for'] + random.choice([['midnight'],['10pm'],['11pm'],['1am']]) +changeFrequency() + ['to a more suitable time']
    }
    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])


def incorrectFrequency(drug1,drug2):
    options = {
        0: drug1['drugName'] + random.choice([['has been prescribed on admission as'],['has been started at a frequency of'],['has been prescribed'],['is prescribed at a frequency of'],['is scheduled to be administered'],['has been selected as']]) + drug1['frequency'] + random.choice([['patient normally takes it'],['the usual maximum frequency is'],['it is usually'],['the normal frequency is']]) + randomFrequency(drug1['frequency']) + please() +['review need to'] + represcribe() + ['prescription'],
        1: ['As per the'] + randomGuidance() + drug1['drugName'] + random.choice([['is normally recommended at a frequency of'],['should usually be given as'],['is normally prescribed as'],['should have a frequency of']]) + randomFrequency(drug1['frequency']) + please() + ['can this be'] + represcribePastTense(),
        2: ['After discussion with'] + ['Dr'] + Patient('') + ['it has been agreed that the'] +  [('frequency','L-Freq')] + ['of'] + drug1['drugName'] + random.choice([['should be'],['needs to be'],['would be best prescribed as']]) + randomFrequency('') + please() + represcribe(),
        3: drug1['drugName'] + random.choice([['should be'],['needs to be'],['would be best prescribed as']]) + randomFrequency(drug1['frequency']) + ['instead of'] + drug1['frequency'],
        4: drug1['drugName'] + ['should have a frequency of'] + randomFrequency('') + please() + ['can this be'] + represcribePastTense(),
        5: ['A frequency of'] + randomFrequency(drug1['drugName']) + ['for'] + drug1['drugName']  + random.choice([['is not normally recommended'],['is not as per policy'],['is not the usual frequency']]) + ['can this be'] + represcribePastTense() + ['as'] + drug1['frequency'],
        6: Patient('gendered') + ['normally takes'] + drug1['drugName'] + drug1['frequency'] + ['please'] + represcribe() + ['as it is currently prescribed as'] + randomFrequency(drug1['frequency']),
        7: Patient('gendered') + ['has'] + pharmokineticIssue() + ['the frequency of'] + drug1['drugName'] + random.choice([['is therefore incorrect'],['needs to be reduced'],['needs to be increased']]) +['can the'] + [('frequency','B-Action'),('be','I-Action'),('changed','L-Action')],
        8: random.choice([['The normal frequency'],['the usual frequency'],['Usually the frequency of'],['the frequency of']]) + drug1['drugName'] + ['is'] + drug1['frequency'] + random.choice([['can this be looked at'],['this needs to be reviewed'],['this needs an urgent review']]) +['and the']  + [('frequency','B-Action'),('amended','L-Action')]
        #this is a tablet it should be a 
    }
    choice = random.randrange(0,len(options),1)
    return tagsentences(options[choice])


def incorrectRoute(drug1, drug2):
    #Incorrect route of administration	
    #Review route of administration. Ranitidine is prescribed orally however all medications are to be administered via the PEG
    sentences = {
        0: ['the prescription for'] + drug1['drugName'] +  ['states the route of administration is'] + drug1['route'] + random.choice([['can this be reviewed and prescribed as'],['would this be more appropriate as']]) + randomRoute(drug1['route']) + ['please review need to'] + represcribe(),
        1: ['Review'] + [('route','B-Route')] +  ['of administration of']  + drug1['drugName'] + ['it is prescribed'] + drug1['route'] + ['however all medications are to be administered via the'] + [('PEG','B-Route')] + please() + represcribe(),
        2: drug1['drugName'] + ['cannot be administered via the'] + drug1['route'] + [('route','B-Route')] + please() + ['review need to'] + amendRoute() + ['to'] + randomRoute(drug1['route']),
        3: ['The route of administration for'] + drug1['drugName'] + ['is currently prescribed as'] + drug1['route'] + ['please can this be reviewed'] + random.choice([['it is normally prescribed as'],['the usual route for this drug is'],['the most appropriate route is normally'],['The most appropriate route for this drug is usually'],['this patient normally takes this drug as']]) +  randomRoute(''),
        4: drug1['drugName'] + ['has been prescribed as'] + drug1['route'] + ['can this be reviewed, this drug is normally'] + [('prescribed','B-Action')]  + ['as'] + randomRoute(drug1['route']),
        5: Patient('') + ['cannot swallow'] + drug1['drugName'] + please() + amendRoute(),
        6: randomGuidance() + ['states that'] + drug1['drugName'] + ['cannot be given via this route'] + please() + amendRoute(),
        7: please() + amendRoute() + ['for the following medications'] + medicationList(3) + ['they are prescribed incorrectly'],
        8: ['Patient does not currently have IV access'] + please() + amendRoute()
    }
    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])

def unclearIndication(drug1,drug2):
    # x drg has been prescibred wthout a clera indicaiot okease reviewe
    # patient has beeen admitted wih c condition. y has been prescribed in response please review need to continue
    biochem = randomBiochem() 
    sentences = {
        0: drug1['drugName'] + ['has been prescribed without a clear indication'] + please() + discontinue() + ['and']+ represcribe() + ['alternative'],
        1: drug1['drugName'] + random.choice([['is not the normal first line option for'],['is not the normal first line option for the treatment of'],['is not in the policy for'],['is no longer recommended for'],['is not first choice for'],['should not be used for'],['should not  be used to treat'],['is not the first line treatment option for']]) + randomIndication() + please() + ['review need to'] + represcribe() + ['this prescription'],
        2: drug1['drugName'] + ['is normally used for'] + randomIndication() + ['there is no clear indication for its use in this patient'] + please()  + discontinue() + ['this prescription'],
        3: drug1['drugName']  + ['is the second line option for']+ randomIndication() + ['can this be'] + discontinued()+ ['and'] +  drug2['drugName'] + started() + ['instead'],
        4: Patient('gendered') + ['s'] + [biochem['test']] + ['is now'] + [biochem['inrange'] + biochem['unit']]  + drug1['drugName'] + ['can therefore be'] + discontinued() + ['as it is no longer indicated'],
        5: ['The indication for']+ drug1['drugName']  +random.choice([['is unclear'],['is not clear']]) + ['can this be reviewed and'] + discontinued(),
        6: ['Patients infection has resolved'] + discontinue() + ['antibiotics'],
        7: drug1['drugName'] + ['is no longer recomended for'] + randomIndication() + drug2['drugName'] + ['is now the first line option'] + discontinue() + drug1['drugName'] + ['and'] + start() + drug2['drugName'],
        8: discontinue() + drug1['drugName'] + ['this patient doesnt need it'],
        9: ['Not sure why patient is prescribed'] + drug1['drugName'] + discontinue() + ['it']
    }
    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])


def inadequateMonitoring(drug1,drug2):
    #Review need to take a digoxin level 
    #drug c requires monitoring of randomLevel
    biochem = randomBiochem()
    sentences =  {
        0: ['Regular monitoring of']  + [biochem['test']] + ['is recommended with'] + drug1['drugName'] + random.choice([['can a level be organised for next'],['can a level be arranged for next'],['can a level be sent for next']]) + randDay('any'),
        1: ['Patient has been taking']  + drug1['drugName'] + ['for the past'] + randTimePeriod('any') + random.choice([['this drug requires regular monitoring of'],['this requires monitoring of'],['review need to send a level for']]) + [biochem['test']] + please() + ['review need to'] + biochemMonitoring(),
        2: [biochem['test']] + random.choice([['has not been measured'],['has not been taken'],['is not being monitored routinely']]) + drug1['drugName'] + ['and'] + drug2['drugName'] + ['require close monitoring. please'] +biochemMonitoring(),
        3: ['Please'] + biochemMonitoring() + ['patient is on several medications which need monitoring including']  + medicationList(4),
        4: drug1['drugName'] + ['and'] + drug2['drugName'] + ['require daily levels of'] +[biochem['test']] + ['ensure that the plan is to'] + biochemMonitoring() + ['and if high'] + reduce_dose() + random.choice([['accordingly'],['as approrpiate'],['as recomended']]),
        5: [('Monitor','B-Action')] + ['heart rate daily'] + drug1['drugName'] + ['is known to reduce the heart rate'],
        6: ['blood pressure must be'] + [('monitored'),('B-Action')] + ['regularly for patients on'] + drug1['drugName'],
        7: ['Consider replacement of'] + [biochem['test']] + ['replace if appropriate']
    }

    choice = random.randrange(0,len(sentences),1)
    return tagsentences(sentences[choice])

def prescriptionDuration(drug1,drug2):
    sentences = {
        0: drug1['drugName'] + ['has been prescribed for'] +randTimePeriod('any') + random.choice([['courses of this drug are usually limited'],['this drug should be prescribed for the shortest time possible'],['this is longer than the normal course lenght'],['should this have already finished'],['patient has now had a prolonged course'],['course length does not usually exceed a couple of days'],['this is longer than normal']])+ ['please review need to'] + discontinue(),
        1: drug1['drugName'] + ['has been prescribed since last'] + randDay('any') + random.choice([['courses of this drug are usually limited'],['this drug should be prescribed for the shortest time possible'],['this is longer than the normal course lenght'],['should this have already finished'],['patient has now had a prolonged course'],['course length does not usually exceed a couple of days'],['this is longer than normal']])+['please review need to'] + discontinue(),
        2: drug1['drugName'] + ['has been prescribed since'] + [randomDate()]+ random.choice([['courses of this drug are usually limited'],['this drug should be prescribed for the shortest time possible'],['this is longer than the normal course lenght'],['should this have already finished'],['patient has now had a prolonged course'],['course length does not usually exceed a couple of days'],['this is longer than normal']])+ ['please review need to'] + discontinue(),
        3: drug1['drugName'] + ['has been prescribed for'] +randTimePeriod('any')+ random.choice([['courses of this drug are usually limited'],['this drug should be prescribed for the shortest time possible'],['this is longer than the normal course length'],['should this have already finished'],['patient has now had a prolonged course'],['course length does not usually exceed a couple of days'],['this is longer than normal']])+ ['please review need to'] + reviewDate(),
        4: Patient('gendered') + random.choice([['has been taking'],['has been prescribed'],['has been using']]) + drug1['drugName'] + ['for'] + randTimePeriod('any') + ['please review need to'] + discontinue() + ['or'] + reviewDate(),
        5: ['Usual course length for'] + drug1['drugName'] + ['is'] + randTimePeriod('days') + ['as per'] + randomGuidance() + random.choice([['this has now been exceeded'],['this means the course should complete tomorrow'],['one day remains of this course']]) + ['can you'] + please() + reviewDate()
    }
    

    choice = random.randrange(0, len(sentences),1)
    return tagsentences(sentences[choice])
    #Duration of prescription has exceeded course length	Amoxicillin has been prescribed for 7 days please review need to discontinue

def medicationOverprescribing(drug1,drug2):
    sentences = {
        0: random.choice([['Patient'],Patient('gendered')]) + ['has been prescribed'] + drug1['drugName']+ please() + discontinue() +  random.choice([['the patient no longer takes this medication'],[f'the patient hasnt taken this medication for {random.randint(1,6)} months'],['the patient is not taking this anymore'],['they are not taking this anymore'],['they no longer take this medication'],[f'they no longer take this']]),
        1: drug1['drugName']  + ['has been prescribed'] + random.choice([['the patient no longer takes this medication'],[f'the patient hasnt taken this medication for {random.randint(1,6)} months'],['the patient is not taking this anymore']]) + please() + ['review need to'] + discontinue(),
        2: please() + ['Review'] + drug1['drugName'] + ['and'] + discontinue() + ['if appropriate would the patient be better off taking'] + drug2['drugName'],
        3: drug1['drugName'] + random.choice([['is one of the strongest drugs in its class'],['is more potent than other medications in the same class']]) + random.choice([['can this be reviewed and an alternative'],['can an alternative be']]) + started(),
        4: ['A dose of'] + drug1['dose'] + ['is higher than necessary for this patient as they have'] + pharmokineticIssue() + ['guidance as per'] + randomGuidance() + ['recommends a dose of'] + drug1['newdose'] + ['review need to'] + reduce_dose() + ['or'] + start() + ['an alternative']
    }
    

    choice = random.randrange(0, len(sentences),1)
    return tagsentences(sentences[choice])

def interactions(drug1, drug2):
    #Drug interaction	Rifampicin will reduce the plasma concentration of clarithromycin due to an interaction review need to switch antibiotics
    sentences = {
        0: drug1['drugName'] + random.choice([['reduces the levels of'],['will reduce the plasma concentration of'],['increases the levels of'],['reduces the levels of'],['competes with'],['increased the clearance of'],['reduces the clearance of']]) + drug2['drugName'] + ['review need to'] + discontinue() + random.choice([[drug1['drugName']],drug2['drugName']]),
        1: drug1['drugName'] + random.choice([['reduces the levels of'],['will reduce the plasma concentration of'],['increases the levels of'],['reduces the levels of'],['competes with'],['increased the clearance of'],['reduces the clearance of']]) + drug2['drugName'] + ['review need to'] + reduce_dose() + ['of'] + random.choice([[drug1['drugName']],drug2['drugName']]),
        2: drug1['drugName'] + random.choice([['reduces the levels of'],['will reduce the plasma concentration of'],['increases the levels of'],['reduces the levels of'],['competes with'],['increased the clearance of'],['reduces the clearance of']]) + drug2['drugName'] + ['review need to'] + start() + ['an alternative'],
        3: random.choice([['patient is at risk of an interaction with'],['an interaction will occur between'],['An interaction between']]) + drug1['drugName'] + ['and'] + drug2['drugName'] + random.choice([['will increase the risk of side effects'],['may cause an adverse event'],['increase the risk of an adverse event'],[f'increase the risk of {sideEffects()}']]) + ['review need to'] + start() + ['alternative or'] + discontinue() + drug1['drugName'] + ['or'] + drug2['drugName'],
        4: ['dose of'] + drug1['drugName'] + ['should be'] + random.choice([['reduced'],['increased']]) + ['by'] + random.choice([['25%'],['50%'],['30%']]) + ['when'] + random.choice([['co-administered with'],['given with'],['prescribed alongside'],['prescribed at the same time as'],['given at the same time as']]) + drug2['drugName'] + ['can dose be'] + represcribePastTense(),
        5: drug1['drugName'] + ['and'] + drug2['drugName'] + ['must not be given together they belong to the same class of']  + randomDrugClass() + discontinue() + ['both medications'],
        6: ['An interaction between'] + drug1['drugName'] + ['and'] +drug2['drugName'] + random.choice([['is best avoided'],['should be avoided'],['means they should be co-administered'],['is advised against']]) + please() + discontinue() +['one of these drugs']  + ['and review need to start an alternative such as'] + medicationList(1),
        7: drug1['drugName'] + ['reduces the absorption of'] + drug2['drugName'] + ['review need to '] + start() + ['an alternative'],
        8: Patient('gendered') + ['states'] + drug1['drugName']+ ['was reduced in dose due to a drug interaction with'] + drug2['drugName'] +  drug2['drugName'] + ['has now been stopped please review need to'] + increase_dose() + random.choice([['back to original dose'],['to prvious dose'],['to original dose']]) + random.choice([['patient is however stable on this new dose so no dose change may be necessary'],['patient is stable on new dose'],['dose could potentially could be increased further'],['blood pressure should be checked before change'],['check UEs in a week if changed'],['increasing the dose could however increase risk of AKI']])
    }

    choice = random.randrange(0, len(sentences),1)
    return tagsentences(sentences[choice])

def transitionErrors(drug1,drug2):
    sentences = {
        0: ['Patient has had a recent admission on']  + randomWard() + ['where'] + drug1['drugName'] + ['was increased from'] + drug1['dose'] + ['to'] + drug2['newdose'] + random.choice([['this was not communicated to GP'],['GP record has not been updated'],['this was not included in the discharge letter'],['this was not communicated on discharge'],['the GPs system has not yet been updated']])+ ['can the dose be'] + represcribePastTense(),
        1: ['last admission'] + drug1['drugName'] + ['was changed to'] +  drug2['drugName'] + random.choice([['current medications can been prescribed from an old list'],['GP system has not been updated yet'],[f'{drug1["drugName"]} has been prescribed however'],['an old GP record has been used for clerking medications in']]) + ['review need to'] + start() + drug2['drugName'] + ['and'] + discontinue() + drug1['drugName'],
        2: Patient('gendered') + random.choice([['recently had a medications review'],['was recently seen by their GP'],['recently had a clinic appointment'],['attended an outpatient clinic last week']]) + random.choice([['where they were told to stop'],['and they were told to stop taking']]) + drug1['drugName'] + ['please review need to'] + discontinue() + ['the change has not yet been updated on the patients medical record'],
        3: random.choice([['patient recently changed address'],['patient has recently moved house'],['patient has switched GP in the past few weeks'],['patient moved house one week ago']]) + random.choice([['GP record has not been updated since'],['the patients medication has not yet been updated'],['The summary care record does therefore not reflect recent changes to the patients medications'],['the gp record is therefore out of date'],['the medication record has not been transferred to the patients new GP']]) + please() + ['check the medication history carefully'] + drug1['drugName'] + ['may need to be'] + discontinued()
    }
    choice = random.randrange(0, len(sentences),1)
    return tagsentences(sentences[choice])



#Poor compliance	Patient struggles with taking alfusozin three times daily please review need to switch to a once daily preparation
def poorCompliance(drug1, drug2):
    sentences = {
        0: ['Patient struggles with taking'] + drug1['drugName'] +multipleFrequency()[1]+ ['please review need to ']+ start() + drug2['drugName'] + ['which allows'] +[('reducing','B-Action'),('the','I-Action'),('frequency','L-Action')] + ['to']+ multipleFrequency()[0],
        1: ['Patient reports poor compliance with'] + drug1['drugName'] + ['review need to'] + start() +['an alternative'],
        2: ['Patient has not been taking medication as prescribed review need to'] + discontinue() +['or'] + start() + ['an alternative'],
        3: ['The patients'] + Relative() + random.choice([['has informed ward staff'],['has stated'],['states']])+ ['that'] + Patient('gendered') + random.choice([['does not take their medication as prescribed'],['has poor compliance with their medications'],['has not been taking their medications'],['has not been taking their medications as prescribed']]) + random.choice([['they take several medications including'],['these medications include'],['they are taking']]) + medicationList(5) + ['can these be reviewed and possible'] + discontinued() + ['or alternatives'] + started(),
        4: ['Patient has not started taking'] + drug1['drugName'] + ['for their'] + randomIndication() + ['can this be'] + represcribePastTense() + ['as an alternative or'] + discontinued(),
        5: Patient('gendered') + ['has never taken'] + drug1['drugName'] + start() + ['an alternative']
    }
    choice = random.randrange(0, len(sentences),1)
    return tagsentences(sentences[choice])

def startNew(drug1, drug2): 
    sentences = {
        0: ['latest guidance from'] + randomGuidance() + ['states that first line option for'] + randomIndication() + ['is'] + drug1['drugName'] + ['review need to'] + start() + drug1['drugName'],
        1: ['Patient has a diagnosis of'] + randomIndication() + random.choice([['however is not on treatment'],['but isnt currently on treatment for this'],['and has never been treated for this'],['they are not taking optimal treatment for this condition']]) + random.choice([['can'],['should']]) + drug1['drugName'] + ['be']  + started() + ['normal starting dose would be'] + drug1['dose'],
        2: start() + drug1['drugName'] + ['for the treatment of'] + randomIndication(),
        3: drug1['drugName'] + random.choice([['is currently out of stock'],['has been discontinued'],['has a long term manufacturing problem'],['is not available from the wholesaler']]) + ['can it be'] + discontinued() + drug2['drugName'] + ['can be'] + started() + ['as an alternative'],
        4: drug1['drugName'] + drug1['dose']  +drug1['frequency'] + ['was started by'] + HCP_location() + ['can this be'] + started(),
        5: ['Patient is suffering from'] + sideEffects() + ['review need to'] + [('treat','B-Action'),('with','L-Action')] + drug1['drugName'],
        6: random.choice([['Please review need to re-start'],['review need to start']]) + drug1['drugName'] + random.choice([['prophylaxis once'],['prophylaxis after']]) + drug2['drugName'] + random.choice([['course if finished'],['is completed']]),
        7: ['please review missing pre-amdmission medications and'] + start() + medicationList(2),
        8: random.choice([['several medications missing on patients chart'],['missing medications not prescribed'],['missing medications include'],['missing reg meds']]) + medicationList(3) + ['please'] + start(),
        9: drug1['drugName'] + ['and'] + drug2['drugName'] + ['not'] + [('prescribed','B-Action')],
        10: drug2['drugName'] + ['not'] + [('prescribed','B-Action')],
        11: ['FAO DOCTORS - Please review the following'] + start() + ['missing meds'] + medicationList(3)
    }
    choice = random.randrange(0, len(sentences),1)
    return tagsentences(sentences[choice])

def formularySwitch(drug1,drug2):
    sentences = {
        0: randomGuidance() + ['guidance published'] + [randomDate()] + random.choice([['recomends a new cost effective option for'],['recommends that for the treatment of'],['advises that for']]) + randomIndication() + drug1['drugName'] + ['should be used can this be'] + started(),
        1: random.choice([['The license of'],['The product literature for']]) + drug1['drugName'] + random.choice([['has changed'],['has been updated']]) + ['it is no longer indicated'] + random.choice([['review need to'],['please can this be']]) + discontinued(),
        2: ['The dosing guidance for'] + drug1['drugName'] + random.choice([['has been updated'],['has changed'],['was recently published']]) + please() + increase_dose() + random.choice([['in line with patients renal function'],['providing their weight is up to date'],['after weighing patient']]),
        3: random.choice([['the local formulary committee'],['the regional medicines management committee'],['the trust drugs and therapeutics group']]) + random.choice([['has approved the use of'],['have recommended the use of']]) + drug1['drugName'] + ['for'] + randomIndication(),
        4: drug1['drugName'] + random.choice([['is no longer the first line formulary choice'],['is not the first formulary choice'],['is not first line on the formulary'],['is no longer recommended']]) + discontinue() + ['the prescription'],
        5: drug1['drugName'] + ['is a more cost effective'] + randomDrugClass() + ['than'] + drug2['drugName'] + discontinue() + drug1['drugName'] + ['and'] + start() + drug2['drugName']
    }
    choice = random.randrange(0, len(sentences),1)
    return tagsentences(sentences[choice])


def test(): 

    drug1 = randomAny('increase')
    drug2 = randomAny('increase')
    
    s = formularySwitch(drug1,drug2)

    return s
    
print(test())


def create():
    #types
    interventionTypes = {
     
        0:{
            "func": reduceDoses,
            "type": "reduce_doses",
            "weight": 10,
            "amend": "reduce"
        },
        1:{
            "func": increaseDose,
            "type": "increase_doses",
            "weight": 10,
            "amend": "reduce"
        },
        2:{
            "func": IncorrectMedications,
            "type": "incorrect_medications",
            "weight": 20,
            "amend": ""
        },
        3:{
            "func": duplicatedTherapy,
            "type": "duplicated_therapy",
            "weight": 20,
            "amend": ""

        },
        4: {
            "func": contraindications,
            "type": "contradindications",
            "weight": 20,
            "amend": ""
        }, 
        5: {
            "func": incorrectDoseIncrease,
            "type": "incorrect_dose_increase",
            "weight": 20,
            "amend": "increase"
        },
        6: {
            "func": incorrectDoseDecrease,
            "type": "incorrect_dose_decrease",
            "weight": 20,
            "amend": "reduce"
        },
        7:  {
            "func": knownAllergy,
            "type": "known_allergy",
            "weight": 20,
            "amend": ""
        },
        8:  {
            "func": adminTime,
            "type": "admin_time",
            "weight": 20,
            "amend": ""
        },
        9:  {
            "func": incorrectFrequency,
            "type": "incorrect_frequency",
            "weight": 20,
            "amend": ""
        },
        10:  {
            "func": incorrectRoute,
            "type": "incorrect_route",
            "weight": 20,
            "amend": ""
        },
        11:  {
            "func": unclearIndication,
            "type": "unclear_indication",
            "weight": 20,
            "amend": ""
        },
        12:  {
            "func": inadequateMonitoring,
            "type": "inadequate_monitoring",
            "weight": 20,
            "amend": ""
        },
        13:  {
            "func": prescriptionDuration,
            "type": "prescription_duration",
            "weight": 20,
            "amend": ""
        },
        14:  {
            "func": medicationOverprescribing,
            "type": "medication_overprescribing",
            "weight": 20,
            "amend": ""
        },
        15:  {
            "func": interactions,
            "type": "interactions",
            "weight": 20,
            "amend": ""
        },
        16:  {
            "func": transitionErrors,
            "type": "transition_errors",
            "weight": 5,
            "amend": ""
        },
        16:  {
            "func": poorCompliance,
            "type": "poor_compliance",
            "weight": 5,
            "amend": ""
        },
        17: {
            "func": startNew,
            "type": "start_new",
            "weight": 5,
            "amend": ""
        },
        18: {
            "func": formularySwitch,
            "type": "formulary_switch",
            "weight": 5,
            "amend": ""
        },
        19: {
            "func":"double"
        }
    }


    #output:   [Type, note , tagged]
    data = []
    epochs = 200
    for epoch in range(epochs):
        print(f'Epoch: {epoch} of {epochs}')
        for y in range(len(interventionTypes)):
            intervention = interventionTypes[y]
            if intervention['func'] != 'double':
                for i in range(intervention['weight']):
                    drug1 = randomAny(intervention['amend'])
                    drug2 = randomAny(intervention['amend'])
                    try:
                        note = intervention['func'](drug1,drug2)
                    except:
                        print(f'Failed {intervention["type"]}')
                    text = ''
                    for a in note: 
                        text = text + str(a[0]) + " "
                    data.append([intervention['type'],text,note])
            elif intervention['func'] == 'double':
                pass
                #create a dunction to put multiple jobs in one note
    df = pd.DataFrame(data)
    df = df.sample(frac=1)
    df.to_csv('datacollection1.csv', index=False)



    #return random.choice(interventionTypes)(drug1,drug2)
#create()


