from math import sqrt, log

def get_distance(ssid, robot):
	return sqrt((int(ssid[0]) - int(robot[0]))**2 + (int(ssid[1]) - int(robot[1]))**2)

def get_alpha(out):
	powers = {}
	distance = {}
	fp = {}	
	robot = {}

	for k in out["rss"].keys():
		powers[k] = out["rss"][k]
		robot[k] = out["robots"][k]
		fp[k] = out["fp"][k]


	for k in out["rss"].keys():
		for item in fp[k]:
			if distance.get(k, None) == None:
				distance[k] = []
			distance[k].append(get_distance(item, robot[k]))

	selected_powers = {} # p1, p2, p3, p4
	selected_distance = {} # r1, r2, r3, r4

	for k in powers.keys():
		for n in range(4):
			if selected_powers.get(k, None) == None:
				selected_powers[k] = []
				selected_distance[k] = []
			selected_powers[k].append(max(powers[k]))
			idx = powers[k].index(max(powers[k]))
			selected_distance[k].append(distance[k][idx])
			powers[k].remove(max(powers[k]))
			distance[k].remove(distance[k][idx])
			
	alpha = {}

	for k in powers.keys():
		p = list(selected_powers[k])
		r = list(selected_distance[k])
		
		for n in range(4):
			pi = p.pop()
			ri = r.pop()

			for m in range(len(p)):
				if alpha.get(k, None) == None:
					alpha[k] = []
				pj = p[m]
				rj = r[m]
				alpha[k].append(float((int(pi) - int(pj))) / (10 * log((float(rj)/float(ri)))))
	
	avg_alpha = {}
	for k in alpha.keys():
		avg_alpha[k] = (sum(alpha[k]) / len(alpha[k]))

	return avg_alpha

def get_estimate(out, alpha):
	powers = {}
	distance = {}
	fp = {}	
	robot = {}

	for k in out["rss"].keys():
		powers[k] = out["rss"][k]
		robot[k] = out["robots"][k]
		fp[k] = out["fp"][k]

	for k in out["rss"].keys():
		for item in fp[k]:
			if distance.get(k, None) == None:
				distance[k] = []
			distance[k].append(get_distance(item, robot[k]))

	selected_powers = {} # p1, p2, p3, p4
	selected_distance = {} # r1, r2, r3, r4
	selected_fp = {}

	for k in powers.keys():
		for n in range(4):
			if selected_powers.get(k, None) == None:
				selected_powers[k] = []
				selected_distance[k] = []
				selected_fp[k] = []
			selected_powers[k].append(max(powers[k]))
			idx = powers[k].index(max(powers[k]))
			selected_distance[k].append(distance[k][idx])
			selected_fp[k].append(fp[k][idx])

			powers[k].remove(max(powers[k]))
			distance[k].remove(distance[k][idx])
			fp[k].remove(fp[k][idx])
			
	rk_lst = {}
	tmp_powers = {}

	for k in selected_powers.keys():
		pk = []
		tmp_powers[k] = list(selected_powers[k])

		for m in range(4):
			pk.append(tmp_powers[k].pop())

			for n in range(len(selected_powers[k])):
				if rk_lst.get(k, None) == None:
					rk_lst[k] = {}
				if rk_lst[k].get(m, None) == None:
					rk_lst[k][m] = []

				rk_lst[k][m].append(selected_distance[k][n] * pow(10, (selected_powers[k][n] - pk[m]) / (10 * alpha[k])))

		print str(k) + ": " + str(rk_lst[k]) + "\n"
	rk = {}

	for k in selected_powers.keys():
		result = 0
		overall = 0
		for n in rk_lst[k].keys():
			if rk.get(k, None) == None:
				rk[k] = []
			rk[k].append(float(sum(rk_lst[k][n])) / len(rk_lst[k][n]))

	estimated_point = {}

	h_lst = {}

	for k in rk.keys():
		if estimated_point.get(k, None) == None:
			estimated_point[k] = []

		r = list(rk[k])

		for ri in rk[k]:
			f_point = list(selected_fp[k])
			idx_i = r.index(ri)
			r.remove(ri)
			f_point_i = f_point[idx_i]
			f_point.remove(f_point_i)

			for rj in r:
				idx_j = r.index(rj)
				f_point_j = f_point[idx_j]
				d = get_distance(f_point_i, f_point_j)
				l = ((ri**2) - (rj**2) + (d**2)) / (2*d)

				if h_lst.get(k, None) == None:
					h_lst[k] = []

				h_lst[k].append((ri**2) - (l**2))

				h = sqrt(abs((ri**2) - (l**2)))
				(x0_1, y0_1) = ((l/d)*(f_point_j[0] - f_point_i[0]) + (h/d)*(f_point_j[1] - f_point_i[1]) + f_point_i[0], (l/d)*(f_point_j[1] - f_point_i[1]) - (h/d)*(f_point_j[0] - f_point_i[0]) + f_point_i[1])
				(x0_2, y0_2) = ((l/d)*(f_point_j[0] - f_point_i[0]) - (h/d)*(f_point_j[1] - f_point_i[1]) + f_point_i[0], (l/d)*(f_point_j[1] - f_point_i[1]) + (h/d)*(f_point_j[0] - f_point_i[0]) + f_point_i[1])

				two_points = [item for item in f_point if item != f_point_j]
				mid_point = ((two_points[0][0] + two_points[1][0]) / 2, (two_points[0][1] + two_points[1][1]) / 2)

				d1 = get_distance((x0_1, y0_1), mid_point)
				d2 = get_distance((x0_2, y0_2), mid_point)

				if d1 > d2:
					estimated_point[k].append((x0_2, y0_2))
				else:
					estimated_point[k].append((x0_1, y0_1))

	result = {}

	for k in estimated_point.keys():
		sum_x = 0
		sum_y = 0

		for (x, y) in estimated_point[k]:
			sum_x += x
			sum_y += y

		n = len(estimated_point[k])

		result[k] = (float(sum_x) / n, float(sum_y) / n)

	errors = {}
	error_distance = {}

	output_file = open("output.csv", "w")
	output_file.write("session id, alpha, estimated, actual, error, error_distance\n")

	for k in result.keys():
#		print str(k) + "- alpha: " + str(alpha[k])
#		print str(k) + "- estimated: " + str(result[k])
#		print str(k) + "- actual: " + str(out["robots"][k])
#		print str(k) + "- h_lst: " + str(h_lst[k])
#		print str(k) + "- selected_powers: " + str(selected_powers[k])
#		print str(k) + "- selected_distance: " + str(selected_distance[k])
#		print str(k) + "- rks: " + str(rk[k])

		(x, y) = result[k]
		(a, b) = out["robots"][k]
		errors[k] = (x-a, y-b)
		error_distance[k] = get_distance(errors[k], (0,0))

#		print str(k) + "- error: " + str(errors[k])
#		print "\n"
		output_file.write(str(k) + ", " + str(alpha[k]) + ", " + str(result[k]) + ", " + str(out["robots"][k]) + ", " + str(errors[k]) + ", " + str(error_distance[k]) + "\n")

	output_file.close()
