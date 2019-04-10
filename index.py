from flask import Flask, render_template, redirect, url_for, request, session, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'any random string'

db = pymysql.connect(host="localhost", user="root", password="root", db="RMdb")

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
	error = None
	if request.method == 'POST':
		usrname = request.form["username"]
		pwd =  request.form['password']

		#prepare a cursor object using cursor() method
		cursor = db.cursor()
		
		cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (usrname, pwd))
		db.commit()
		return redirect(url_for('index'))

	return render_template("signup.html",error = error)

	db.close()

@app.route("/login", methods = ['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		usrname = request.form["username"]
		pwd =  request.form['password']

		#prepare a cursor object using cursor() method
		cursor = db.cursor()
	
		if cursor.execute("SELECT * FROM user WHERE username = '"+usrname+"' AND password = '"+pwd+"'"):

			db.commit()
			results = cursor.fetchall()
			for row in results:
				custName = row[0]
				custPassword = row[1]
				session['username'] = custName
				session['logged_in'] = True
				return redirect(url_for('index', guest = custName))
			

		else:
			error = 'Invalid username or password! Please try again!'
			return render_template("login.html",error = error)

	return render_template("login.html",error = error)

	db.close()	

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.debug = True
	app.run(host="0.0.0.0", port=8000)