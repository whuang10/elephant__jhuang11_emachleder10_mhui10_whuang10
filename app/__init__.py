# Team Elephant (Jeffrey Huang, Matthew Hui, Winnie Huang, Ethan Machleder)
# SoftDev
# P0 -- Da Art of Storytellin' (Pt. 2)
# 2021-01-06
from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session
import os

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)

@app.route("/") #, methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session: #Checks if the user is logged in
        return render_template('response.html', user = 'abc')
    else:
        return render_template( 'login.html')







if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
