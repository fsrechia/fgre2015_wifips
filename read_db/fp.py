#!/usr/bin/python
# I ran this script on my local machine, it requries PANDAS library! -Arvind

import pandas as pd

def get_ssid_x(ssid):
	x = 5500 - 600 * (ord(ssid[-2].lower()) - 98)
	return x

def get_ssid_y(ssid):
	y = 200 + 360 * (int(ssid[-1]) - 1)
	return y


df = pd.read_csv('data/rssi_values.csv')

df['ssid_loc_x'] = df.apply(lambda x: get_ssid_x(x['ssid']), axis=1)
df['ssid_loc_y'] = df.apply(lambda x: get_ssid_y(x['ssid']), axis=1)

del df['s_id']

df.to_csv('for_heat_map.csv', index=False)