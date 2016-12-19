#!/usr/bin/env python

import sqlite3

import os
import time
import glob
import readprobe

# global variables
speriod=(15*60)-1
dbname='/var/www/templog.db'

isRunning = False
fanOnThreshold = 9999
fanOffThreshold = 0
timeToDisplay = 1

# store the temperature in the database
def log_temperature(temp):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now','localtime'), (?))", (temp,))

    # commit the changes
    conn.commit()

    conn.close()

# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])

    conn.close()


def get_settings():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("SELECT * FROM settings")
    settings = curs.fetchone()

    global isRunning
    global fanOnThreshold
    global fanOffThreshold
    global timeToDisplay
    
    isRunning = bool(settings[0])
    fanOnThreshold = float(settings[1])
    fanOffThreshold = float(settings[2])
    timeToDisplay = int(settings[3])

    conn.close()

    return

def main():
    # get the temperature from the device file
    temperature = readprobe.printReading()
    print temperature

    # Store the temperature in the database
    log_temperature(temperature)
    display_data()

    get_settings()

    if(isRunning):
        if temperature >= fanOnThreshold and temperature <= fanOffThreshold:
            os.system('python /var/www/html/cgi-bin/fan.py on')
        else:
            os.system('python /var/www/html/cgi-bin/fan.py off')
    else:
        os.system('python /var/www/html/cgi-bin/fan.py off')


if __name__=="__main__":
    main()