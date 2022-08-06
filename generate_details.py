import random
import names


def Patient(type): 
    name = names.get_last_name()
    x = random.choice([0,1])
    genderedName = ''
    if x == 0: 
        genderedName = [("Mr ",'o'),(name,'o')]
    else: 
        genderedName = [("Mrs ","o"),(name,"o")]

    if type == 'gendered':
        return genderedName
    else:
        return [name]

def Relative():
    relatives = {
        0: [("Daughter","o")],
        1: [("Son","o")],
        2: [("Wife","o")],
        3: [("Husband","o")],
        4: [("Niece","o")],
        5: [("Nephew","o")],
        6: [("Son in law","o")],
        7: [("Daughter in law","o")],
        8: [("Step son","o")],
        9: [("Step Daughter","o")],
        10: [("Grandson","o")],
        11: [("Grandaughter","o")],
        12: [("Nephew","o")],

    }
    choice = random.randrange(0,len(relatives),1)
    relative = relatives[choice]
    return relative

def Pharmacist():
    name = [(names.get_first_name(),'o')]
    full = names.get_full_name().split(" ")
    fullName = [(full[0],'o'),(full[1],'o')]
    speciality = ['respiratory','cardiology','endocrinology','transplant','antimicrobial','antibiotic','frailty','renal','EPMA']
    jobTitles = {
        0: [('Pre-registration','o'),('Pharmacist','o')],
        1: [('Senior','o'),('Pharmacist','o')],
        2: [('Advanced','o'),('Clinical','o'),('Pharmacist','o')],
        3: [('Specialist','o'),('Pharmacist','o')],
        4: [('Trainee','o'),('Pharmacist','o')],
        5: [(random.choice(speciality),'o'),('pharmacist','o')]
    }
    x = random.randint(1,100)
    jt = []
    if x <= 80:
        jt.append(('Pharmacist','o'))
    else: 
        choice = random.randrange(0,len(jobTitles),1)
        jt = jt + jobTitles[choice]
    
    #bleep or phone
    randomNumber = random.randint(1000,9999)
    phoneType = {
        0: [('Bleep:','o'),(randomNumber,'o')],
        1: [('Ext:','o'),(randomNumber,'o')],
        2: [('#','o'),(randomNumber,'o')],
    }
    phone =  phoneType[random.randrange(0,len(phoneType),1)]
    #random ward 
    wardDigit = random.choice(['1','2','3','4','5'])
    wardAlpha = random.choice(['A','B','C','D','E'])
    ward = [('ward','o'),(wardDigit+wardAlpha,'o')]
        
    options = {
        0: phone,
        1: ward,
        2: jt,
        3: phone + ward,
        4: phone + jt,
        5: jt + ward,
        6: jt + phone + ward,
        7: ['']
    }
    user = random.choice([name, fullName]) + options[random.randrange(0,len(options),1)]
    return user

def HCP(): 
    #returns array
    hcp = {
        0: [('the','o'),('GP','o')],
        1: [('a','o'),('pharmacist','o')],
        2: [('a','o'),('doctor','o')],
        3: [('a','o'),('nurse','o')],
        4: [('a','o'),('specialist','o'),('nurse','o')],
        5: [('Dr','o'),(names.get_last_name(),'o')]
    }
    choice = random.randrange(0,len(hcp),1)
    return hcp[choice]

def HCP_location(): 
    #returns array
    hcp = {
        0: [('GP','o')],
        1: [('A/E','o')],
        2: [('Accident and Emergency','o')],
        3: [('a','o'),('nurse','o'),('at','o'),('the','o'),('walk','o'),('in','o'),('centre','o')],
        4: [('a','o'),('specialist','o'),('nurse','o')],
        5: [('the','o'),('out','o'),('of','o'),('hours','o'),('GP','o')],
        6: [('NHS','o'),('111','o')],
        7: [('the','o'),('community','o'),('pharmacist','o')]
    }
    choice = random.randrange(0,len(hcp),1)
    return hcp[choice]

def randDay(type):
    weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    weekends = ["Saturday","Sunday"]
    all = weekdays + weekends
    if type =="weekday":
        return [(random.choice(weekdays),"o")]
    if type == "weekend":
        return [(random.choice(weekends),"o")]
    if type == "any":
        return [(random.choice(all),"o")]

def randTimePeriod(type):
    gap = None
    if type == "any":
        gap = random.choice([0,1])
    elif type == 'days':
        gap = 0
    elif type == 'weeks':
        gap = 1
    
    timeperiod = None
    if gap == 0:
        timeperiod = [(random.randrange(2,28,1),'o'),('days','o')]
    elif gap == 1:
        timeperiod = [(random.randrange(2,6,1),'o'),('weeks','o')]

    return timeperiod

def please():
    if random.choice([0,1]) == 0:
        return [("please","o")]
    else:
        return[]


def randomDate():
    #does not need to be a date object
    days = random.randrange(1,28,1)
    months = random.randrange(1,12,1)
    date = f"{days}/{months}/2022"
    return date

def pharmacokineticChange():
    # add random date to the pharmacokinetic change
    recorded_date = ''
    if random.randint(1,10) > 6:
        recorded_date = randomDate()


    randomCreat = f'random.randrange(10,100,1) {recorded_date}'
    akiStage = f'random.choice([1,2,3]) {recorded_date}'
    randomAge = random.randrange(50,80,1)
    
    randomWeight = f'random.randrange(40,100,1) {recorded_date}'
    weightUnit = random.choice(["kg","pounds","lbs","kilogrammes"])

    
    changes =  {
        0: f"The renal function has decreased to {randomCreat} ml/min",
        1: f"The renal function has decreased from {randomCreat} ml/min",
        2: f"The patient has an AKI stage {akiStage}",
        3: "The patient has acute liver failure",
        4: f"patient is over the age of {randomAge}",
        5: f"weight is less than {randomWeight}{weightUnit}",
        6: f"weight is over {randomWeight}kg",
        7: f"The patients renal function has decreased and is now {randomCreat} ml/min",
    }
    choice = random.randrange(0,len(changes),1)
    return [changes[choice]]

def randomGuidance():
    guidance = {
        0: "bnf",
        1: "medusa",
        2: "martindale",
        3: "summary of product characteritics",
        4: "spc",
        5: "British National formulary",
        6: "renal drug database"
    }
    choice = random.randrange(0,len(guidance),1)
    return [guidance[choice]]

   