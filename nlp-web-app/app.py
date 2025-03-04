from flask import Flask,render_template,request,redirect,session
from db import Database
import spacy
import json

app = Flask(__name__)
app.secret_key = 'HimanshuYadav'

dbo = Database()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perform_registration', methods=['POST'])
def perform_registration():
    firstname = request.form.get('first')
    lastname = request.form.get('last')
    email = request.form.get('email')
    password = request.form.get('password')
    fullname = firstname+" "+lastname
    response = dbo.insert(fullname,email,password)
    if response:
        return render_template('login.html',message="Registration Successful, Kindly Login to Proceed",code = 1)
    else:
        return render_template('register.html',message="Email already exist.")

@app.route('/perform_login',methods=['POST'])
def perform_login():
    useremail = request.form.get('email')
    password = request.form.get('password')  
    with open('users.json','r') as rf:
            users = json.load(rf)
    if dbo.checkforlogin(useremail,password):
        session['user'] = users[useremail][0]
        return redirect('/profile')
    else:
        return render_template('login.html',message="Incorrect Email or Password",code=0)
    
@app.route('/profile')
def profile():
    if 'user' in session:
        return render_template('profile.html')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user session
    return redirect('/')  # Redirect to login pag


@app.route('/ner')
def ner():
    if 'user' in session:
        return render_template('ner.html') 
    else:
        return redirect('/') 


@app.route('/perform_ner', methods=['POST'])
def perform_ner():
    if 'user' in session:
        usertext = request.form.get('text')
        #generating a nlp model to do ner
        nlp = spacy.load('en_core_web_md')
        ner_labels = nlp.get_pipe('ner').labels
        docs = nlp(usertext)
        entities = []
        for ents in docs.ents:
            entities.append((ents.text,ents.label_))

        extraction = ''
        extraction = "<br>".join(f"{i[0]} =====> {i[1]}" for i in entities)
        return render_template('ner.html',message=extraction,usertext=usertext)

    else:
        return redirect('/')



#not in the current use
@app.route('/sentiment_analysis')
def sentiment_analysis():
    if 'user' in session:
        return "sentiment_analysis hoga yrr"  
    else:
        return redirect('/')      
@app.route('/abuse_detection')
def abuse_detection():
    if 'user' in session:
        return "abuse_detection hoga yrr"   
    else:
        return redirect('/')   

if __name__ == '__main__':
    app.run(debug=True,port=5050)
