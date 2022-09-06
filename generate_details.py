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
    elif type == '':
        return [names.get_full_name()]

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

def randomWard():
    wardDigit = random.choice(['1','2','3','4','5'])
    wardAlpha = random.choice(['A','B','C','D','E'])
    ward = [('ward','o'),(wardDigit+wardAlpha,'o')]
    return ward

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
    ward = randomWard()
        
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
        5: [('Dr','o'),(names.get_last_name(),'o')],
        6: [('hepatologist','o')],
        7: [('consultant','o')],
        8: [('surgeon','o')]
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

def pharmokineticIssue():
    issue = ['poor renal function','liver impairment','low body weight','obesity','malnutrition','reduced renal function','poor kidney function','reduced liver clearance','low volume of distribution','hypoperfusion of kidneys','high output stoma','low albumin levels']
    return [random.choice(issue)]

def randomGuidance():
    guidance = {
        0: "bnf",
        1: "medusa",
        2: "martindale",
        3: "summary of product characteritics",
        4: "spc",
        5: "British National formulary",
        6: "renal drug database",
        7: "local policy",
        8: "trust guidance",
        9: "medicines information department"
    }
    choice = random.randrange(0,len(guidance),1)
    return [guidance[choice]]

def randomDrugClass():
    classes = ['calcium channel blocker','cardiac glycoside','ace inhibitor','beta blocker','penicillin','Direct oral anticoagulant','macrolide','sulphonylurea','biguanide','carbonic anhydrase inhibitor','aminoglycoside','glycopeptide','Dipeptidylpeptidase-4 inhibitor','Phosphodiesterase type-5 inhibitor']
    return [random.choice(classes)]

def ivostReasons():
    ivosts = ['patient no longer nill by mouth','patient now able to swallow','patient no longe NBM','patient now eaiting and drinking','biovability of oral drug is near complete']
    return [random.choice(ivosts)]

def receptorTypes():
    receptor = ['beta adrenoreceptors','penicillin binding protein','beta 2 receptors','calcium channel receptors','']


def contraindicationType():
    # drug x in contraindicated in....
    contraindications =  ['Acute myocardial infarction','cardiogenic shock','congenital QT syndrome','immediately after cerebrovascular accident','patients dependent on pacemaker','second- and third-degree heart block','severe hypotension','sick-sinus syndrome','sino-atrial block',   'unstable angina','unstable or acute heart failure','Atrial fibrillation','mild to moderate hypotension','retinitis pigmentosa','Arrhythmias', 'atrioventricular block', 'dizziness', 'headache', 'hypertension', 'vision disorders','Abdominal pain','angioedema','constipation','diarrhoea','eosinophilia','hyperuricaemia','hypotension','muscle cramps','nausea','QT interval prolongation','skin reactions','syncope','vertigo']

    return [random.choice(contraindications)]

def sideEffects():
    sideEffects = ['Acute myocardial infarction','cardiogenic shock','congenital QT syndrome', 'dizziness', 'headache', 'hypertension', 'vision disorders','Abdominal pain','angioedema','constipation','diarrhoea','eosinophilia','hyperuricaemia','hypotension','muscle cramps','nausea','QT interval prolongation','skin reactions','syncope','vertigo']
    return [random.choice(sideEffects)]

def planAuthor():
    return random.choice([['Dr'],['Consultant'],['registrar'],['ward round'],['clinical notes'],['on call dr'],['house officer'],['SHO'],['specialist registrar'],['microbiologist'],['cardiologist'],['respiratory conculstant'],['hepatologist'],['gastroenterologist'],['elderly care consultant'],['AKI team'],['diabetes specialist nurses']])

def allergyReaction():
    return [random.choice(['rash','stevens johnson syndrome','nausea','exacerbation of myasthenia gravis','diarrhoea','vomitting','hives','itch'])]

def medRecSource():
    return [random.choice(['Summary Care Record','GP Record','Latest Clinic Letter','MAR Chart','Nursing home MAR Chart','relative', 'inpatient drug chart'])]

def administrationTimes():
    return [random.choice(['in the morning','at night','at lunchtime','before food','after food','in the evening'])]

