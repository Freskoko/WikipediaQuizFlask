import wikipedia as wk
import random
import re

DEBUG = False
wincounter = 0

def findfamous():
    with open("data/famouspeople.txt","r") as f:
        lines = f.readlines()
        randomnum = random.randint(1,125)

        person = (lines[randomnum]).strip()

        if DEBUG == True:
            print(f"foundfamous = {person}")
        
        return person
    

def findfacts():
    famousperson = findfamous()
    famousperson = famousperson.replace(" ","_")

    try:
        result = wk.summary(famousperson, auto_suggest=False) #sentences = 10
        famousperson = famousperson.replace(" ","_")

    except Exception as e:
            print(f"Error! {famousperson} |||||| {e}")

    if DEBUG == True:
        print("foundfact")
    return(famousperson,result)


def cleandata(tup):
    name = tup[0].replace("_"," ")
    text = tup[1]

    prohibitedWords = []
    prohibitedWords.append(name)
    for i in name.split(" "):
        prohibitedWords.append(i)

    big_regex = re.compile('|'.join(map(re.escape, prohibitedWords)))
    result = big_regex.sub("XXXXXXX", text)
    result = result.replace(" She "," They ").replace(" He "," They ").replace(" His "," Their ").replace(" Her "," Their ")
    #.replace("his","their").replace("her","their")

    num = random.randint(1,3)

    randomlines = result.split(".")
    randomlines.pop(0)
    randomlines.pop(0)

    randomFact = random.choice(randomlines)
    

    if DEBUG == True:
        print(prohibitedWords)
        print("cleaned-data")
    return (randomFact,name,num)

def gameloop():
    result,name,num = (cleandata(findfacts()))

    print(result)
    print("-------------------------")

    guesses = [0,0,0,0,0,0]
    guesses[num] = name
    guesses = guesses[1:6]

    for j,i in enumerate(guesses):
        if i == 0:
            guesses[j] = findfamous()

    for i in guesses:
        print(i)

    print("-------------------------")

    while True:
        inp = int(input("Who do you think this is? 1,2,3?    "))    
        if inp in [1,2,3,4,5] and inp != "":
            break
        else:
            pass

    if inp == num:
        print(f"Correct! it was {name}")

        global wincounter
        wincounter += 1

    if inp != num:
        print(f"Wrong! it was {name}")


if __name__ == "__main__":

    while True:

        try:
            gameloop()
        except Exception as e:
            print("Error!", {e})

        inp2 = input("Play Again? q to quit     ")
        print("-------------------------")
        
        if inp2 == "q":
            print(wincounter)
            break
        if inp2 == "y":
            pass



#TODO = SOMETIMES COUNTIRIES GO AWAY, CHOOSING SAME COUNTRY TWICE, sometimes no text, invaldi literal