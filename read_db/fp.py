def fixed_point(ssid):
	x = 5500 - 600 * (ord(ssid[-2]) - 98)
	y = 200 + 360 * (int(ssid[-1]) - 1)
	return (x, y)
