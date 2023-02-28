from flask import Flask, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import wikipedia as wk
import random
import re
from retry import retry
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('all')

#TODO - BETTER TEXT REPLACE HE/HER - WIKIPEDIA BETTER SEARCH (KNOWLEDGE TREE?) - CSS (PACKAGE?)

#------------
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "123"


@app.route('/', methods=['GET',"POST"])
def home():

    def findfamous():
        with open("data/famouspeople.txt","r") as f:
            lines = f.readlines()

            person = random.choice(lines).strip()
            
            return person
    
    @retry(FileNotFoundError, delay=1, tries=5)
    def findfacts():
        famousperson = findfamous()
        famousperson = famousperson.replace(" ","_")

        try:
            result = wk.summary(famousperson, auto_suggest=False) #sentences = 10
            famousperson = famousperson.replace(" ","_")
            
        except Exception as e:
            raise FileNotFoundError

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


        #here NLTK

        print("pre")

        randomlines = sent_tokenize(result)
        randomlines.pop(0)
        randomlines.pop(0)

        print("post")

        randomFact = random.choice(randomlines)

        num = random.randint(1,3)

        return (randomFact,name,num)

    def gameloop():
        result,name,num = (cleandata(findfacts()))

        guesses = [0,0,0,0,0,0]
        guesses[num] = name
        guesses = guesses[1:6]

        for j,i in enumerate(guesses):
            if i == 0:
                guesses[j] = findfamous()


        return result,guesses,name,num

    correctornot="?"

    if session.get("points") is not None:
        pass
    else:
        session["points"] = 0


    if request.method == 'POST':

        if request.form['submit_button'] == 'New Try':

            result,guesses,name,num = gameloop()

            session['name'] = name.split(" ")[0]
        
            print("New Try")
            print(guesses)

            return render_template("home.html",result = result, guesses = guesses,correctornot=correctornot,points = session["points"])

        elif request.form['submit_button'] != 'New Try':

            submi = request.form['submit_button']

            print("player clicked button")
            print(submi)
            print(session['name'])
            
            if submi == session['name']:

                session["points"] = session["points"] + 1
        
                return render_template("home.html",correctornot=correctornot,result = "correct",points = session["points"])


            if submi != session['name']:

                session["points"] = session["points"] - 1

                return render_template("home.html",correctornot=correctornot,result = "wrong",points = session["points"])
            

    elif request.method == 'GET':
       
        print("No Post Back Call")

        return render_template('home.html', result = "Click play to get started!", guesses = [],points = session["points"])


if __name__ == '__main__':
    app.run()