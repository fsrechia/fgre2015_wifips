#!/usr/bin/env python

# runme.py v0.1

import subprocess
import re
import MySQLdb
import datetime
import urllib
import json
import logging
import socket

##############
### Config ###
##############
DEBUG = False
robot_id = socket.gethostname().partition('.')[0]
interface_to_scan = 'wlan0'
robot_loc_url = 'http://robotcontrol.wilab2.ilabt.iminds.be:5056/Robot/LocationsMem'

## Database Config. 
dbhost = '10.11.17.1'
dbuser = 'root'
dbpwd = 'password'
dbname = 'fgreproject'
##############

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Loading script')

# Function that scans the interface passed to it
def scan_interface(interface):
    # run shell script
    proc = subprocess.Popen('iwlist {} scan'.format(interface), shell=True, stdout=subprocess.PIPE, )
    stdout_str = proc.communicate()[0]
    stdout_list=stdout_str.split('\n')

    essids=list()
    addresses=list()
    rssis = list()

    # parse output of shell script line by line
    for line in stdout_list:
        line=line.strip()

        # extract AP name
        match=re.search('ESSID:"(\S+)"',line)
        if match:
            essids.append(match.group(1))

        # extract MAC
        match=re.search('Address: (\S+)',line)
        if match:
            addresses.append(match.group(1))
        
        # extract RSSI value
        match=re.search('Quality=(\S+)  Signal level=(\S+) (\S+)',line)
        if match:
            rssis.append(match.group(2))

    return essids, addresses, rssis


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

    #close connection   
    conn.close()
    return


# Get Robot Location
def get_robot_location(robot_id, robot_loc_url):
    json_url = urllib.urlopen(robot_loc_url)
    json_obj = json.loads(json_url.read())
    try:
        x = json_obj[str(robot_id)]['x']
        y = json_obj[str(robot_id)]['y']
    except:
        x = 0
        y = 0
    return x, y


# Main
def main():
    logger.info('Running main()')

    # generating session_id for this run
    session_id = '{}{}'.format(datetime.datetime.now().strftime("%m%d%H%M%S"), robot_id)
    logger.info('Generated session_id')

    # capture all the SSIDs, MAC addresses, and RSSI values as seen by robot_id
    essids, addresses, rssis = scan_interface(interface_to_scan)
    logger.info('Scanned all SSIDs (interface: {})'.format(interface_to_scan))

    robot_x, robot_y = get_robot_location(robot_id[5:], robot_loc_url)
    logger.info('Captured location of robot id: {}'.format(robot_id))

    logger.info('Inserting data into database')
    for (essid, address, rssi) in zip(essids, addresses, rssis):
        if re.match('^zotac', str(essid).lower()):
            query = "INSERT INTO rssi_values (ssid, session_id, rssi, timestamp, robot_id, loc_x, loc_y) VALUES ('{}', '{}', '{}', now(), '{}', '{}', '{}')".format(essid, session_id, rssi, robot_id, robot_x, robot_y)
            run_query(dbhost, dbuser, dbpwd, dbname, query)
    
    logger.info('Complete')

if __name__ == "__main__":
    main()