#!/usr/bin/python

import MySQLdb

## Database Config.
#dbhost = '10.11.17.1'
dbhost = '[2001:6a8:1d80:2041:225:90ff:fe1d:24d8]'
dbuser = 'root'
dbpwd = 'password'
dbname = 'fgreproject'
##############

# Connect to database and dump data
def run_query(dbhost, dbuser, dbpass, dbname, query):
    # connect to MySQL
    conn = MySQLdb.connect(host= dbhost,
                      user=dbuser,
                      passwd=dbpass,
                      db=dbname)
    x = conn.cursor()

    try:
        x.execute(query)
        conn.commit()
    except:
       conn.rollback()


    results = x.fetchall()
    conn.close()
    return results


def main():
    query = """SELECT DISTINCT session_id
FROM  `rssi_values`
WHERE robot_id =  "robot5"
ORDER BY rssi ASC"""

    print "running query"
    result = run_query(dbhost, dbuser, dbpwd, dbname, query)
    sessions = [list(row) for row in result]
    for session in sessions:
        query = "SELECT rssi,ssid,loc_x,loc_y FROM `rssi_values` WHERE session_id = '"+session[0]+"' ORDER BY rssi ASC LIMIT 0, 4"
        session_power = run_query(dbhost, dbuser, dbpwd, dbname, query)
        #for pw in session_power:
            #print pw
    #print only last session
    print session
    for pw in session_power:
        print pw

if __name__ == "__main__":
    main()
