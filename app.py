from flask import Flask,render_template,redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy  
from flask_mail import Mail
import os
from bs4 import BeautifulSoup
import requests
import wikipedia

username="your mail id"
password="Your mail password"

app=Flask(__name__)

app.config.update(
		MAIL_SERVER='smtp.gmail.com',
		MAIL_PORT='465',
		MAIL_USE_SSL=True,
		MAIL_USERNAME=username,
		MAIL_PASSWORD=password

	)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/covid_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mail=Mail(app)

class Covid_people(db.Model):

	# id, name, email, phone, percent
	pid = db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(80), unique=False, nullable=False)
	email=db.Column(db.String(100), unique=False, nullable=False)
	phone=db.Column(db.String(50), unique=False, nullable=False)
	percent=db.Column(db.String(12), unique=False, nullable=False)

def get_data(URL):
    req=requests.get(URL)
    return req.text

import pickle
file=open('model.pkl','rb')
classifier=pickle.load(file)
file.close()

@app.route('/', methods=["GET","POST"])

def infer():
	if request.method=="POST":
		Dict1=request.form
		sex=int(Dict1["sex"])
		pneumonia=int(Dict1["pneumonia"])
		age=int(Dict1["age"])
		diabetes=int(Dict1["diabetes"])
		COPD=int(Dict1["COPD"])
		asthma=int(Dict1["asthma"])
		inmsupr=int(Dict1["inmsupr"])
		hyper=int(Dict1["hyper"])
		breadth=int(Dict1["breadth"])
		cardio=int(Dict1["cardio"])
		obesity=int(Dict1["obesity"])
		kidney=int(Dict1["kidney"])
		smoke=int(Dict1["smoke"])
		contact=int(Dict1["contact"])
		fever=int(Dict1["fever"])
		inp_f=[sex,pneumonia,age,diabetes,COPD,asthma,inmsupr,hyper,breadth,cardio,obesity,kidney,smoke,contact,fever]
		inp_prob=classifier.predict_proba([inp_f])[0][1]
		name=Dict1["P_name"]
		email=Dict1["email"]
		phn=Dict1["phn"]
		percent=inp_prob*100
		ip=round(percent)
		entry_data=Covid_people(name=name, email=email, phone=phn, percent=percent)
		db.session.add(entry_data)
		db.session.commit()
		mail.send_message(f"New result arrive for {name}",sender=email, recipients=[username], 
			body=f"The covid probability of the patient is {ip} \n Name:\t{name}\n Phone number:\t{phn}\n EMAIL ID:\t{email}\n fever:\t{fever}\n age:\t{age}")
		if ip>=60:
			mail.send_message("Thanking for using our COVID predictor", sender=username, recipients=[email], 
				body= f"Thank you for using our Covid predictor. You have a High rate of covid. Please contact with nearest hospital As Soon As Possible. Your chance is {ip}%")
		elif ip<60:
			mail.send_message("Thanking for using our COVID predictor", sender=username, recipients=[email], 
				body= f"Thank you for using our Covid predictor. You are quite safe.But please test at the nearest hospital to be safe. Your chance is {ip}%")	

		return render_template('result.html',infected=round(inp_prob*100))
	return render_template('index.html')
		#return "Hello" + str(inp_prob)

@app.route('/about')
def about():
	mydata=get_data('https://www.worldometers.info/coronavirus/#countries')
	soup=BeautifulSoup(mydata,'html.parser')
	list1=[]
	for i in range(0,6):
		x=soup.find_all('tbody')[0].find_all('tr')[i]
		string1=""
		string1+=x.get_text()
		new_data=string1.split("\n")
		while("" in new_data) : 
			new_data.remove("") 
		list1.append(new_data)
	results=wikipedia.summary("Coronavirus",sentences=10)		
	return render_template('about.html',rows=list1,main=results)

@app.route('/admin')
def admin():
	if not session.get('logged_in'):
		return render_template('admin.html')
	return render_template('admin.html')

@app.route('/login', methods=["GET","POST"])
def login():
	#session['logged_in'] = False
	#session.pop('logged_in',None)

	if request.method=="POST":
		session.pop('logged_in',None)
		if request.form['pass'] == 'password' and request.form['name'] == 'admin':
			session['logged_in'] = True
			#dict2={"name":"admin","pass":"password"}
			admin=request.form['name']
			return render_template('login.html')
		flash('Wrong Username or password!')	
		return render_template('admin.html')
	elif('logged_in' in session and session['logged_in']==True):
		return render_template('login.html')	
	else:
		flash('Wrong Username or password!')
		return admin()

@app.route('/')
def logout():
	session['logged_in'] = False
	return infer()

@app.route('/show')
def show():
	rows=Covid_people.query.all()
	return render_template('show.html',rows=rows)

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/what')
def what():
	return render_template('what.html')	

@app.route("/delete/<string:pid>",methods=["GET","POST"])
def delete(pid):
	if ('logged_in' in session and session['logged_in']==True):
		row=Covid_people.query.filter_by(pid=pid).first()
		db.session.delete(row)
		db.session.commit()
		rows=Covid_people.query.all()
		return render_template('show.html',rows=rows)

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.debug=True
	app.run()	
