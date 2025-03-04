from flask import Flask,render_template,request,redirect
from db import Database

app = Flask(__name__)

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
    fullname = firstname+lastname
    response = dbo.insert(fullname,email,password)
    if response:
        return render_template('login.html',message="Registration Successful, Kindly Login to Proceed",code = 1)
    else:
        return render_template('register.html',message="Email already exist.")

@app.route('/perform_login',methods=['POST'])
def perform_login():
    useremail = request.form.get('email')
    password = request.form.get('password')  
    if dbo.checkforlogin(useremail,password):
        return redirect('/profile')
    else:
        return render_template('login.html',message="Incorrect Email or Password",code=0)
    
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/ner')
def ner():
    return "ner hoga yrr"        
@app.route('/sentiment_analysis')
def sentiment_analysis():
    return "sentiment_analysis hoga yrr"        
@app.route('/abuse_detection')
def abuse_detection():
    return "abuse_detection hoga yrr"        

if __name__ == '__main__':
    app.run(debug=True,port=5050)