def randomIndication():
    return [random.choice(['hypertension','diabetes','high blood pressure','copd','asthma','community acquired pneumonia','CAP','hospital acquired pneumonia','HAP','urinary tract infection','UTI','endocarditis','prostatitis','epilepsy','parkinsons disease','alzheimers disease','dementia','parkinsons'])]


def randomBiochem():
    biochem = {
        0: {
            'test': 'potassium',
            'inrange': str(random.randint(35,50)/10),
            'low': str(random.randint(2,35)/10),
            'high': str(random.randint(5,7)/10),
            'unit': 'mmol/L'
        },
        1: {
            'test': 'sodium',
            'inrange': str(random.randint(133,150)),
            'low': str(random.randint(120,133)),
            'high': str(random.randint(150,160)),
            'unit': 'mmol/L'
        },
        2: {
            'test': 'calcium',
            'inrange': str(random.randint(220,262)/100),
            'low': str(random.randint(180,220)/10),
            'high': str(random.randint(262,320)/100),
            'unit': 'mmol/L'
        },
        3: {
            'test': 'magnesium',
            'inrange': str(random.randint(75,150)),
            'low': str(random.randint(20,75)),
            'high': str(random.randint(150,200)),
            'unit': 'mmol/L'
        },
        4: {
            'test': 'phosphate',
            'inrange': str(random.randint(80,150)/100),
            'low': str(random.randint(10,80)/100),
            'high': str(random.randint(150,240)/100),
            'unit': 'mmol/L'
        },
        5: {
            'test': 'folate',
            'inrange': str(random.randint(80,150)/100),
            'low': str(random.randint(10,80)/100),
            'high': str(random.randint(150,240)/100),
            'unit': 'mmol/L'
        }
    }
    choice = random.randrange(0,len(biochem),1)
    return biochem[choice]

def randomFrequency(firstFrequency):
    frequency = firstFrequency
    while firstFrequency == frequency:
        frequency = random.choice(["TDS","BD","OD","OM","ON","QDS","BID","TID","PRN","when required","four times daily","6 hourly","each morning","each night","twice daily","three hourly","four hourly", "three times daily","once daily","eight hourly","twelve hourly","five times daily","six time daily","2 hourly"])
        freq_tag = []

        frequency = frequency.split(" ")
        if len(frequency) == 1:
            return [(frequency[0],"B-Freq")]
        else:
            for i,x in enumerate(frequency):
                if i == 0:
                    freq_tag.append((x,"B-Freq"))
                elif i == len(freq_tag)-1:
                    freq_tag.append((x,"L-Freq"))
                else: 
                    freq_tag.append((x,"I-Freq"))
            return freq_tag

def randomRoute(firstRoute):
    route = firstRoute
    while route == firstRoute:
        route = random.choice(["oral","IV","intravenous","intramuscular","eye","inhaled","sublingually","PO","NG","PEG","NJ","Via Enteral Feeding Tube"])
        route_Tag = []

        route = route.split(" ")
        if len(route) == 1:
            route_Tag.append((route[0],"B-Route"))
        else:
            for i,x in enumerate(route):
                if i == 0:
                    route_Tag.append((x,"B-Route"))
                elif i == len(route_Tag)-1:
                    route_Tag.append((x,"L-Route"))
                else: 
                    route_Tag.append((x,"I-Route"))

    return route_Tag

def multipleFrequency():
    freq = {
        0: [('three','B-Freq'),('times','I-Freq'),('daily','L-Freq')],
        1: [('three','B-Freq'),('times','I-Freq'),('a','I-Freq'),('day','L-Freq')],
        2: [('four','B-Freq'),('times','I-Freq'),('a','I-Freq'),('day','L-Freq')],
        3: [('four','B-Freq'),('times','I-Freq'),('daily','L-Freq')]
    } 
    lowerFreq = {
        0: [('once','B-Freq'),('daily','L-Freq')],
        1: [('twice','B-Freq'),('a','I-Freq'),('day','L-Freq')],
        2: [('twice','B-Freq'),('daily','L-Freq')]
    }
    
    choice = random.randrange(0,len(freq),1)
    lowerChoice = random.randrange(0,len(lowerFreq),1)
    return (lowerFreq[lowerChoice],freq[choice])