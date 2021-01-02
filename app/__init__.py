# Team Elephant (Jeffrey Huang, Matthew Hui, Winnie Huang, Ethan Machleder)
# SoftDev
# K15 -- Sessions Greetings
# 2020-12-11
from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session
import os
import sqlite3

#Create db for user information
db = sqlite3.connect("p0database.db")
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (username text, password text)""")
db.commit()
db.close()

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #need this, if we didn't include this it would produce a runtime error

#Checks if user is in session
@app.route("/") #methods=['GET', 'POST']
def disp_loginpage():
    if 'username' in session:
        return render_template('homepage.html', user = 'abc')
    else:
        return render_template( 'login.html')

@app.route("/register")
def register():
    return render_template('register.html')

#Registration for new user, stores info into users db
@app.route("/register_auth")
def registerConfirming():
    db = sqlite3.connect("p0database.db")
    usernames_list = "SELECT usernames FROM users;"
    u = request.args['new_username']
    p = request.args['new_password_1']
    p1 = request.args['new_password_2']
    if p != p1:
        return render_template('invalid_register.html', error_type = "Passwords do not match, try again")
    elif u in usernames_list:
        return render_template('invalid_register.html', error_type = "username already exists")
    else:
        c1 = db.cursor()
        c1.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        db.commit()
        print("testing register")
        return render_template("homepage.html", user = u)
db.close()


#Checks credentials of login attempt
@app.route("/auth") # methods=['GET', 'POST']
def welcome():
    db = sqlite3.connect("p0database.db")
    c2 = db.cursor()
    username = request.args['username']
    password = request.args['password']

    u_list = []
    for x in c2.execute("SELECT username FROM users"):
        for y in x:
            u_list.append(y)
    p_list = []
    for a in c2.execute("SELECT password FROM users"):
        for b in a:
            p_list.append(b)

    if username in u_list:
        if password in p_list:
            session["username"] = username
            return render_template('homepage.html', user = username)
    else:
        return render_template('invalid.html')
    return render_template ( 'homepage.html')  #response to a form submission
db.close()

#Displays homepage when successful login
@app.route("/homepage")


#Displays login page and removes user from session
@app.route("/logout")
def logout():
    session.pop('username', None) #removes the session
    return render_template('login.html')


#Enables debugging, auto-restarting of server when this file is modified
if __name__ == "__main__": #false if this file imported as module
    app.debug = True
    app.run()
