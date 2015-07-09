from math import sqrt, log

# getting the distance between two points.
# input
# 
def get_distance(x1, y1, x0, y0):
	return sqrt((x1-x0)**2 + (y1-y0)**2)

# getting the alpha from powers and radiuses
def get_alpha(lst_p, lst_r):
	def _get_alpha(pi, pj, ri, rj):
		return (pi-pj)/(10.0 * log(float(ri)/float(rj)))

	lst = zip(lst_p, lst_r)

	lst_alpha = []

	for (p1, r1) in lst:
		lst.remove((p1, r1))
		for (p2, r2) in lst:
			lst_alpha.append(_get_alpha(p1, p2, r1, r2))

	return sum(lst_alpha)/len(lst_alpha)

#getting the estimated radius from the power
def get_radius(powers, lst_p, lst_r):
	def _get_radius(p, pi, ri):
		return ri * pow(10, ((pi - p)/ 10 * get_alpha(lst_p, lst_r)))

	lst = zip(lst_p, lst_r)

	lst_radius = []
	lst_radius_result = []

	for power in powers:
		for (p1, r1) in lst:
			lst_radius.append(_get_radius(power, p1, r1))
		lst_radius_result.append(sum(lst_radius)/len(lst_radius))

	return lst_radius_result

#
def get_area(lst_r, lst_point):
	def _get_l(ri, rj, d):
		return (ri**2 - rj**2 + d**2) / 2*d

	def _get_h(ri, l):
		return sqrt(ri**2 - l**2)

	def _get_x0(xi, xj, yi, yj, l, h):
		d = get_distance(xi, yi, xj, yj)
		x0_1 = (l/d)*(xj-xi) + (h/d)*(yj-yi) + xi
		x0_2 = (l/d)*(xj-xi) - (h/d)*(yj-yi) + yi
		return [x0_1, x0_2]

	def _get_y0(xi, xj, yi, yj, l, h):
		d = get_distance(xi, yi, xj, yj)
		y0_1 = (l/d)*(xj-xi) - (h/d)*(yj-yi) + xi
		y0_2 = (l/d)*(yj-yi) + (h/d)*(xj-xi) + yi
		return [y0_1, y0_2]

	def _determine(lst_x, lst_y, other_point):
		candidate = []
		for n in range(len(lst_x)):
			candidate.append((lst_x[n], lst_y[n]))

		calculate = []
		for (x1, y1) in candidate:
			lst = []
			for (x0, y0) in other_point:
				lst.append(get_distance(x1, y1, x0, y0))
			calculate.append(sum(lst))

		if calculate[0] > calculate[1]:
			return candidate[0]
		else:
			return candidate[1]
				
	lst = zip(lst_r, lst_point)
	lst_result = []

	for (ri, (xi, yi)) in lst:
		lst.remove((ri, (xi, yi)))
		for (rj, (xj, yj)) in lst:
			d = get_distance(xi, yi, xj, yj)
			l = _get_l(ri, rj, d)
			h = _get_h(ri, l)
			other_point = list(lst)
			other_point.remove((ri,xi,yi))
			other_point.remove((rj,xj,yj))
			lst_result.append(_determine(_get_x0(xi, xj, yi, yj, l, h), _get_y0(xi, xj, yi, yj, l, h), other_point))

	return lst_result

def get_point(lst):
	return (float(sum(lst[0]))/len(lst), float(sum(lst[1]))/len(lst))	

