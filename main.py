from voter import Voter
from flask import Flask, render_template, request, flash
from AddVoter import add_voter, voters
from datetime import datetime
from block import Block
import os
import time as t

app = Flask(__name__)
app.secret_key = os.urandom(24)

VOTERS=[]
li=[]
Blockchain = []
bc = tuple()


posts = [

    {
        'author': "Bond, James Bond",
        'title': 'How to cast your vote',
        'content': 'content 1',
        'date_posted': str(datetime.date(datetime.now()))+" at "+str(datetime.time(datetime.now()))
    },
    {
        'author': "I AM Grooooooooot",
        'title': 'Overview of Electo.ai',
        'content': 'content 1',
        'date_posted': str(datetime.date(datetime.now()))+" at "+str(datetime.time(datetime.now()))
    },
    {
        'author': "Its a me, Mario",
        'title': 'Technology behind Electo.ai',
        'content': 'content 2',
        'date_posted': str(datetime.date(datetime.now()))+" at "+str(datetime.time(datetime.now()))
    }

    ]



@app.route("/")
def home():
    return render_template("index.html", posts = posts)

@app.route("/generate", methods = ['POST',"GET"])
def generate():
    if request.method == 'POST':
        result = request.form
        voter = add_voter(result['ID'])

        if voter.get_key() in voters:
            flash("Passcode already generated", "info")

            for i in VOTERS:
                if voter.get_key() == i.get_key():
                    result = i.voter.disp()
            return render_template("generate.html", result=result, cond=True)

        if voter.verify():
            flash("Your vote is already registered", "info")

        else:
            voters.append(voter.get_key())
            VOTERS.append(voter)
            pk=voter.get_key()
            li.clear()
            li.append(pk)
            prk=voter.disp()[pk][0]
            li.append(prk)
            return render_template("generate.html",result = voter.disp(), cond = True)

    return render_template("generate.html", cond = False)

@app.route("/voter_login", methods = ['POST','GET'])
def voter_login():
    if request.method == 'POST':
        result = request.form
        public_key = result['public_key']
        private_key = result['private_key']
        permit = False

        for i in VOTERS:
            if i.voter.public_key == public_key and i.voter.private_key == private_key:
                permit = True
                if i.voter.amount == 1:
                    i.voter.trans_vote()
                    return render_template("profile.html",result=li)
                else:
                    flash("Your vote is already registered", "info")
                    break
                break
        if not permit:
            flash("who the hell are you?", "danger")

    if not li:
        flash("Generate your secure passcode first", "info")
        return  render_template("generate.html")

    return render_template("vote.html",pk = li[0], prk =li[1])

@app.route("/profile", methods = ['POST', 'GET'])
def profile():
    trans = {'public_key': '',
             'time': '',
             'candidate': ''}
    if request.method == 'POST':
        result = request.form
        flash("Successfully voted, your session has ended", "success")
        trans['public_key'] = li[0]
        trans['time'] = str(t.time())
        trans['candidate'] = result['candidate']
        Blockchain.append(Block(trans))
        return render_template("ends.html")



@app.route("/candid")
def candid():
    return render_template('candid.html', title="Candidates")
    
@app.route("/analysis", methods = ['POST', 'GET'])
def analysis():
    vote_count = {'con':0,'bjp':0,'aap':0,'no':0}
    for i in Blockchain:
        can = i.trans['candidate']
        if can == "INC":
            vote_count['con'] +=1
        elif can == "BJP":
            vote_count['bjp'] +=1
        elif can == "AAP":
            vote_count['aap'] +=1
        else:
            vote_count['no'] +=1

    return render_template("analysis.html",result=vote_count, title="Analysis")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/ends")
def ends():
    return render_template('ends.html', title='Thankyou')



if __name__ == "__main__":
    app.run(debug=True)
