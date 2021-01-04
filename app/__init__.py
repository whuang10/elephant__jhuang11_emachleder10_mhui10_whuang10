# Team Elephant (Jeffrey Huang, Matthew Hui, Winnie Huang, Ethan Machleder)
# SoftDev
# P0 - Da Art of Storytellin' (Pt. 2)
# 2021-1-11
from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session
import os
import sqlite3

#Create db for user and story information
db = sqlite3.connect("p0database.db")
c = db.cursor()
#c.execute('DROP TABLE IF EXISTS stories') #for changing columns
#c.execute('DROP TABLE IF EXISTS users') #for changing columns
c.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username text, password text, contributions text)""")
c.execute("""CREATE TABLE IF NOT EXISTS stories (story_id INTEGER PRIMARY KEY, title text, entire text, recent text, contributors text)""")
db.commit()
db.close()

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #need this, if we didn't include this it would produce a runtime error

#Checks if user is in session
@app.route("/") #methods=['GET', 'POST']
def disp_loginpage():
    if 'username' in session:
        return render_template('homepage.html', user = username_homepage)
    else:
        return render_template('login.html')

#Routes user to registration page
@app.route("/register")
def register():
    return render_template('register.html')

#Registration for new user, stores user info into users db
@app.route("/register_auth")
def registerConfirming():
    db = sqlite3.connect("p0database.db")
    c2 = db.cursor()
    usernames_list = "SELECT usernames FROM users;"
    u = request.args['new_username']
    p = request.args['new_password_1']
    p1 = request.args['new_password_2']
    c = ''
    id_list = []
    for x in c2.execute("SELECT user_id FROM users"):
        for b in x:
            id_list.append(b)
    if len(id_list) == 0:
        i = 0
    else:
        i = int(id_list[-1]) + 1
    if p != p1:
        return render_template('invalid_register.html', error_type = "Passwords do not match, try again")
    elif u in usernames_list:
        return render_template('invalid_register.html', error_type = "Username already exists, try again")
    else:
        c1 = db.cursor()
        c1.execute("INSERT INTO users (user_id, username, password, contributions) VALUES (?, ?, ?, ?)", (i, u, p, c))
        db.commit()
        print("testing register")
        return render_template("login.html", error_type = "Please login with your new account")
db.close()

#Checks credentials of login attempt
@app.route("/auth") # methods=['GET', 'POST']
def welcome():
    db = sqlite3.connect("p0database.db")
    c2 = db.cursor()
    username = request.args['username']
    password = request.args['password']

    #establishes the username so we can use it in other areas when we redirect to homepage
    global username_homepage
    username_homepage = username

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
            global id
            id = u_list.index(username)
            #print(str(i) + " HERE IS THE user_id")
            return render_template('homepage.html', user = username)
    else:
        return render_template('login.html', error_type = "Invalid login attempt, try again")
    return render_template ('homepage.html')  #response to a form submission
db.close()

#Displays homepage when successful login
@app.route("/homepage")
def returnHome():
    return render_template('homepage.html', user = username_homepage)

#Asks user for a title for a new story
@app.route("/create_story")
def title_maker():
    print(str(id) + " HEREIS THE USER_id")
    return render_template('story_creation.html', titleExists = 0)

#make story
@app.route("/story_check")
def story_check():
    title = request.args['temp-title']
    orig_story = request.args['story']
    user = id
    title_list = []
    db = sqlite3.connect("p0database.db")
    c3 = db.cursor()
    userConts = []

    for x in c3.execute("SELECT title FROM stories"):
        for y in x:
            title_list.append(y.lower())
        for y in x:
            if (title.lower() == y):
                return render_template('story_creation.html', titleExists = 1, story = orig_story )
            else:
                c3.execute("INSERT INTO stories (title, entire, recent, contributors) VALUES (?, ?, ?, ?)", (title + " ", orig_story, orig_story, user))
                for x in c3.execute("SELECT contributions FROM users"):
                    for y in x:
                        userConts.append(y)
                updatedUserConts = userConts[user] + title + " "
                c3.execute("UPDATE users SET contributions = ? WHERE user_id = ?", (updatedUserConts,user))
                db.commit()
                return render_template('story_view.html', story = orig_story, title = title)

db.close()

# #Checks to see if the title exists
# @app.route("/title-check")
# def title_Check():
#     title = request.args['temp-title']

#     db = sqlite3.connect("p0database.db")
#     c3 = db.cursor()
#     if ("SELECT LOCATE(title, titles) FROM stories;") == 0:
#         return render_template('story_creation.html', story_error = "Title Already Exists")
#     else:
#         return render_template('story_creation.html', title = title)
# db.close()

# #Creates story and adds it to the database
# @app.route("/create_story")
# def story_add():
#     db = sqlite3.connect("p0database.db")
#     c4 = db.cursor()
#     orig_story = request.args['story']
#     c4.execute("INSERT INTO stories (title, entire, recent) VALUES (?, ?, ?)", (title, orig_story, orig_story))
#     c4.execute("INSERT INTO users (contributions) VALUES (?)", (title))
#     return render_template('display_recent.html')
# db.close()

#Displays login page and removes user from session
@app.route("/logout")
def logout():
    session.pop('username', None) #removes the session
    return render_template('login.html')

#Enables debugging, auto-restarting of server when this file is modified
if __name__ == "__main__": #false if this file imported as module
    app.debug = True
    app.run()
