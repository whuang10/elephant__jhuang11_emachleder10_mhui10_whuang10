# Team Elephant (Jeffrey Huang, Matthew Hui, Winnie Huang, Ethan Machleder)
# SoftDev
# K16 -- No Trouble
# 2020-12-15

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
print("sucessfully connected to sqlite")

#==========================================================

# CODE TO POPULATE THE course_grades db CONTAINING courses.csv DATA

c.execute('DROP TABLE IF EXISTS course_grades')
c.execute('''CREATE TABLE "course_grades"(
	"name" TEXT,
	"grade" INTEGER,
	 "id" INTEGER)
	 ''')