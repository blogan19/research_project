import random
import names
def Patient(): 
    name = names.get_first_name()
    return (name,'o')
def HCP(): 
    #returns array
    hcp = {
        0: [('GP','o')],
        1: [('A/E','o')],
        2: [('walk','o'),('in','o'),('center','o')],
        3: [('specialist','o'),('nurse','o')],
        4: [('out','o'),('of','o'),('hours','o'),('GP','o')],
        5: [('NHS','o'),('111','o')],
        6: [('community','o'),('pharmacy','o')]
    }
    choice = random.randrange(0,len(hcp),1)
    return hcp[choice]



