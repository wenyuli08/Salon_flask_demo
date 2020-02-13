# -*- coding: utf-8 -*-

import time
import os
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug import check_password_hash, generate_password_hash

app = Flask(__name__)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'salon.db')
SECRET_KEY = "1db8QHemTMWNCUJNUpct9ytgh032rgfs6"
app.config.from_object(__name__)
db = SQLAlchemy()
db.init_app(app)
dateCompare = list()

### models

class Owner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def is_authenticated(self):
		return True
		
	def __repr__(self):
		return '<User %r>' % self.username

class Stylist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	appointment = db.relationship('Appointment', backref='stylist', lazy='select')

	def __init__(self, username, password):
		self.username = username
		self.password = password
		
	def is_authenticated(self):
		return False

	def __repr__(self):
		return '<User %r>' % self.username

class Patron(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	appointment = db.relationship('Appointment', backref='patron', lazy='select')

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def is_authenticated(self):
		return False
		
	def __repr__(self):
		return '<User %r>' % self.username

class Appointment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'), nullable=False)
	stylist_id = db.Column(db.Integer, db.ForeignKey('stylist.id'), nullable=False)
	date = db.Column(db.Date, nullable=False)
	time = db.Column(db.Integer, nullable=False)

	def __init__(self, p_id, s_id, date, time):
		self.patron_id = p_id
		self.stylist_id = s_id
		self.date = date
		self.time = time

	def __repr__(self):
		return '<User %r>' % self.patron_id

### controllers

@app.cli.command("initdb")
def initdb_command():
	db.drop_all()
	db.create_all()

	# One owner
	owner = Owner("owner", "pass")
	db.session.add(owner)

	# stylists
	mary = Stylist("Mary", "qwert")
	victor = Stylist("Victor", "asdfg")
	tom = Stylist("Tom", "tom")
	print(isinstance(tom, Stylist))
	db.session.add(mary)
	db.session.add(victor)
	db.session.add(tom)

	db.session.commit()

	# patrons
	peter = Patron("Peter", "abcde")
	anne = Patron("Anne", "fghij")
	lucy = Patron("Lucy", "lucy")
	print(isinstance(lucy, Patron))
	db.session.add(peter)
	db.session.add(anne)
	db.session.add(lucy)

	db.session.commit()

	# appointments
	date = datetime.datetime.now()
	date = date.date()
	a1 = Appointment(peter.id, mary.id, date, 11)
	date2 = datetime.date(2018, 11, 14)
	a2 = Appointment(peter.id, victor.id, date2, 3)
	date3 = datetime.date(2018, 11, 17)
	a3 = Appointment(anne.id, tom.id, date3, 1)
	date4 = datetime.date(2018, 11, 16)
	a4 = Appointment(lucy.id, mary.id, date4, 4)
	db.session.add(a1)
	db.session.add(a2)
	db.session.add(a3)
	db.session.add(a4)

	# commit
	db.session.commit()
	print('Initialized the database.')

def print_table(stylist_id):
	listOfDate = list()
	today = datetime.date.today()
	for x in range(0, 7):
		if today.isoweekday() != 1 and today.isoweekday() != 7:
			strd = today.strftime("%A\n%d-%m-%y")
			listOfDate.append(strd)
		i = datetime.timedelta(days=1)
		today += i
	
	listOf10 = list()
	listOf11 = list()
	listOf12 = list()
	listOf1 = list()
	listOf2 = list()
	listOf3 = list()
	listOf4 = list()
	listOf5 = list()
	listOf6 = list()
	listOf7 = list()
	for i in range(0, 5):
		listOf10.append("Available")
		listOf11.append("Available")
		listOf12.append("Available")
		listOf1.append("Available")
		listOf2.append("Available")
		listOf3.append("Available")
		listOf4.append("Available")
		listOf5.append("Available")
		listOf6.append("Available")
		listOf7.append("Available")
	appointments = Appointment.query.filter_by(stylist_id = stylist_id).all()
	temp_today = datetime.date.today()
	for x in range(0, 7):
		if temp_today.isoweekday() != 1 and temp_today.isoweekday() != 7:
			dateCompare.append(temp_today)
		i = datetime.timedelta(days=1)
		temp_today += i
	for a in appointments:
		if a.time == 10:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf10.pop(counter)
					listOf10.insert(counter, a.patron.username)
					break
				counter += 1
		elif a.time == 11:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf11.pop(counter)
					listOf11.insert(counter, a.patron.username)
					break
				counter += 1			
		elif a.time == 12:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf12.pop(counter)
					listOf12.insert(counter, a.patron.username)
					break
				counter += 1
		elif a.time == 1:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf1.pop(counter)
					listOf1.insert(counter, a.patron.username)
					break
				counter += 1
		elif a.time == 2:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf2.pop(counter)
					listOf2.insert(counter, a.patron.username)
					break
				counter += 1
		elif a.time == 3:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf3.pop(counter)
					listOf3.insert(counter, a.patron.username)
					break
				counter += 1
		elif a.time == 4:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf4.pop(counter)
					listOf4.insert(counter, a.patron.username)
					break
				counter += 1
		elif a.time == 5:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf5.pop(counter)
					listOf5.insert(counter, a.patron.username)
					break
				counter += 1
		elif a.time == 6:
			counter = 0
			for b in dateCompare:
				if a.date == b:
					listOf6.pop(counter)
					listOf6.insert(counter, a.patron.username)
					break
				counter += 1
	return [listOfDate, listOf10, listOf11, listOf12, listOf1, listOf2, listOf3, listOf4, listOf5, listOf6, listOf7]

def get_user_id(username):
	rv = Owner.query.filter_by(username=username).first()
	if rv is None:
		rv = Stylist.query.filter_by(username=username).first()
	if rv is None:
		rv = Patron.query.filter_by(username=username).first()
	return rv.user_id if rv else None

@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		user = Owner.query.filter_by(id=session['user_id']).first()
		if user is None:
			user = Stylist.query.filter_by(id=session['user_id']).first()
		if user is None:
			user = Patron.query.filter_by(id=session['user_id']).first()
		g.user = user

@app.route("/")
@app.route("/home")
def default():
	return render_template("layout.html")

@app.route("/login/", methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':

		user = Owner.query.filter_by(username=request.form['username']).first()
		if user is None:
			user = Stylist.query.filter_by(username=request.form['username']).first()
		if user is None:
			user = Patron.query.filter_by(username=request.form['username']).first()
		if user is None:
			error = 'Invalid username'
		elif not user.password == request.form['password']:
			error = 'Invalid password'
		else:
			flash('You were logged in')
			g.user = user
			session['user_id'] = user.id
			if isinstance(user, Owner):
				print("owner")
				return redirect(url_for('ownerProfile'))
			elif isinstance(user, Stylist):
				print("stylist")
				return redirect(url_for('stylistProfile', stylist_id = g.user.id))
			else:
				print("patron")
				return redirect(url_for('patronProfile'))

	return render_template("login.html", error=error)

@app.route('/registerStylist/', methods=['GET', 'POST'])
def registerStylist():
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			db.session.add(Stylist(request.form['username'], generate_password_hash(request.form['password'])))
			db.session.commit()
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('signup.html', error=error)

@app.route('/register/', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			db.session.add(Patron(request.form['username'], generate_password_hash(request.form['password'])))
			db.session.commit()
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('signup.html', error=error)

@app.route("/ownerProfile/")
def ownerProfile():
	listOfStylists = Stylist.query.all()
	return render_template("ownerHome.html", stylistsList = listOfStylists)

@app.route("/<stylist_id>/")
def stylistProfile(stylist_id):
	print(g.user)
	listOfLists = print_table(stylist_id)
	return render_template("stylistHome.html", dateList = listOfLists[0], row10 = listOfLists[1],
						row11 = listOfLists[2], row12 = listOfLists[3], row1 = listOfLists[4],
						row2 = listOfLists[5], row3 = listOfLists[6], row4 = listOfLists[7],
						row5 = listOfLists[8], row6 = listOfLists[9], row7 = listOfLists[10])

@app.route("/patronProfile/")
def patronProfile():
	listOfStylists = Stylist.query.all()
	appointments = Appointment.query.filter_by(patron_id = g.user.id).all()
	return render_template("patronHome.html", stylistsList = listOfStylists, appointments = appointments)

@app.route("/<stylist_id>/bookastylist")
def patron_stylist(stylist_id):
	listOfLists = print_table(stylist_id)
	return render_template("patron-stylist.html", cur_stylist = stylist_id, dateList = listOfLists[0], row10 = listOfLists[1],
						row11 = listOfLists[2], row12 = listOfLists[3], row1 = listOfLists[4],
						row2 = listOfLists[5], row3 = listOfLists[6], row4 = listOfLists[7],
						row5 = listOfLists[8], row6 = listOfLists[9], row7 = listOfLists[10])

@app.route('/<curuser>/<curstylist>/<curdate>/<curtime>/book/')
def book(curuser, curstylist, curdate, curtime):
	flash('Booked successfully')
	interval = datetime.timedelta(days=int(curdate))
	new_date = dateCompare[0] + interval
	db.session.add(Appointment(curuser, curstylist, new_date, curtime))
	db.session.commit()
	appointments = Appointment.query.filter_by(patron_id = g.user.id).all()
	return render_template('patronHome.html', appointments = appointments, flag = 1)

@app.route('/<appt_id>/canceled/')
def cancel(appt_id):
	flash('Canceled successfully')
	appt = Appointment.query.filter_by(id=appt_id).first()
	db.session.delete(appt)
	db.session.commit()
	appointments = Appointment.query.filter_by(patron_id = g.user.id).all()
	listOfStylists = Stylist.query.all()
	return render_template('patronHome.html', stylistsList = listOfStylists, appointments = appointments)

@app.route('/logout/')
def logout():
	session.pop('user_id', None)
	flash('You were logged out')
	return redirect(url_for('default'))