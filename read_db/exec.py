#!/usr/bin/python

from parsing import parsing_file
from rssi_func import centroid_weighted
import logging
import sys
import MySQLdb
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
csv_name = 'rssi_values.csv'

## Database Config. 
dbhost = '10.11.17.1'
#dbhost = '[2001:6a8:1d80:2041:225:90ff:fe1d:24d8]'
dbuser = 'root'
dbpwd = 'password'
dbname = 'fgreproject'
##############

# Connect to database and dump data 
def run_query(dbhost, dbuser, dbpass, dbname, query, dump_csv=True, csv_op_name):
    # connect to MySQL
    conn = MySQLdb.connect(host= dbhost,
                      user=dbuser,
                      passwd=dbpass,
                      db=dbname)
    x = conn.cursor()

    '''
    try:
        x.execute(query)
        conn.commit()
    except:
       conn.rollback()
    '''
    x.execute(query)
    results = x.fetchall()
    if dump_csv:
        fd = open(csv_op_name, 'w+')
        opFile = csv.writer(fd)
        opFile.writerows(results)
        fd.close()

    conn.close()
    return results


def main():
	logger.info('Running main()')
	#file_name = str(sys.argv[1])
	#print file_name
	#logger.info('File name is set to ' + file_name)

	query = """SELECT * FROM (SELECT id, session_id, rssi, ssid, timestamp, robot_id, loc_x, loc_y,
@id_id:=CASE WHEN @id_session_id <> session_id THEN 0 ELSE @id_id+1 END as rn,
@id_session_id := session_id AS clset
FROM
(SELECT @id_session_id := -1) s,
(SELECT @id_id := -1) c,
(SELECT * FROM rssi_values ORDER BY session_id, id, rssi) t) x WHERE rn < 5"""

    logger.info("running query : {}".format(query))
    result = run_query(dbhost, dbuser, dbpwd, dbname, query, True, csv_name)

    logger.info('csv output generated: {}'.format(csv_name))

	logger.info('Print the output')
	output = parsing_file(file_name)
	centroid_weighted(output)

if __name__ == "__main__":
	main()








def main():
    

if __name__ == "__main__":
    main()
