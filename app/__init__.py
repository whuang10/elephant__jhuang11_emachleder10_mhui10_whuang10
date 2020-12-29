# Team Elephant (Jeffrey Huang, Matthew Hui, Winnie Huang, Ethan Machleder)
# SoftDev
# P0 -- Da Art of Storytellin' (Pt. 2)
# 2021-01-06

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session
import os
import sqlite3

#the conventional way:
#from flask import Flask, render_template, request

db = sqlite3.connect("p0database.db")


app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #Need this, if we didn't include this it would produce a runtime error


@app.route("/") #, methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session: #Checks if the user is logged in
        return render_template('homepage.html', user = 'abc')
    else:
        return render_template( 'login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/register_auth")
def registerConfirming():
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (username text, password text)""")
    db.commit()
    usernames_list_1 = "SELECT usernames FROM users;"
    u = request.args['new_username']
    p = request.args['new_password_1']
    p1 = request.args['new_password_2']
    if p != p1:
        return render_template('invalid_register.html', error_type = "Passwords do not match, try again")
    elif u in usernames_list:
        return render_template('invalid_register.html', error_type = "username already exists")
    else:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        c.commit()
        print("testing register")
        return render_template("homepage.html", user = u)


@app.route("/auth") # , methods=['GET', 'POST'])
def welcome():
    username = request.args['username']
    password = request.args['password']
    usernames_list_2 = "SELECT username FROM users;"
    passwords_list_2 = "SELECT password FROM users;"
    if username in usernames_list :
        if password in passwords_list:
            session["username"] = username
            return render_template('homepage.html', user = username)
    else:
        return render_template('invalid.html')

    return render_template ( 'homepage.html')  #response to a form submission

@app.route("/homepage")


@app.route("/logout")
def logout():
    session.pop('username', None) #removes the session
    return render_template('login.html')

db.close()

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
