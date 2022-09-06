import random

#spelling mistake list: 

#https://www.thoughtco.com/commonly-misspelled-words-in-english-1692761 

def keyboardError(sentence):

    keys = [
        ['q','w','e','r','t','y','u','i','o','p'],
        ['a','s','d','f','g','h','j','k','l',';'],
        ['z','x','c','v','b','n','m',',','.','?']
    ]

    #pick random word
    choice = random.randint(0,len(sentence)-1)
    word = list(sentence[choice][0])
    
    letterPos = random.randint(0,len(word)-1)
    letter =  word[letterPos]

    opts = []
    position = None

    for pos,i in enumerate(keys):
        for c, x in enumerate(i):
            if letter == x: 
                print(f'location is array: {pos} pos: {c} = {keys[pos][c]} ')    
                position = (pos,c)


    if position[1] != 0: 
        opts.append(keys[position[0]][position[1]-1])
    if position[1] != 9: 
        opts.append(keys[position[0]][position[1]+1])
    if position[0] != 0:
        opts.append(keys[position[0]-1][position[1]])
    if position[0] != 2:
        opts.append(keys[position[0]+1][position[1]])

    word[letterPos]  = random.choice(opts)
    word = "".join(word)

    sentence[choice] = (word,sentence[choice][1])
    return(sentence)

