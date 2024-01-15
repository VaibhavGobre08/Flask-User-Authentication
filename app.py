from flask import Flask, render_template, request, redirect,session
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField
#from wtforms.validators import DataRequired, Email, ValidationError
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/flask'

db = SQLAlchemy(app)
app.secret_key = 'secreat_key'

class Register(db.Model):
   id = db.Column(db.Integer,primary_key=True, autoincrement=True)
   name = db.Column(db.String(200),nullable=False)
   email = db.Column(db.String(200),unique=True,  nullable=False)
   password = db.Column(db.String(200))

   def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

   def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
   db.create_all()

@app.route('/')
def index() :
     return render_template('index.html')


#login
@app.route('/login', methods=['GET','POST'])
def login() :
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        user = Register.query.filter_by(email=email).first()

        if user and user.check_password(password):
            #session['name'] = user.name
            session['email'] = user.email
            #ssion['password'] = user.password
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid')

    return render_template("login.html")


#register
@app.route('/register', methods=['GET', 'POST'])
def register() :
    if request.method =='POST':
        # handel request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = Register(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
   

    return render_template("register.html")

#dashboard
@app.route('/dashboard')
def dashboard() :
    if session['email']:
        user = Register.query.filter_by(email=session['email']).first()
        return render_template("dashboard.html",user=user)
    return redirect('/login')
    

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

if __name__=='__main__' :
    app.run(debug=True)