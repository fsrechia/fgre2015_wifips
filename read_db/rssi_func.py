# rss_to_distance
# changing the rssi value to the distance
# inputs
#  rssi: the rssi value to be translated
#  ref_rssi: the reference rssi value
#  alpha: path loss exponent
# output: the distance 

def rss_to_distance(rssi, ref_rssi, alpha):
	loss = int(ref_rssi) - int(rssi)
	k = 1
	return k*float(pow(10, float(loss)/(float(alpha)*10)))

def centroid_weighted(output):
	g = open("output.csv", "w")
	def _calculating(lst): # estimated location
		tmp = zip(*lst)
		powers = tmp[0]	# three powers
		loc = tmp[1]	# three locations
		weights = []

		for power in powers:
			weights.append(1.0/(rss_to_distance(power, -10, 5.0)**2))

		values = []

		for n in range(len(loc)):
			values.append(tuple([weights[n]*i for i in loc[n]]))

		tmp2 = zip(*values)
		value_x = tmp2[0]
		value_y = tmp2[1]
		sum_of_weights = sum(weights)
		estimated_location = tuple([float(sum(value_x))/sum_of_weights, float(sum(value_y))/sum_of_weights])
		return estimated_location

	output["distance"] = {}

	for (k, lst) in output["rss"].items(): # session id and the rssi lists for each session id
		for v in lst:
			if output["distance"].get(k, None) == None:
				output["distance"][k] = []
			output["distance"][k].append(rss_to_distance(v, -10, 3.0))

	def _error_distance(output, loc_e, k):
		loc = output["robots"][k] # the criterion (y)
		return (loc_e[0] - loc[0], loc_e[1] - loc[1])

	output["three_powers"] = {}
	output["indexes"] = {}

	for (k, lst) in output["distance"].items():
		if output["three_powers"].get(k, None) == None:
			output["three_powers"][k] = []
		if output["indexes"].get(k, None) == None:
			output["indexes"][k] = []

		tmp = list(lst)
		
		for n in range(3):
			val = max(tmp)
			index = lst.index(val)
			output["three_powers"][k].append((max(tmp), output["fp"][k][index]))
			output["indexes"][k].append(index)
			tmp.remove(max(tmp))

	result = [] # estimated locations for each session id

	g = open("output.csv", "w")

	for (k, lst) in output["three_powers"].items():
		g.write("session id, " + str(k) + "\n")
		loc = output["robots"][k]
		g.write("robots location, (" + str(loc[0]) + ", " + str(loc[1]) + ")\n")
		val = _calculating(lst)
		g.write("estimated location, (" + str(val[0]) + ", " + str(val[1]) + ")\n")
		err = _error_distance(output, val, k)
		g.write("error distance, (" + str(err[0]) + ", " + str(err[1]) + ")\n\n")
