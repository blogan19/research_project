import random

def represcribe():
    represcribeActions = {
        0: [('represcribe','B-Action')],
        1: [('re-prescribe','B-Action')],
        2: [('amend','B-Action')],
        3: [('review','B-Action')],
        4: [('alter', 'B-Action')],
        5: [('change','B-Action')]

    }
    choice = random.randrange(0,len(represcribeActions),1)
    return represcribeActions[choice]

def represcribePastTense():
    represcribeActions = {
        0: [('represcribed','B-Action')],
        1: [('re-prescribed','B-Action')],
        2: [('amended','B-Action')],
        3: [('reviewed','B-Action')],
        4: [('altered', 'B-Action')],
        5: [('changed','B-Action')]
    }
    choice = random.randrange(0,len(represcribeActions),1)
    return represcribeActions[choice]

def discontinue():
    discontinueActions= {
        0: [('discontinue','B-Action')],
        1: [('stop','B-Action')],
        2: [('delete','B-Action')],
        3: [('remove','B-Action')],
        4: [('suspend','B-Action')],
        5: [('temporarily','B-Action'),('suspend','L-Action')]
    }
    choice = random.randrange(0,len(discontinueActions),1)
    return discontinueActions[choice]

def discontinued(): 
    discontinueActionPastTense = {
        0: [('discontinued','B-Action')],
        1: [('stopped','B-Action')],
        2: [('deleted','B-Action')],
        3: [('removed','B-Action')],
        4: [('suspended','B-Action')],
        5: [('temporarily','B-Action'),('suspended','L-Action')]
    }
    choice = random.randrange(0,len(discontinueActionPastTense),1)
    return discontinueActionPastTense[choice]

def start():
    startActions= {
        0: [('start','B-Action')],
        1: [('resume','B-Action')],
        2: [('prescribe','B-Action')],
        3: [('add','B-Action'),('a','I-Action'),('prescription','I-Action'),('for','o')],
        4: [('generate','B-Action'),('an','I-Action'),('order','L-Action')],
    }
    choice = random.randrange(0,len(startActions),1)
    return startActions[choice]

def started():
    startPastTense = {
        0: [('started','B-Action')],
        1: [('prescribed','B-Action')],
        2: [('commenced','B-Action')]
    }
    choice = random.randrange(0,len(startPastTense),1)
    return startPastTense[choice]

def reduced():
    reduction_actions = {
            0: [('re-prescribed','B-Action'),('at','I-Action'),('a','I-Action'),('lower','I-Action'),('dose','L-Action')],
            1: [('amended','B-Action')],
            2: [('decreased','B-Action')],
            3: [('reduced','B-Action')],
            4: [('re-prescribed')],
            5: [('represcribed','B-Action')],
            6: [('changed','B-Action')],
            7: [('lowered','B-Action')]
        }
    choice = random.randrange(0,len(reduction_actions),1)
    return reduction_actions[choice]

def reduce_dose():
    reduction_actions = {
            0: [('re-prescribe','B-Action'),('at','I-Action'),('a','I-Action'),('lower','I-Action'),('dose','L-Action')],
            1: [('amend','B-Action'),('dose','L-Action')],
            2: [('decrease','B-Action'),('dose','L-Action')],
            3: [('reduce','B-Action'),('dose','L-Action')],
            4: [('re-prescribe','B-Action')],
            5: [('represcribe','B-Action')],
            6: [('change','B-Action'),('dose','L-Action')],
            7: [('review','B-Action'),('need','I-Action'),('to','I-Action'),('amend','I-Action'),('the','I-Action'),('dose','L-Action')],
            8: [('lower','B-Action'),('the','I-Action'),('dose','L-Action')],
            9: [('decrease','B-Action'),('the','I-Action'),('dose','L-Action')]
        }
    choice = random.randrange(0,len(reduction_actions),1)
    return reduction_actions[choice]

def increase_dose():
    increase_actions = {
            0: [('re-prescribe','B-Action'),('at','I-Action'),('a','I-Action'),('higher','I-Action'),('dose','L-Action')],
            1: [('amend','B-Action'),('dose','L-Action')],
            2: [('increase','B-Action'),('dose','L-Action')],
            3: [('re-prescribe','B-Action'),('dose','L-Action')],
            4: [('represcribe','B-Action')],
            5: [('change','B-Action'),('dose','L-Action')],
            6: [('review','B-Action'),('need','I-Action'),('to','I-Action'),('amend','I-Action'),('the','I-Action'),('dose','L-Action')],
            7: [('increase','B-Action'),('the','I-Action'),('dose','L-Action')],
            8: [('raise','B-Action'),('dose','L-Action')],
            9: [('prescribe','B-Action'),('at','I-Ation'),('higher','I-Action'),('dose','L-Action')]
        }
    choice = random.randrange(0,len(increase_actions),1)
    return increase_actions[choice]
def increased():
    reduction_actions = {
            0: [('re-prescribed','B-Action'),('at','I-Action'),('a','I-Action'),('lower','I-Action'),('dose','L-Action')],
            1: [('amended','B-Action')],
            2: [('increased','B-Action')],
            3: [('re-prescribed')],
            4: [('represcribed','B-Action')],
            5: [('changed','B-Action')],
        }
    choice = random.randrange(0,len(reduction_actions),1)
    return reduction_actions[choice]

def changeFrequency():
    options = {
        0: [('amend','B-Action'),('frequency','L-Action')],
        1: [('change','B-Action'),('frequency','L-Action')],
        2: [('amend','B-Action'),('adminstration','I-Action'),('times','L-Action')],
        3: [('adjust','B-Action'),('frequency','L-Action')],
        4: [('alter','B-Action'),('frequency','L-Action')]
    }
    choice = random.randrange(0,len(options),1)
    return options[choice]

def amendRoute():
    options = {
        0: [('amend','B-Action'),('route','L-Action')],
        1: [('change','B-Action'),('route','L-Action')],
        2: [('adjust','B-Action'),('route','L-Action')],
        3: [('alter','B-Action'),('route','L-Action')],
        4: [('adjust','B-Action'),('route','L-Action')]
    }
    choice = random.randrange(0,len(options),1)
    return options[choice]

def biochemMonitoring():
    options = {
        0: [('send','B-Action'),('level','L-Action')],
        1: [('take','B-Action'),('bloods','L-Action')],
        2: [('send','B-Action'),('bloods','L-Action')],
        3: [('monitor','B-Action'),('levels','I-Action'),('accordingly','L-Action')]
    }
    choice = random.randrange(0,len(options),1)
    return options[choice]

def reviewDate():
    options = {
        0: [('add','B-Action'),('stop','I-Action'),('date','L-Action')],
        1: [('add','B-Action'),('course','I-Action'),('length','L-Action')],
        2: [('add','B-Action'),('review','I-Action'),('date','L-Action')],
        3: [('specify','B-Action'),('course','I-Action'),('length','L-Action')]
    }
    choice = random.randrange(0,len(options),1)
    return options[choice]
