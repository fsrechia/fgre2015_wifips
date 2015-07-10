import json
import logging

from fp import fixed_point

def parsing_file(file_name):
	f = open(file_name, "r")

	rssi = "rss"
	fp_loc = "fp"
	ts = "timestamp"
	m_loc = "robots"

	output = {} 
	output[rssi] = {}
	output[fp_loc] = {}
	output[ts] = {}
	output[m_loc] = {}
	sess_id = ""

	for line in f:
		line = line.replace("\"", "")
		line = line.strip()
		line = line.split(",")
		sess_id = line[1].strip()

		if output[rssi].get(sess_id, None) == None:
			output[rssi][sess_id] = []
		output[rssi][sess_id].append(line[2].strip())

		if output[fp_loc].get(sess_id, None) == None:
			output[fp_loc][sess_id] = []
		output[fp_loc][sess_id].append(fixed_point(line[3].strip()))

		if output[ts].get(sess_id, None) == None:	
			output[ts][sess_id] = []
		output[ts][sess_id].append(line[4].strip())

		if output[m_loc].get(sess_id, None) == None:
			output[m_loc][sess_id] = []
		output[m_loc][sess_id] = (int(line[6].strip()), int(line[7].strip()))

	print output
	return output
