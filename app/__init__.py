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
#c.execute("DROP TABLE IF EXISTS stories") #for changing columns
#c.execute("DROP TABLE IF EXISTS users") #for changing columns
c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text, contributions text)""")
c.execute("""CREATE TABLE IF NOT EXISTS stories (id INTEGER PRIMARY KEY, title text, entire text, recent text, contributors text)""")
db.commit()
db.close()

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32) #need this, if we didn't include this it would produce a runtime error

#Checks if user is in session
@app.route("/", methods = ['GET', 'POST']) #methods=['GET', 'POST']
def disp_loginpage():
    if "user" in session:
        return render_template('homepage.html', user = session["user"])
    else:
        return render_template('login.html')

#Routes user to registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    return render_template('register.html')

#Registration for new user, stores user info into users db
@app.route("/register_auth", methods = ['GET', 'POST'])
def registerConfirming():
    db = sqlite3.connect("p0database.db")
    c1 = db.cursor()

    #gets all the data from the register.html form to check if they exist/match
    u = request.form['new_username']
    p = request.form['new_password_1']
    p1 = request.form['new_password_2']
    c = ''

    #Gets a list of all the registered usernames to check later on
    usernames_list = []
    for x in c1.execute("SELECT username FROM users;"):
        usernames_list.append(x[0])

    if len(u.strip()) == 0:
        return render_template('register.html', error_type = "Please enter valid username, try again")
    if len(p.strip()) == 0:
        return render_template('register.html', error_type = "Please enter valid password, try again")
    #Then checks if the username exists
    elif u in usernames_list:
        return render_template('register.html', error_type = "Username already exists, try again")
    #Firsts check if the passwords match
    elif p != p1:
        return render_template('register.html', error_type = "Passwords do not match, try again")
    #If both pass, it adds the newly registered user and directs the user to the login page
    else:
        c1.execute("INSERT INTO users (username, password, contributions) VALUES (?, ?, ?)", (u, p, c))
        db.commit()
        return render_template("login.html", error_type = "Please login with your new account")
db.close()

#Checks credentials of login attempt
@app.route("/auth", methods = ['GET', 'POST']) # methods=['GET', 'POST']
def welcome():
    db = sqlite3.connect("p0database.db")
    c2 = db.cursor()
    username = request.form['username']
    password = request.form['password']

    u_list = []
    for x in c2.execute("SELECT username FROM users"):
        for y in x:
            u_list.append(y)
    p_list = []
    for a in c2.execute("SELECT password FROM users"):
        for b in a:
            p_list.append(b)

    usersContributions = []
    if username in u_list:
        user_index = u_list.index(username)
        for x in c2.execute("SELECT contributions FROM users"):
            usersContributions.append(x[0])
        user_conts = usersContributions[user_index].split("~")

        if (len(user_conts) >= 1):
            user_conts.pop()

    if username in u_list:
        if password in p_list:
            session["user"] = username
            return render_template('homepage.html', user = username, contribution_list = user_conts, message = "Your Login Has Been Successful! \(^-^)/")
    else:
        return render_template('login.html', error_type = "Invalid login attempt, try again")
    #return render_template ('homepage.html', user = username, contribution_list = user_conts)  #response to a form submission
db.close()

#Displays homepage when successful login
@app.route("/homepage", methods = ['GET', 'POST'])
def returnHome():
    db = sqlite3.connect("p0database.db")
    c4 = db.cursor()

    usersContributions = []
    userList = []
    for x in c4.execute("SELECT username FROM users"):
        userList.append(x[0])
    user_index = userList.index(session["user"])

    for x in c4.execute("SELECT contributions FROM users"):
        usersContributions.append(x[0])

    user_conts = usersContributions[user_index].split("~")
    if (len(user_conts) >= 1):
        user_conts.pop()

    return render_template('homepage.html', user = session["user"], contribution_list = user_conts)
db.close()

#Asks user for a title for a new story
@app.route("/create_story", methods = ['GET', 'POST'])
def create_story():
    return render_template('story_creation.html', titleExists = 0)

#Allows the user to make their own story. (Includes story details & title)
@app.route("/story_check", methods = ['GET', 'POST'])
def story_check():
    #Info from the html file
    title = request.form['temp-title']
    orig_story = request.form['story']
    username = session["user"]

    #Declares lists used to store information gathered from the sqlite database
    userConts = []
    title_list = []
    userList = []

    #Establishing a connection & Cursor with the Sqlite database
    db = sqlite3.connect("p0database.db")
    c3 = db.cursor()

    #To make sure the user title doesn't contain bad spacing before & after the Title
    title = title.strip()

    #Gets the User's index so it can get their contributions
    for x in c3.execute("SELECT username FROM users"):
        userList.append(x[0])
    user_index = userList.index(username)

    #Fills in the title_list with all the titles that currently exist
    for x in c3.execute("SELECT title FROM stories"):
        for y in x:
            title_list.append(y.lower())

    #Checks if title already exists, decided to use the .lower to make case sensitive but same titles not work
    if (title.lower() in title_list):
            return render_template('story_creation.html', titleExists = 1, story = orig_story )
    else:
        c3.execute("INSERT INTO stories (title, entire, recent, contributors) VALUES (?, ?, ?, ?)", (title , orig_story, orig_story, username + ","))
        #gets a list of all the user contributions
        for x in c3.execute("SELECT contributions FROM users"):
            for y in x:
                userConts.append(y)
        #String with the user contributions of a specific person separated by ~ since we figure it was the least used symbol
        updatedUserConts = userConts[user_index] + title + "~"
        #Updates the database with new dataupdatedUserConts
        c3.execute("UPDATE users SET contributions = ? WHERE username = ?", (updatedUserConts, username))
        db.commit()
        return render_template('story_view.html', entire = orig_story, title = title)
db.close()

#Displays a story
@app.route("/story_view", methods = ['GET', 'POST'])
def story_view():
    db = sqlite3.connect("p0database.db")
    c4 = db.cursor()
    title = request.form['title']
    editor = int(request.form['editor'])
    title_list = []
    entire_list = []
    recent_list = []
    for x in c4.execute("SELECT title FROM stories"):
        title_list.append(x[0])
    for x in c4.execute("SELECT entire FROM stories"):
        entire_list.append(x[0])
    for x in c4.execute("SELECT recent FROM stories"):
        recent_list.append(x[0])
    story_index = title_list.index(title)
    return render_template('story_view.html', entire = entire_list[story_index], recent = recent_list[story_index], title = title, editor = editor)
db.close()

#Displays stories that the user can edit
@app.route("/story_edit", methods = ['GET', 'POST'])
def story_edit():
    db = sqlite3.connect("p0database.db")
    c5 = db.cursor()
    username = session["user"]
    list_titles = []
    list_output = []
    for x in c5.execute("SELECT title FROM stories"):
        list_titles.append(x[0])
    count = 0
    for x in c5.execute("SELECT contributors FROM stories"):
        if username in x[0]: #nothing happens
            print()
        else:
            list_output.append(list_titles[count])
        count = count + 1
    return render_template('story_edit.html', title_list = list_output)
db.close()

#Allows user to edit a story he hasn't already editted
@app.route("/story_editor", methods = ['GET', 'POST'])
def story_editor():
    db = sqlite3.connect("p0database.db")
    c6 = db.cursor()
    username = session["user"]
    new_text = request.form['new_text']
    title = request.form['title']
    c6.execute("UPDATE stories SET recent = ? WHERE title = ?", (new_text, title))

    entire = c6.execute("SELECT entire FROM stories WHERE title = ?", (title,))
    entire = c6.fetchone()[0]
    new_entire = entire + "\n" + new_text
    c6.execute("UPDATE stories SET entire = ? WHERE title = ?", (new_entire, title))

    contributors = c6.execute("SELECT contributors FROM stories WHERE title = ?", (title,))
    contributors = c6.fetchone()[0]
    new_contributors =  contributors + username + ","
    c6.execute("UPDATE stories SET contributors = ? WHERE title = ?", (new_contributors, title))

    contributions = c6.execute("SELECT contributions FROM users WHERE username = ?", (username,))
    contributions = c6.fetchone()[0]
    new_contributions = contributions + title + "~"
    c6.execute("UPDATE users SET contributions = ? WHERE username = ?", (new_contributions, username))

    db.commit()
    return render_template('story_view.html', entire = new_text, title = title, editor = 1)
db.close()

#Displays login page and removes user from session
@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.pop("user", None) #removes the session
    return render_template('login.html')

#Enables debugging, auto-restarting of server when this file is modified
if __name__ == "__main__": #false if this file imported as module
    app.debug = True
    app.run()
