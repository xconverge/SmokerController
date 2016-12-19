#!/usr/bin/env python

import sqlite3
import sys

# global variables
speriod=(15*60)-1
dbname='/var/www/templog.db'

isRunning = False
fanOnThreshold = 9999
fanOffThreshold = 0
timeToDisplay = 1

# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"


# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    print_graph_script(table)
    print "</head>"


# get data from the database
# if an interval is passed, 
# return a list of records from the database
def get_data(interval):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM temps")
    else:
        curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','localtime','-%s hours')" % interval)

    rows=curs.fetchall()
    conn.close()
    return rows


# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""

    for row in rows[:-1]:
        rowstr="['{0}', {1}],\n".format(str(row[0]),str(row[1]))
        chart_table+=rowstr

    row=rows[-1]
    rowstr="['{0}', {1}]\n".format(str(row[0]),str(row[1]))
    chart_table+=rowstr

    return chart_table


# print the javascript to generate the chart
# pass the table generated from the database info
def print_graph_script(table):
    # google chart snippet
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Time', 'Temperature'],
%s
        ]);
        var options = {
          title: 'Temperature'
        };
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""

    print chart_code % (table)


# print the div that contains the graph
def show_graph():
    print "<h2>Temperature Chart</h2>"
    print '<div id="chart_div" style="width: 900px; height: 500px;"></div>'


# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("SELECT timestamp,max(temp) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    rowmax=curs.fetchone()
    rowstrmax="{0}&nbsp&nbsp&nbsp{1}F".format(str(rowmax[0]),str(rowmax[1]))

    curs.execute("SELECT timestamp,min(temp) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)    
    rowmin=curs.fetchone()
    rowstrmin="{0}&nbsp&nbsp&nbsp{1}F".format(str(rowmin[0]),str(rowmin[1]))

    curs.execute("SELECT avg(temp) FROM temps WHERE timestamp>datetime('now','localtime','-%s hour') AND timestamp<=datetime('now','localtime')" % option)
    rowavg=curs.fetchone()

    print "<hr>"

    print "<h2>Minumum temperature&nbsp</h2>"
    print rowstrmin
    print "<h2>Maximum temperature</h2>"
    print rowstrmax
    print "<h2>Average temperature</h2>"
    print "%.3f" % rowavg+"F"

    print "<hr>"

    print "<h2>In the last hour:</h2>"
    print "<table>"
    print "<tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td></tr>"

    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','localtime','-1 hour') AND timestamp<=datetime('now','localtime')")
    for row in rows:
        rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}F</td></tr>".format(str(row[0]),str(row[1]))
        print rowstr
    print "</table>"
    print "<hr>"

    conn.close()


def print_settings_controls():
    # Empty iframe for running php scripts
    print """<iframe style="display:none;" name="phpFrame"></iframe>"""

    start = """<a href="start.php" target="phpFrame"><button type="button">Start</button></a>"""
    stop = """<a href="stop.php" target="phpFrame"><button type="button">Stop</button></a>"""

    fanOn = """
                <input type="text" id="fanOn" value="{0}">
                """.format(str(fanOnThreshold))

    fanOff = """
                <input type="text" id="fanOff" value="{0}">
                """.format(str(fanOffThreshold))

    time = """
            <input type="text" id="timeToDisplay" value="{0}">
            """.format(str(timeToDisplay))

    print "<table border=1 frame=hsides rules=rows,columns>"
    print "<tr><td><strong>Is Running</strong></td><td><strong>Fan On Threshold [F]</strong></td><td><strong>Fan Off Threshold [F]</strong></td><td><strong>Time To Display [hrs]</strong></td></tr>"
    current="<tr><td>{0}&emsp;&emsp;</td><td>{1} F</td><td>{2} F</td><td>{3}</td></tr>".format(str(isRunning),str(fanOnThreshold),str(fanOffThreshold),str(timeToDisplay))
    print current 
    controls="<tr><td>{0}{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>".format(str(start),str(stop),str(fanOn),str(fanOff),str(time))
    print controls
    print "</table>"

    print "<br>"
    print """<a href="" id="settingsBtn" target="phpFrame"><button type="button">Update settings</button></a>"""
    print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    print """<a href="clearDB.php" target="phpFrame"><button type="button">Clear Data</button></a>"""
    print "<br>"

    print """
          <script type="text/javascript">
          document.getElementById("settingsBtn").onclick = function(){
                var onVal = document.getElementById("fanOn").value;
                var offVal = document.getElementById("fanOff").value;
                var timeVal = document.getElementById("timeToDisplay").value;
                location.href='updateSettings.php?fanOn=' + onVal + '&fanOff=' + offVal + '&time=' + timeVal; 
            } 
            </script>
            """

# check that the option is valid
# and not an SQL injection
def validate_input(option_str):
    # check that the option string represents a number
    if option_str.isalnum():
        # check that the option is within a specific range
        if int(option_str) > 0 and int(option_str) <= 24:
            return option_str
        else:
            return None
    else: 
        return None


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
    # Read settings from settings table in db
    get_settings()

    # get data from the database
    records=get_data(timeToDisplay)

    # print the HTTP header
    printHTTPheader()

    if len(records) != 0:
        # convert the data into a table
        table=create_table(records)
    else:
        print "No data found"

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("Smoker Temperature Logger", table)

    # print the page body
    print "<body>"
    print "<h1>Smoker Temperature Logger</h1>"
    print "<hr>"
    print_settings_controls()
    show_graph()
    show_stats(timeToDisplay)
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()

